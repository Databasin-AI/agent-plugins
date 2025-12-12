---
name: databasin-automations
description: Expert skill for creating, managing, and troubleshooting Databasin automations through natural language interaction. Use this skill when users need to create new automations with scheduled or triggered tasks, modify existing automation settings, manage automation tasks (notebook, SQL, job, file drop, pipeline), test executions, troubleshoot failures, or work with automation schedules and triggers.
---

# Databasin Automations Skill

Expert skill for creating, managing, and troubleshooting Databasin automations through natural language interaction using the `databasin` CLI.

## When to Use This Skill

Use this skill when the user requests help with:

- **Creating new automations** - "Create an automation to run my pipeline daily at 2 AM"
- **Modifying existing automations** - "Update the schedule for automation 123"
- **Managing automation tasks** - "Add a SQL task to this automation"
- **Testing automations** - "Test if automation 456 runs correctly"
- **Deleting automations** - "Remove automation 789"
- **Understanding automation types** - "What task types are available?"
- **Troubleshooting execution issues** - "Why did my automation fail?"
- **Working with schedules** - "Change this to run every 6 hours instead of daily"
- **Managing triggers** - "Set up an event trigger for file uploads"
- **Monitoring automation status** - "Show me the execution history for this automation"

## Core Capabilities

This skill provides complete automation lifecycle management through the Databasin CLI:

1. **Automation Creation** - Create automations with cron schedules, intervals, or event triggers
2. **Task Management** - Add/update/delete tasks (notebook, SQL, job, file drop, pipeline, docker)
3. **Schedule Configuration** - Set up cron expressions, intervals, and time zones
4. **Execution Control** - Start, stop, enable, disable automations
5. **Status Monitoring** - Check execution status, logs, and history
6. **Troubleshooting** - Diagnose failures and configuration issues

## Available CLI Commands

All automation operations are performed through the `databasin automations` command:

### List Automations

```bash
databasin automations list [options]

Options:
  -p, --project <id>       Filter by project ID (recommended)
  --count                  Return only the count of automations
  --limit <number>         Limit number of results
  --fields <fields>        Comma-separated list of fields to display
  --active                 Filter to only active automations
  --running                Filter to only currently running automations
  --json                   Output in JSON format
  --csv                    Output in CSV format

Examples:
  databasin automations list -p proj-001
  databasin automations list -p proj-001 --active --json
  databasin automations list -p proj-001 --count
  databasin automations list -p proj-001 --fields name,schedule,status
```

### Get Automation Details

```bash
databasin automations get <id> [options]

Options:
  --fields <fields>        Comma-separated list of fields to display
  --json                   Output in JSON format
  --csv                    Output in CSV format

Examples:
  databasin automations get 123
  databasin automations get 123 --json
  databasin automations get 123 --fields name,schedule,tasks
```

### Create Automation

```bash
databasin automations create [file] [options]

Arguments:
  [file]                   JSON file with automation configuration
                          (interactive wizard if not provided)

Options:
  -p, --project <id>       Project ID for the automation

Examples:
  databasin automations create automation.json -p proj-001
  databasin automations create -p proj-001  # Interactive mode
```

### Update Automation

```bash
databasin automations update <id> [file] [options]

Arguments:
  <id>                     Automation ID
  [file]                   JSON file with updated configuration
                          (interactive wizard if not provided)

Examples:
  databasin automations update 123 updates.json
  databasin automations update 123  # Interactive mode
```

### Run Automation

```bash
databasin automations run <id>

Arguments:
  <id>                     Automation ID

Examples:
  databasin automations run 123
```

### Stop Automation

```bash
databasin automations stop <id>

Arguments:
  <id>                     Automation ID

Examples:
  databasin automations stop 123
```

### Delete Automation

```bash
databasin automations delete <id> [options]

Arguments:
  <id>                     Automation ID

Options:
  -y, --yes               Skip confirmation prompt

Examples:
  databasin automations delete 123
  databasin automations delete 123 --yes  # Skip confirmation
```

## Typical Workflows

### A. Creating a New Automation

**User Request:** "Create an automation to run my pipeline daily at 2 AM"

**Steps:**

1. **Interactive Creation (Recommended)**

   ```bash
   databasin automations create -p proj-001
   ```

   The CLI will prompt for all required information:
   - Automation name
   - Schedule (cron expression)
   - Active status
   - Pipeline ID (optional)
   - Cluster size
   - Job timeout

   **Interactive Example:**

   ```
   📝 Interactive Automation Creation

   ? Select project for automation: proj-001 (My Project)
   ? Enter automation name: Daily Pipeline Execution
   ? Enter schedule (cron format): 0 2 * * *
   ? Enable automation immediately? Yes
   ? Link to a pipeline? Yes
   ? Enter pipeline ID: 123
   ? Select cluster size: Small (s)
   ? Enter job timeout (seconds): 3600

   📋 Automation Configuration:
     Name: Daily Pipeline Execution
     Schedule: 0 2 * * * (Daily at 2 AM)
     Active: true
     Project: proj-001
     Pipeline: 123

   ? Create this automation? Yes

   ✓ Automation created successfully

   Automation Details:
     ID: 456
     Name: Daily Pipeline Execution
     Schedule: 0 2 * * *
     Active: true

   ℹ Run automation manually: databasin automations run 456
   ```

