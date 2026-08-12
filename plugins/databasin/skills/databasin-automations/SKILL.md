---
name: databasin-automations
description: Discover caller-visible Databasin automations and draft redacted proposals for unsupported automation changes.
---

# Databasin Automations

Use this skill to find automation resources and plan future automation work. The current MCP does not create, update, delete, enable, disable, or run automations.

## Available tools

- `databasin_get_context` returns caller-visible projects, accessible connections, limits, and capabilities.
- `databasin_search` searches caller-visible automations, pipelines, and connectors.
- `databasin_describe_resource` returns a bounded, redacted automation or related-resource description when the backend capability is available.

## Workflow

1. Call `databasin_get_context` and remain inside the caller-visible project set.
2. Use `databasin_search` to locate relevant automations and dependencies.
3. Use `databasin_describe_resource` for a selected automation, pipeline, or connector. If it reports `CAPABILITY_UNAVAILABLE`, explain the limitation instead of guessing configuration or status.
4. For create, update, delete, enable, disable, test, or run requests, return a redacted proposal only.

Include schedule or trigger intent, task outline, dependencies, timezone assumptions, risks, and validation checks. Never request or expose credentials, tokens, secret task parameters, notebook contents, or private configuration. Do not write automation files or invoke a shell, CLI, generic HTTP client, or arbitrary API route.

Any future automation mutation must use dedicated fixed-purpose MCP tools, server-side validation, explicit user approval, and an idempotency key or stable plan hash. Never claim an automation was created, changed, enabled, or run.
