---
name: databasin-pipelines
description: Create, modify, and manage Databasin data pipelines through natural language conversation. Use when users want to create new pipelines, add/remove artifacts from existing pipelines, modify pipeline schedules or configurations, or get information about pipeline setup. Handles all connector types (RDBMS, file storage, cloud warehouses, APIs) with automatic validation and error correction before submission to the Databasin API.
---

# Databasin Pipelines Management

## Overview

Assist users in creating and managing Databasin data pipelines through natural language conversation. Guide users step-by-step, automatically fetch API information, validate configurations, and handle technical details seamlessly using the Databasin CLI.

## When to Use This Skill

Activate when users request:

- Creating new data pipelines
- Cloning existing pipelines (NEW) - duplicate pipelines with optional modifications
- Modifying existing pipeline schedules, cluster sizes, or configurations
- Adding or removing tables/files/artifacts from pipelines
- Getting information about connectors or pipeline requirements
- Understanding pipeline configurations
- Listing or viewing pipeline details

## Core Workflow

### 1. Pipeline Creation

**Step A: Gather Requirements Conversationally**

Ask the user for:

- Pipeline name (max 27 chars)
- Source connector type (MySQL, S3, Snowflake, etc.)
- Target connector type
- What data to ingest (tables, files, patterns)
- Schedule preference (e.g., "daily at 2 AM", "every 6 hours")
- Email for notifications

**Step B: Fetch Available Connectors**

Use the CLI to list connectors for the project:

```bash
# Get count of connectors (token-efficient)
databasin connectors list -p <project_id>

# Get full connector list with specific fields (when needed)
databasin connectors list -p <project_id> --full --fields "connectorID,connectorName,connectorType,isActive" --json

# Get details for a specific connector
databasin connectors get <connector_id> --json
```

**Key Points:**

- Default `list` command returns count only (token-efficient)
- Use `--full` flag to get actual connector objects
- Use `--fields` to limit response size to only needed fields
- Use `--json` for programmatic parsing
- Filter to active connectors by checking `isActive` field

**Step C: Determine Connector-Specific Data Needs**

Consult `references/pipeline-automation.md` for connector-specific screen flows:

- **RDBMS (MySQL, PostgreSQL, SQL Server)**: Need catalog → schema → tables → columns
- **File Storage (S3, Azure Blob)**: Need file patterns and format details
- **Cloud Warehouse (Snowflake, Databricks)**: Need database → schema → tables → columns

Use CLI commands to fetch metadata:

```bash
# Get catalogs for a connector
databasin connectors get <connector_id> --json | jq '.catalogs'

# Get schemas for a connector
databasin connectors get <connector_id> --json | jq '.schemas'

# Note: Specific metadata endpoints may vary - check API documentation
```

**Step D: Build Configuration**

Use templates from `assets/`:

- Start with `pipeline-template.json`
- Add items using `artifact-templates.json` (choose appropriate template type)
- Fill in all user-provided and API-fetched values

**Step E: Create Pipeline**

Use the CLI create command:

```bash
# Create from configuration file
databasin pipelines create pipeline-config.json -p <project_id>

# Create interactively (simplified, for basic pipelines)
databasin pipelines create -p <project_id>

# Get JSON response for programmatic handling
databasin pipelines create pipeline-config.json -p <project_id> --json
```

**Validation Notes:**

- CLI automatically validates configuration before submission
- Shows clear error messages with field names and types
- Provides suggestions for fixing common issues
- No need for separate validation step

**Step F: Confirm Success**

The CLI will display:

- Pipeline ID
- Pipeline name and status
- Source and target connectors
- Next steps (e.g., "Run with: databasin pipelines run <id>")

---

### 1B. Pipeline Cloning (NEW - Alternative to Creating from Scratch)

**When to Clone Instead of Create:**

- Promoting pipelines between environments (dev → staging → prod)
- Creating test versions with different connectors
- Generating schedule variations (hourly vs daily)
- Backing up before major modifications

**Step A: Identify Pipeline to Clone**

```bash
# List pipelines to find the one to clone
databasin pipelines list --project <project_id>

# Get details of the pipeline to clone
databasin pipelines get <pipeline_id> --json
```

**Step B: Preview Clone (Optional but Recommended)**

```bash
# Dry-run to preview changes without creating
databasin pipelines clone <pipeline_id> --dry-run

# With modifications
databasin pipelines clone <pipeline_id> \
  --name "Dev Pipeline" \
  --source <new-source-id> \
  --target <new-target-id> \
  --schedule "0 */6 * * *" \
  --dry-run
```

