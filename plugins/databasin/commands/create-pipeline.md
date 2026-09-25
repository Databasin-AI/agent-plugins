---
description: Inspect Databasin resources and draft a redacted pipeline plan
---

# Plan Databasin Pipeline

Use the `databasin-pipelines` skill. The current MCP cannot create, validate,
clone, schedule, or run pipelines.

Call `databasin_get_capabilities`, then use `databasin_get_context`,
`databasin_search`, and `databasin_get_schema` as needed. Use
`databasin_run_agent` only with the fixed `metadata_readonly` profile and an
explicit authorized scope when direct metadata is insufficient. Treat absent or
denied capabilities as boundaries. Do not invoke a shell or generic API client,
collect credentials, write secret or deployment files, or simulate execution.

Return a redacted, non-executable proposal covering source and destination references, artifacts, transformations, schedule intent, assumptions, risks, and validation checks. Explain the unavailable capability. Any future execution requires validation, explicit approval, and an idempotency key or stable plan hash.
