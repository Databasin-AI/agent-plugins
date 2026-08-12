---
name: databasin-pipelines
description: Inspect caller-visible Databasin pipeline context and draft redacted, non-executable pipeline proposals.
---

# Databasin Pipelines

Use this skill to understand existing pipeline resources and plan future pipeline work. The current MCP does not create, update, clone, schedule, validate, or run pipelines.

## Available tools

- `databasin_get_context` returns caller-visible projects, accessible connection identifiers, limits, and capabilities.
- `databasin_search` searches caller-visible pipelines, connectors, and automations.
- `databasin_describe_resource` returns a bounded, redacted resource description when the backend capability is available.
- `databasin_browse_schema` browses bounded source or destination schema metadata.
- `databasin_get_semantic_context` returns approved definitions and relationships when available.
- `databasin_profile_table` returns policy-filtered aggregate profiles when available.
- `databasin_validate_plan` validates a supported plan without execution; do not imply that it validates pipeline creation unless its returned capability explicitly says so.

## Workflow

1. Call `databasin_get_context` and resolve the project and accessible connectors from returned data.
2. Use `databasin_search` to find relevant pipelines and connectors. Never invent IDs or cross project boundaries.
3. Use `databasin_describe_resource` for selected resources and `databasin_browse_schema` for the minimum necessary schema metadata.
4. Use semantic context or aggregate profiling only when available and necessary. Treat `CAPABILITY_UNAVAILABLE` as a boundary.
5. For create, modify, clone, schedule, validate, or run requests, produce a redacted, non-executable proposal. Do not simulate success.

The proposal may include source and destination references, artifact intent, transformations, schedule intent, assumptions, risks, and validation checks. It must not contain credentials, tokens, URLs supplied to bypass fixed routes, secret configuration, or raw data copied merely for exploration.

Do not invoke a shell, CLI, generic HTTP client, or arbitrary API route. Any future pipeline mutation must use a dedicated MCP proposal/validation/execution flow, explicit user approval, and an idempotency key or stable plan hash.
