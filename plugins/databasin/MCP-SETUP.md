# MCP setup

The plugin registers a local stdio MCP server through the Claude [`.mcp.json`](.mcp.json)
or the Codex [`.mcp.codex.json`](.mcp.codex.json). Both start a shared Node launcher.
It prefers an exact preinstalled client, then npm/npx, Bun, or pnpm, with this pin:

```text
@databasin/mcp-client@0.2.3 --environment prod
```

The local client connects to `https://databasin.cloud/mcp` with true Streamable
HTTP MCP, discovers product tools from the server, and mirrors those tools to the
host. It pins protocol version `2026-07-28`; there is no REST or legacy-protocol
fallback.

## Authentication

The client exposes two local tools:

- `databasin_auth_status` checks local sign-in state.
- `databasin_login` starts DataBasin Auth0 device sign-in and returns the
  approved activation URL and a short-lived user code.

Enter credentials only on the sign-in page or its selected identity provider. The client stores tokens in the
OS-protected credential store by default and sends a bearer token only on remote
`tools/call` requests. It does not place tokens in MCP output.

Version 0.9.2 upgrades the client to Auth0. Sign in again after upgrading:
legacy Microsoft sessions are not reused or deleted. Automatic renewal requires
the Auth0 application's Refresh Token grant and the API's Allow Offline Access
setting. If no refresh token is issued, sign in again when the access token expires.

## Local checks

### Linux desktop credential storage

The Codex-only configuration explicitly forwards `DBUS_SESSION_BUS_ADDRESS` and
`XDG_RUNTIME_DIR` from the host session to the MCP process. Codex otherwise
filters these variables, preventing the client from reaching the Linux Secret
Service even when the user is already signed in. These are session connection
settings, not tokens; no values are bundled or copied into configuration.
`env_vars` is a Codex field, not a Claude Code field. Claude Code already inherits the desktop environment. On macOS and Windows,
unset Linux variables do not change the native credential-store behavior.

Run the host inside your logged-in desktop session with an available, unlocked
Secret Service/keyring. Forwarding variables does not provision or unlock a
keyring on headless machines. Do not enable plaintext token storage as a workaround.

### Headless containers

For an Azure agent container without a desktop, select encrypted persistence with
`DATABASIN_MCP_CREDENTIAL_STORE=file`. Provision exactly one of
`DATABASIN_MCP_STORE_KEY` (32 random bytes, base64 encoded) or
`DATABASIN_MCP_STORE_KEY_FILE` (absolute private key-file path) from the platform's
secret manager. The key must be outside the cache and is never generated beside it.
Set `DATABASIN_MCP_AUTH_DIR` to a per-user persistent private directory if needed;
otherwise the cache is under `~/.databasin/mcp/auth`. Require owner-only permissions
(0700 directories, 0600 files), no symlinked secret/cache files, and no sharing
between replicas. Key and cache must both survive restarts to preserve sign-in.

Then call `databasin_login` in the MCP session and complete the displayed device
sign-in on another device. Tokens stay encrypted in the container; no browser,
keyring, libsecret, or D-Bus session is required. The desktop keyring remains the
default; failure never automatically selects a weaker store.

For ephemeral automation, `DATABASIN_MCP_ACCESS_TOKEN` can instead supply an
unexpired Auth0 token issued for the Databasin MCP native client and selected API
audience. It is verified, never persisted/refreshed, and takes precedence over
device login. Remove it and restart before switching to device login. Configure
secrets outside chat, images, command arguments, and plugin files. Environment
secrets remain accessible to other code in the same container; isolate users.

For Node-only images without a package manager, preinstall the pinned client
during image construction and set `DATABASIN_MCP_CLIENT_PATH` to its absolute
`dist/cli.js` path. The version must match the plugin pin. This also avoids npm
network access on startup. Bun-only package-manager hosts work through `bun x`.

If an older manually configured `databasin` MCP server shadows the plugin,
remove that obsolete registration before testing the plugin. Keep credentials
in the OS store. Restart the host and use a new session after updating.

Before enabling the plugin, verify the runtime and credential store:

```bash
databasin-mcp doctor --environment prod
```

After installing the plugin, restart the host or reload plugins. Confirm that
`tools/list` contains the two local authentication tools plus the server-owned
product tools. Call `databasin_get_capabilities` after sign-in before other
product workflows.

## Release gates

Do not merge or submit a release that references an unpublished client. Before
each plugin version is released:

1. Publish `@databasin/mcp-client@0.2.3` under npm's `latest` tag.
2. Deploy the true-MCP server to the production `/mcp` endpoint.
3. Verify production negotiation at protocol `2026-07-28` and compare the live
   `tools/list` names, descriptions, schemas, annotations, and timeout metadata
   with the server catalog.
4. Complete the clean-install test in [SUBMISSION.md](SUBMISSION.md).