**Step C: Clone Pipeline**

```bash
# Clone with default name (adds " (Clone)" suffix)
databasin pipelines clone <pipeline_id>

# Clone with customizations
databasin pipelines clone <pipeline_id> \
  --name "Production ETL" \
  --source <prod-source-connector-id> \
  --target <prod-target-connector-id> \
  --schedule "0 2 * * *"
```

**Available Clone Options:**

- `--name <name>` - Override pipeline name (default: original + " (Clone)")
- `--source <id>` - Override source connector ID
- `--target <id>` - Override target connector ID
- `--schedule <cron>` - Override schedule (cron expression)
- `--dry-run` - Preview changes without creating

**Features:**

1. **Smart Name Generation** - Automatically adds " (Clone)" if name not specified
2. **Configuration Validation** - Validates connectors exist and schedule is valid
3. **Connector Caching** - Efficient API usage when fetching connector details
4. **Clear Diff Display** - Shows exactly what changed from original
5. **Preserves Everything** - Artifacts, job details, all pipeline settings copied
6. **Dry-Run Mode** - Preview before committing

**Example Output:**

```
$ databasin pipelines clone 8901 --name "Production ETL" --dry-run

✔ Source pipeline loaded: Daily User Sync (8901)
✔ Configuration valid

Changes:
  ~ Name: "Daily User Sync" → "Production ETL"
  ✓ Source: StarlingPostgres (5459) [unchanged]
  ✓ Target: ITL TPI Databricks (5765) [unchanged]
  ✓ Schedule: "0 2 * * *" [unchanged]
  ✓ Artifacts: 2 items [unchanged]

Preview: Pipeline would be cloned as follows

Original:
  Name: Daily User Sync
  Source: StarlingPostgres (5459)
  Target: ITL TPI Databricks (5765)
  Schedule: 0 2 * * *
  Artifacts: 2 items

Cloned:
  Name: Production ETL
  Source: StarlingPostgres (5459)
  Target: ITL TPI Databricks (5765)
  Schedule: 0 2 * * *
  Artifacts: 2 items

✓ Dry run successful
Use --confirm (or remove --dry-run) to create this pipeline
```

**Success Output (After Clone):**

```
✔ Pipeline created: 8905

Next steps:
  $ databasin pipelines run 8905    # Test the cloned pipeline
  $ databasin pipelines logs 8905   # View execution logs
```

**Error Handling:**

```bash
# Pipeline not found
$ databasin pipelines clone 99999
✖ Failed to clone pipeline
Error: Pipeline not found

# Invalid connector ID
$ databasin pipelines clone 8901 --source 99999
✖ Configuration validation failed
Errors:
  ✖ sourceConnectorId: Connector 99999 not found or not accessible

# Invalid cron expression
$ databasin pipelines clone 8901 --schedule "invalid"
✖ Configuration validation failed
Errors:
  ✖ schedule: Invalid cron expression: "invalid"
  Expected format: "minute hour day month dayOfWeek" (e.g., "0 2 * * *")
```

**Use Cases:**

1. **Environment Promotion** - Clone from dev to prod with different connectors
2. **Testing** - Clone production pipeline for testing with test connectors
3. **Schedule Variations** - Create hourly version of daily pipeline
4. **Backup/Template** - Clone before major modifications

---

### 2. Pipeline Modification

#### Simple Updates (Interactive)

```bash
# Interactive update (prompts for changes)
databasin pipelines update <pipeline_id>

# Update from configuration file
databasin pipelines update <pipeline_id> update-config.json

# Get JSON response
databasin pipelines update <pipeline_id> update-config.json --json
```

**What can be updated interactively:**

- Pipeline name
- Enabled/disabled status
- Schedule (cron format)
- Configuration settings

**For complex changes:**

1. Fetch current config: `databasin pipelines get <id> --json > current.json`
2. Modify the JSON file as needed
3. Validate by attempting update: `databasin pipelines update <id> modified.json`
4. CLI handles validation and provides feedback

#### View Pipeline Details

```bash
# Get full pipeline details
databasin pipelines get <pipeline_id> --json

# Get specific fields only
databasin pipelines get <pipeline_id> --fields "pipelineName,status,schedule,clusterSize"

# Interactive selection (if ID not provided)
databasin pipelines get
```

### 3. Artifact Management

