---
description: Create a DataBasin pipeline using the interactive wizard or programmatic workflow
---

# Create DataBasin Pipeline

## Purpose

Create DataBasin data pipelines using one of three approaches:

1. **Interactive Wizard** (Recommended for Manual Use) - Full guided experience with schema discovery
2. **Programmatic Creation** (Recommended for Automation) - Individual CLI commands to build JSON payload
3. **Direct API Call** (Advanced) - Raw API requests with manual configuration

For complete reference documentation and examples, see:
- **Complete Guide**: `src/cli/PIPELINE-CREATION-GUIDE.md`
- **Working Example**: `src/cli/example-pipeline-create.sh`

## Prerequisites

```bash
# Verify CLI is available
databasin --version

```

---

## Programmatic Creation

Create pipelines programmatically by gathering information via individual CLI commands, then submitting a JSON payload.

### Complete Working Example

A fully functional bash script demonstrating this workflow is available at:
**`src/cli/example-pipeline-create.sh`**

The script demonstrates:
- Color-coded output with progress indicators
- Configuration variables for easy customization
- Complete 12-step workflow from data gathering to pipeline creation
- JSON validation and user confirmation
- Error handling and validation

### Workflow Overview

#### Step 1: Get Project Information

```bash
# List all projects and find target project
databasin projects list --json | jq '.[] | select(.internalId == "N1r8Do")'

# Extract project details
PROJECT_JSON=$(databasin projects list --json | jq -r '.[] | select(.internalId == "N1r8Do")')
INSTITUTION_ID=$(echo "$PROJECT_JSON" | jq -r '.institutionId')
```

#### Step 2: Get User Information

```bash
# Get current user details
databasin auth whoami --json

# Extract user ID
USER_JSON=$(databasin auth whoami --json)
USER_ID=$(echo "$USER_JSON" | jq -r '.id')
```

#### Step 3: List and Verify Connectors

```bash
# List all connectors for project
databasin connectors list --project N1r8Do --full --json

# Verify specific connectors exist
CONNECTORS_JSON=$(databasin connectors list --project N1r8Do --full --json)
SOURCE_CONNECTOR=$(echo "$CONNECTORS_JSON" | jq -r '.[] | select(.connectorID == "5464")')
TARGET_CONNECTOR=$(echo "$CONNECTORS_JSON" | jq -r '.[] | select(.connectorID == "5075")')
```

#### Step 4: Discover Schemas and Tables

```bash
# For RDBMS connectors (postgres, mysql, etc.)
databasin sql catalogs <connectorId>
databasin sql tables <connectorId> <schema>

# For lakehouse connectors (databricks, snowflake)
databasin sql catalogs <connectorId>
databasin sql schemas <connectorId> --catalog <catalog>
databasin sql tables <connectorId> <schema> --catalog <catalog>
```

#### Step 5: Get AI Ingestion Recommendations (Optional)

```bash
# Get AI-powered ingestion type recommendations
databasin api post /api/connector/ingestiontype \
  --data '{
    "connectorID": 5464,
    "objects": ["users", "orders"],
    "chosenDatabaseSchema": "main",
    "catalog": "config"
  }'
```

#### Step 6: Build JSON Payload

```bash
# Create complete pipeline configuration
cat > pipeline.json <<'EOF'
{
  "pipelineName": "Automated Pipeline",
  "sourceConnectorID": "5464",
  "targetConnectorID": "5075",
  "institutionID": 42,
  "internalID": "N1r8Do",
  "ownerID": 31,
  "ingestionPattern": "datalake",
  "targetCatalogName": "hive_metastore",
  "targetSchemaName": "default",
  "jobDetails": {
    "jobName": "Automated Pipeline-job",
    "jobRunSchedule": "0 2 * * *",
    "jobRunTimeZone": "America/New_York",
    "jobClusterSize": "Small",
    "jobTimeoutSeconds": "43200",
    "jobOwnerEmail": "",
    "tags": [],
    "emailNotifications": [],
    "jobTimeout": "43200"
  },
  "items": [
    {
      "sourceObjectName": "users",
      "targetObjectName": "users",
      "sourceSchema": "main",
      "columns": "*",
      "ingestionType": "full",
      "primaryKeys": null,
      "timestampColumn": null,
      "autoExplode": false,
      "detectDeletes": false,
      "priority": false,
      "replaceTable": false,
      "backloadNumDays": 0,
      "snapshotRetentionPeriod": 3
    }
  ]
}
EOF
```

#### Step 7: Create Pipeline

```bash
# Submit pipeline configuration
databasin api post /api/pipeline --data @pipeline.json
```

### Programmatic Workflow Script Template

