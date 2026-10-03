import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { spawnSync } from 'node:child_process';
import { CLIENT_PACKAGE, selectLaunch } from '../plugins/databasin/scripts/launch-mcp.mjs';

test('launcher chooses pinned runners, supports preinstallation, and never silently changes versions', () => {
  const root = mkdtempSync(join(tmpdir(), 'databasin-launcher-'));
  try {
    const env = { PATH: root }; const options = { env, pluginRoot: root, platform: 'linux' };
    assert.throws(() => selectLaunch(options), /No package runner/);
    for (const name of ['pnpm', 'bunx', 'bun', 'npx']) {
      writeFileSync(join(root, name), '', { mode: 0o755 });
      const selected = selectLaunch(options);
      assert.equal(selected.command, join(root, name));
      assert.ok(selected.args.includes(CLIENT_PACKAGE));
    }
    const install = join(root, 'client'); mkdirSync(join(install, 'dist'), { recursive: true });
    const cli = join(install, 'dist', 'cli.js'); writeFileSync(cli, '');
    writeFileSync(join(install, 'package.json'), JSON.stringify({ name: '@databasin/mcp-client', version: '0.2.3' }));
    assert.deepEqual(selectLaunch({ ...options, env: { ...env, DATABASIN_MCP_CLIENT_PATH: cli } }).args, [cli]);
    writeFileSync(join(install, 'package.json'), JSON.stringify({ name: '@databasin/mcp-client', version: '0.2.2' }));
    assert.throws(() => selectLaunch({ ...options, env: { ...env, DATABASIN_MCP_CLIENT_PATH: cli } }), /must be/);
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test('missing runner returns actionable stderr without polluting MCP stdout or exposing environment', () => {
  const result = spawnSync(process.execPath, ['plugins/databasin/scripts/launch-mcp.mjs'], { encoding: 'utf8',
    env: { PATH: '/nonexistent', DATABASIN_MCP_ACCESS_TOKEN: 'DO_NOT_PRINT' } });
  assert.equal(result.status, 1); assert.equal(result.stdout, '');
  assert.match(result.stderr, /preinstall/); assert.doesNotMatch(result.stderr, /DO_NOT_PRINT/);
});
