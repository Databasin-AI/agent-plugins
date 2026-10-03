import { spawn } from 'node:child_process';
import { accessSync, constants, existsSync, readFileSync } from 'node:fs';
import { basename, delimiter, dirname, isAbsolute, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

export const CLIENT_PACKAGE = '@databasin/mcp-client@0.2.3';
const CLIENT_VERSION = CLIENT_PACKAGE.slice('@databasin/mcp-client@'.length);
class LaunchConfigurationError extends Error {}

function executable(name, env, platform) {
  for (const directory of (env.PATH ?? '').split(delimiter).filter(Boolean)) {
    // Never execute commands from the working directory through an empty PATH component.
    if (!isAbsolute(directory)) continue;
    const candidate = join(directory, platform === 'win32' ? `${name}.exe` : name);
    try { accessSync(candidate, constants.X_OK); return candidate; } catch {}
  }
}

export function selectLaunch({ env = process.env, platform = process.platform, node = process.execPath,
  pluginRoot = fileURLToPath(new URL('..', import.meta.url)) } = {}) {
  const installed = env.DATABASIN_MCP_CLIENT_PATH ?? join(pluginRoot, 'node_modules', '@databasin', 'mcp-client', 'dist', 'cli.js');
  if (env.DATABASIN_MCP_CLIENT_PATH !== undefined || existsSync(installed)) {
    if (!isAbsolute(installed) || !existsSync(installed)) throw new LaunchConfigurationError('DATABASIN_MCP_CLIENT_PATH must point to the installed pinned client dist/cli.js.');
    const metadata = JSON.parse(readFileSync(join(dirname(installed), '..', 'package.json'), 'utf8'));
    if (metadata.name !== '@databasin/mcp-client' || metadata.version !== CLIENT_VERSION || basename(installed) !== 'cli.js' || basename(dirname(installed)) !== 'dist') {
      throw new LaunchConfigurationError(`The preinstalled client must be ${CLIENT_PACKAGE}.`);
    }
    return { command: node, args: [installed] };
  }
  // Windows npm ships .cmd shims: use its JS entrypoint with Node, never shell:true.
  if (platform === 'win32') {
    for (const directory of (env.PATH ?? '').split(delimiter).filter(isAbsolute)) {
      const npx = join(directory, 'node_modules', 'npm', 'bin', 'npx-cli.js');
      if (existsSync(npx)) return { command: node, args: [npx, '--yes', '--quiet', CLIENT_PACKAGE] };
    }
  } else {
    const npx = executable('npx', env, platform);
    if (npx) return { command: npx, args: ['--yes', '--quiet', CLIENT_PACKAGE] };
  }
  const bun = executable('bun', env, platform);
  if (bun) return { command: bun, args: ['x', CLIENT_PACKAGE] };
  const bunx = executable('bunx', env, platform);
  if (bunx) return { command: bunx, args: [CLIENT_PACKAGE] };
  const pnpm = executable('pnpm', env, platform);
  if (pnpm) return { command: pnpm, args: ['dlx', CLIENT_PACKAGE] };
  throw new LaunchConfigurationError(`No package runner is available. Install npm/npx, Bun, or pnpm, or preinstall ${CLIENT_PACKAGE} and set DATABASIN_MCP_CLIENT_PATH to its absolute dist/cli.js path.`);
}

export function launch() {
  let selected;
  try { selected = selectLaunch(); }
  catch (error) {
    process.stderr.write(`Databasin MCP cannot start. ${error instanceof LaunchConfigurationError ? error.message : 'The preinstalled client metadata could not be read. Check its installation and permissions.'}\n`);
    process.exitCode = 1;
    return;
  }
  const child = spawn(selected.command, [...selected.args, ...process.argv.slice(2)], { stdio: 'inherit', shell: false });
  const signals = ['SIGINT', 'SIGTERM'];
  const listeners = signals.map(signal => { const listener = () => child.kill(signal); process.on(signal, listener); return listener; });
  child.once('error', () => { process.stderr.write('Databasin MCP could not launch the selected runtime. Check its installation and permissions.\n'); process.exitCode = 1; });
  child.once('exit', (code, signal) => {
    signals.forEach((value, index) => process.removeListener(value, listeners[index]));
    process.exitCode = code ?? (signal === 'SIGINT' ? 130 : signal === 'SIGTERM' ? 143 : 1);
  });
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) launch();
