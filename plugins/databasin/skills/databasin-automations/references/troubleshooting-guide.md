# Databasin Automations Troubleshooting Guide

Complete guide to diagnosing and resolving common automation issues in Databasin.

## Table of Contents

1. [Introduction](#introduction)
2. [General Troubleshooting Approach](#general-troubleshooting-approach)
3. [Automation Not Running](#automation-not-running)
4. [Automation Running But Failing](#automation-running-but-failing)
5. [Scheduling Issues](#scheduling-issues)
6. [Task Configuration Errors](#task-configuration-errors)
7. [Performance Issues](#performance-issues)
8. [Common Error Messages](#common-error-messages)
9. [Debugging Strategies](#debugging-strategies)
10. [Best Practices](#best-practices)
11. [Quick Diagnostic Checklist](#quick-diagnostic-checklist)

---

## Introduction

This guide provides practical solutions for troubleshooting Databasin automations. Use this guide when:

- Automations don't execute as scheduled
- Executions fail with errors
- Tasks don't complete successfully
- Performance is degraded
- Configuration validation fails

### How to Use This Guide

1. **Identify the symptom** - Start with the section matching your issue
2. **Follow diagnostic steps** - Execute suggested CLI commands
3. **Apply the solution** - Implement the recommended fix
4. **Verify the fix** - Test the automation after changes

### Where to Find Logs

Automation logs and execution history are available through:

```bash
# Get automation details including last run status
databasin automations get <automation_id>

# Check execution history (full JSON)
databasin automations get <automation_id> --json
```

**Log Information Includes:**

- Last execution timestamp
- Execution status (Success/Failed/Running)
- Error messages
- Task-level status
- Execution duration

---

## General Troubleshooting Approach

### Step 1: Check Automation Status

```bash
# Get current automation status
databasin automations get <automation_id>
```

**Verify:**

- Automation is active (`isActive: 1`)
- Schedule is correct
- Last run status and timestamp
- Error messages (if any)

### Step 2: Review Configuration

```bash
# Get full configuration
databasin automations get <automation_id> --json
```

**Check:**

- Required fields are present
- Task configurations are valid
- Connection IDs exist
- File paths are correct
- Cron expression is valid

### Step 3: Test Manually

```bash
# Run automation manually
databasin automations run <automation_id>

# Monitor execution
databasin automations get <automation_id>
```

**Observe:**

- Does it start successfully?
- Which task fails (if any)?
- What error message appears?
- How long does it run before failing?

### Step 4: Check Dependencies

```bash
# Verify pipeline exists (if pipeline task)
databasin pipelines get <pipeline_id>

# Verify connector exists (if SQL task)
databasin connectors get <connector_id>
databasin connectors test <connector_id>

# Verify project access
databasin projects list
```

### Step 5: Apply Fix and Test

After making changes:

```bash
# Update automation
databasin automations update <automation_id> fix.json

# Test fix
databasin automations run <automation_id>

# Monitor result
databasin automations get <automation_id>
```

---

## Automation Not Running

### Symptom

Automation is scheduled but never executes at the expected time.

### Diagnostic Steps

**1. Check if automation is active:**

```bash
databasin automations get <automation_id> --fields name,isActive,status
```

**Expected Output:**

```
Name:     Daily ETL Pipeline
Active:   1 (✓)
Status:   active
```

**Issue:** If `isActive: 0`, the automation is disabled.

**Solution:**

```bash
# Create activation file
echo '{"isActive": 1}' > activate.json

# Activate automation
databasin automations update <automation_id> activate.json

# Verify
databasin automations get <automation_id> --fields isActive
```

---

**2. Verify schedule expression:**

```bash
databasin automations get <automation_id> --fields schedule
```

**Expected Output:**

```
Schedule: 0 2 * * * (Daily at 2 AM)
```

**Common Issues:**

| Invalid Expression | Should Be   | Reason                           |
| ------------------ | ----------- | -------------------------------- |
| `0 2 * * * *`      | `0 2 * * *` | Too many fields (6 instead of 5) |
| `0 25 * * *`       | `0 2 * * *` | Invalid hour (25 > 23)           |
| `60 2 * * *`       | `0 2 * * *` | Invalid minute (60 > 59)         |
| `0 2 * * 7`        | `0 2 * * 0` | Invalid weekday (7 should be 0)  |
| `0 2 32 * *`       | `0 2 1 * *` | Invalid day (32 > 31)            |

**Solution:**

```bash
# Fix schedule
echo '{"jobDetails": {"jobRunSchedule": "0 2 * * *"}}' > fix_schedule.json

# Update automation
databasin automations update <automation_id> fix_schedule.json
```

**Validate Cron Expression:**

```
Format: minute hour day month weekday
- Minute: 0-59
- Hour: 0-23
- Day: 1-31
- Month: 1-12
- Weekday: 0-6 (0 = Sunday)
```

---

**3. Check project access:**

```bash
# List automations in project
databasin automations list -p <project_id>

# If automation doesn't appear, check project access
databasin projects list
```

**Issue:** User doesn't have access to project containing automation.

**Solution:**

- Request project access from administrator
- Verify you're logged in with correct credentials:
  ```bash
  databasin auth status
  databasin login  # Re-authenticate if needed
  ```

---

**4. Verify timezone configuration:**

```bash
databasin automations get <automation_id> --json | grep timezone
```

**Expected:**

```json
"jobRunTimeZone": "America/New_York"
```

**Issue:** Wrong timezone causing execution at unexpected time.

**Solution:**

```bash
# Update timezone
echo '{
  "jobDetails": {
    "jobRunTimeZone": "America/Chicago"
  }
}' > fix_timezone.json

databasin automations update <automation_id> fix_timezone.json
```

**Common Timezones:**

- `America/New_York` (EST/EDT)
- `America/Chicago` (CST/CDT)
- `America/Denver` (MST/MDT)
- `America/Los_Angeles` (PST/PDT)
- `UTC`
- `Europe/London`

---

**5. Check for conflicting executions:**

```bash
databasin automations get <automation_id> --fields status,lastRun
```

**Issue:** Automation is still running from previous execution.

**Output:**

```
Status:      Running
Last Run:    2024-11-23 02:00:00 (Still running)
```

**Solution:**

```bash
# Stop current execution
databasin automations stop <automation_id>

# Wait for stop confirmation
databasin automations get <automation_id>

# Adjust schedule to prevent overlap
# If execution takes 30 minutes, don't schedule every 15 minutes!
```

---

### Prevention

**Create automations inactive by default:**

```json
{
  "automationName": "New Automation",
  "isActive": 0,
  ...
}
```

**Test thoroughly before activating:**

```bash
# Create inactive
databasin automations create automation.json -p proj-001

# Test manually
databasin automations run <automation_id>

# Activate only after successful test
echo '{"isActive": 1}' > activate.json
databasin automations update <automation_id> activate.json
```

---

## Automation Running But Failing

### Symptom

Automation starts executing but fails during task execution.

### Task-Specific Failures

#### Pipeline Task Failures

**Symptom:**

```
Last Status:  Failed
Error:        Pipeline execution failed
```

**Diagnostic Steps:**

```bash
# Get automation details
databasin automations get <automation_id> --json

# Extract pipeline ID from automationTask array
# Look for: "taskType": "pipeline", "jobID": "pipeline-123"

# Check pipeline status
databasin pipelines get pipeline-123

# Verify pipeline configuration
databasin pipelines get pipeline-123 --json
```

**Common Issues:**

1. **Pipeline doesn't exist:**

   ```
   Error: Pipeline not found (404)
   ```

   **Solution:**

   ```bash
   # Verify pipeline ID
   databasin pipelines list -p <project_id> --full

   # Update automation with correct pipeline ID
   echo '{
     "automationTask": [{
       "taskType": "pipeline",
       "jobID": "correct-pipeline-id",
       "automationOrderNumber": 1
     }]
   }' > fix_pipeline.json

   databasin automations update <automation_id> fix_pipeline.json
   ```

2. **Pipeline has invalid source/target:**

   ```
   Error: Connection refused (connector-58)
   ```

   **Solution:**

   ```bash
   # Test connector
   databasin connectors test 58

   # If connector fails, fix connector first
   databasin connectors get 58

   # Update connector credentials
   echo '{
     "connectorUsername": "correct_user",
     "connectorPassword": "correct_password"
   }' > fix_connector.json

   databasin connectors update 58 fix_connector.json
   ```

3. **Pipeline timeout:**

   ```
   Error: Pipeline execution timeout after 3600 seconds
   ```

   **Solution:**

   ```bash
   # Increase automation timeout
   echo '{
     "jobDetails": {
       "jobTimeout": "7200"
     }
   }' > increase_timeout.json

   databasin automations update <automation_id> increase_timeout.json
   ```

---

#### SQL Task Failures

**Symptom:**

```
Last Status:  Failed
Error:        SQL query execution failed
```

**Diagnostic Steps:**

```bash
# Get automation with SQL task details
databasin automations get <automation_id> --json

# Extract SQL task configuration:
# - sqlTargetConnectionID
# - sqlQueryMap

# Test the connection
databasin connectors test <connection_id>
```

**Common Issues:**

1. **Invalid connection ID:**

   ```
   Error: Connection not found (404)
   ```

   **Solution:**

   ```bash
   # List available connectors
   databasin connectors list -p <project_id> --full --fields connectorID,connectorName,connectorType

   # Update automation with correct connection ID
   echo '{
     "automationTask": [{
       "taskType": "sql",
       "sqlTargetConnectionID": 58,
       "sqlQueryMap": ["SELECT * FROM table"],
       "automationOrderNumber": 1
     }]
   }' > fix_sql_connection.json

   databasin automations update <automation_id> fix_sql_connection.json
   ```

2. **SQL syntax error:**

   ```
   Error: Syntax error in SQL query
   ```

   **Solution:**

   ```bash
   # Test SQL query manually using Databasin SQL editor or connector
   # Fix query syntax

   # Update automation with corrected query
   echo '{
     "automationTask": [{
       "taskType": "sql",
       "sqlTargetConnectionID": 58,
       "sqlQueryMap": [
         "SELECT * FROM sales WHERE date > CURRENT_DATE - 7",
         "UPDATE analytics SET updated_at = NOW()"
       ],
       "automationOrderNumber": 1
     }]
   }' > fix_sql_query.json

   databasin automations update <automation_id> fix_sql_query.json
   ```

3. **Query timeout:**

   ```
   Error: SQL query timeout after 1800 seconds
   ```

   **Solution:**

   ```bash
   # Option 1: Increase timeout
   echo '{
     "jobDetails": {
       "jobTimeout": "3600"
     }
   }' > increase_timeout.json

   databasin automations update <automation_id> increase_timeout.json

   # Option 2: Optimize query
   # - Add indexes
   # - Reduce result set
   # - Use WHERE clauses
   # - Break into smaller queries
   ```

4. **Connection authentication failure:**

   ```
   Error: Authentication failed for connection 58
   ```

   **Solution:**

   ```bash
   # Test connection
   databasin connectors test 58

   # Update connector credentials
   echo '{
     "connectorUsername": "new_username",
     "connectorPassword": "new_password"
   }' > fix_credentials.json

   databasin connectors update 58 fix_credentials.json

   # Test again
   databasin connectors test 58

   # Re-run automation
   databasin automations run <automation_id>
   ```

---

#### Notebook Task Failures

**Symptom:**

```
Last Status:  Failed
Error:        Notebook execution failed
```

**Diagnostic Steps:**

```bash
# Get automation details
databasin automations get <automation_id> --json

# Extract notebook path from automationTask
# Look for: "taskType": "notebook", "notebookPath": "/path/to/notebook"
```

**Common Issues:**

1. **Notebook path not found:**

   ```
   Error: Notebook not found at path /analytics/daily_summary
   ```

   **Solution:**

   ```bash
   # Verify correct notebook path in Databricks
   # Update automation with correct path

   echo '{
     "automationTask": [{
       "taskType": "notebook",
       "notebookPath": "/correct/path/to/notebook",
       "automationOrderNumber": 1
     }]
   }' > fix_notebook_path.json

   databasin automations update <automation_id> fix_notebook_path.json
   ```

2. **Notebook execution error:**

   ```
   Error: Notebook execution failed with error: KeyError 'missing_column'
   ```

   **Solution:**
   - Fix notebook code in Databricks
   - Verify notebook has required inputs
   - Test notebook manually in Databricks
   - Ensure notebook dependencies are installed

3. **Notebook timeout:**

   ```
   Error: Notebook execution timeout
   ```

   **Solution:**

   ```bash
   # Increase timeout
   echo '{
     "jobDetails": {
       "jobTimeout": "7200"
     }
   }' > increase_timeout.json

   databasin automations update <automation_id> increase_timeout.json
   ```

---

#### Docker Task Failures

**Symptom:**

```
Last Status:  Failed
Error:        Docker container execution failed
```

**Diagnostic Steps:**

```bash
# Get automation details
databasin automations get <automation_id> --json

# Extract Docker configuration:
# - dockerImage
# - dockerCommand
# - dockerEnvironment (if any)
```

**Common Issues:**

1. **Docker image not found:**

   ```
   Error: Docker image not found: myorg/myimage:latest
   ```

   **Solution:**

   ```bash
   # Verify image name and tag
   # Ensure image is accessible from Databasin cluster

   echo '{
     "automationTask": [{
       "taskType": "docker",
       "dockerImage": "correct-org/correct-image:tag",
       "dockerCommand": "python script.py",
       "automationOrderNumber": 1
     }]
   }' > fix_docker_image.json

   databasin automations update <automation_id> fix_docker_image.json
   ```

2. **Container execution error:**

   ```
   Error: Container exited with code 1
   ```

   **Solution:**
   - Check container logs
   - Verify command syntax
   - Ensure required environment variables are set
   - Test container locally:
     ```bash
     docker run myorg/myimage:latest python script.py
     ```

3. **Resource limits exceeded:**

   ```
   Error: Container killed - out of memory
   ```

   **Solution:**

   ```bash
   # Increase cluster size
   echo '{
     "jobDetails": {
       "jobClusterSize": "L"
     }
   }' > increase_cluster.json

   databasin automations update <automation_id> increase_cluster.json
   ```

---

#### File Drop Task Failures

**Symptom:**

```
Last Status:  Failed
Error:        File operation failed
```

**Diagnostic Steps:**

```bash
# Get automation details
databasin automations get <automation_id> --json

# Extract file task configuration:
# - sourceFileId
# - targetFileId
# - operation (copy/move)
```

**Common Issues:**

1. **Source file not found:**

   ```
   Error: Source file not found: file-123
   ```

   **Solution:**
   - Verify source file exists
   - Check file ID is correct
   - Ensure file hasn't been moved/deleted

2. **Target location permission denied:**

   ```
   Error: Permission denied writing to target location
   ```

   **Solution:**
   - Verify write permissions on target
   - Check connector credentials
   - Test connector:
     ```bash
     databasin connectors test <target_connector_id>
     ```

3. **Insufficient storage:**

   ```
   Error: Insufficient storage space at target
   ```

   **Solution:**
   - Free up space at target location
   - Use different target location
   - Archive/delete old files

---

### Connection Issues

**Symptom:**

```
Error: Connection refused
Error: Network timeout
Error: Unable to reach host
```

**Diagnostic Steps:**

```bash
# Test connector directly
databasin connectors test <connector_id>

# Get connector details
databasin connectors get <connector_id>
```

**Common Issues:**

1. **Connector is down:**

   ```bash
   # Test connection
   databasin connectors test <connector_id>
   # Output: Connection test failed - Unable to reach host
   ```

   **Solution:**
   - Verify host is accessible
   - Check firewall rules
   - Verify credentials:

     ```bash
     echo '{
       "connectorUsername": "correct_user",
       "connectorPassword": "correct_password"
     }' > fix_connector.json

     databasin connectors update <connector_id> fix_connector.json
     databasin connectors test <connector_id>
     ```

2. **Network timeout:**

   ```
   Error: Connection timeout after 30 seconds
   ```

   **Solution:**

   ```bash
   # Increase connection timeout in connector additional details
   echo '{
     "connectorAdditionalDetails": "connectTimeout=60000"
   }' > increase_connector_timeout.json

   databasin connectors update <connector_id> increase_connector_timeout.json
   ```

3. **SSL/TLS errors:**

   ```
   Error: SSL certificate verification failed
   ```

   **Solution:**

   ```bash
   # Add SSL parameters to connector
   echo '{
     "connectorAdditionalDetails": "ssl=true&sslmode=require"
   }' > fix_ssl.json

   databasin connectors update <connector_id> fix_ssl.json
   ```

---

### Permission Errors

**Symptom:**

```
Error: Access denied (403)
Error: Permission denied
Error: Unauthorized (401)
```

**Diagnostic Steps:**

```bash
# Check authentication
databasin auth status

# Verify project access
databasin projects list

# Check connector permissions
databasin connectors get <connector_id>
```

**Solutions:**

1. **Re-authenticate:**

   ```bash
   databasin login
   ```

2. **Verify project access:**
   - Request access from project administrator
   - Ensure user is added to project team

3. **Update connector credentials:**

   ```bash
   echo '{
     "connectorUsername": "user_with_permissions",
     "connectorPassword": "correct_password"
   }' > fix_permissions.json

   databasin connectors update <connector_id> fix_permissions.json
   ```

4. **Check automation ownership:**
   - Ensure user has permission to modify automation
   - Contact automation creator or admin

---

## Scheduling Issues

### Running at Wrong Time

**Symptom:**
Automation runs at unexpected times.

**Diagnostic Steps:**

```bash
# Check schedule and timezone
databasin automations get <automation_id> --json | grep -E "(jobRunSchedule|jobRunTimeZone)"
```

**Common Issues:**

1. **Wrong timezone:**

   ```json
   "jobRunTimeZone": "UTC"  // Should be "America/New_York"
   ```

   **Solution:**

   ```bash
   echo '{
     "jobDetails": {
       "jobRunTimeZone": "America/New_York"
     }
   }' > fix_timezone.json

   databasin automations update <automation_id> fix_timezone.json
   ```

2. **AM/PM confusion:**

   ```
   Schedule: 0 2 * * *  (2 AM, not 2 PM)
   ```

   For 2 PM, use:

   ```bash
   echo '{
     "jobDetails": {
       "jobRunSchedule": "0 14 * * *"
     }
   }' > fix_time.json

   databasin automations update <automation_id> fix_time.json
   ```

3. **Daylight Saving Time:**
   - Use timezone-aware scheduling
   - Avoid scheduling during DST transitions (2 AM)

---

### Not Running at Scheduled Time

**Symptom:**
Automation scheduled but executions are missed.

**Diagnostic Steps:**

```bash
# Check active status
databasin automations get <automation_id> --fields isActive,status

# Check last run
databasin automations get <automation_id> --fields lastRun,lastStatus
```

**Common Issues:**

1. **Automation is inactive:**

   ```bash
   # Activate
   echo '{"isActive": 1}' > activate.json
   databasin automations update <automation_id> activate.json
   ```

2. **Previous execution still running:**

   ```bash
   # Check status
   databasin automations get <automation_id> --fields status

   # If "Running", wait or stop
   databasin automations stop <automation_id>
   ```

3. **Schedule overlaps with execution time:**

   ```
   Schedule: Every 15 minutes
   Execution time: 30 minutes average
   Result: Missed executions due to overlap
   ```

   **Solution:**

   ```bash
   # Adjust schedule to allow completion
   echo '{
     "jobDetails": {
       "jobRunSchedule": "0 * * * *"
     }
   }' > fix_schedule.json

   databasin automations update <automation_id> fix_schedule.json
   ```

---

### Running Too Frequently

**Symptom:**
Automation runs more often than expected.

**Diagnostic Steps:**

```bash
# Check schedule
databasin automations get <automation_id> --fields schedule
```

**Common Issues:**

1. **Misunderstood cron syntax:**

   ```
   Wrong:  * * * * *     (Every minute!)
   Right:  0 * * * *     (Every hour)

   Wrong:  */1 * * * *   (Every minute!)
   Right:  */10 * * * *  (Every 10 minutes)
   ```

   **Solution:**

   ```bash
   # Fix schedule
   echo '{
     "jobDetails": {
       "jobRunSchedule": "0 * * * *"
     }
   }' > fix_frequency.json

   databasin automations update <automation_id> fix_frequency.json
   ```

---

### Skipping Executions

**Symptom:**
Some scheduled executions don't run.

**Diagnostic Steps:**

```bash
# Check execution history
databasin automations get <automation_id> --json

# Check for overlapping executions
databasin automations list -p <project_id> --running
```

**Common Issues:**

1. **Concurrent execution limit reached:**
   - System may limit concurrent automations
   - Wait for other automations to complete
   - Stagger schedules:
     ```bash
     # Automation 1: 0 2 * * *  (2:00 AM)
     # Automation 2: 0 3 * * *  (3:00 AM)
     # Automation 3: 0 4 * * *  (4:00 AM)
     ```

2. **Previous execution timeout:**

   ```bash
   # Increase timeout
   echo '{
     "jobDetails": {
       "jobTimeout": "7200"
     }
   }' > increase_timeout.json

   databasin automations update <automation_id> increase_timeout.json
   ```

---

### Timezone Problems

**Symptom:**
Automation runs at correct time in one timezone but wrong in another.

**Solution:**

```bash
# Always specify explicit timezone
echo '{
  "jobDetails": {
    "jobRunTimeZone": "America/New_York"
  }
}' > set_timezone.json

databasin automations update <automation_id> set_timezone.json
```

**Common Timezones:**

- US Eastern: `America/New_York`
- US Central: `America/Chicago`
- US Mountain: `America/Denver`
- US Pacific: `America/Los_Angeles`
- UTC: `UTC`
- UK: `Europe/London`

---

## Task Configuration Errors

### Invalid Task Type

**Symptom:**

```
Error: Invalid task type specified
```

**Diagnostic Steps:**

```bash
# Check task configuration
databasin automations get <automation_id> --json
```

**Valid Task Types:**

- `pipeline`
- `sql`
- `notebook`
- `job`
- `file`
- `docker`

**Solution:**

```bash
# Fix task type
echo '{
  "automationTask": [{
    "taskType": "pipeline",
    "taskName": "Run Data Pipeline",
    "jobID": "pipeline-123",
    "automationOrderNumber": 1,
    "isActive": true
  }]
}' > fix_task_type.json

databasin automations update <automation_id> fix_task_type.json
```

---

### Missing Required Fields

**Symptom:**

```
Error: Missing required field for task type
```

**Required Fields by Task Type:**

| Task Type  | Required Fields                        |
| ---------- | -------------------------------------- |
| `pipeline` | `jobID` (pipeline ID)                  |
| `sql`      | `sqlTargetConnectionID`, `sqlQueryMap` |
| `notebook` | `notebookPath`                         |
| `job`      | `jobID` (Databricks job ID)            |
| `file`     | `sourceFileId`, `targetFileId`         |
| `docker`   | `dockerImage`, `dockerCommand`         |

**Solution:**

```bash
# SQL task example with all required fields
echo '{
  "automationTask": [{
    "taskType": "sql",
    "taskName": "Run Analytics Query",
    "sqlTargetConnectionID": 58,
    "sqlQueryMap": [
      "SELECT * FROM sales WHERE date > CURRENT_DATE - 7"
    ],
    "automationOrderNumber": 1,
    "isActive": true
  }]
}' > fix_required_fields.json

databasin automations update <automation_id> fix_required_fields.json
```

---

### Incorrect Parameter Format

**Symptom:**

```
Error: Invalid parameter format
```

**Common Issues:**

1. **sqlQueryMap not an array:**

   ```json
   // Wrong
   "sqlQueryMap": "SELECT * FROM table"

   // Right
   "sqlQueryMap": ["SELECT * FROM table"]
   ```

2. **isActive not a boolean/number:**

   ```json
   // Wrong
   "isActive": "true"

   // Right
   "isActive": true
   // Or
   "isActive": 1
   ```

3. **Numeric fields as strings:**

   ```json
   // Wrong
   "sqlTargetConnectionID": "58"

   // Right
   "sqlTargetConnectionID": 58
   ```

4. **Missing quotes on strings:**

   ```json
   // Wrong
   "taskType": pipeline

   // Right
   "taskType": "pipeline"
   ```

---

### JSON Syntax Errors

**Symptom:**

```
Error: Invalid JSON format
Error: Unexpected token
```

**Common Issues:**

1. **Trailing commas:**

   ```json
   // Wrong
   {
     "name": "Test",
     "active": true,  // <- Remove this comma
   }

   // Right
   {
     "name": "Test",
     "active": true
   }
   ```

2. **Missing commas:**

   ```json
   // Wrong
   {
     "name": "Test"
     "active": true
   }

   // Right
   {
     "name": "Test",
     "active": true
   }
   ```

3. **Unquoted keys:**

   ```json
   // Wrong
   {
     name: "Test"
   }

   // Right
   {
     "name": "Test"
   }
   ```

4. **Single quotes instead of double:**

   ```json
   // Wrong
   {
     'name': 'Test'
   }

   // Right
   {
     "name": "Test"
   }
   ```

**Validation Tools:**

```bash
# Validate JSON before submitting
cat automation.json | jq .

# If invalid, jq will show error:
# parse error: Expected separator between values at line 5, column 8
```

---

### Validation Failures

**Symptom:**

```
Error: Automation validation failed
```

**Diagnostic Steps:**

```bash
# Get full error message
databasin automations create automation.json -p proj-001

# CLI will show specific validation error:
# ✘ Validation failed: Invalid cron expression
```

**Common Validation Errors:**

| Error                   | Cause                    | Solution                                          |
| ----------------------- | ------------------------ | ------------------------------------------------- |
| Invalid cron expression | Malformed schedule       | Use valid cron: `0 2 * * *`                       |
| Missing automation name | `automationName` not set | Add `"automationName": "My Automation"`           |
| Invalid project ID      | Project doesn't exist    | Verify project: `databasin projects list`         |
| Invalid connection ID   | Connector doesn't exist  | Verify connector: `databasin connectors get <id>` |
| Invalid cluster size    | Wrong size code          | Use: `XS`, `S`, `M`, `L`, `XL`                    |
| Timeout too large       | Exceeds maximum          | Maximum: 18000 seconds (5 hours)                  |

---

## Performance Issues

### Slow Execution

**Symptom:**
Automation takes longer than expected to complete.

**Diagnostic Steps:**

```bash
# Check execution duration
databasin automations get <automation_id> --fields lastRun,duration

# Get full execution details
databasin automations get <automation_id> --json
```

**Common Causes:**

1. **Insufficient cluster resources:**

   ```bash
   # Increase cluster size
   echo '{
     "jobDetails": {
       "jobClusterSize": "L"
     }
   }' > increase_cluster.json

   databasin automations update <automation_id> increase_cluster.json
   ```

2. **Inefficient SQL queries:**
   - Add indexes to database tables
   - Optimize WHERE clauses
   - Reduce result set size
   - Use query limits:
     ```sql
     -- Add LIMIT to reduce data transfer
     SELECT * FROM large_table WHERE date > '2024-01-01' LIMIT 10000
     ```

3. **Large data transfers:**
   - Break into smaller batches
   - Use incremental loads
   - Filter data at source

4. **Sequential task execution:**
   - Tasks run in order (by `automationOrderNumber`)
   - Cannot parallelize within single automation
   - Consider splitting into multiple automations

---

### Timeouts

**Symptom:**

```
Error: Execution timeout after N seconds
```

**Diagnostic Steps:**

```bash
# Check current timeout
databasin automations get <automation_id> --json | grep jobTimeout
```

**Solutions:**

1. **Increase timeout:**

   ```bash
   echo '{
     "jobDetails": {
       "jobTimeout": "10800"
     }
   }' > increase_timeout.json

   databasin automations update <automation_id> increase_timeout.json
   ```

2. **Optimize tasks:**
   - Break large tasks into smaller ones
   - Optimize SQL queries
   - Reduce data volume
   - Use more efficient algorithms

3. **Check connector timeouts:**

   ```bash
   # Increase connector timeout
   echo '{
     "connectorAdditionalDetails": "connectTimeout=60000&queryTimeout=120000"
   }' > fix_connector_timeout.json

   databasin connectors update <connector_id> fix_connector_timeout.json
   ```

**Recommended Timeouts:**

| Workload         | Timeout (seconds) |
| ---------------- | ----------------- |
| Quick queries    | 1,800 (30 min)    |
| Medium ETL       | 3,600 (1 hour)    |
| Large ETL        | 7,200 (2 hours)   |
| Heavy processing | 10,800 (3 hours)  |
| Maximum          | 18,000 (5 hours)  |

---

### Resource Limits

**Symptom:**

```
Error: Out of memory
Error: Disk space exceeded
Error: CPU limit reached
```

**Solutions:**

1. **Increase cluster size:**

   ```bash
   echo '{
     "jobDetails": {
       "jobClusterSize": "XL"
     }
   }' > increase_resources.json

   databasin automations update <automation_id> increase_resources.json
   ```

2. **Optimize data processing:**
   - Process data in chunks
   - Use streaming instead of batch
   - Clear intermediate results
   - Reduce memory footprint

3. **Monitor resource usage:**
   - Check execution logs
   - Profile memory usage
   - Identify bottlenecks

---

### Concurrent Execution Conflicts

**Symptom:**

```
Error: Automation already running (409)
Error: Resource locked by another execution
```

**Solutions:**

1. **Prevent overlapping executions:**

   ```bash
   # Ensure schedule allows execution to complete
   # If execution takes 30 minutes, schedule at least 1 hour apart

   echo '{
     "jobDetails": {
       "jobRunSchedule": "0 */2 * * *"
     }
   }' > prevent_overlap.json

   databasin automations update <automation_id> prevent_overlap.json
   ```

2. **Increase timeout for long-running tasks:**

   ```bash
   echo '{
     "jobDetails": {
       "jobTimeout": "7200"
     }
   }' > increase_timeout.json

   databasin automations update <automation_id> increase_timeout.json
   ```

3. **Stop conflicting execution:**

   ```bash
   # Stop current execution if stuck
   databasin automations stop <automation_id>

   # Wait for stop confirmation
   databasin automations get <automation_id>

   # Re-run
   databasin automations run <automation_id>
   ```

---

## Common Error Messages

### Authentication and Authorization

#### "Unauthorized (401)"

**Cause:** JWT token expired or invalid.

**Solution:**

```bash
# Re-authenticate
databasin login

# Verify authentication
databasin auth status
```

**Prevention:**

- CLI automatically refreshes tokens
- Re-login if you see persistent 401 errors

---

#### "Access denied (403)"

**Cause:** User doesn't have permission for requested operation.

**Solution:**

- Verify project access:
  ```bash
  databasin projects list
  ```
- Request access from project administrator
- Ensure logged in with correct user:
  ```bash
  databasin auth status
  databasin login
  ```

**Prevention:**

- Verify permissions before creating automations
- Use service accounts with appropriate roles

---

### Resource Not Found

#### "Automation not found (404)"

**Cause:** Automation doesn't exist or user doesn't have access.

**Solution:**

```bash
# List all automations
databasin automations list -p <project_id> --full

# Verify automation ID
databasin automations get <correct_id>
```

**Prevention:**

- Save automation IDs after creation
- Use descriptive names for easy identification

---

### Conflict Errors

#### "Automation is already running (409)"

**Cause:** Automation execution already in progress.

**Solution:**

```bash
# Option 1: Wait for completion
databasin automations get <automation_id>

# Option 2: Stop current execution
databasin automations stop <automation_id>

# Wait for stop confirmation
databasin automations get <automation_id>

# Then run again
databasin automations run <automation_id>
```

**Prevention:**

- Schedule with sufficient spacing between runs
- Set appropriate timeouts
- Monitor execution duration

---

### Validation Errors

#### "Invalid configuration (400)"

**Cause:** Automation configuration doesn't meet requirements.

**Common Issues:**

1. **Missing required fields:**

   ```
   Error: Missing required field: automationName
   ```

   **Solution:** Add missing field to configuration.

2. **Invalid field values:**

   ```
   Error: Invalid cluster size: XXL (valid: XS, S, M, L, XL)
   ```

   **Solution:** Use valid cluster size.

3. **Invalid cron expression:**

   ```
   Error: Invalid cron format
   ```

   **Solution:** Fix cron expression (5 fields, valid ranges).

**Prevention:**

- Validate JSON before submission
- Reference field documentation
- Use templates for new automations

---

### Execution Errors

#### "Pipeline execution failed"

**Cause:** Pipeline task failed during execution.

**Solution:**

```bash
# Check pipeline status
databasin pipelines get <pipeline_id>

# Test pipeline separately
databasin pipelines run <pipeline_id>

# Check connector health
databasin connectors test <connector_id>

# Review pipeline configuration
databasin pipelines get <pipeline_id> --json
```

**Prevention:**

- Test pipelines before adding to automations
- Monitor pipeline health
- Set up error notifications

---

#### "SQL query error"

**Cause:** SQL query failed during execution.

**Common SQL Errors:**

| Error             | Cause                   | Solution                           |
| ----------------- | ----------------------- | ---------------------------------- |
| Syntax error      | Invalid SQL             | Fix query syntax                   |
| Table not found   | Wrong table name        | Verify table exists                |
| Column not found  | Wrong column name       | Verify column exists               |
| Permission denied | Insufficient privileges | Grant permissions                  |
| Timeout           | Query too slow          | Optimize query or increase timeout |

**Solution:**

```bash
# Test query manually first
# Fix query in automation:

echo '{
  "automationTask": [{
    "taskType": "sql",
    "sqlTargetConnectionID": 58,
    "sqlQueryMap": [
      "SELECT * FROM correct_table WHERE date > CURRENT_DATE - 7"
    ],
    "automationOrderNumber": 1
  }]
}' > fix_sql.json

databasin automations update <automation_id> fix_sql.json
```

**Prevention:**

- Test queries in SQL editor first
- Use parameterized queries when possible
- Add proper error handling
- Set reasonable timeouts

---

#### "Connection refused"

**Cause:** Unable to connect to database/service.

**Solution:**

```bash
# Test connector
databasin connectors test <connector_id>

# If test fails, check connector configuration
databasin connectors get <connector_id>

# Fix connector issues:
# - Verify host is reachable
# - Check credentials
# - Verify firewall rules
# - Test network connectivity

# Update connector
echo '{
  "connectorHost": "correct-host.example.com",
  "connectorPort": "3306",
  "connectorUsername": "correct_user",
  "connectorPassword": "correct_password"
}' > fix_connector.json

databasin connectors update <connector_id> fix_connector.json

# Test again
databasin connectors test <connector_id>
```

**Prevention:**

- Regularly test connectors
- Monitor connector health
- Use connection pooling
- Set up alerts for connection failures

---

#### "Timeout exceeded"

**Cause:** Task execution exceeded configured timeout.

**Solution:**

```bash
# Option 1: Increase timeout
echo '{
  "jobDetails": {
    "jobTimeout": "7200"
  }
}' > increase_timeout.json

databasin automations update <automation_id> increase_timeout.json

# Option 2: Optimize task
# - Improve query performance
# - Reduce data volume
# - Increase cluster size
# - Break into smaller tasks
```

**Prevention:**

- Set realistic timeouts based on expected duration
- Monitor execution times
- Optimize slow queries
- Use appropriate cluster sizes

---

## Debugging Strategies

### Enable Verbose Logging

While the CLI doesn't have a verbose flag, you can get detailed information:

```bash
# Get full automation details
databasin automations get <automation_id> --json

# Save to file for analysis
databasin automations get <automation_id> --json > automation_debug.json

# Analyze specific sections
cat automation_debug.json | jq '.automationTask'
cat automation_debug.json | jq '.jobDetails'
cat automation_debug.json | jq '.lastRunStatus'
```

---

### Test Tasks Individually

Before running full automation, test each component:

**1. Test Connectors:**

```bash
# Extract connection IDs from automation
databasin automations get <automation_id> --json | jq '.automationTask[].sqlTargetConnectionID'

# Test each connector
databasin connectors test 58
databasin connectors test 59
```

**2. Test Pipelines:**

```bash
# Extract pipeline IDs from automation
databasin automations get <automation_id> --json | jq '.automationTask[] | select(.taskType=="pipeline") | .jobID'

# Test each pipeline
databasin pipelines run pipeline-123
databasin pipelines get pipeline-123
```

**3. Test SQL Queries:**

- Copy queries from automation configuration
- Run in Databasin SQL editor
- Verify results before adding to automation

**4. Test Schedule:**

```bash
# Verify cron expression using online tools
# Example: crontab.guru

# Test with manual run first
databasin automations run <automation_id>

# Monitor execution
databasin automations get <automation_id>
```

---

### Check Execution History

```bash
# Get last execution details
databasin automations get <automation_id> --json | jq '{
  lastRun: .lastRun,
  lastStatus: .lastStatus,
  lastError: .lastError,
  duration: .duration
}'

# For multiple runs, check audit logs (if enabled)
databasin automations get <automation_id> --json | jq '.auditInformation'
```

---

### Validate Dependencies

**Check all dependencies exist and are accessible:**

```bash
# 1. Verify project access
databasin projects list

# 2. Check connectors
databasin automations get <automation_id> --json | \
  jq '.automationTask[].sqlTargetConnectionID' | \
  sort -u | \
  while read id; do
    echo "Testing connector $id..."
    databasin connectors test $id
  done

# 3. Check pipelines
databasin automations get <automation_id> --json | \
  jq '.automationTask[] | select(.taskType=="pipeline") | .jobID' | \
  while read id; do
    echo "Checking pipeline $id..."
    databasin pipelines get $id
  done
```

---

### Use CLI Commands for Diagnosis

**Comprehensive diagnostic script:**

```bash
#!/bin/bash
AUTOMATION_ID=$1
PROJECT_ID=$2

echo "=== Automation Diagnostic Report ==="
echo ""

echo "1. Automation Status:"
databasin automations get $AUTOMATION_ID --fields name,isActive,status,lastRun,lastStatus
echo ""

echo "2. Schedule Configuration:"
databasin automations get $AUTOMATION_ID --json | jq '.jobDetails | {schedule: .jobRunSchedule, timezone: .jobRunTimeZone, timeout: .jobTimeout, clusterSize: .jobClusterSize}'
echo ""

echo "3. Task Configuration:"
databasin automations get $AUTOMATION_ID --json | jq '.automationTask[] | {order: .automationOrderNumber, type: .taskType, name: .taskName, active: .isActive}'
echo ""

echo "4. Testing Connectors:"
databasin automations get $AUTOMATION_ID --json | \
  jq -r '.automationTask[] | select(.sqlTargetConnectionID) | .sqlTargetConnectionID' | \
  sort -u | \
  while read id; do
    echo "  Connector $id:"
    databasin connectors test $id 2>&1 | head -1
  done
echo ""

echo "5. Checking Pipelines:"
databasin automations get $AUTOMATION_ID --json | \
  jq -r '.automationTask[] | select(.taskType=="pipeline") | .jobID' | \
  while read id; do
    echo "  Pipeline $id:"
    databasin pipelines get $id --fields status 2>&1 | head -1
  done
echo ""

echo "=== End Diagnostic Report ==="
```

**Usage:**

```bash
chmod +x diagnose_automation.sh
./diagnose_automation.sh <automation_id> <project_id>
```

---

## Best Practices

### Testing Before Scheduling

**Always test manually before activating:**

```bash
# Step 1: Create automation inactive
echo '{
  "automationName": "New Automation",
  "isActive": 0,
  "jobDetails": {
    "jobRunSchedule": "0 2 * * *",
    "jobTimeout": "3600"
  },
  ...
}' > automation.json

databasin automations create automation.json -p proj-001

# Step 2: Test manually
databasin automations run <automation_id>

# Step 3: Monitor execution
databasin automations get <automation_id>

# Step 4: If successful, activate
echo '{"isActive": 1}' > activate.json
databasin automations update <automation_id> activate.json
```

---

### Error Notifications

**Set up email notifications for failures:**

```json
{
	"jobDetails": {
		"emailNotifications": ["team@example.com", "oncall@example.com", "alerts@example.com"]
	}
}
```

**Benefits:**

- Immediate notification of failures
- Faster response to issues
- Better visibility into automation health

---

### Monitoring Strategies

**1. Regular Status Checks:**

```bash
# Check all automations daily
databasin automations list -p <project_id> --full --fields name,lastRun,lastStatus

# Filter to failed automations
databasin automations list -p <project_id> --full --json | \
  jq '.[] | select(.lastStatus == "Failed") | {id: .automationID, name: .automationName, error: .lastError}'
```

**2. Track Execution Times:**

```bash
# Monitor for performance degradation
databasin automations get <automation_id> --json | \
  jq '{name: .automationName, lastDuration: .duration, avgDuration: .averageDuration}'
```

**3. Resource Utilization:**

- Monitor cluster sizes
- Track timeout occurrences
- Identify resource-intensive automations

---

### Retry Configuration

**For transient failures, implement retry logic:**

While Databasin automations don't have built-in retry, you can:

1. **Monitor failures and re-run:**

   ```bash
   # Check for failures
   STATUS=$(databasin automations get <automation_id> --json | jq -r '.lastStatus')

   # Re-run if failed
   if [ "$STATUS" == "Failed" ]; then
     echo "Automation failed, retrying..."
     databasin automations run <automation_id>
   fi
   ```

2. **Schedule more frequently:**

   ```
   Instead of: 0 2 * * * (Daily at 2 AM)
   Use: 0 2,14 * * * (Twice daily at 2 AM and 2 PM)

   Benefits: Second chance if first run fails
   ```

3. **Use external orchestration:**
   - Airflow
   - Luigi
   - Custom scripts with retry logic

---

### Graceful Degradation

**Design automations to handle partial failures:**

**1. Break into smaller tasks:**

```json
{
	"automationTask": [
		{
			"taskType": "sql",
			"taskName": "Extract Data",
			"automationOrderNumber": 1
		},
		{
			"taskType": "sql",
			"taskName": "Transform Data",
			"automationOrderNumber": 2
		},
		{
			"taskType": "sql",
			"taskName": "Load Data",
			"automationOrderNumber": 3
		}
	]
}
```

**Benefits:**

- Identify which step failed
- Easier to recover
- Can restart from failure point

**2. Use idempotent operations:**

- DELETE + INSERT instead of UPDATE
- TRUNCATE + LOAD instead of MERGE
- CREATE OR REPLACE instead of CREATE

**3. Add validation steps:**

```sql
-- Validation task
SELECT COUNT(*) as row_count FROM staging_table WHERE date = CURRENT_DATE

-- Only proceed if validation passes
```

---

## Quick Diagnostic Checklist

Use this flowchart-style checklist to quickly diagnose automation issues:

### Is the automation running at all?

**NO** → Check:

- [ ] Is `isActive` set to 1?
  ```bash
  databasin automations get <id> --fields isActive
  ```
- [ ] Is the cron expression valid?
  ```bash
  databasin automations get <id> --fields schedule
  ```
- [ ] Is the timezone correct?
  ```bash
  databasin automations get <id> --json | grep jobRunTimeZone
  ```
- [ ] Do you have project access?
  ```bash
  databasin projects list
  ```

**YES** → Continue to next question

---

### Is the automation completing successfully?

**NO** → Check:

- [ ] What is the error message?
  ```bash
  databasin automations get <id> --fields lastError
  ```
- [ ] Which task is failing?
  ```bash
  databasin automations get <id> --json | jq '.automationTask'
  ```
- [ ] Test components individually:

  ```bash
  # Test connectors
  databasin connectors test <connector_id>

  # Test pipelines
  databasin pipelines get <pipeline_id>
  ```

- [ ] Is it timing out?
  ```bash
  databasin automations get <id> --json | jq '.jobDetails.jobTimeout'
  ```

**YES** → Continue to next question

---

### Is it running at the expected time?

**NO** → Check:

- [ ] Verify timezone:
  ```bash
  databasin automations get <id> --json | grep jobRunTimeZone
  ```
- [ ] Verify cron expression:
  ```bash
  databasin automations get <id> --fields schedule
  ```
- [ ] Check for AM/PM confusion (use 24-hour format)

**YES** → Continue to next question

---

### Is it running too frequently/infrequently?

**YES** → Check:

- [ ] Verify cron syntax:
  ```
  * * * * * = Every minute (probably wrong!)
  0 * * * * = Every hour
  0 */6 * * * = Every 6 hours
  0 2 * * * = Daily at 2 AM
  ```
- [ ] Check for overlapping executions:
  ```bash
  databasin automations get <id> --fields status,duration
  ```

---

### Is it slow or timing out?

**YES** → Check:

- [ ] Current timeout setting:
  ```bash
  databasin automations get <id> --json | jq '.jobDetails.jobTimeout'
  ```
- [ ] Cluster size:
  ```bash
  databasin automations get <id> --json | jq '.jobDetails.jobClusterSize'
  ```
- [ ] Query optimization needed?
- [ ] Data volume too large?

---

### Quick Fix Commands Reference

**Activate automation:**

```bash
echo '{"isActive": 1}' > activate.json
databasin automations update <id> activate.json
```

**Fix schedule:**

```bash
echo '{"jobDetails": {"jobRunSchedule": "0 2 * * *"}}' > schedule.json
databasin automations update <id> schedule.json
```

**Increase timeout:**

```bash
echo '{"jobDetails": {"jobTimeout": "7200"}}' > timeout.json
databasin automations update <id> timeout.json
```

**Increase cluster size:**

```bash
echo '{"jobDetails": {"jobClusterSize": "L"}}' > cluster.json
databasin automations update <id> cluster.json
```

**Fix timezone:**

```bash
echo '{"jobDetails": {"jobRunTimeZone": "America/New_York"}}' > timezone.json
databasin automations update <id> timezone.json
```

**Stop running automation:**

```bash
databasin automations stop <id>
```

**Test manually:**

```bash
databasin automations run <id>
databasin automations get <id>
```

---

## Summary

This troubleshooting guide covers the most common automation issues in Databasin:

**Key Takeaways:**

1. **Always test before activating** - Create inactive, test manually, then activate
2. **Use appropriate timeouts** - Based on expected execution duration
3. **Monitor regularly** - Check status, duration, and errors
4. **Test dependencies** - Verify connectors, pipelines, and connections
5. **Set up notifications** - Get alerts for failures
6. **Optimize performance** - Right-size clusters, optimize queries
7. **Use CLI for diagnosis** - Get detailed information with JSON output
8. **Follow the checklist** - Systematic approach to troubleshooting

**Most Common Issues:**

1. Automation inactive (`isActive: 0`)
2. Invalid cron expression
3. Wrong timezone
4. Task timeout exceeded
5. Connector authentication failure
6. Pipeline configuration error
7. SQL query syntax error
8. Overlapping executions

**Best Diagnostic Command:**

```bash
# Get complete automation state
databasin automations get <automation_id> --json
```

**When to Get Help:**

If you've:

- Followed this guide
- Tested all dependencies
- Verified configuration
- Reviewed logs
- And still have issues

Contact Databasin support with:

- Automation ID
- Project ID
- Error messages
- CLI command output
- Steps you've already tried

---

## Additional Resources

- **Databasin Automations Skill** - `SKILL.md`
- **CLI Reference** - `databasin automations --help`
- **API Documentation** - `references/api-endpoints.md` (if available)
- **Connectors Troubleshooting** - Databasin Connectors Skill
- **Pipelines Troubleshooting** - Databasin Pipelines Skill

---

_Last Updated: 2024-11-23_
