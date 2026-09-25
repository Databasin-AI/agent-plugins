---
description: List accessible Databasin connectors using read-only MCP inspection
---

# List Databasin Connectors

Call `databasin_get_capabilities`, then use `databasin_get_context` to resolve
the caller-visible project and connector set. Use `databasin_search` to narrow
the list and `databasin_get_schema` when the user asks for catalogs, schemas,
tables, or columns on a selected connector.

Do not invoke a shell or CLI, request credentials, expose secret fields, or imply that listing tests or changes a connector. Report only fields returned by MCP and preserve opaque IDs exactly.