#### Add Artifacts to Pipeline

```bash
# Add artifact from configuration file
databasin pipelines artifacts add <pipeline_id> artifact-config.json

# Add artifact interactively
databasin pipelines artifacts add <pipeline_id>
```

**Interactive artifact creation supports:**

- **Tables**: table name, schema, mode (append/overwrite/upsert)
- **Files**: file path, format (CSV/JSON/Parquet/Excel)
- **API Endpoints**: endpoint URL, HTTP method

**Artifact configuration file format:**

```json
{
	"type": "table",
	"config": {
		"tableName": "customers",
		"schema": "public",
		"mode": "upsert"
	}
}
```

**For file-based artifacts:**

```json
{
	"type": "file",
	"config": {
		"fileName": "sales_data.csv",
		"fileFormat": "csv",
		"delimiter": ",",
		"containsHeader": true
	}
}
```

**Note on adding multiple artifacts:**
The `artifacts add` command accepts ONE artifact at a time. To add multiple artifacts to a pipeline, run the command multiple times:

```bash
# Add first artifact
databasin pipelines artifacts add <pipeline_id> orders-artifact.json

# Add second artifact
databasin pipelines artifacts add <pipeline_id> customers-artifact.json

# Or use interactive mode multiple times
databasin pipelines artifacts add <pipeline_id>
# ... follow prompts for first artifact ...

databasin pipelines artifacts add <pipeline_id>
# ... follow prompts for second artifact ...
```

#### Remove Artifacts

```bash
# Remove with confirmation prompt
databasin pipelines artifacts remove <pipeline_id> <artifact_id>

# Remove without confirmation
databasin pipelines artifacts remove <pipeline_id> <artifact_id> --yes

# Interactive selection of artifact (if ID not provided)
databasin pipelines artifacts remove <pipeline_id>
```

**Key Features:**

- Shows artifact details before removal
- Lists all artifacts if ID not provided
- Confirmation prompt prevents accidents
- `--yes` flag for automation/scripting

### 4. Pipeline Operations

#### List Pipelines

```bash
# List all pipelines in a project
databasin pipelines list -p <project_id>

# Get count only
databasin pipelines list -p <project_id> --count

# Filter by status
databasin pipelines list -p <project_id> --status active

# Limit results
databasin pipelines list -p <project_id> --limit 20

# Get specific fields
databasin pipelines list -p <project_id> --fields "pipelineID,pipelineName,status"

# JSON output
databasin pipelines list -p <project_id> --json
```

#### Run Pipeline

```bash
# Run immediately
databasin pipelines run <pipeline_id>

# Wait for completion (when implemented)
databasin pipelines run <pipeline_id> --wait

# Interactive selection
databasin pipelines run
```

#### Delete Pipeline

```bash
# Delete with confirmation
databasin pipelines delete <pipeline_id>

# Delete without confirmation
databasin pipelines delete <pipeline_id> --yes
```

**Safety features:**

- Shows pipeline details before deletion
- Warns if pipeline is currently running
- Confirms action is irreversible
- Lists artifact count

## Integration Workflows

### End-to-End: MySQL to Snowflake Daily Sync

This workflow demonstrates how the pipelines skill integrates with the connectors and automations skills to create a complete ETL solution. This example shows **Parts 3-5** of the full workflow (pipeline creation and testing). For the complete workflow including connector setup and automation, see `CROSS-SKILL-WORKFLOW-EXAMPLE.md`.

**Full Workflow Context:**

1. **Part 1-2** (Connectors skill): Create MySQL source and Snowflake target connectors
2. **Part 3-5** (Pipelines skill - THIS SECTION): Create pipeline with artifacts and test
3. **Part 6-7** (Automations skill): Schedule daily automated runs with monitoring

---

#### Prerequisites

Before creating the pipeline, you need connector IDs from the connectors skill:

```bash
# These connectors should already be created via the connectors skill
# conn-mysql-001: MySQL source connector (mysql-orders-source)
# conn-snow-002: Snowflake target connector (snowflake-warehouse)

# Verify connectors exist and are active
databasin connectors get conn-mysql-001
databasin connectors get conn-snow-002
databasin connectors test conn-mysql-001
databasin connectors test conn-snow-002
```

**If connectors don't exist yet,** use the `databasin-connectors` skill to create them first. See `CROSS-SKILL-WORKFLOW-EXAMPLE.md` Parts 1-2 for detailed connector setup.

---