2. **File-Based Creation (Advanced)**

   For complex automations with multiple tasks, create a JSON configuration file:

   **automation.json:**

   ```json
   {
   	"automationName": "Daily Pipeline Execution",
   	"internalID": "proj-001",
   	"isActive": 1,
   	"isPrivate": 0,
   	"auditEnabled": 0,
   	"jobDetails": {
   		"jobRunSchedule": "0 2 * * *",
   		"jobRunTimeZone": "America/New_York",
   		"jobClusterSize": "s",
   		"jobTimeout": "18000",
   		"tags": [],
   		"emailNotifications": ["user@example.com"]
   	},
   	"automationTask": [
   		{
   			"taskType": "pipeline",
   			"taskName": "Run Data Pipeline",
   			"jobID": "123",
   			"automationOrderNumber": 1,
   			"isActive": true
   		}
   	]
   }
   ```

   **Create the automation:**

   ```bash
   databasin automations create automation.json -p proj-001
   ```

3. **Verify Creation**

   ```bash
   databasin automations get 456
   ```

   This displays the automation details including:
   - Schedule with human-readable translation
   - Active status
   - Task configuration
   - Next scheduled run time

4. **Confirm Success**

   Inform user:
   - Automation ID (e.g., 456)
   - Next scheduled run time
   - How to manually run: `databasin automations run 456`
   - How to view details: `databasin automations get 456`

### B. Modifying Automation Schedule

**User Request:** "Change automation 123 to run every 6 hours instead of daily"

**Steps:**

1. **Check Current Configuration**

   ```bash
   databasin automations get 123
   ```

   **Output:**

   ```
   Automation ID:    123
   Name:             Daily Sales Sync
   Schedule:         0 2 * * * (Daily at 2 AM)
   Status:           active
   Project:          proj-001
   Last Run:         2024-11-23 02:00:00
   ```

2. **Update Schedule (Interactive)**

   ```bash
   databasin automations update 123
   ```

   **Interactive Flow:**

   ```
   📝 Interactive Automation Update

   ✓ Automation loaded

   Current configuration:
     Name: Daily Sales Sync
     Schedule: 0 2 * * * (Daily at 2 AM)
     Active: true
     Running: false

   ? Update automation name? No
   ? Update schedule? Yes
   ? Enter new schedule (cron format): 0 */6 * * *
   ? Update active status? No
   ? Update cluster size? No
   ? Update timeout? No

   📋 Fields to Update:
     jobRunSchedule: 0 */6 * * * (Every 6 hours)

   ? Apply these updates? Yes

   ✓ Automation updated successfully

   Updated Automation:
     ID: 123
     Name: Daily Sales Sync
     Schedule: 0 */6 * * *
     Active: true
     Updated Fields: jobRunSchedule
   ```

3. **Update Schedule (File-Based)**

   **updates.json:**

   ```json
   {
   	"jobRunSchedule": "0 */6 * * *"
   }
   ```

   ```bash
   databasin automations update 123 updates.json
   ```

4. **Verify Update**
   ```bash
   databasin automations get 123 --fields schedule
   ```

### C. Adding Tasks to an Automation

**User Request:** "Add a SQL task to automation 123 that queries the sales database"

**Steps:**

1. **Get Current Automation**

   ```bash
   databasin automations get 123 --json
   ```

   This shows the current task configuration.

2. **Create Updated Configuration**

   Add the new SQL task to the `automationTask` array:

   **updated_automation.json:**

   ```json
   {
   	"automationTask": [
   		{
   			"taskType": "pipeline",
   			"taskName": "Run Data Pipeline",
   			"jobID": "123",
   			"automationOrderNumber": 1,
   			"isActive": true
   		},
   		{
   			"taskType": "sql",
   			"taskName": "Query Sales Data",
   			"sqlTargetConnectionID": 58,
   			"sqlQueryMap": ["SELECT * FROM sales WHERE date > CURRENT_DATE - 7"],
   			"automationOrderNumber": 2,
   			"isActive": true
   		}
   	]
   }
   ```

3. **Update Automation**

   ```bash
   databasin automations update 123 updated_automation.json
   ```

4. **Verify Task Addition**

   ```bash
   databasin automations get 123 --fields tasks
   ```

5. **Confirm Addition**

   Show user:
   - Updated automation details
   - Task order in automation
   - How to test: `databasin automations run 123`

### D. Troubleshooting Failed Automation

**User Request:** "My automation 456 failed last night, what went wrong?"

**Steps:**

1. **Get Automation Status**

   ```bash
   databasin automations get 456
   ```

   **Output shows:**

   ```
   Automation ID:    456
   Name:             Nightly ETL Process
   Schedule:         0 2 * * *
   Status:           active
   Last Run:         2024-11-23 02:00:15
   Last Status:      Failed
   Error:            SQL query timeout after 1800 seconds
   ```

2. **Analyze Error**

   Common automation issues:
   - **Invalid schedule expression** - Check cron format
   - **Task configuration errors** - Validate task fields
   - **Connection failures** - Verify connection IDs
   - **Timeout exceeded** - Increase `jobTimeout`
   - **Permission issues** - Check user access
   - **SQL errors** - Validate queries
   - **Resource constraints** - Increase cluster size

3. **Get Detailed Information**

   ```bash
   databasin automations get 456 --json
   ```

   Review:
   - Task configuration
   - Connection IDs
   - SQL queries
   - File paths
   - Timeout settings

4. **Suggest Fixes**

   Based on the error "SQL query timeout after 1800 seconds":

   **Increase timeout:**

   ```json
   {
   	"jobDetails": {
   		"jobTimeout": "3600"
   	}
   }
   ```

   ```bash
   databasin automations update 456 timeout_fix.json
   ```

5. **Test Fix**

   ```bash
   databasin automations run 456
   ```

   Monitor execution:

   ```bash
   databasin automations get 456
   ```

