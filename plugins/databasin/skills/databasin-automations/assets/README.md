# Databasin Automation Templates

This directory contains practical, real-world automation templates that users can copy and customize for their Databasin projects.

## Available Templates

### 1. simple-pipeline-automation.json

**Use Case:** Run a single pipeline on a daily schedule

**Features:**

- Daily execution at 2 AM
- Single pipeline task
- Simple cron expression
- Email notifications
- Small cluster size

**Customization:**

- Update `automationName` to describe your workflow
- Set `internalID` to your project ID
- Change `jobID` to your pipeline ID
- Adjust `jobRunSchedule` for your preferred time
- Update `emailNotifications` with your email addresses

**Example Usage:**

```bash
databasin automations create simple-pipeline-automation.json -p proj-001
```

---

### 2. sql-query-automation.json

**Use Case:** Execute SQL queries against a database on schedule

**Features:**

- Hourly execution
- Multiple SQL queries in sequence
- Database connector reference
- Transaction-safe operations

**Customization:**

- Update `sqlTargetConnectionID` to your database connector ID
- Modify `sqlQueryMap` array with your SQL queries
- Adjust `jobRunSchedule` for your frequency needs
- Set appropriate `jobTimeout` based on query complexity

**Example Usage:**

```bash
databasin automations create sql-query-automation.json -p proj-001
```

**Note:** Get your connector ID using:

```bash
databasin connectors list -p proj-001
```

---

### 3. notebook-automation.json

**Use Case:** Run Jupyter notebooks for weekly reporting

**Features:**

- Weekly execution (Sunday at midnight)
- Databricks notebook execution
- Audit tracking enabled
- Medium cluster for analytical workloads

**Customization:**

- Update `notebookPath` to your notebook location
- Change `jobRunSchedule` for different frequencies
- Adjust `jobClusterSize` based on notebook requirements
- Enable/disable `auditEnabled` as needed

**Example Usage:**

```bash
databasin automations create notebook-automation.json -p proj-001
```

---

### 4. multi-task-etl-automation.json

**Use Case:** Complex ETL workflow with multiple task types

**Features:**

- Pipeline extraction task
- SQL validation and transformation
- Notebook reporting
- Task sequencing via `automationOrderNumber`
- Full audit tracking

**Customization:**

- Update each task's configuration independently
- Add or remove tasks from `automationTask` array
- Maintain sequential `automationOrderNumber` values
- Adjust `jobTimeout` to accommodate all tasks

**Example Usage:**

```bash
databasin automations create multi-task-etl-automation.json -p proj-001
```

**Task Execution Order:**

1. Extract data via pipeline
2. Validate and transform with SQL
3. Generate quality report via notebook

---

### 5. file-drop-automation.json

**Use Case:** Triggered automation based on file arrival

**Features:**

- Event-triggered (not schedule-based)
- File monitoring in S3/ADLS
- File movement operations
- Automated processing workflow

**Customization:**

- Update `monitorPath` to your storage location
- Change `filePattern` to match your file types
- Modify file source/target connector IDs
- Update `sourcePath` and `targetPath` as needed

**Example Usage:**

```bash
databasin automations create file-drop-automation.json -p proj-001
```

**Important:** Set `jobRunSchedule` to empty string for trigger-based automations.

---

### 6. docker-automation.json

**Use Case:** Run Docker containers for ML training or custom jobs

**Features:**

- Docker container execution
- Environment variables configuration
- Resource limits (CPU, memory, GPU)
- Volume mounts for data access
- Multi-task workflow with logging

**Customization:**

- Update `dockerImage` to your container registry
- Modify `dockerCommand` for your execution needs
- Configure `dockerEnvironmentVariables` for your application
- Adjust `dockerResourceLimits` based on requirements
- Update `dockerVolumeMounts` for data access

**Example Usage:**

```bash
databasin automations create docker-automation.json -p proj-001
```

**Task Execution Order:**

1. Train ML model in Docker container
2. Log metrics to database
3. Generate performance report

---

## General Template Usage

### Step 1: Copy Template

```bash
cp simple-pipeline-automation.json my-automation.json
```

### Step 2: Customize Values

Edit `my-automation.json` and replace:

- `proj-001` with your project ID
- `pipeline-123` with your resource IDs
- `user@example.com` with your email
- Schedule expressions with your timing needs

### Step 3: Create Automation

```bash
databasin automations create my-automation.json -p your-project-id
```

### Step 4: Test Execution

```bash
databasin automations run <automation_id>
```

### Step 5: Activate

```bash
# Create activation file
echo '{"isActive": 1}' > activate.json

# Update automation
databasin automations update <automation_id> activate.json
```

---

## Common Cron Schedule Examples

| Description      | Cron Expression | When it Runs                |
| ---------------- | --------------- | --------------------------- |
| Every hour       | `0 * * * *`     | At minute 0 of every hour   |
| Every 6 hours    | `0 */6 * * *`   | At 12 AM, 6 AM, 12 PM, 6 PM |
| Daily at 2 AM    | `0 2 * * *`     | At 2:00 AM every day        |
| Weekdays at 9 AM | `0 9 * * 1-5`   | At 9:00 AM Monday-Friday    |
| Weekly on Sunday | `0 0 * * 0`     | At midnight every Sunday    |
| Monthly on 1st   | `0 0 1 * *`     | At midnight on the 1st      |
| Every 15 minutes | `*/15 * * * *`  | Every 15 minutes            |