#### Part 3.1: Create Pipeline Configuration

Create file: `data-pipeline.json`

```json
{
	"name": "Daily Orders Sync",
	"description": "Sync orders from MySQL to Snowflake with transformation",
	"projectId": "YOUR_PROJECT_ID",
	"sourceConnectorId": "conn-mysql-001",
	"targetConnectorId": "conn-snow-002",
	"schedule": null,
	"configuration": {
		"syncMode": "incremental",
		"incrementalColumn": "updated_at",
		"batchSize": 5000,
		"parallelism": 4,
		"errorHandling": "skip_and_log",
		"maxErrors": 100,
		"enableTransformations": true,
		"conflictResolution": "target_wins"
	},
	"tags": ["daily", "orders", "incremental", "production"]
}
```

**Key Configuration Options:**

- `syncMode`: "incremental" (only syncs changed data using `incrementalColumn`)
- `incrementalColumn`: "updated_at" (must be indexed timestamp column in source)
- `batchSize`: 5000 rows per batch (tune based on row size)
- `errorHandling`: "skip_and_log" (continues processing, logs errors)

---

#### Part 3.2: Create the Pipeline

```bash
databasin pipelines create data-pipeline.json
```

**Expected Output:**

```
✓ Pipeline created successfully
ID: pipeline-daily-sync-001
Name: Daily Orders Sync
Source: mysql-orders-source (conn-mysql-001)
Target: snowflake-warehouse (conn-snow-002)
Status: Draft (no artifacts configured)
Created: 2025-11-23 10:35:22

Next steps:
  1. Add source artifact: databasin pipelines artifacts add pipeline-daily-sync-001 source-artifact.json
  2. Add target artifact: databasin pipelines artifacts add pipeline-daily-sync-001 target-artifact.json
  3. Test pipeline: databasin pipelines run pipeline-daily-sync-001
```

**Important:** Save the pipeline ID `pipeline-daily-sync-001` - you'll need it for artifacts and automation.

---

#### Part 4.1: Create Source Artifact Configuration

Create file: `orders-source-artifact.json`

```json
{
	"artifactType": "table",
	"name": "orders",
	"description": "Orders table from production MySQL",
	"configuration": {
		"tableName": "orders",
		"schema": "ecommerce_prod",
		"columns": [
			{
				"name": "order_id",
				"dataType": "BIGINT",
				"nullable": false,
				"primaryKey": true,
				"description": "Unique order identifier"
			},
			{
				"name": "customer_id",
				"dataType": "BIGINT",
				"nullable": false,
				"indexed": true
			},
			{
				"name": "order_date",
				"dataType": "TIMESTAMP",
				"nullable": false,
				"indexed": true
			},
			{
				"name": "total_amount",
				"dataType": "DECIMAL(10,2)",
				"nullable": false
			},
			{
				"name": "status",
				"dataType": "VARCHAR(50)",
				"nullable": false
			},
			{
				"name": "updated_at",
				"dataType": "TIMESTAMP",
				"nullable": false,
				"indexed": true,
				"description": "Used for incremental sync"
			}
		],
		"filterCondition": "status != 'DELETED'",
		"incrementalColumn": "updated_at"
	}
}
```

**Important Source Fields:**

- `tableName`: Exact table name in source database
- `schema`: Source schema/database name
- `filterCondition`: Optional WHERE clause (e.g., exclude soft-deleted records)
- `incrementalColumn`: Must match pipeline configuration for incremental sync

---

#### Part 4.2: Add Source Artifact to Pipeline

```bash
databasin pipelines artifacts add pipeline-daily-sync-001 orders-source-artifact.json
```

**Expected Output:**

```
✓ Source artifact added successfully
Artifact ID: artifact-source-001
Table: ecommerce_prod.orders
Columns: 6 detected
Primary Key: order_id
Incremental Column: updated_at
Estimated Rows: 145,832

Pipeline Status: Ready for target artifact
```

---

#### Part 4.3: Create Target Artifact Configuration

Create file: `orders-target-artifact.json`

