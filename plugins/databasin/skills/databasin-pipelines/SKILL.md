---
name: databasin-pipelines
description: Inspect caller-visible Databasin pipeline context and draft redacted, non-executable pipeline proposals. Use for pipeline discovery, dependency analysis, source/destination schema planning, or proposed pipeline changes.
---

# Databasin Pipelines

Use this skill to understand existing pipeline resources and plan future pipeline work. The current MCP does not create, update, clone, schedule, validate, or run pipelines.

## Tools

Treat the connected server's `tools/list` response as authoritative. Authenticate
with the client-local `databasin_auth_status` and `databasin_login` tools when
needed, then call `databasin_get_capabilities` before product tools.

- Use `databasin_get_context` for caller-visible projects and connectors.
- Use `databasin_search` for bounded pipeline, connector, and automation metadata.
- Use `databasin_get_schema` for bounded source or destination schema metadata.
- Use `databasin_run_agent` with the fixed `metadata_readonly` profile only when a
  deeper metadata question cannot be answered from the direct discovery tools.

## Workflow

1. Call `databasin_get_capabilities`, then `databasin_get_context`, and resolve
   the project and accessible connectors from returned data.
2. Use `databasin_search` to find relevant pipelines and connectors. Never invent IDs or cross project boundaries.
3. Use `databasin_get_schema` for the minimum necessary source and destination
   metadata, one hierarchy level at a time.
4. If authorized metadata is insufficient, ask a focused question or use
   `databasin_run_agent` within the explicit returned scope.
5. For create, modify, clone, schedule, validate, or run requests, produce a
   redacted, non-executable proposal. Do not simulate success.

The proposal may include source and destination references, artifact intent, transformations, schedule intent, assumptions, risks, and validation checks. It must not contain credentials, tokens, URLs supplied to bypass fixed routes, secret configuration, or raw data copied merely for exploration.

Do not invoke a shell, CLI, generic HTTP client, or arbitrary API route. Any future pipeline mutation must use a dedicated MCP proposal/validation/execution flow, explicit user approval, and an idempotency key or stable plan hash.