6. **Prevent Future Issues**

   Recommendations:
   - Set appropriate timeout for workload
   - Add email notifications
   - Enable audit logging
   - Use appropriate cluster size
   - Optimize SQL queries

### E. Managing Automation Execution

**User Request:** "Start the automation manually and monitor its progress"

**Steps:**

1. **Check Automation Status**

   ```bash
   databasin automations get 123
   ```

   Verify:
   - Automation is active
   - Not currently running
   - Configuration is correct

2. **Start Automation**

   ```bash
   databasin automations run 123
   ```

   **Output:**

   ```
   ⠹ Starting automation execution...
   ✓ Automation execution started

     Execution ID: exec-789
     Status: running

   ℹ Automation is running in the background
   ℹ Check status with 'databasin automations get 123'
   ```

3. **Monitor Progress**

   ```bash
   # Check periodically
   databasin automations get 123
   ```

   Shows current status:
   - Running / Completed / Failed
   - Current task execution
   - Time elapsed

4. **Stop if Needed**

   ```bash
   databasin automations stop 123
   ```

   **Confirmation:**

   ```
   ✓ Automation: Daily Sales Sync

   ⚠ This will stop the currently running execution
     Automation: Daily Sales Sync
     Status: Running

   ? Stop this automation? Yes

   ✓ Automation stopped successfully

   Automation stopped
     Status: stopped
     Message: Execution terminated by user

   ℹ Check status with: databasin automations get 123
   ```

### F. Deleting an Automation

**User Request:** "Delete automation 789"

**Steps:**

1. **Get Automation Details**

   ```bash
   databasin automations get 789
   ```

   Shows what will be deleted:

   ```
   Automation ID:    789
   Name:             Old Weekly Report
   Schedule:         0 0 * * 0
   Status:           inactive
   Tasks:            5 tasks
   Created:          2023-06-15
   ```

2. **Delete with Confirmation**

   ```bash
   databasin automations delete 789
   ```

   **Confirmation Prompt:**

   ```
   ✓ Automation: Old Weekly Report (789)

   ⚠ WARNING: This action cannot be undone!
     Automation: Old Weekly Report
     Schedule: 0 0 * * 0 (Weekly on Sunday)
     Active: false
     ID: 789

   ? Are you sure you want to delete this automation? Yes

   ✓ Automation deleted successfully

   Deleted automation: Old Weekly Report
   ```

3. **Delete Without Confirmation** (Use with caution)

   ```bash
   databasin automations delete 789 --yes
   ```

4. **Warn About Impact**

   IMPORTANT: Deleting will:
   - Stop scheduled executions
   - Remove all tasks
   - Delete execution history
   - Cannot be undone

### G. Listing and Filtering Automations

**User Request:** "Show me all active automations in my project"

**Steps:**

1. **List All Automations**

   ```bash
   databasin automations list -p proj-001
   ```

   **Output (Table Format):**

   ```
   ID    Name                    Status     Schedule        Last Run
   123   Daily Sales Sync        ✓ Active   0 2 * * *      Success
   456   Hourly Analytics        ✓ Active   0 * * * *      Running
   789   Weekly Reports          ✗ Inactive 0 0 * * 0      Never
   ```

2. **Filter Active Only**

   ```bash
   databasin automations list -p proj-001 --active
   ```

3. **Filter Currently Running**

   ```bash
   databasin automations list -p proj-001 --running
   ```

4. **Get Count Only** (Token Efficient)

   ```bash
   databasin automations list -p proj-001 --count
   ```

   **Output:**

   ```
   3
   ```

5. **JSON Output for Scripting**

   ```bash
   databasin automations list -p proj-001 --json
   ```

   **Output:**

   ```json
   [
     {
       "automationID": 123,
       "automationName": "Daily Sales Sync",
       "isActive": 1,
       "jobRunSchedule": "0 2 * * *",
       "lastRunStatus": "Success"
     },
     ...
   ]
   ```

6. **CSV Output for Reports**

   ```bash
   databasin automations list -p proj-001 --csv
   ```

   **Output:**

   ```csv
   automationID,automationName,isActive,jobRunSchedule,lastRunStatus
   123,Daily Sales Sync,1,0 2 * * *,Success
   456,Hourly Analytics,1,0 * * * *,Running
   ```

7. **Limit Results**

   ```bash
   databasin automations list -p proj-001 --limit 10
   ```

8. **Select Specific Fields**
   ```bash
   databasin automations list -p proj-001 --fields name,schedule,status
   ```

## Authentication

### JWT Token Management

All CLI commands use the authentication configured during `databasin login`.

**Check Authentication Status:**

```bash
databasin auth status
```

**Login if Needed:**

```bash
databasin login
```

**Token Refresh:**

The CLI automatically refreshes tokens before they expire. If you get 401 errors:

```bash
databasin login
```

## Configuration Defaults

### Required Organizational Fields

When creating automations, these fields are required:

- `internalID` - Project identifier (string) - Use `-p` flag or include in JSON
- `automationName` - Name of the automation
- `jobRunSchedule` - Cron expression for schedule

**How to get project ID:**

```bash
databasin projects list
```

### Task Type Selection

**Guide users to correct type:**

| User Needs              | Task Type  | Required Fields                        |
| ----------------------- | ---------- | -------------------------------------- |
| Run Databricks notebook | `notebook` | `notebookPath`                         |
| Execute SQL queries     | `sql`      | `sqlTargetConnectionID`, `sqlQueryMap` |
| Trigger Databricks job  | `job`      | `jobID`                                |
| Move/copy files         | `file`     | `sourceFileId`, `targetFileId`         |
| Execute pipeline        | `pipeline` | `jobID` (pipeline ID)                  |
| Run Docker container    | `docker`   | `dockerImage`, `dockerCommand`         |

