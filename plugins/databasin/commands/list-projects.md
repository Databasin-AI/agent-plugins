---
description: List accessible Databasin projects using read-only MCP inspection
---

# List Databasin Projects

Use `databasin_get_context` to list projects accessible to the current user. Use `databasin_search` or `databasin_describe_resource` only when the user asks for relevant resource details and the capability is available.

Do not invoke a shell or CLI, request credentials, or claim that listing changes permissions or project state. Report only fields returned by MCP and preserve opaque IDs exactly.
