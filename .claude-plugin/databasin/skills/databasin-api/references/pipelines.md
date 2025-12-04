# Pipelines Guide

**Working with Databasin data integration pipelines**

---

## Overview

Pipelines orchestrate data movement and transformation between connectors. They define ETL (Extract, Transform, Load) workflows.

**Base endpoint:** `/api/pipeline`

---

## List Pipelines

### Recommended: Filter by Project

```bash
# Count pipelines in project
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do" --count

# Get summary
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do" --summary

# Get specific fields
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do" \
  --fields=pipelineID,pipelineName,isActive,lastRunStatus
```

---

### Filter by Institution

```bash
# Get pipelines for organization
bun run scripts/api-call.ts GET "/api/pipeline?institutionID=1" --count

# Combine filters
bun run scripts/api-call.ts GET "/api/pipeline?institutionID=1&internalID=N1r8Do" --summary
```

---

## Pipeline Fields

### Essential Fields

- **`pipelineID`** - Unique pipeline ID
- **`pipelineName`** - Display name
- **`pipelineDescription`** - Description
- **`institutionID`** - Organization ID
- **`internalID`** - Project internal ID
- **`ownerID`** - User ID of pipeline owner

---

### Configuration Fields

- **`sourceConnectorID`** - Source connector ID
- **`targetConnectorID`** - Target connector ID
- **`transformConfig`** - Transformation configuration (JSON)
- **`scheduleConfig`** - Schedule configuration (JSON)

---

### Status Fields

- **`isActive`** - Whether pipeline is active (1 = yes, 0 = no)
- **`isDeleted`** - Deletion status
- **`lastRunStatus`** - Status of last run (success, failed, running)
- **`lastRunDate`** - Timestamp of last run
- **`nextRunDate`** - Timestamp of next scheduled run

---

## Get Specific Pipeline

### By Pipeline ID

```bash
# Get pipeline details
bun run scripts/api-call.ts GET /api/pipeline/123

# Get specific fields only
bun run scripts/api-call.ts GET /api/pipeline/123 \
  --fields=pipelineID,pipelineName,isActive,lastRunStatus
```

---

### Version 2 Endpoint

```bash
# Use v2 endpoint if available
bun run scripts/api-call.ts GET /api/pipeline/v2/123
```

---

## Create Pipeline

### Basic Example

```bash
bun run scripts/api-call.ts POST /api/pipeline '{
  "pipelineName": "Sales Data Sync",
  "pipelineDescription": "Sync sales data from Salesforce to warehouse",
  "sourceConnectorID": 58,
  "targetConnectorID": 62,
  "institutionID": 1,
  "internalID": "N1r8Do",
  "ownerID": 5,
  "isActive": 1,
  "transformConfig": {
    "mappings": [
      {"source": "AccountName", "target": "account_name"},
      {"source": "Revenue", "target": "revenue"}
    ]
  },
  "scheduleConfig": {
    "frequency": "daily",
    "time": "02:00"
  }
}'
```

---

### Required Fields

- **`pipelineName`** - Must be unique within project
- **`sourceConnectorID`** - Valid connector ID
- **`targetConnectorID`** - Valid connector ID
- **`institutionID`** - Organization ID
- **`internalID`** - Project internal ID
- **`ownerID`** - Your user ID

---

## Update Pipeline

```bash
bun run scripts/api-call.ts PUT /api/pipeline '{
  "pipelineID": 123,
  "pipelineName": "Updated Name",
  "isActive": 1
}'
```

---

## Delete Pipeline

```bash
bun run scripts/api-call.ts DELETE /api/pipeline '{"pipelineID": 123}'
```

**Note:** This soft-deletes the pipeline

---

## Run Pipeline

### Start Pipeline Execution

```bash
bun run scripts/api-call.ts POST /api/pipeline/run '{"pipelineID": 123}'
```

---

### Check Run Status

```bash
# Get pipeline with status
bun run scripts/api-call.ts GET /api/pipeline/123 \
  --fields=pipelineID,lastRunStatus,lastRunDate
```

---

## Pipeline Logs

### Get Logs for Pipeline

```bash
# Get logs for pipeline
bun run scripts/api-call.ts GET /api/pipeline/logs "pipelineID=123"

# Get logs for specific run
bun run scripts/api-call.ts GET /api/pipeline/logs "pipelineID=123&currentRunID=456"
```