### Schedule Type Selection

**Common cron patterns:**

| User Needs       | Cron Expression | Description                          |
| ---------------- | --------------- | ------------------------------------ |
| Every hour       | `0 * * * *`     | At minute 0 of every hour            |
| Every 6 hours    | `0 */6 * * *`   | At minute 0 of hours 0, 6, 12, 18    |
| Daily at 2 AM    | `0 2 * * *`     | At 2:00 AM every day                 |
| Weekdays at 9 AM | `0 9 * * 1-5`   | At 9:00 AM Monday-Friday             |
| Weekly on Sunday | `0 0 * * 0`     | At midnight every Sunday             |
| Monthly on 1st   | `0 0 1 * *`     | At midnight on the 1st of each month |

**Cron format:** `minute hour day month weekday`

- Minute: 0-59
- Hour: 0-23
- Day: 1-31
- Month: 1-12
- Weekday: 0-6 (0 = Sunday)

## Validation and Error Handling

### Pre-Creation Validation

The CLI validates automation configurations before creating them:

**Common Validation Errors:**

1. **Missing Required Fields**

   ```
   Error: Missing required field: automationName
   Fix: Add automationName to configuration
   ```

2. **Invalid Cron Expression**

   ```
   Error: Invalid cron format (use digits, *, -, /, and spaces)
   Fix: Use valid cron syntax (e.g., "0 2 * * *")
   ```

3. **Invalid Task Configuration**
   ```
   Error: SQL task missing sqlTargetConnectionID
   Fix: Provide connection ID for database
   ```

### Post-Creation Testing

**Always test after creation:**

```bash
databasin automations run <automation_id>
```

**Common Execution Errors:**

1. **Schedule Not Triggering**

   ```
   Cause: Automation not active or invalid schedule
   Fix: Enable automation and verify cron expression
   ```

2. **Task Failed**

   ```
   Cause: Connection error, invalid query, or timeout
   Fix: Check task logs and connection settings
   ```

3. **Timeout Exceeded**
   ```
   Cause: Task running longer than jobTimeout
   Fix: Increase timeout or optimize task
   ```

## Best Practices

### 1. Naming Conventions

**Recommend:**

```
[Frequency] [Action] [Target]

Examples:
- "Daily Sales Data Sync"
- "Hourly Analytics Refresh"
- "Weekly Report Generation"
- "Real-time Event Processing"
```

### 2. Schedule Management

**Start Inactive, Test, Then Activate:**

Create automation with `"isActive": 0`:

```json
{
  "automationName": "New Automation",
  "isActive": 0,
  ...
}
```

Test manually:

```bash
databasin automations run <automation_id>
```

Activate after successful test:

```json
{
	"isActive": 1
}
```

```bash
databasin automations update <automation_id> activate.json
```

### 3. Task Ordering

**Logical Sequence:**

```
Task 1: Extract data (file or pipeline)
Task 2: Transform data (SQL or notebook)
Task 3: Load data (SQL or file drop)
Task 4: Notify (optional)
```

**Example:**

```json
{
	"automationTask": [
		{
			"taskType": "pipeline",
			"taskName": "Extract Customer Data",
			"automationOrderNumber": 1
		},
		{
			"taskType": "sql",
			"taskName": "Transform and Validate",
			"automationOrderNumber": 2
		},
		{
			"taskType": "notebook",
			"taskName": "Generate Analytics",
			"automationOrderNumber": 3
		}
	]
}
```

### 4. Timeout Configuration

**Adjust based on workload:**

- Quick queries: 1,800 seconds (30 minutes)
- Medium ETL: 3,600 seconds (1 hour)
- Large processing: 10,800 seconds (3 hours)
- Maximum: 18,000 seconds (5 hours)

**Don't exceed job duration:**

```bash
# If automation takes 30 minutes to run,
# don't schedule every 15 minutes!

# Bad: Could overlap
"jobRunSchedule": "*/15 * * * *"  # Every 15 minutes

# Good: Safe interval
"jobRunSchedule": "0 * * * *"  # Every hour
```

### 5. Error Notifications

**Set up email alerts:**

```json
{
	"jobDetails": {
		"emailNotifications": ["team@example.com", "oncall@example.com"]
	}
}
```

### 6. Audit Tracking

**Enable for compliance:**

```json
{
	"auditEnabled": 1,
	"auditInformation": {
		"irbNumber": "IRB-2024-001",
		"piName": "Dr. Smith"
	}
}
```

## Token Efficiency

### CLI Optimization Features

The CLI provides built-in token efficiency:

1. **Required Project Filtering**

   ```bash
   # Always filter by project
   databasin automations list -p proj-001
   ```

2. **Count Mode**

   ```bash
   # Get count without fetching full data
   databasin automations list -p proj-001 --count
   ```

3. **Field Selection**

   ```bash
   # Return only needed fields
   databasin automations list -p proj-001 --fields name,schedule
   ```

4. **Result Limiting**

   ```bash
   # Limit results
   databasin automations list -p proj-001 --limit 10
   ```

5. **Smart Warnings**

   The CLI warns when queries return large datasets:

   ```
   ⚠ Large result set detected (150 automations)

   Consider:
   - Use --count to get only the count
   - Use --fields to limit displayed fields
   - Use --limit to reduce number of results
   ```

### Token Efficiency Best Practices

**Instead of:**

```bash
# Returns all automations (potentially 100s)
databasin automations list
```

**Use:**

