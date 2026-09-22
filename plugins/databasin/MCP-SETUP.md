# MCP setup

The plugin registers a local stdio MCP server through [`.mcp.json`](.mcp.json):

```text
npx -y @databasin/mcp-client@0.2.0 --environment prod
```

The local client connects to `https://databasin.cloud/mcp` with true Streamable
HTTP MCP, discovers product tools from the server, and mirrors those tools to the
host. It pins protocol version `2026-07-28`; there is no REST or legacy-protocol
fallback.

## Authentication

The client exposes two local tools:

- `databasin_auth_status` checks local sign-in state.
- `databasin_login` starts Microsoft Entra device sign-in and returns a
  short-lived Microsoft URL and user code.

Enter credentials only on Microsoft's page. The client stores tokens in the
OS-protected credential store and sends a bearer token only on remote
`tools/call` requests. It does not place tokens in MCP output.

## Local checks

Before enabling the plugin, verify the runtime and credential store:

```bash
npx -y @databasin/mcp-client@0.2.0 doctor --environment prod
```

After installing the plugin, restart the host or reload plugins. Confirm that
`tools/list` contains the two local authentication tools plus the server-owned
product tools. Call `databasin_get_capabilities` after sign-in before other
product workflows.

## Release gates

Do not merge or submit a release that references an unpublished client. Before
version `0.9.0` is released:

1. Publish `@databasin/mcp-client@0.2.0` under npm's `latest` tag.
2. Deploy the true-MCP server to the production `/mcp` endpoint.
3. Verify production negotiation at protocol `2026-07-28` and compare the live
   `tools/list` names, descriptions, schemas, annotations, and timeout metadata
   with the server catalog.
4. Complete the clean-install test in [SUBMISSION.md](SUBMISSION.md).
