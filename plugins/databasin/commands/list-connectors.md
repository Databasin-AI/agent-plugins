---
description: List accessible Databasin connectors using read-only MCP inspection
---

# List Databasin Connectors

Use `databasin_get_context` to resolve the caller-visible project and connector set, then `databasin_search` to narrow the list. If the user selects one for more detail, use `databasin_describe_resource`; explain `CAPABILITY_UNAVAILABLE` if the backend description contract is not enabled.

Do not invoke a shell or CLI, request credentials, expose secret fields, or imply that listing tests or changes a connector. Report only fields returned by MCP and preserve opaque IDs exactly.
