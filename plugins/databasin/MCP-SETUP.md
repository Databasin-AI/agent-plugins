# Remote MCP setup

Remote MCP wiring is intentionally deployment-gated. Add it only after the Databasin MCP service has been deployed and registered with the target Claude Code or Codex/OpenAI host.

## Current tool names

- `databasin_get_context`
- `databasin_search`
- `databasin_describe_resource`
- `databasin_browse_schema`
- `databasin_get_semantic_context`
- `databasin_profile_table`
- `databasin_validate_plan`
- `databasin_run_sql`
- `databasin_get_operation`
- `databasin_cancel_operation`

## Before wiring the host

1. Deploy the MCP service.
2. Register it with the intended host and obtain the real approved configuration values.
3. Configure the host with those values using its supported MCP/app integration.
4. Verify OAuth discovery, audience validation, user-preserving downstream delegation, per-tool scopes, and each tool's availability.
5. Verify every tool annotation against actual side effects. In particular, `databasin_run_sql` enqueues an operation and must not be advertised as read-only merely because its SQL is restricted to reads.
6. Run the positive and negative cases in [`../../tests/AGENT-BEHAVIOR-MATRIX.md`](../../tests/AGENT-BEHAVIOR-MATRIX.md) against the deployed server.

No `.mcp.json` or `.app.json` is checked in at this stage. Do not create one until a real deployment/registration supplies the endpoint or app metadata. This repository also does not invent privacy URLs, terms URLs, or visual assets.