**Cron Format:** `minute hour day month weekday`

---

## Task Types Reference

### Pipeline Task

```json
{
	"taskType": "pipeline",
	"taskName": "Run Pipeline",
	"jobID": "pipeline-123",
	"automationOrderNumber": 1,
	"isActive": true
}
```

### SQL Task

```json
{
	"taskType": "sql",
	"taskName": "Execute Queries",
	"sqlTargetConnectionID": 58,
	"sqlQueryMap": ["SELECT * FROM table"],
	"automationOrderNumber": 1,
	"isActive": true
}
```

### Notebook Task

```json
{
	"taskType": "notebook",
	"taskName": "Run Analysis",
	"notebookPath": "/path/to/notebook",
	"automationOrderNumber": 1,
	"isActive": true
}
```

### File Task

```json
{
	"taskType": "file",
	"taskName": "Move Files",
	"sourceFileId": "connector-123",
	"targetFileId": "connector-456",
	"sourcePath": "/source/",
	"targetPath": "/target/",
	"fileOperation": "move",
	"automationOrderNumber": 1,
	"isActive": true
}
```

### Docker Task

```json
{
	"taskType": "docker",
	"taskName": "Run Container",
	"dockerImage": "image:tag",
	"dockerCommand": "python script.py",
	"dockerEnvironmentVariables": { "KEY": "value" },
	"dockerResourceLimits": { "cpu": "2", "memory": "4Gi" },
	"automationOrderNumber": 1,
	"isActive": true
}
```

---

## Best Practices

### 1. Start Inactive

Always create automations with `"isActive": 0` and test before activating:

```bash
# Test manually first
databasin automations run <id>

# Activate after successful test
echo '{"isActive": 1}' > activate.json
databasin automations update <id> activate.json
```

### 2. Set Appropriate Timeouts

Match timeout to expected execution duration:

- Quick queries: 1,800 seconds (30 minutes)
- Medium ETL: 3,600 seconds (1 hour)
- Large jobs: 7,200-10,800 seconds (2-3 hours)
- Maximum: 18,000 seconds (5 hours)

### 3. Avoid Schedule Overlaps

Don't schedule faster than execution time:

```json
// BAD: 30-minute job scheduled every 15 minutes
"jobRunSchedule": "*/15 * * * *"

// GOOD: 30-minute job scheduled every hour
"jobRunSchedule": "0 * * * *"
```

### 4. Use Email Notifications

Get alerts for failures:

```json
"emailNotifications": ["team@example.com", "oncall@example.com"]
```

### 5. Enable Audit Tracking

For compliance and troubleshooting:

```json
"auditEnabled": 1,
"auditInformation": {
  "purpose": "Daily ETL workflow",
  "owner": "Data Team"
}
```

### 6. Order Tasks Logically

Use `automationOrderNumber` to sequence tasks:

```json
[
	{ "taskType": "pipeline", "automationOrderNumber": 1 },
	{ "taskType": "sql", "automationOrderNumber": 2 },
	{ "taskType": "notebook", "automationOrderNumber": 3 }
]
```

---

## Troubleshooting

### Validation Errors

**Error:** Missing required fields
**Solution:** Ensure `automationName`, `internalID`, and `jobRunSchedule` are present

### Schedule Not Triggering

**Error:** Automation created but not running
**Solution:** Verify `isActive` is set to 1 and cron expression is valid

### Task Failures

**Error:** Task execution failed
**Solution:** Check connection IDs, file paths, and permissions

### Timeout Errors

**Error:** Job exceeded timeout
**Solution:** Increase `jobTimeout` or optimize task performance

---

## Getting Help

### List Available Resources

```bash
# List projects
databasin projects list

# List connectors
databasin connectors list -p proj-001

# List pipelines
databasin pipelines list -p proj-001

# List automations
databasin automations list -p proj-001
```

### Check Automation Status

```bash
# Get automation details
databasin automations get <id>

# View execution history
databasin automations get <id> --json
```

### CLI Help

```bash
# General help
databasin automations --help

# Command-specific help
databasin automations create --help
```

---

## Template Compatibility

All templates are compatible with Databasin API version 2.1+ and tested with the databasin CLI.

**Required CLI Version:** 1.0.0+

**Check your version:**

```bash
databasin --version
```

---

## Contributing

Have a useful automation pattern? Share it with the team!

1. Create a new template file following the naming convention
2. Include descriptive `_comment` and `_description` fields
3. Use realistic placeholder values
4. Add documentation to this README
5. Test the template before sharing

---

## Support

For questions or issues:

- Review the automation skill documentation: `SKILL.md`
- Check the Databasin CLI documentation
- Contact the Databasin support team

---

Last Updated: 2024-11-23