```bash
# Returns only automations in specific project
databasin automations list -p proj-001
```

**Instead of:**

```bash
# Returns full automation objects
databasin automations list -p proj-001 --json
```

**Use:**

```bash
# Returns only count
databasin automations list -p proj-001 --count
```

**Instead of:**

```bash
# Returns all fields
databasin automations get 123 --json
```

**Use:**

```bash
# Returns specific fields
databasin automations get 123 --fields name,schedule,status
```

## Output Format Options

All commands support multiple output formats:

### Table Format (Default)

Best for human viewing:

```bash
databasin automations list -p proj-001
```

**Output:**

```
ID    Name                    Status     Schedule        Last Run
123   Daily Sales Sync        ✓ Active   0 2 * * *      Success
456   Hourly Analytics        ✓ Active   0 * * * *      Running
```

### JSON Format

Best for scripting and integration:

```bash
databasin automations list -p proj-001 --json
```

**Output:**

```json
[
	{
		"automationID": 123,
		"automationName": "Daily Sales Sync",
		"isActive": 1,
		"jobRunSchedule": "0 2 * * *",
		"lastRunStatus": "Success"
	}
]
```

### CSV Format

Best for spreadsheets and reports:

```bash
databasin automations list -p proj-001 --csv
```

**Output:**

```csv
automationID,automationName,isActive,jobRunSchedule,lastRunStatus
123,Daily Sales Sync,1,0 2 * * *,Success
```

## Complete Automation Example

Here's a complete example showing the full automation lifecycle:

### 1. Create Automation

**automation.json:**

```json
{
	"automationName": "Daily ETL Workflow",
	"internalID": "proj-001",
	"isActive": 0,
	"isPrivate": 0,
	"auditEnabled": 1,
	"auditInformation": {
		"purpose": "Daily data synchronization",
		"owner": "Data Engineering Team"
	},
	"jobDetails": {
		"jobRunSchedule": "0 2 * * *",
		"jobRunTimeZone": "America/New_York",
		"jobClusterSize": "M",
		"jobTimeout": "7200",
		"tags": ["etl", "daily", "production"],
		"emailNotifications": ["data-team@company.com"]
	},
	"automationTask": [
		{
			"taskType": "pipeline",
			"taskName": "Extract Source Data",
			"jobID": "pipeline-123",
			"automationOrderNumber": 1,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "Validate and Transform",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": [
				"UPDATE staging.data SET processed = true WHERE valid = true",
				"DELETE FROM staging.data WHERE valid = false"
			],
			"automationOrderNumber": 2,
			"isActive": true
		},
		{
			"taskType": "notebook",
			"taskName": "Generate Analytics",
			"notebookPath": "/analytics/daily_summary",
			"automationOrderNumber": 3,
			"isActive": true
		}
	]
}
```

**Create:**

```bash
databasin automations create automation.json -p proj-001
```

### 2. Test Automation

```bash
databasin automations run 456
```

### 3. Monitor Execution

```bash
databasin automations get 456
```

### 4. Activate if Successful

**activate.json:**

```json
{
	"isActive": 1
}
```

```bash
databasin automations update 456 activate.json
```

### 5. Monitor Ongoing

```bash
# Check status periodically
databasin automations get 456

# List all running automations
databasin automations list -p proj-001 --running
```

## Integration Workflows

### End-to-End: MySQL to Snowflake Daily Sync

This workflow demonstrates how the automations skill integrates with connectors and pipelines to create a complete automated ETL solution. This example shows only the automation-specific parts of the workflow. For the complete end-to-end setup including connector and pipeline creation, see `CROSS-SKILL-WORKFLOW-EXAMPLE.md`.

#### Workflow Overview

This workflow assumes you have already completed:

- **Part 1-2**: Created MySQL source connector (`conn-mysql-001`) and Snowflake target connector (`conn-snow-002`) using `databasin-connectors` skill
- **Part 3-5**: Built and tested a data pipeline (`pipeline-daily-sync-001`) that syncs orders from MySQL to Snowflake using `databasin-pipelines` skill

The automation skill handles Parts 6-8:

- **Part 6**: Create automation to run pipeline on schedule
- **Part 7**: Test and monitor automation execution
- **Part 8**: Verify end-to-end workflow

**What the Complete Workflow Achieves:**

```
MySQL Orders Table → Pipeline (Extract/Transform/Load) → Snowflake DWH
         ↑                                                      ↓
         └──────── Automated Daily at 2 AM ───────────────────┘
```

#### Prerequisites

Before using this automation workflow, you need:

- **Pipeline ID**: `pipeline-daily-sync-001` (created via `databasin-pipelines` skill)
- **Connector IDs**: `conn-mysql-001` and `conn-snow-002` (created via `databasin-connectors` skill)
- **Project ID**: Your Databasin project ID
- **Pipeline tested**: Pipeline should run successfully manually before automating

**Verify Prerequisites:**

```bash
# Check connectors exist and are active
databasin connectors get conn-mysql-001
databasin connectors get conn-snow-002

# Check pipeline exists and works
databasin pipelines get pipeline-daily-sync-001
databasin pipelines run pipeline-daily-sync-001 --wait
```

#### Part 6: Create Automation for Scheduled Runs

**Step 6.1: Create Automation Configuration**

Create file: `daily-sync-automation.json`