```json
{
	"artifactType": "table",
	"name": "orders",
	"description": "Orders table in Snowflake analytics warehouse",
	"configuration": {
		"tableName": "ORDERS",
		"schema": "ORDERS",
		"database": "ANALYTICS_DB",
		"createIfNotExists": true,
		"dropAndRecreate": false,
		"columns": [
			{
				"name": "ORDER_ID",
				"dataType": "NUMBER(19,0)",
				"nullable": false,
				"primaryKey": true
			},
			{
				"name": "CUSTOMER_ID",
				"dataType": "NUMBER(19,0)",
				"nullable": false
			},
			{
				"name": "ORDER_DATE",
				"dataType": "TIMESTAMP_NTZ",
				"nullable": false
			},
			{
				"name": "TOTAL_AMOUNT",
				"dataType": "NUMBER(10,2)",
				"nullable": false
			},
			{
				"name": "STATUS",
				"dataType": "VARCHAR(50)",
				"nullable": false
			},
			{
				"name": "UPDATED_AT",
				"dataType": "TIMESTAMP_NTZ",
				"nullable": false
			},
			{
				"name": "SYNCED_AT",
				"dataType": "TIMESTAMP_NTZ",
				"nullable": false,
				"defaultValue": "CURRENT_TIMESTAMP()",
				"description": "Timestamp when row was synced to Snowflake"
			}
		],
		"columnMappings": [
			{
				"source": "order_id",
				"target": "ORDER_ID",
				"transformation": null
			},
			{
				"source": "customer_id",
				"target": "CUSTOMER_ID",
				"transformation": null
			},
			{
				"source": "order_date",
				"target": "ORDER_DATE",
				"transformation": "CONVERT_TZ('UTC')"
			},
			{
				"source": "total_amount",
				"target": "TOTAL_AMOUNT",
				"transformation": null
			},
			{
				"source": "status",
				"target": "STATUS",
				"transformation": "UPPER(${status})"
			},
			{
				"source": "updated_at",
				"target": "UPDATED_AT",
				"transformation": "CONVERT_TZ('UTC')"
			},
			{
				"source": null,
				"target": "SYNCED_AT",
				"transformation": "CURRENT_TIMESTAMP()"
			}
		],
		"preLoadSQL": [
			"ALTER SESSION SET TIMEZONE = 'UTC'",
			"ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF3'"
		],
		"postLoadSQL": [
			"ANALYZE TABLE ANALYTICS_DB.ORDERS.ORDERS",
			"UPDATE ANALYTICS_DB.ORDERS.SYNC_METADATA SET last_sync = CURRENT_TIMESTAMP() WHERE pipeline_id = 'pipeline-daily-sync-001'"
		]
	}
}
```

**Important Target Fields:**

- `createIfNotExists`: Auto-create table on first run
- `columnMappings`: Maps source columns to target columns with optional transformations
- `transformation`: SQL expressions for data conversion
  - `CONVERT_TZ('UTC')`: Convert timestamps to UTC timezone
  - `UPPER(${status})`: Uppercase transformation
  - `CURRENT_TIMESTAMP()`: Generated column (no source mapping)
- `preLoadSQL`: SQL statements executed before data load (session configuration)
- `postLoadSQL`: SQL statements executed after successful load (metadata updates)

---

#### Part 4.4: Add Target Artifact to Pipeline

```bash
databasin pipelines artifacts add pipeline-daily-sync-001 orders-target-artifact.json
```

**Expected Output:**

```
✓ Target artifact added successfully
Artifact ID: artifact-target-001
Table: ANALYTICS_DB.ORDERS.ORDERS
Column Mappings: 7 configured
Transformations: 3 detected
Pre-load SQL: 2 statements
Post-load SQL: 2 statements

Pipeline Status: Ready to run
Validation: PASSED
  ✓ All source columns mapped
  ✓ Data type compatibility verified
  ✓ Primary key constraints compatible
  ✓ Transformations syntax valid
```

---

#### Part 5: Test Pipeline Execution

Before scheduling with automation, test the pipeline manually:

```bash
databasin pipelines run pipeline-daily-sync-001 --wait
```

**Expected Output (~2-5 minutes depending on data volume):**

