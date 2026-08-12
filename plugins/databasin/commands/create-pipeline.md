---
description: Inspect Databasin resources and draft a redacted pipeline plan
---

# Plan Databasin Pipeline

Use the `databasin-pipelines` skill and the planning-only `databasin-pipeline-creator` agent. The current MCP cannot create, validate, clone, schedule, or run pipelines.

Use `databasin_get_context`, `databasin_search`, `databasin_describe_resource`, `databasin_browse_schema`, and available semantic/profile tools as needed. Some backend capabilities may report `CAPABILITY_UNAVAILABLE`; do not bypass that boundary. Do not invoke a shell or CLI, collect credentials, write secret or deployment files, or simulate execution.

Return a redacted, non-executable proposal covering source and destination references, artifacts, transformations, schedule intent, assumptions, risks, and validation checks. Explain the unavailable capability. Any future execution requires validation, explicit approval, and an idempotency key or stable plan hash.
