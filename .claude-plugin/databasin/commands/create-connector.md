---
description: Create and test a Databasin connector with guided configuration
---

# Create Databasin Connector

## Purpose
Creates a new Databasin data connector by guiding the user through all required configuration fields, validating against connector schemas, creating the connector via CLI, and automatically testing the connection. Use when adding new data sources to a Databasin project.

## Required Information
Before executing, gather or confirm:
- **project_id**: Databasin project ID (prompt user if not in context)
- **connector_category**: Category type (RDBMS, FileAPI, CRM/ERP, etc.)
- **connector_name**: Specific connector (MySQL, PostgreSQL, S3, etc.)
- **connector_fields**: All required fields based on selected connector type

## Configuration File Locations
- Connector types: `static/config/connectors/v2/types/`
- Field definitions: `static/config/connectors/v2/fields/DatabasinConnectorFieldsAuth.json`

## Connector Type ID Mapping

**CRITICAL**: The API expects `connectorType` as an integer ID and `connectorSubType` as the exact connector name string.

### Type IDs (from static config files):
- **RDBMS** = 1 (DatabasinConnectorRDBMS.json)
- **Big Data & NoSQL** = 2 (DatabasinConnectorBigDataNoSQL.json)
- **File & API** = 3 (DatabasinConnectorFileAPI.json)
- **Marketing** = 4 (DatabasinConnectorMarketing.json)
- **CRM & ERP** = 5 (DatabasinConnectorCRMERP.json)
- **ECommerce** = 6 (DatabasinConnectorECommerce.json)
- **Accounting** = 7 (DatabasinConnectorAccounting.json)
- **Collaboration** = 8 (DatabasinConnectorCollaboration.json)
- **AI & LLM** = 9 (DatabasinConnectorAILLM.json)

### Important Notes:
- **Case Sensitive**: `connectorSubType` must match exactly as defined in the JSON config files (e.g., "Postgres" not "postgres", "MySQL" not "mysql")
- Each type JSON file contains an `availableConnectors` array with the exact `connectorName` values to use
- To find valid connector names: `jq '.availableConnectors[].connectorName' /path/to/type/file.json`

### Example JSON Format:
```json
{
  "connectorName": "My Database",
  "connectorType": 1,
  "connectorSubType": "Postgres",
  "connectorAuthType": "basic",
  "institutionID": 17,
  "internalID": "project-id",
  "connectorHost": "localhost",
  "connectorPort": "5432",
  "connectorDatabaseName": "mydb",
  "connectorUsername": "user",
  "connectorPassword": "pass"
}
```

## Steps

### Step 1: Determine Project Context
Check if project ID is available in conversation context or recent commands.

If not available, prompt user:
```
What is your Databasin project ID?
```

Store the project ID for use in Step 8.

### Step 2: Select Connector Category
List available connector categories by reading the types directory:

Command:
```bash
ls static/config/connectors/v2/types/
```

Parse the filenames to extract categories:
- `DatabasinConnectorRDBMS.json` → RDBMS (Relational Databases)
- `DatabasinConnectorFileAPI.json` → File & API
- `DatabasinConnectorCRMERP.json` → CRM/ERP
- `DatabasinConnectorAccounting.json` → Accounting
- `DatabasinConnectorCollaboration.json` → Collaboration
- `DatabasinConnectorECommerce.json` → E-Commerce
- `DatabasinConnectorMarketing.json` → Marketing
- `DatabasinConnectorBigDataNoSQL.json` → Big Data/NoSQL
- `DatabasinConnectorAILLM.json` → AI/LLM

Present these options to the user and ask them to select one.

### Step 3: Select Specific Connector
Load the selected category's JSON file and parse available connectors.

Command:
```bash
cat static/config/connectors/v2/types/DatabasinConnector{Category}.json
```

Parse the JSON and extract `availableConnectors` array. For each connector, show:
- `connectorName`
- `active` status (only show active connectors)

Present the list to the user and have them select the specific connector they want to create.

### Step 4: Load Connector Requirements
From the selected connector object, extract:
- `connectorRequiredFields` - array of field IDs that are required
- `connectorOptionalFields` - array of field IDs that are optional
- `connectorAuthTypes` - array of supported authentication type IDs

Store these for field mapping in the next step.

### Step 5: Load Field Definitions
Read the field definitions file:

Command:
```bash
cat static/config/connectors/v2/fields/DatabasinConnectorFieldsAuth.json
```

Parse the JSON to get the complete field definitions. Map the field IDs from Step 4 to their definitions which include:
- `fieldName` - Human-readable name
- `apiName` - API property name to use in JSON
- `fieldType` - Data type
- `helpText` - Help text to show user

### Step 6: Prompt for Required Fields
For each required field ID (from Step 4), look up the field definition (from Step 5) and prompt the user:

```
{fieldName}: {helpText}
Enter value for {fieldName}:
```

Special handling:
- **connectorName field (reqID: 1)**: Always first, this becomes the connector name
- **Authentication fields**: If the field is related to credentials (username, password, apiKey), note this is sensitive
- **Port fields**: Suggest common defaults (e.g., 5432 for PostgreSQL, 3306 for MySQL)
- **Boolean fields**: Accept yes/no and convert to true/false

