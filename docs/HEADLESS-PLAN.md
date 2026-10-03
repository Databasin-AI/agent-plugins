# Headless plugin fixes for issues 6–9

## Implementation and dependencies

1. Client 0.2.3 fixes lazy native loading, safe diagnostics, encrypted container
   persistence, and externally supplied short-lived tokens. Keep keyring as the
   default and all existing Auth0 claim checks. Its `docs/HEADLESS-REMEDIATION.md`
   records the storage design, security constraints, and release gates.
2. Plugin 0.9.4 launches Node, not a hard-coded package manager. Select an exact
   preinstalled client first, then npm, Bun, or pnpm. Never use a shell or retry
   through another runner after the launched client fails. A bare Node image
   needs the pinned package preinstalled during image construction.
3. Claude uses its documented plugin-root substitution in `.mcp.json`. Codex
   uses plugin-relative `cwd` and explicit environment forwarding in a separate
   `.mcp.codex.json`. No secret values are written into either configuration.
4. Validate runner selection and pinning on Linux/macOS/Windows, plus strict
   manifests and environment allowlists. Client CI runs non-root containers with
   no npm and both missing-native-library and missing-session-bus conditions.

## Release order and remaining environment verification

The plugin's 0.2.3 dependency must be published and qualified before this plugin
branch is merged. Then publish the matching plugin version and registry record.
Do not close the reported issues merely because validation accepts the manifest.
Verify the released plugin inside the reporting Azure Container App, including
real user device sign-in, restart, refresh, and an authorized MCP call. This
requires identifying that app and provisioning its chosen credential source.

The implementation does not make the private client repository public. Public
support points to this repository; npm keeps the correct private provenance
source. No production MCP routes or authorization rules are changed.

References: [Claude MCP](https://code.claude.com/docs/en/mcp#plugin-provided-mcp-servers),
[OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins),
[OWASP cryptographic storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html).
