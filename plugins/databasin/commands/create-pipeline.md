---
description: Create a Databasin pipeline using the pipeline agent and an interactive workflow
---

# Create Databasin Pipeline

Have the @agent-databasin-pipeline-creator agent guide the user through creating a Databasin data pipeline using the databasin-pipeline.

The skill supports:
- Database/Catalog, Schema, and Table discovery
- AI recommendations for how to ingest data
- Programmatic creation using individual CLI commands
- Full validation and error handling
- Complete documentation and working examples

The databasin-pipelines skill provides comprehensive documentation, examples, and templates for all pipeline creation approaches.

## Instructions

Use the databasin-pipelines skill and the databasin CLI tool to create a new pipeline based on the information provide in the conversation, the databasin CLI help and docs, available templates, and information returned by the databasin CLI such as a list of schemas for the user to choose from. The agent should ask the user clarifying questions when more context is needed, or a choice needs to be made.