```json
{
	"automationName": "Daily Orders Sync Automation",
	"internalID": "YOUR_PROJECT_ID",
	"isActive": 1,
	"isPrivate": 0,
	"auditEnabled": 1,
	"auditInformation": {
		"purpose": "Automated daily sync of orders from MySQL to Snowflake",
		"owner": "Data Engineering Team"
	},
	"jobDetails": {
		"jobRunSchedule": "0 2 * * *",
		"jobRunTimeZone": "America/New_York",
		"jobClusterSize": "M",
		"jobTimeout": "7200",
		"tags": ["production", "daily", "orders", "automated"],
		"emailNotifications": ["data-team@example.com"]
	},
	"automationTask": [
		{
			"taskType": "pipeline",
			"taskName": "Run Orders Sync Pipeline",
			"jobID": "pipeline-daily-sync-001",
			"automationOrderNumber": 1,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "Validate Data Quality",
			"sqlTargetConnectionID": "conn-snow-002",
			"sqlQueryMap": [
				"SELECT CASE WHEN COUNT(*) > 0 AND MAX(SYNCED_AT) > DATEADD(hour, -1, CURRENT_TIMESTAMP()) THEN 'PASS' ELSE 'FAIL' END as validation_result FROM ANALYTICS_DB.ORDERS.ORDERS"
			],
			"automationOrderNumber": 2,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "Update Sync Metadata",
			"sqlTargetConnectionID": "conn-snow-002",
			"sqlQueryMap": [
				"INSERT INTO ANALYTICS_DB.ORDERS.SYNC_LOG (pipeline_id, sync_time, rows_synced, status) SELECT 'pipeline-daily-sync-001', CURRENT_TIMESTAMP(), COUNT(*), 'SUCCESS' FROM ANALYTICS_DB.ORDERS.ORDERS WHERE SYNCED_AT > DATEADD(hour, -1, CURRENT_TIMESTAMP())"
			],
			"automationOrderNumber": 3,
			"isActive": true
		}
	]
}
```

**Key Configuration Highlights:**

- **Schedule**: `"0 2 * * *"` = Daily at 2:00 AM EST
- **Multi-task workflow**: Pipeline execution → Data validation → Metadata update
- **Task 1 (Pipeline)**: Runs the pipeline created in previous steps using `jobID: "pipeline-daily-sync-001"`
- **Task 2 (SQL)**: Validates data was synced within last hour using connector `conn-snow-002`
- **Task 3 (SQL)**: Updates sync metadata table for monitoring
- **Timeout**: 7200 seconds (2 hours) for complete workflow
- **Notifications**: Email alerts to data team

**Important Fields:**

- `jobID`: Must match your pipeline ID from Part 3-5
- `sqlTargetConnectionID`: Must match your Snowflake connector ID from Part 2
- `jobRunSchedule`: Cron expression for schedule
- `automationOrderNumber`: Defines task execution order (1, 2, 3...)

**Step 6.2: Create the Automation**

```bash
databasin automations create daily-sync-automation.json -p YOUR_PROJECT_ID
```

**Expected Output:**

```
✓ Automation created successfully

Automation Details:
  ID: auto-daily-sync-001
  Name: Daily Orders Sync Automation
  Schedule: 0 2 * * * (Daily at 2:00 AM America/New_York)
  Next Run: 2025-11-24 02:00:00 EST
  Status: Active
  Tasks: 3 configured
    1. Run Orders Sync Pipeline (pipeline)
    2. Validate Data Quality (sql)
    3. Update Sync Metadata (sql)

Automation is now active and will run on schedule.

ℹ Test immediately: databasin automations run auto-daily-sync-001
ℹ View status: databasin automations get auto-daily-sync-001
```

**Important:** Save the automation ID `auto-daily-sync-001` for testing and monitoring.

#### Part 7: Test Automation Immediately

Before waiting for the scheduled run, test the automation manually to verify it works correctly.

**Step 7.1: Run Automation Once**

```bash
databasin automations run auto-daily-sync-001
```

**Expected Output (~3-6 minutes):**

```
⠹ Starting automation execution...
✓ Automation execution started

  Execution ID: exec-auto-20251123-104500
  Status: running

ℹ Automation is running in the background
ℹ Check status with 'databasin automations get auto-daily-sync-001'

Starting automation: Daily Orders Sync Automation

[10:45:00] Starting Task 1/3: Run Orders Sync Pipeline
[10:45:02] ✓ Pipeline pipeline-daily-sync-001 started
[10:47:24] ✓ Pipeline completed successfully (2m 22s)
[10:47:24]   - Rows processed: 142
[10:47:24]   - Status: SUCCESS

[10:47:25] Starting Task 2/3: Validate Data Quality
[10:47:28] ✓ SQL validation passed
[10:47:28]   - Result: PASS
[10:47:28]   - Query duration: 2.3s

[10:47:29] Starting Task 3/3: Update Sync Metadata
[10:47:31] ✓ Metadata updated
[10:47:31]   - Rows inserted: 1
[10:47:31]   - Query duration: 1.8s

[10:47:35] Automation completed successfully

Summary:
  Total Duration: 2m 35s
  Tasks Completed: 3/3
  Tasks Failed: 0/3
  Status: SUCCESS

Next scheduled run: 2025-11-24 02:00:00 EST
```

**Verification Checklist:**

- ✓ All 3 tasks completed successfully
- ✓ Pipeline processed data (check rows count > 0)
- ✓ Data validation passed
- ✓ Metadata updated
- ✓ Total duration reasonable (< 5 minutes for incremental sync)

**Troubleshooting Test Execution:**

- ❌ "Pipeline not found" → Verify pipeline ID matches: `databasin pipelines list -p YOUR_PROJECT_ID`
- ❌ "Connection failed" → Test connector: `databasin connectors test conn-snow-002`
- ❌ "SQL validation failed" → Check table exists in Snowflake: `ANALYTICS_DB.ORDERS.ORDERS`
- ❌ "Timeout exceeded" → Increase `jobTimeout` in automation config

