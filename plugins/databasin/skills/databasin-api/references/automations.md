# Automations Guide

**Working with Databasin pipeline automations and scheduling**

---

## Overview

Automations define scheduled executions and triggers for pipelines. They control when and how pipelines run automatically.

**Base endpoint:** `/api/automations`

**⚠️ IMPORTANT:** This endpoint requires `internalID` parameter or returns null.

---

## List Automations

### Required Parameter: internalID

```bash
# Count automations in project
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --count

# Get summary
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --summary

# Get specific fields
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" \
  --fields=automationID,automationName,pipelineID,isActive,scheduleType
```

---

### Without internalID Returns Null

```bash
# ❌ Returns null
bun run scripts/api-call.ts GET /api/automations --count
# Output: {"count": 0}

# ✅ With internalID returns data
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --count
# Output: {"count": 17}
```

**See:** [Error Handling Guide](./error-handling.md) for null response troubleshooting

---

## Automation Fields

### Essential Fields

- **`automationID`** - Unique automation ID
- **`automationName`** - Display name
- **`pipelineID`** - Associated pipeline ID
- **`institutionID`** - Organization ID
- **`internalID`** - Project internal ID
- **`ownerID`** - User ID of automation owner

---

### Schedule Configuration

- **`scheduleType`** - Schedule type (cron, interval, trigger, etc.)
- **`scheduleConfig`** - Schedule configuration (JSON)
- **`cronExpression`** - Cron expression if using cron schedule
- **`intervalMinutes`** - Interval in minutes if using interval schedule

---

### Status Fields

- **`isActive`** - Whether automation is enabled (1 = yes, 0 = no)
- **`isDeleted`** - Deletion status
- **`lastRunDate`** - Timestamp of last execution
- **`nextRunDate`** - Timestamp of next scheduled execution
- **`lastRunStatus`** - Status of last run (success, failed, running)

---

### Trigger Configuration

- **`triggerType`** - Trigger type (schedule, event, manual, etc.)
- **`triggerConfig`** - Trigger configuration (JSON)
- **`triggerConditions`** - Conditions that activate automation

---

## Get Specific Automation

```bash
# By automation ID
bun run scripts/api-call.ts GET /api/automations/456

# Get specific fields only
bun run scripts/api-call.ts GET /api/automations/456 \
  --fields=automationID,automationName,pipelineID,isActive,scheduleType
```

---

## Create Automation

### Basic Cron Schedule Example

```bash
bun run scripts/api-call.ts POST /api/automations '{
  "automationName": "Daily Sales Sync",
  "pipelineID": 123,
  "scheduleType": "cron",
  "cronExpression": "0 2 * * *",
  "institutionID": 1,
  "internalID": "N1r8Do",
  "ownerID": 5,
  "isActive": 1
}'
```

**Cron expression:** `0 2 * * *` = Every day at 2:00 AM

---

### Interval Schedule Example

```bash
bun run scripts/api-call.ts POST /api/automations '{
  "automationName": "Hourly Data Refresh",
  "pipelineID": 123,
  "scheduleType": "interval",
  "intervalMinutes": 60,
  "institutionID": 1,
  "internalID": "N1r8Do",
  "ownerID": 5,
  "isActive": 1
}'
```

---

### Event Trigger Example

```bash
bun run scripts/api-call.ts POST /api/automations '{
  "automationName": "File Upload Trigger",
  "pipelineID": 123,
  "triggerType": "event",
  "triggerConfig": {
    "eventType": "file_uploaded",
    "connectorID": 58,
    "path": "/data/incoming"
  },
  "institutionID": 1,
  "internalID": "N1r8Do",
  "ownerID": 5,
  "isActive": 1
}'
```

---

### Required Fields

When creating an automation, these fields are typically required:

- **`automationName`** - Must be unique within project
- **`pipelineID`** - Valid pipeline ID
- **`scheduleType`** or **`triggerType`** - How automation runs
- **`institutionID`** - Organization ID
- **`internalID`** - Project internal ID
- **`ownerID`** - Your user ID

---

## Update Automation

### Update Schedule

```bash
bun run scripts/api-call.ts PUT /api/automations '{
  "automationID": 456,
  "cronExpression": "0 3 * * *",
  "isActive": 1
}'
```

---

### Enable/Disable Automation