Build a configuration object mapping each `apiName` to the user's provided value.

### Step 7: Prompt for Optional Fields
Ask the user:
```
Do you want to configure optional fields? (yes/no)
```

If yes, iterate through optional field IDs and prompt similarly to Step 6, allowing the user to skip any field.

Add provided optional fields to the configuration object.

### Step 8: Determine Connector Type and SubType
Look up the connector type ID and exact subtype name from the selected connector:

1. **Get connectorType ID**: Use the mapping from "Connector Type ID Mapping" section above
   - Example: RDBMS category = 1, File & API = 3, etc.

2. **Get exact connectorSubType**: Extract the `connectorName` field from the selected connector in Step 3
   - Example: For Postgres, use exactly "Postgres" (capital P)
   - Example: For MySQL, use exactly "MySQL"
   - **Case sensitivity matters!**

3. **Get institutionID**: This is typically 17 for most deployments (check existing connectors in the project)

### Step 9: Assemble Connector JSON
Create a complete connector configuration JSON object with ALL fields at the root level:

```json
{
  "connectorName": "{value from field reqID:1}",
  "connectorType": {numeric ID from Step 8},
  "connectorSubType": "{exact name from Step 8}",
  "connectorAuthType": "{auth type from connector config}",
  "institutionID": {institution ID from Step 8},
  "internalID": "{project_id from Step 1}",
  "connectorHost": "{value from field apiName:connectorHost}",
  "connectorPort": "{value from field apiName:connectorPort}",
  "connectorDatabaseName": "{value from field apiName:connectorDatabaseName}",
  "connectorUsername": "{value from auth field}",
  "connectorPassword": "{value from auth field}",
  "{other collected fields...}": "{values...}"
}
```

**Important**:
- All fields go at the root level (NO nested "configuration" object)
- Use the `apiName` from field definitions as the JSON property name
- Include only fields that were collected in Steps 6-7
- `connectorType` is an integer, `connectorSubType` is a string

### Step 10: Save Connector JSON to File
Generate a timestamp-based filename and save the JSON:

Command:
```bash
cat > connector-$(date +%Y%m%d-%H%M%S).json << 'EOF'
{assembled JSON from Step 9}
EOF
```

Store the filename for use in the next step.

Success: File created message with filename
Failure: Stop workflow, report write error

### Step 11: Create Connector via CLI
Execute the Databasin CLI create command:

Command:
```bash
src/cli/dist/linux-x64/databasin connectors create {filename} --project {project_id}
```

Success: Extract the connector ID from the output (look for "ID: {connectorID}")
Failure: Stop workflow, show error details, suggest checking:
- JWT authentication (may need to run `databasin auth login`)
- Project ID validity
- Required field completeness

Store the connector ID for testing.

### Step 12: Test Connector Connection
Automatically test the newly created connector:

Command:
```bash
src/cli/dist/linux-x64/databasin connectors test {connectorID}
```

Success: Report successful connection with any returned connection details
Failure: Proceed to Step 13 for troubleshooting

### Step 13: Troubleshoot Failed Connection (if needed)
If the test fails, analyze the error output and provide guidance:

**Common Database Connection Errors:**
- "Connection refused" → Check host and port are correct, firewall allows connection
- "Authentication failed" → Verify username/password are correct
- "Database does not exist" → Check database name spelling
- "SSL required" → May need to add SSL/TLS configuration

**Common API Connection Errors:**
- "Invalid credentials" → Check API key or OAuth tokens
- "Unauthorized" → Verify authentication type matches API requirements
- "Timeout" → Check base URL is correct and API is reachable

**Offer to Update Configuration:**
Ask the user:
```
Would you like to update the connector configuration to fix the issue? (yes/no)
```

If yes:
1. Show current configuration from the JSON file
2. Ask which field(s) need to be updated
3. Create an update JSON with only the changed fields
4. Save to `connector-update-{timestamp}.json`
5. Execute: `databasin connectors update {connectorID} connector-update-{timestamp}.json`
6. Retry the test (return to Step 12)

If no, end workflow and report the connector ID for manual troubleshooting.

## Error Handling

- **Step 2-5 (File reading fails)**: Stop workflow, verify the Databasin config files exist at the specified paths
- **Step 10 (File write fails)**: Check write permissions in current directory
- **Step 11 (Create fails - 401)**: User needs to authenticate first: `databasin auth login`
- **Step 11 (Create fails - 400)**: Configuration validation failed, check required fields match API expectations
- **Step 11 (Create fails - 404)**: Project ID not found, verify project exists
- **Step 12 (Test unavailable)**: Some connectors don't support testing (`testConnectorSupport: false`), this is expected
- **Any step (JSON parse fails)**: Config file may be malformed, check JSON syntax

## Output

When complete, report:
- Connector ID of created connector
- Connector name and type
- Test result (success or failure details)
- Location of saved JSON configuration file(s)
- Next steps (e.g., "Use this connector in a pipeline with `databasin pipelines create`")

## Notes

- The workflow uses the comprehensive connector configuration system with 121+ supported connector types
- Field definitions are looked up dynamically to provide context-specific help text
- Authentication types are validated against the connector's supported auth methods
- Some connectors may have connector-specific fields beyond the common ones
- The generated JSON files are saved in the current working directory for reference and reuse