#### Part 8: Monitor Automation

**Step 8.1: View Automation Status**

```bash
databasin automations get auto-daily-sync-001
```

**Expected Output:**

```
Automation ID:    auto-daily-sync-001
Name:             Daily Orders Sync Automation
Schedule:         0 2 * * * (Daily at 2:00 AM America/New_York)
Status:           active
Project:          YOUR_PROJECT_ID
Created:          2025-11-23 10:35:22
Last Run:         2025-11-23 10:45:00
Last Status:      Success
Next Run:         2025-11-24 02:00:00

Tasks (3):
  1. Run Orders Sync Pipeline (pipeline) - Active
  2. Validate Data Quality (sql) - Active
  3. Update Sync Metadata (sql) - Active

Recent Executions:
  2025-11-23 10:45:00 - SUCCESS (2m 35s)
  2025-11-23 02:00:15 - SUCCESS (2m 41s)
  2025-11-22 02:00:12 - SUCCESS (2m 38s)
```

**Step 8.2: Check Execution History (if available)**

```bash
databasin automations list -p YOUR_PROJECT_ID --fields name,schedule,lastRun,status
```

**Expected Output:**

```
ID                    Name                            Schedule      Last Run             Status
--------------------  ------------------------------  ------------  -------------------  --------
auto-daily-sync-001   Daily Orders Sync Automation   0 2 * * *     2025-11-23 10:45:00  ✓ Active
```

**Step 8.3: Monitor Ongoing Executions**

```bash
# List currently running automations
databasin automations list -p YOUR_PROJECT_ID --running

# View specific automation with JSON output for detailed monitoring
databasin automations get auto-daily-sync-001 --json
```

**Monitoring Best Practices:**

1. Check automation status daily for first week
2. Review email notifications for failures
3. Monitor execution duration trends
4. Verify data freshness in Snowflake
5. Set up alerts for execution failures (see Part 11 in full workflow)

#### Workflow Complete

**What You've Built:**

You now have a fully automated ETL workflow that runs daily:

1. **2 Data Connectors** (from `databasin-connectors` skill):
   - `conn-mysql-001`: MySQL source database
   - `conn-snow-002`: Snowflake data warehouse

2. **1 Data Pipeline** (from `databasin-pipelines` skill):
   - `pipeline-daily-sync-001`: Extracts orders, transforms timestamps, loads to Snowflake

3. **1 Automation** (from `databasin-automations` skill):
   - `auto-daily-sync-001`: Runs pipeline daily at 2 AM, validates data, updates metadata

**What Happens Every Night at 2 AM:**

1. Automation triggers (`auto-daily-sync-001`)
2. Task 1: Pipeline runs (`pipeline-daily-sync-001`)
   - Extracts new/updated orders from MySQL
   - Applies transformations (timezone conversion, uppercase status)
   - Loads data to Snowflake
3. Task 2: Validates data quality
   - Checks data was synced within last hour
   - Verifies row counts
4. Task 3: Updates sync metadata
   - Logs sync time, rows processed, status
   - Enables monitoring and alerting
5. Sends email notification to data team

**Success Metrics:**

- **Setup Time**: ~15-20 minutes for complete workflow
- **Daily Runtime**: ~2-5 minutes (incremental sync)
- **Maintenance**: Minimal - monitors itself
- **Reliability**: Automatic retries, error notifications, audit logging

**Next Steps:**

- Add more pipelines for other tables (customers, products, order_items)
- Configure Slack notifications for failures
- Set up monitoring dashboards in Reportbasin
- Add more data quality validation rules
- Scale Snowflake warehouse for larger data volumes

**Quick Reference Commands:**

```bash
# View automation status
databasin automations get auto-daily-sync-001

# Run automation manually
databasin automations run auto-daily-sync-001

# Update automation schedule
databasin automations update auto-daily-sync-001 new-schedule.json

# Stop automation execution
databasin automations stop auto-daily-sync-001

# Disable automation temporarily
databasin automations update auto-daily-sync-001 '{"isActive": 0}'
```

#### Troubleshooting This Workflow

**Issue 1: Automation Not Running on Schedule**

**Symptoms:**

- No executions at scheduled time (2 AM)
- Last run time doesn't match schedule

**Diagnosis:**

```bash
databasin automations get auto-daily-sync-001 --fields schedule,isActive,nextRun
```

**Solutions:**

1. Verify `isActive: 1` in configuration
2. Check cron expression is valid: `0 2 * * *`
3. Verify timezone is correct: `America/New_York`
4. Check for overlapping executions (previous run still in progress)
5. Review automation service health

**Issue 2: Pipeline Task Fails**

**Symptoms:**

- Task 1 (Run Orders Sync Pipeline) fails
- Subsequent tasks don't execute

**Diagnosis:**

```bash
# Check pipeline status
databasin pipelines get pipeline-daily-sync-001

# View automation execution logs
databasin automations get auto-daily-sync-001

# Test pipeline separately
databasin pipelines run pipeline-daily-sync-001 --wait
```

**Solutions:**

1. Verify pipeline ID is correct in automation config
2. Test pipeline manually to isolate issue
3. Check connector health: `databasin connectors test conn-mysql-001`
4. Review pipeline logs for specific errors
5. Increase `jobTimeout` if pipeline timing out

**Issue 3: Data Validation Task Fails**

**Symptoms:**

- Task 2 (Validate Data Quality) fails
- Validation query returns "FAIL"

**Diagnosis:**