```bash
# Disable
bun run scripts/api-call.ts PUT /api/automations '{
  "automationID": 456,
  "isActive": 0
}'

# Enable
bun run scripts/api-call.ts PUT /api/automations '{
  "automationID": 456,
  "isActive": 1
}'
```

---

## Delete Automation

```bash
bun run scripts/api-call.ts DELETE /api/automations '{"automationID": 456}'
```

**Note:** This soft-deletes the automation (sets isDeleted=1)

---

## Schedule Types

### Cron Schedules

**Format:** Standard cron expression (5 fields)

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
* * * * *
```

**Examples:**

- `0 2 * * *` - Daily at 2:00 AM
- `0 */4 * * *` - Every 4 hours
- `0 9 * * 1` - Every Monday at 9:00 AM
- `*/15 * * * *` - Every 15 minutes
- `0 0 1 * *` - First day of month at midnight

---

### Interval Schedules

**Format:** Minutes between executions

**Examples:**

- `intervalMinutes: 60` - Every hour
- `intervalMinutes: 30` - Every 30 minutes
- `intervalMinutes: 1440` - Every 24 hours (daily)
- `intervalMinutes: 15` - Every 15 minutes

---

### Event Triggers

**Types:**

- **`file_uploaded`** - When file appears in connector
- **`data_changed`** - When data changes in source
- **`webhook`** - HTTP webhook trigger
- **`manual`** - Manual execution only

---

## Common Scenarios

### Scenario 1: List All Automations in Project

```bash
# Get project internalId
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalId

# Count automations
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --count

# Get automation details
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" \
  --fields=automationID,automationName,pipelineID,isActive,scheduleType
```

---

### Scenario 2: Create Daily Automation

```bash
# Step 1: Get pipeline ID
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do" \
  --fields=pipelineID,pipelineName

# Step 2: Get user context
bun run scripts/api-call.ts GET /api/my/account --fields=id
bun run scripts/api-call.ts GET /api/my/projects \
  --fields=id,internalId,institutionId

# Step 3: Create automation
bun run scripts/api-call.ts POST /api/automations '{
  "automationName": "Daily ETL",
  "pipelineID": 123,
  "scheduleType": "cron",
  "cronExpression": "0 2 * * *",
  "institutionID": 1,
  "internalID": "N1r8Do",
  "ownerID": 5,
  "isActive": 1
}'
```

---

### Scenario 3: Find Automations for Specific Pipeline

```bash
# Get all automations
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do"

# Filter by pipelineID client-side with jq
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" | \
  jq '.[] | select(.pipelineID == 123)'
```

---

### Scenario 4: Monitor Automation Execution

```bash
# Check automation status
bun run scripts/api-call.ts GET /api/automations/456 \
  --fields=lastRunStatus,lastRunDate,nextRunDate

# If failed, check pipeline logs
bun run scripts/api-call.ts GET /api/pipeline/logs "pipelineID=123"
```

---

### Scenario 5: Update Schedule to Run More Frequently

```bash
# Change from daily to every 6 hours
bun run scripts/api-call.ts PUT /api/automations '{
  "automationID": 456,
  "cronExpression": "0 */6 * * *"
}'

# Or use interval instead
bun run scripts/api-call.ts PUT /api/automations '{
  "automationID": 456,
  "scheduleType": "interval",
  "intervalMinutes": 360
}'
```

---

### Scenario 6: Temporarily Pause Automation

```bash
# Disable automation (keeps schedule, just deactivates)
bun run scripts/api-call.ts PUT /api/automations '{
  "automationID": 456,
  "isActive": 0
}'

# Re-enable later
bun run scripts/api-call.ts PUT /api/automations '{
  "automationID": 456,
  "isActive": 1
}'
```

---

## Token Efficiency

### Efficient Queries

```bash
# ✅ Count only (~50 tokens)
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --count

# ✅ Summary view (~500-2,000 tokens)
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --summary

# ✅ Specific fields (~500-1,000 tokens)
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" \
  --fields=automationID,automationName,pipelineID,isActive \
  --limit=25
