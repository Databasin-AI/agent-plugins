---
description: Inspect Databasin connector context and draft a redacted connector proposal
---

# Plan Databasin Connector

Use the `databasin-connectors` skill. This command is inspect-and-plan only: the current MCP cannot create, update, test, or delete connectors.

Use `databasin_get_context`, `databasin_search`, `databasin_describe_resource`, and, when relevant, `databasin_browse_schema` to gather current non-secret context. `databasin_describe_resource` may report `CAPABILITY_UNAVAILABLE`; do not bypass that boundary. Do not invoke a shell or CLI, request credentials, write configuration files, or claim that a connector was created or tested.

Return a redacted proposal with the selected project, connector type, non-secret fields, dependencies, unresolved secret references, risks, and validation checks. State that capability is unavailable. Any future mutation requires validation, explicit user approval, and an idempotency key or stable plan hash.