```bash
# Check Snowflake table exists and has recent data
# Run this SQL in Snowflake:
# SELECT COUNT(*), MAX(SYNCED_AT) FROM ANALYTICS_DB.ORDERS.ORDERS;
```

**Solutions:**

1. Verify table name and schema in SQL query
2. Check connector ID matches Snowflake connector: `conn-snow-002`
3. Adjust validation time window (currently 1 hour)
4. Verify pipeline actually loaded data (check Task 1 output)
5. Test SQL query directly in Snowflake

**Issue 4: Metadata Update Task Fails**

**Symptoms:**

- Task 3 (Update Sync Metadata) fails
- INSERT statement errors

**Diagnosis:**

```bash
# Verify SYNC_LOG table exists in Snowflake
# CREATE TABLE IF NOT EXISTS ANALYTICS_DB.ORDERS.SYNC_LOG (
#   pipeline_id VARCHAR(100),
#   sync_time TIMESTAMP,
#   rows_synced NUMBER,
#   status VARCHAR(50)
# );
```

**Solutions:**

1. Create SYNC_LOG table if missing (see SQL above)
2. Check table permissions for insert
3. Verify connector has write access
4. Review SQL syntax in `sqlQueryMap`
5. Set task `onFailure: "continue"` if metadata is optional

**Issue 5: Performance Degradation**

**Symptoms:**

- Automation duration increased from 2m to 15m
- Timeout errors

**Diagnosis:**

```bash
# View recent execution times
databasin automations get auto-daily-sync-001

# Check pipeline performance
databasin pipelines get pipeline-daily-sync-001
```

**Solutions:**

1. Increase `jobTimeout` from 7200 to 10800 (3 hours)
2. Optimize pipeline configuration (increase batch size)
3. Check MySQL database load during sync time
4. Increase Snowflake warehouse size (S → M → L)
5. Review data volume growth trends

**Common Error Messages:**

| Error                              | Cause                 | Solution                                                                  |
| ---------------------------------- | --------------------- | ------------------------------------------------------------------------- |
| `Pipeline not found (404)`         | Invalid pipeline ID   | Verify pipeline exists: `databasin pipelines get pipeline-daily-sync-001` |
| `Connection test failed`           | Connector issue       | Test connectors: `databasin connectors test conn-mysql-001`               |
| `SQL query timeout`                | Long-running query    | Increase `jobTimeout` or optimize query                                   |
| `Validation failed: FAIL`          | Data quality issue    | Check validation query and data freshness                                 |
| `Automation already running (409)` | Overlapping execution | Wait for completion or adjust schedule                                    |
| `Permission denied (403)`          | Insufficient access   | Check user has project access                                             |

**Reference Documentation:**

For detailed troubleshooting of specific components:

- **Connector issues**: See `databasin-connectors` skill troubleshooting guide
- **Pipeline issues**: See `databasin-pipelines` skill troubleshooting guide
- **Automation issues**: See "Troubleshooting Failed Automation" workflow in this document (Workflow D)
- **Complete workflow**: See `CROSS-SKILL-WORKFLOW-EXAMPLE.md` for full end-to-end setup

## When to Use Other Skills

**Use `databasin-api` skill when:**

- Need API endpoint details
- Understanding token efficiency
- Troubleshooting API errors
- Learning about automation API structure

**Use `databasin-connectors` skill when:**

- Setting up connections for SQL tasks
- Troubleshooting connection issues
- Managing connector credentials
- Understanding connection IDs

**Use `databasin-pipelines` skill when:**

- Creating pipelines to use in automations
- Managing pipeline artifacts
- Understanding pipeline dependencies
- Troubleshooting pipeline execution

## Common Error Messages and Solutions

### Authentication Errors

**Error:** `401 Unauthorized`

**Solution:**

```bash
databasin login
```

### Not Found Errors

**Error:** `Automation not found (404)`

**Solution:**

```bash
# List available automations
databasin automations list -p proj-001

# Verify automation ID
databasin automations get <correct_id>
```

### Permission Errors

**Error:** `Access denied (403)`

**Solution:**

- Verify you have permission to access the project
- Check with project administrator
- Ensure you're logged in with correct user

### Conflict Errors

**Error:** `Automation is already running (409)`

**Solution:**

```bash
# Wait for current execution to complete, or
databasin automations stop <id>
```

### Validation Errors

**Error:** `Invalid automation configuration`

**Solution:**

- Check required fields are present
- Validate cron expression format
- Verify task configurations
- Ensure connection IDs exist

## Summary

This skill enables complete automation lifecycle management through natural language using the Databasin CLI:

1. **Create** - Interactive wizard or file-based creation with validation
2. **Update** - Modify schedules, settings, and configurations
3. **Run** - Execute automations manually for testing
4. **Stop** - Stop running executions with safety checks
5. **Delete** - Remove automations with confirmation
6. **List** - View and filter automations with multiple formats
7. **Monitor** - Check status, logs, and execution history
8. **Troubleshoot** - Diagnose and fix execution issues

### Key Principles

Always:

- Filter by project for token efficiency
- Use interactive mode for simple operations
- Test automations after changes
- Provide clear error messages
- Reference CLI help when needed
- Prioritize reliability and monitoring
- Avoid schedule overlaps
- Set appropriate timeouts
- Use confirmation for destructive operations

### Output Format Strategy

- **Table format** - Default, best for human viewing
- **JSON format** - Best for scripting and integration
- **CSV format** - Best for spreadsheets and reports
- **Count mode** - Most token-efficient for large datasets

The goal is to make automation management simple, safe, and efficient through conversational interaction powered by the robust Databasin CLI.