```
Starting pipeline: Daily Orders Sync (pipeline-daily-sync-001)
Mode: Incremental (using updated_at column)

[10:40:15] Initializing pipeline...
[10:40:16] ✓ Validated source connector (conn-mysql-001)
[10:40:17] ✓ Validated target connector (conn-snow-002)
[10:40:18] ✓ Executing pre-load SQL (2 statements)
[10:40:19] Detecting incremental changes...
[10:40:21] Found 2,847 new/updated rows since last sync

[10:40:22] Extracting data from MySQL...
[10:40:24] ✓ Batch 1/1: 2,847 rows extracted
[10:40:25] Applying transformations...
[10:40:26] ✓ Converted 2,847 timestamps to UTC
[10:40:26] ✓ Applied 2,847 status uppercasing
[10:40:27] Loading data to Snowflake...
[10:40:35] ✓ Batch 1/1: 2,847 rows loaded

[10:40:36] ✓ Executing post-load SQL (2 statements)
[10:40:37] Pipeline completed successfully

Summary:
  Duration: 2m 22s
  Rows Processed: 2,847
  Rows Succeeded: 2,847
  Rows Failed: 0
  Throughput: 20 rows/sec
  Data Volume: 1.2 MB

Execution ID: exec-20251123-104015
View logs: databasin pipelines logs pipeline-daily-sync-001 exec-20251123-104015
```

**Performance Notes:**

- First run (full sync): ~8-12 minutes for 145,832 rows
- Incremental runs: Typically <3 minutes
- Throughput varies with row size and network speed

---

#### Verify Pipeline Results

Run this SQL query in Snowflake to verify data was loaded correctly:

```sql
SELECT
    COUNT(*) as total_rows,
    MAX(SYNCED_AT) as last_sync,
    MAX(ORDER_DATE) as latest_order,
    COUNT(DISTINCT STATUS) as status_count
FROM ANALYTICS_DB.ORDERS.ORDERS;
```

**Expected Result:**

```
TOTAL_ROWS  LAST_SYNC             LATEST_ORDER         STATUS_COUNT
---------   -------------------   ------------------   ------------
2,847       2025-11-23 10:40:37   2025-11-23 08:15:42  5
```

---

#### Next Steps: Automation

The pipeline is now configured and tested. To schedule automatic daily runs:

**Use the `databasin-automations` skill** to create a scheduled automation that:

- Runs this pipeline daily at 2:00 AM
- Validates data quality after sync
- Updates sync metadata
- Sends notifications on success/failure

```bash
# Preview of automation creation (handled by automations skill)
databasin automations create daily-sync-automation.json
```

See `CROSS-SKILL-WORKFLOW-EXAMPLE.md` Parts 6-7 for complete automation setup, or invoke the `databasin-automations` skill.

**Automation will handle:**

- Scheduled execution (e.g., daily at 2 AM)
- Multi-task workflows (pipeline → validation → notification)
- Retry logic on failures
- Success/failure notifications
- Execution history and monitoring

---

#### Troubleshooting

**No rows detected in incremental sync:**

```bash
# Reset incremental state to force full sync
databasin pipelines reset-state pipeline-daily-sync-001
```

**Transformation errors:**

```bash
# View detailed error logs
databasin pipelines logs pipeline-daily-sync-001 --level error
```

**Connection failures during run:**

```bash
# Re-test connectors
databasin connectors test conn-mysql-001 --verbose
databasin connectors test conn-snow-002 --verbose
```

---

## CLI Command Reference

### Pipeline Commands

| Command   | Description                              | Example                                                          |
| --------- | ---------------------------------------- | ---------------------------------------------------------------- |
| `list`    | List pipelines in project                | `databasin pipelines list -p myproject`                          |
| `get`     | Get pipeline details                     | `databasin pipelines get 123`                                    |
| `create`  | Create new pipeline                      | `databasin pipelines create config.json -p myproject`            |
| `clone`   | Clone existing pipeline (NEW)            | `databasin pipelines clone 123 --name "New Name"`                |
| `update`  | Update pipeline                          | `databasin pipelines update 123 update.json`                     |
| `delete`  | Delete pipeline                          | `databasin pipelines delete 123`                                 |
| `run`     | Execute pipeline                         | `databasin pipelines run 123`                                    |
| `logs`    | View execution logs                      | `databasin pipelines logs 123`                                   |
| `history` | View execution history (NEW)             | `databasin pipelines history 123 --limit 10`                     |

### Artifact Commands

| Command            | Description              | Example                                               |
| ------------------ | ------------------------ | ----------------------------------------------------- |
| `artifacts add`    | Add artifact to pipeline | `databasin pipelines artifacts add 123 artifact.json` |
| `artifacts remove` | Remove artifact          | `databasin pipelines artifacts remove 123 456`        |

### Connector Commands

