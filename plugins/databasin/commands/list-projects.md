---
description: List accessible Databasin projects using read-only MCP inspection
---

# List Databasin Projects

Call `databasin_get_capabilities`, then use `databasin_get_context` to list
projects accessible to the current user. Use `databasin_search` only when the
user asks for relevant pipeline, connector, or automation details.

Do not invoke a shell or CLI, request credentials, or claim that listing changes permissions or project state. Report only fields returned by MCP and preserve opaque IDs exactly.