```

---

### Avoid

```bash
# ❌ Without internalID - returns null
bun run scripts/api-call.ts GET /api/automations
```

---

## Relationship to Pipelines

Automations control **when** pipelines run. Each automation is associated with exactly one pipeline.

**Workflow:**

1. Create pipeline (defines **what** to do)
2. Create automation (defines **when** to do it)
3. Automation triggers pipeline execution on schedule/event

**Example:**

```bash
# Pipeline: "Sales Data Sync"
# ↓
# Automation: "Daily at 2 AM" (runs the pipeline)
```

---

## Troubleshooting

### Problem: Automation not executing

**Check:**

1. Automation is active (`isActive=1`)
2. Associated pipeline exists and is active
3. Schedule/trigger is configured correctly
4. Next run date is set

```bash
# Check automation status
bun run scripts/api-call.ts GET /api/automations/456 \
  --fields=isActive,nextRunDate,lastRunStatus

# Check associated pipeline
bun run scripts/api-call.ts GET /api/pipeline/123 --fields=isActive
```

---

### Problem: Getting null response

**Solution:** Must include `internalID` parameter

```bash
# ❌ Returns null
bun run scripts/api-call.ts GET /api/automations

# ✅ Include internalID
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do"
```

**See:** [Error Handling Guide](./error-handling.md)

---

### Problem: Automation runs but pipeline fails

**Solution:** Check pipeline logs for errors

```bash
# Get pipeline logs
bun run scripts/api-call.ts GET /api/pipeline/logs "pipelineID=123"

# Check connector status
bun run scripts/api-call.ts GET /api/connector/58 --fields=isActive
```

**See:** [Pipelines Guide](./pipelines.md)

---

### Problem: Invalid cron expression

**Common mistakes:**

- Using 6 fields (should be 5)
- Invalid ranges (e.g., hour 24)
- Wrong syntax for intervals

**Validation:**

```bash
# Test cron expression online: crontab.guru
# Or use interval schedule instead
```

---

## Best Practices

### 1. Use Descriptive Names

```bash
# ✅ Good
"automationName": "Daily Sales Sync at 2 AM"

# ❌ Bad
"automationName": "automation1"
```

---

### 2. Start with Inactive, Test, Then Activate

```bash
# Create as inactive
"isActive": 0

# Test manually first
bun run scripts/api-call.ts POST /api/pipeline/run '{"pipelineID": 123}'

# Activate after successful test
bun run scripts/api-call.ts PUT /api/automations '{
  "automationID": 456,
  "isActive": 1
}'
```

---

### 3. Monitor Execution History

```bash
# Check last run status regularly
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" \
  --fields=automationName,lastRunStatus,lastRunDate
```

---

### 4. Use Appropriate Schedule Type

- **Cron:** For specific times/days (e.g., "every Monday at 9 AM")
- **Interval:** For regular frequency (e.g., "every 30 minutes")
- **Event:** For reactive triggers (e.g., "when file arrives")

---

### 5. Avoid Overlapping Executions

```bash
# If pipeline takes 30 minutes to run,
# don't schedule every 15 minutes!

# ❌ Bad: Could overlap
"intervalMinutes": 15  # Pipeline runs longer than this

# ✅ Good: Safe interval
"intervalMinutes": 60  # Allows time for completion
```

---

## Cron Expression Reference

### Common Patterns

```bash
# Every minute
* * * * *

# Every hour at minute 0
0 * * * *

# Every day at midnight
0 0 * * *

# Every day at 2:30 AM
30 2 * * *

# Every Monday at 9 AM
0 9 * * 1

# Every weekday at 8 AM
0 8 * * 1-5

# First day of month at midnight
0 0 1 * *

# Every 15 minutes
*/15 * * * *

# Every 6 hours
0 */6 * * *

# Twice daily (6 AM and 6 PM)
0 6,18 * * *
```

---

### Field Ranges

- **Minute:** 0-59
- **Hour:** 0-23 (0 = midnight)
- **Day of month:** 1-31
- **Month:** 1-12
- **Day of week:** 0-6 (0 = Sunday, 6 = Saturday)

---

### Special Characters

- **`*`** - Any value
- **`*/n`** - Every n units
- **`,`** - List of values (e.g., `1,15` = 1st and 15th)
- **`-`** - Range of values (e.g., `1-5` = 1 through 5)

---

## See Also

- **[Pipelines Guide](./pipelines.md)** - Creating and managing pipelines
- **[Projects & Organizations](./projects-and-organizations.md)** - Get project internalId
- **[Error Handling Guide](./error-handling.md)** - Troubleshooting null responses
- **[Token Efficiency Guide](./token-efficiency.md)** - Optimize API usage
- **[Working Endpoints](./working-endpoints.md)** - Complete endpoint reference

---

**Last Updated:** 2025-11-17
