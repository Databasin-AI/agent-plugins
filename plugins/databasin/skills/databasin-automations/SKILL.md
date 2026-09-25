---
name: databasin-automations
description: Discover caller-visible Databasin automations and draft redacted proposals for unsupported automation changes. Use for automation inventory, dependencies, schedules, or change planning.
---

# Databasin Automations

Use this skill to find automation resources and plan future automation work. The current MCP does not create, update, delete, enable, disable, or run automations.

## Tools

Treat the connected server's `tools/list` response as authoritative. Authenticate
with the client-local `databasin_auth_status` and `databasin_login` tools when
needed, then call `databasin_get_capabilities` before product tools.

- Use `databasin_get_context` for caller-visible projects and connectors.
- Use `databasin_search` for bounded automation, pipeline, and connector metadata.
- Use `databasin_run_agent` with the fixed `metadata_readonly` profile only when a
  deeper metadata question cannot be answered from context and search. Use the
  run status and cancellation tools only for the returned run identifier.

## Workflow

1. Call `databasin_get_capabilities`, then `databasin_get_context`, and remain
   inside the caller-visible project set.
2. Use `databasin_search` to locate relevant automations and dependencies.
3. If authorized metadata is insufficient, either ask a focused question or use
   `databasin_run_agent` within an explicit returned institution/project scope.
4. For create, update, delete, enable, disable, test, or run requests, return a
   redacted proposal only.

Include schedule or trigger intent, task outline, dependencies, timezone assumptions, risks, and validation checks. Never request or expose credentials, tokens, secret task parameters, notebook contents, or private configuration. Do not write automation files or invoke a shell, CLI, generic HTTP client, or arbitrary API route.

Any future automation mutation must use dedicated fixed-purpose MCP tools, server-side validation, explicit user approval, and an idempotency key or stable plan hash. Never claim an automation was created, changed, enabled, or run.
