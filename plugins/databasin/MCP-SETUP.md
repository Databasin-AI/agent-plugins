# Remote MCP setup

Remote MCP wiring is intentionally deployment-gated. Add it only after the Databasin MCP service has been deployed and registered with the target Claude Code or Codex/OpenAI host. This repository contains no guessed endpoint, app ID, credentials, privacy URL, terms URL, or demo URL.

## Supported tool catalog

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

The catalog has ten supported names. A deployment must advertise only the
runtime-enabled subset whose backend capability is available. Reviewers must be
able to call every tool in the production scan, so unavailable tools must be
omitted from `tools/list` and from the submitted cases.

## Before wiring the host

1. Deploy the MCP service at a public production HTTPS origin.
2. Register it with the intended host and obtain the real approved configuration values.
3. Configure the host with those values using its supported MCP/app integration.
4. Verify OAuth discovery, audience validation, user-preserving downstream delegation, per-tool scopes, and each tool's availability.
5. Verify every tool annotation against actual side effects. `databasin_run_sql` enqueues an operation, so its `readOnlyHint` must be `false` even though the SQL policy is read-oriented. `databasin_cancel_operation` changes operation state and is marked destructive because cancellation can stop work irreversibly.
6. Configure the exact domain-verification challenge value supplied by the OpenAI submission flow at `/.well-known/openai-apps-challenge`.
7. Bind the five positive and three negative cases in [`../../tests/AGENT-BEHAVIOR-MATRIX.md`](../../tests/AGENT-BEHAVIOR-MATRIX.md) to the production `tools/list` response, rewriting any positive case whose named capability is not advertised. Retain evidence for the resulting submission cases; never ask reviewers to call an unavailable tool.
8. Complete the remaining external gates in [`SUBMISSION.md`](SUBMISSION.md).

No `.mcp.json` or `.app.json` is checked in at this stage. Do not create one until a real deployment/registration supplies the endpoint or app metadata. This repository also does not invent privacy URLs, terms URLs, credentials, or visual assets.