---

### Log Fields

Logs typically include:

- **`timestamp`** - When log entry was created
- **`level`** - Log level (info, warning, error)
- **`message`** - Log message
- **`runID`** - Pipeline run ID
- **`pipelineID`** - Pipeline ID

---

## Common Scenarios

### Scenario 1: List All Pipelines in Project

```bash
# Get project internalId
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalId

# Count pipelines
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do" --count

# Get pipeline summary
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do" \
  --fields=pipelineID,pipelineName,isActive,lastRunStatus
```

---

### Scenario 2: Create and Run Pipeline

```bash
# Step 1: Get connectors for source and target
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" \
  --fields=connectorID,connectorName

# Step 2: Create pipeline
bun run scripts/api-call.ts POST /api/pipeline '{
  "pipelineName": "My New Pipeline",
  "sourceConnectorID": 58,
  "targetConnectorID": 62,
  "institutionID": 1,
  "internalID": "N1r8Do",
  "ownerID": 5,
  "isActive": 1
}'

# Step 3: Run pipeline (use returned pipelineID)
bun run scripts/api-call.ts POST /api/pipeline/run '{"pipelineID": 123}'
```

---

### Scenario 3: Monitor Pipeline Execution

```bash
# Check status
bun run scripts/api-call.ts GET /api/pipeline/123 \
  --fields=lastRunStatus,lastRunDate,nextRunDate

# Get logs if failed
bun run scripts/api-call.ts GET /api/pipeline/logs "pipelineID=123"
```

---

### Scenario 4: Update Pipeline Schedule

```bash
bun run scripts/api-call.ts PUT /api/pipeline '{
  "pipelineID": 123,
  "scheduleConfig": {
    "frequency": "hourly",
    "interval": 4
  }
}'
```

---

### Scenario 5: Deactivate Pipeline

```bash
# Deactivate
bun run scripts/api-call.ts PUT /api/pipeline '{
  "pipelineID": 123,
  "isActive": 0
}'

# Reactivate
bun run scripts/api-call.ts PUT /api/pipeline '{
  "pipelineID": 123,
  "isActive": 1
}'
```

---

## Token Efficiency

### Efficient Queries

```bash
# ✅ Count only (~50 tokens)
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do" --count

# ✅ Summary view (~500-2,000 tokens)
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do" --summary

# ✅ Specific fields (~500-1,000 tokens)
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do" \
  --fields=pipelineID,pipelineName,isActive \
  --limit=25
```

---

### Avoid

```bash
# ❌ Without filters - may return too much data
bun run scripts/api-call.ts GET /api/pipeline
```

---

## Related Endpoints

### Automations

Pipelines can have associated automations:

```bash
# Get automations for project
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --count
```

See **[working-endpoints.md](./working-endpoints.md)** for details.

---

## Troubleshooting

### Problem: Pipeline won't run

**Check:**

1. Pipeline is active (`isActive=1`)
2. Source connector is active
3. Target connector is active
4. Connector credentials are valid

```bash
# Check pipeline status
bun run scripts/api-call.ts GET /api/pipeline/123 --fields=isActive

# Check connectors
bun run scripts/api-call.ts GET /api/connector/58 --fields=connectorID,isActive
bun run scripts/api-call.ts GET /api/connector/62 --fields=connectorID,isActive
```

---

### Problem: Pipeline fails

**Solution:** Check logs for error details

```bash
# Get pipeline logs
bun run scripts/api-call.ts GET /api/pipeline/logs "pipelineID=123"

# Get specific run logs
bun run scripts/api-call.ts GET /api/pipeline/logs "pipelineID=123&currentRunID=456"
```

---

### Problem: Can't find pipeline

**Solution:** Verify you're using correct internalID filter

```bash
# Get your projects first
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalId

# Then query with correct internalID
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do"
```

---

## See Also

- **[connectors.md](./connectors.md)** - Working with connectors
- **[projects-and-organizations.md](./projects-and-organizations.md)** - Get project details
- **[token-efficiency.md](./token-efficiency.md)** - Optimize API usage
- **[working-endpoints.md](./working-endpoints.md)** - Complete endpoint reference
- **[error-handling.md](./error-handling.md)** - Troubleshooting guide

---

**Last Updated:** 2025-11-17