```bash
#!/bin/bash
set -e  # Exit on error

# Configuration
PROJECT_ID="N1r8Do"
SOURCE_CONNECTOR_ID="5464"
TARGET_CONNECTOR_ID="5075"
PIPELINE_NAME="Programmatic-Pipeline-$(date +%s)"

# 1. Get project info
PROJECT_JSON=$(databasin projects list --json | jq -r ".[] | select(.internalId == \"$PROJECT_ID\")")
INSTITUTION_ID=$(echo "$PROJECT_JSON" | jq -r '.institutionId')

# 2. Get user info
USER_JSON=$(databasin auth whoami --json)
USER_ID=$(echo "$USER_JSON" | jq -r '.id')

# 3. Verify connectors exist
CONNECTORS_JSON=$(databasin connectors list --project "$PROJECT_ID" --full --json)
SOURCE_CONNECTOR=$(echo "$CONNECTORS_JSON" | jq -r ".[] | select(.connectorID == \"$SOURCE_CONNECTOR_ID\")")
TARGET_CONNECTOR=$(echo "$CONNECTORS_JSON" | jq -r ".[] | select(.connectorID == \"$TARGET_CONNECTOR_ID\")")

if [ -z "$SOURCE_CONNECTOR" ] || [ -z "$TARGET_CONNECTOR" ]; then
    echo "Error: Connectors not found"
    exit 1
fi

# 4. Discover tables (example - adjust for your connector type)
# TABLES_JSON=$(databasin sql tables "$SOURCE_CONNECTOR_ID" "main" --json)

# 5. Build artifacts array
ARTIFACTS_JSON='[
  {
    "sourceObjectName": "users",
    "targetObjectName": "users",
    "sourceSchema": "main",
    "columns": "*",
    "ingestionType": "full"
  }
]'

# 6. Build complete payload
PAYLOAD=$(cat <<EOF
{
  "pipelineName": "$PIPELINE_NAME",
  "sourceConnectorID": "$SOURCE_CONNECTOR_ID",
  "targetConnectorID": "$TARGET_CONNECTOR_ID",
  "institutionID": $INSTITUTION_ID,
  "internalID": "$PROJECT_ID",
  "ownerID": $USER_ID,
  "ingestionPattern": "datalake",
  "targetCatalogName": "hive_metastore",
  "targetSchemaName": "default",
  "jobDetails": {
    "jobName": "$PIPELINE_NAME-job",
    "jobRunSchedule": "0 2 * * *",
    "jobRunTimeZone": "America/New_York",
    "jobClusterSize": "Small",
    "jobTimeoutSeconds": "43200"
  },
  "items": $ARTIFACTS_JSON
}
EOF
)

# 7. Create pipeline
echo "$PAYLOAD" | jq . > /tmp/pipeline.json
databasin api post /api/pipeline --data @/tmp/pipeline.json
```

For a complete, production-ready version of this script with error handling, validation, and user prompts, see **`src/cli/example-pipeline-create.sh`**.

---

## Required Payload Fields

### Always Required

- `pipelineName` - Unique, descriptive name
- `sourceConnectorID` - Source data connector
- `targetConnectorID` - Target data connector
- `institutionID` - Organization/institution ID (from project)
- `internalID` - Project internal ID
- `ownerID` - User ID creating the pipeline
- `ingestionPattern` - Either "datalake" or "data warehouse"
- `targetSchemaName` or `targetCatalogName` - Target destination
- `jobDetails` - Scheduling configuration
- `items` - Array of artifacts (minimum 1)

### Job Details

- `jobRunSchedule` - Cron expression or null for manual
- `jobRunTimeZone` - IANA timezone (e.g., "America/New_York")
- `jobClusterSize` - "Small", "Medium", or "Large"
- `jobTimeoutSeconds` - Max execution time (default: 43200 = 12 hours)

### Artifact (Item) Fields

- `sourceObjectName` - Table/object name in source
- `targetObjectName` - Table/object name in target
- `sourceSchema` - Source schema name
- `columns` - Column list or "*" for all
- `ingestionType` - "full", "incremental", or "snapshot"
- `primaryKeys` - Array of key columns (null if none)
- `timestampColumn` - For incremental (null if not applicable)
- `autoExplode` - Boolean (default: false)
- `detectDeletes` - Boolean (default: false)
- `priority` - Boolean (default: false)
- `replaceTable` - Boolean (default: false)
- `backloadNumDays` - Number (default: 0)
- `snapshotRetentionPeriod` - Number (default: 3)

## Examples

### Batch Create Multiple Pipelines

```bash
# Loop through configurations
for config in configs/*.json; do
  databasin api post /api/pipeline --data @"$config"
done
```

---

## Getting Help

### Command Help

```bash

# Connector listing
databasin connectors --help


# Pipeline create help
databasin pipelines create --help

# SQL discovery
databasin sql --help
```

### Common Issues

**Issue:** "Institution ID is required"
- **Solution:** Ensure project has valid `institutionId` field
- **Check:** `databasin projects list --fields id,internalId,institutionId`

**Issue:** "Connector not found"
- **Solution:** Verify connector belongs to the correct project
- **Check:** `databasin connectors list --project <projectId>`

**Issue:** "Validation failed"
- **Solution:** Review payload structure against required fields above
- **Debug:** Use `--debug` flag to see detailed validation errors


