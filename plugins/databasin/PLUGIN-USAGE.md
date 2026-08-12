# Databasin plugin usage

This plugin supplies Databasin-specific workflows for Claude Code and Codex/OpenAI. It is designed to guide an agent through the fixed-purpose Databasin MCP tools; it is not an arbitrary API client and does not require the Databasin CLI at runtime.

## Supported workflows

- Discover caller-visible projects, connectors, pipelines, and automations.
- Browse bounded catalog, schema, table, and column metadata.
- Retrieve approved semantic context and aggregate table profiles when those backend capabilities are enabled.
- Validate a read-only SQL plan before execution.
- Submit an enabled read-only SQL operation, poll bounded result pages, and cancel an operation.
- Draft redacted connector, pipeline, and automation proposals without pretending unsupported mutations were applied.

## Safety model

- Start with `databasin_get_context` and remain within the returned projects and connectors.
- Prefer metadata, semantic context, and aggregate profiles over raw rows.
- Never provide credentials, tokens, connection strings, arbitrary URLs, headers, roles, or model-supplied identities to tools.
- Never use a generic API request or the CLI to bypass missing MCP capabilities.
- Treat `CAPABILITY_UNAVAILABLE` as a real boundary.
- Validate SQL before calling `databasin_run_sql`; execution may be disabled by deployment policy.
- Keep SQL columns, rows, bytes, and time ranges bounded.

## Example prompts

- “Which Databasin projects and connectors can I access?”
- “Find pipelines related to customer analytics.”
- “Browse the schemas available through this connector.”
- “Explain the approved revenue metric before writing SQL.”
- “Validate and run a bounded read-only query for monthly totals.”
- “Draft a redacted pipeline proposal using these existing connectors.”

## MCP connection

The plugin repository intentionally does not contain a guessed production MCP URL or OpenAI app registration ID. Follow [MCP-SETUP.md](MCP-SETUP.md) after a real endpoint has been deployed and registered.

The files under `examples/` and older skill reference directories document historical CLI behavior. They are not active MCP instructions, may be stale, and must never override the current skill contract or server authorization.