| Command       | Description                        | Example                                                |
| ------------- | ---------------------------------- | ------------------------------------------------------ |
| `list`        | List connectors (count by default) | `databasin connectors list -p myproject`               |
| `list --full` | List full connector objects        | `databasin connectors list -p myproject --full`        |
| `get`         | Get connector details              | `databasin connectors get 123`                         |
| `create`      | Create connector                   | `databasin connectors create config.json -p myproject` |
| `update`      | Update connector                   | `databasin connectors update 123 update.json`          |
| `delete`      | Delete connector                   | `databasin connectors delete 123`                      |
| `test`        | Test connection                    | `databasin connectors test 123`                        |

### Global Options

All commands support:

- `--json`: Output in JSON format
- `--csv`: Output in CSV format
- `--help`: Show command help
- `-p, --project <id>`: Specify project ID

## Output Formats

The CLI supports three output formats:

### Table Format (Default)

```
┌─────────┬──────────────┬────────┬─────────┐
│ ID      │ Name         │ Status │ Enabled │
├─────────┼──────────────┼────────┼─────────┤
│ 123     │ My Pipeline  │ active │ true    │
│ 124     │ Test Pipeline│ paused │ false   │
└─────────┴──────────────┴────────┴─────────┘
```

### JSON Format

```bash
databasin pipelines list -p myproject --json
```

```json
{
	"data": [
		{
			"pipelineID": 123,
			"pipelineName": "My Pipeline",
			"status": "active",
			"enabled": true
		}
	]
}
```

### CSV Format

```bash
databasin pipelines list -p myproject --csv
```

```csv
pipelineID,pipelineName,status,enabled
123,My Pipeline,active,true
124,Test Pipeline,paused,false
```

## Token Efficiency Features

The CLI is designed for optimal token usage in LLM interactions:

### 1. Count Mode (Default for Connectors)

```bash
# Returns only count (saves ~200K tokens vs full response)
databasin connectors list -p myproject
# Output: "Total connectors: 42"
```

### 2. Field Filtering

```bash
# Get only needed fields
databasin pipelines list -p myproject --fields "pipelineID,pipelineName,status"
```

### 3. Result Limiting

```bash
# Limit results to reduce response size
databasin pipelines list -p myproject --limit 10
```

### 4. Warnings for Large Responses

The CLI automatically warns when responses exceed token thresholds and suggests optimizations.

## Using Bundled Resources

### References Directory

- **pipeline-automation.md**: Complete guide to pipeline creation process, screen flows, and API endpoints
- **api-endpoints.md**: Quick API endpoint reference
- **examples.md**: Real-world pipeline configuration examples for different scenarios

### Assets Directory

- **pipeline-template.json**: Base template for all pipelines
- **artifact-templates.json**: Templates for different artifact types (database tables, CSV files, JSON files, etc.)

## Configuration Defaults

When user doesn't specify, use these sensible defaults:

- **Cluster size**: M (medium)
- **Timezone**: UTC
- **Timeout**: 43200 seconds (12 hours)
- **Ingestion pattern**: "data warehouse" for RDBMS, "datalake" for Databricks/Snowflake
- **Source naming**: true
- **Create catalogs**: false for data warehouse, true for datalake

## Best Practices

### 1. Be Conversational

Don't overwhelm with technical questions. Gather info naturally:

- "What data do you want to sync?"
- "How often should this run?"
- "I'll set the cluster to Medium and schedule it for daily at 2 AM UTC. Sound good?"

### 2. Use Token-Efficient Commands

```bash
# Good - get count first
databasin connectors list -p myproject
# Output: 42 connectors

# Then get details only if needed
databasin connectors list -p myproject --full --fields "connectorID,connectorName" --limit 10
```

```bash
# Avoid - fetching all connectors with full objects
databasin connectors list -p myproject --full --json
# Could return 200K+ tokens
```

### 3. Handle Errors Gracefully

The CLI provides detailed error messages:

```
❌ Error: Pipeline not found (404)
  Pipeline ID: 999
  Suggestion: Run 'databasin pipelines list --project myproject' to see available pipelines
```

Use these suggestions to guide the user.

### 4. Leverage Interactive Mode

When user is unsure:

```bash
# Let them select interactively
databasin pipelines get
databasin pipelines artifacts add <pipeline_id>
databasin connectors test
```

### 5. Show Next Steps

After creating a pipeline:

```
✓ Pipeline created: Sales Data Sync
  ID: 123
  Status: active

Next steps:
- Run now: databasin pipelines run 123
- Add more artifacts: databasin pipelines artifacts add 123
- View details: databasin pipelines get 123
```

## Common Patterns

### Database Delta Sync

