---
description: Create and test a Databasin connector with guided configuration
---

# Create Databasin Connector

Use the @databasin-connectors skill to guide the user through creating a new data connector with proper validation and testing.

The skill will handle:
- Selecting connector category (RDBMS, File & API, CRM/ERP, etc.)
- Choosing specific connector type (MySQL, PostgreSQL, S3, Salesforce, etc.)
- Gathering required and optional configuration fields
- Validating field values against connector schemas
- Creating the connector via Databasin CLI
- Testing the connection automatically
- Troubleshooting connection failures and offering configuration updates

The skill provides access to 121+ supported connector types with comprehensive configuration templates and field definitions.

## Required Context
- **project_id**: Databasin project ID (skill will prompt if not available)

## Output
- Connector ID of created connector
- Connection test results
- Location of saved JSON configuration file(s)
- Next steps for using the connector in pipelines