```json
{
	"ingestionType": "delta",
	"watermarkColumnName": ["updated_at"],
	"mergeColumns": ["id"],
	"detectDeletes": true
}
```

### CSV File Ingestion

```json
{
	"sourceFileName": "data/*.csv",
	"sourceFileFormat": "csv",
	"sourceFileDelimiter": ",",
	"containsHeader": true,
	"columnHeaderLineNumber": 1
}
```

### JSON with Nested Structures

```json
{
	"sourceFileFormat": "json",
	"autoExplode": true
}
```

For detailed examples, see `references/examples.md`.

## Workflow Examples

### Example 1: Create Pipeline for MySQL to Snowflake

```bash
# 1. Check available connectors
databasin connectors list -p myproject
# Output: "Total connectors: 12"

# 2. Get MySQL connectors
databasin connectors list -p myproject --full --fields "connectorID,connectorName,connectorType" --json | jq '.data[] | select(.connectorType=="MySQL")'

# 3. Get Snowflake connectors
databasin connectors list -p myproject --full --fields "connectorID,connectorName,connectorType" --json | jq '.data[] | select(.connectorType=="Snowflake")'

# 4. Create pipeline from prepared config
databasin pipelines create mysql-to-snowflake.json -p myproject

# 5. Run the pipeline
databasin pipelines run <new_pipeline_id>
```

### Example 2: Add Tables to Existing Pipeline

```bash
# 1. Get pipeline details
databasin pipelines get 123

# 2. Prepare artifact configs (or use interactive mode)
databasin pipelines artifacts add 123

# Interactive prompts:
# - Select artifact type: Table
# - Enter table name: orders
# - Enter schema name: sales
# - Select mode: append

# 3. Verify artifacts were added
databasin pipelines get 123 --fields "artifacts"
```

### Example 3: Update Pipeline Schedule

```bash
# 1. View current configuration
databasin pipelines get 123

# 2. Update interactively
databasin pipelines update 123

# Prompts:
# - Update pipeline name? No
# - Update enabled status? No
# - Update schedule? Yes
# - Enter schedule (cron format): 0 2 * * *
# - Apply these updates? Yes
```

### Example 4: Batch Pipeline Creation

```bash
# Create multiple pipelines from config files
for config in configs/pipeline-*.json; do
  echo "Creating pipeline from $config"
  databasin pipelines create "$config" -p myproject --json
done
```

## Error Handling

### Common Errors and Solutions

**Pipeline Not Found (404)**

```bash
databasin pipelines get 999
# Error: Pipeline not found (404)
# Suggestion: Run 'databasin pipelines list --project myproject'
```

**Invalid Configuration (400)**

```bash
databasin pipelines create bad-config.json -p myproject
# Error: Invalid pipeline configuration (400)
# Details: Missing required field: pipelineName
```

**Access Denied (403)**

```bash
databasin pipelines delete 123
# Error: Access denied (403)
# Suggestion: You don't have permission to delete this pipeline
```

**Token Issues**

```bash
databasin pipelines list -p myproject
# Error: Authentication failed
# Suggestion: Run 'databasin login' to refresh credentials
```

## Quick Reference

**Create Pipeline:**

1. Gather requirements conversationally
2. Fetch connectors: `databasin connectors list -p <project> --full`
3. Get connector-specific data (catalogs, schemas, tables)
4. Build config from templates (`assets/`)
5. Create: `databasin pipelines create config.json -p <project>`
6. Confirm success and provide next steps

**Modify Pipeline:**

- Simple changes: `databasin pipelines update <id>`
- Complex changes: Fetch with `get`, modify, update with `update`

**Manage Artifacts:**

- Add: `databasin pipelines artifacts add <id> [config.json]`
- Remove: `databasin pipelines artifacts remove <id> [artifact_id]`
- Both support interactive mode if file/ID not provided

**Token Efficiency:**

- Use count mode for connectors (default)
- Use `--fields` to limit response size
- Use `--limit` to cap results
- Use JSON format for programmatic parsing

## Migration Notes

This skill has been migrated from custom TypeScript scripts to the Databasin CLI.

**Key Changes:**

- No more manual `.token` file management
- Built-in authentication via `databasin login`
- Token-efficient commands (count mode, field filtering)
- Interactive prompts for better UX
- Consistent error handling and messages
- Multiple output formats (table, JSON, CSV)

**See `PIPELINES-MIGRATION-MAPPING.md` for detailed script-to-CLI mapping.**
