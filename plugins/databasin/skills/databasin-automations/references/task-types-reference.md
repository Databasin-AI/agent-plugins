# Databasin Automation Task Types Reference

Complete reference for all automation task types supported in Databasin automations.

## Overview

Databasin automations support **6 task types** that can be combined in sequence to create complex workflows. Each task type serves a specific purpose and has its own set of required and optional parameters.

### Available Task Types

| Task Type  | Primary Use Case                | Key Features                                |
| ---------- | ------------------------------- | ------------------------------------------- |
| `pipeline` | Execute Databasin pipelines     | Data ingestion, transformation, movement    |
| `sql`      | Run SQL queries                 | Data transformation, validation, cleanup    |
| `notebook` | Execute Databricks notebooks    | Complex analytics, custom Python/Scala code |
| `job`      | Trigger Databricks jobs         | Pre-configured Databricks job execution     |
| `file`     | Move/copy files between storage | File management, archival, distribution     |
| `docker`   | Run Docker containers           | Custom containerized workloads              |

### When to Use Each Task Type

**Pipeline Task** - Use when you need to:

- Ingest data from external sources
- Transform data using Databasin connectors
- Move data between storage systems
- Execute pre-configured Databasin pipelines

**SQL Query Task** - Use when you need to:

- Execute SQL statements against databases
- Transform data in place
- Validate data quality
- Clean up staging tables
- Run multiple sequential SQL operations

**Notebook Task** - Use when you need to:

- Run custom Python or Scala analytics
- Execute Databricks notebooks
- Perform machine learning operations
- Generate complex reports
- Use Spark for distributed processing

**Job Task** - Use when you need to:

- Execute pre-configured Databricks jobs
- Trigger existing job definitions
- Run jobs with specific parameters

**File Drop Task** - Use when you need to:

- Move files between storage locations
- Copy files from one connector to another
- Archive processed files
- Distribute files to multiple destinations

**Docker Task** - Use when you need to:

- Run containerized applications
- Execute custom tools not available in Databricks
- Run legacy applications
- Integrate third-party processing

---

## Pipeline Task Type

Execute a Databasin pipeline as part of an automation.

### Purpose

The pipeline task type allows you to trigger existing Databasin pipelines within an automation workflow. This is the most common task type for data movement and transformation operations.

### Required Fields

| Field                   | Type    | Description                    |
| ----------------------- | ------- | ------------------------------ |
| `taskType`              | String  | Must be `"pipeline"`           |
| `taskName`              | String  | Descriptive name for this task |
| `jobID`                 | String  | The pipeline ID to execute     |
| `automationOrderNumber` | Integer | Execution order (1-based)      |
| `isActive`              | Boolean | Whether this task is enabled   |

### Optional Fields

| Field                        | Type    | Default | Description                                                       |
| ---------------------------- | ------- | ------- | ----------------------------------------------------------------- |
| `notebookTargetConnectionID` | Integer | -1      | Connection ID for notebook execution (if pipeline uses notebooks) |
| `jobTargetConnectionID`      | Integer | -1      | Connection ID for job execution (if pipeline uses jobs)           |

### Complete JSON Example

```json
{
	"taskType": "pipeline",
	"taskName": "Extract Customer Data",
	"jobID": "pipeline-123",
	"automationOrderNumber": 1,
	"isActive": true,
	"notebookTargetConnectionID": -1,
	"jobTargetConnectionID": -1
}
```

### Multi-Task Example

```json
{
	"automationName": "Daily Customer ETL",
	"internalID": "proj-001",
	"jobRunSchedule": "0 2 * * *",
	"isActive": 1,
	"jobDetails": {
		"jobRunSchedule": "0 2 * * *",
		"jobRunTimeZone": "America/New_York",
		"jobClusterSize": "M",
		"jobTimeout": "3600",
		"tags": ["etl", "daily"],
		"emailNotifications": ["team@example.com"]
	},
	"automationTask": [
		{
			"taskType": "pipeline",
			"taskName": "Extract Customer Data",
			"jobID": "pipeline-123",
			"automationOrderNumber": 1,
			"isActive": true
		}
	]
}
```

### Common Patterns

**Sequential Pipeline Execution:**

```json
{
	"automationTask": [
		{
			"taskType": "pipeline",
			"taskName": "Extract from Source A",
			"jobID": "pipeline-100",
			"automationOrderNumber": 1,
			"isActive": true
		},
		{
			"taskType": "pipeline",
			"taskName": "Extract from Source B",
			"jobID": "pipeline-101",
			"automationOrderNumber": 2,
			"isActive": true
		},
		{
			"taskType": "pipeline",
			"taskName": "Merge and Load",
			"jobID": "pipeline-102",
			"automationOrderNumber": 3,
			"isActive": true
		}
	]
}
```

### Error Handling

**Common Errors:**

1. **Pipeline Not Found**

   ```
   Error: Pipeline with ID 'pipeline-123' not found
   Solution: Verify pipeline ID exists using `databasin pipelines list`
   ```

2. **Pipeline Failed**

   ```
   Error: Pipeline execution failed
   Solution: Check pipeline logs, verify source connections, ensure data sources are accessible
   ```

3. **Insufficient Permissions**
   ```
   Error: User does not have permission to execute pipeline
   Solution: Verify user has access to pipeline and all connectors it uses
   ```

### Best Practices

1. **Use Descriptive Task Names** - Clearly indicate what the pipeline does
2. **Set Appropriate Timeout** - Pipeline tasks can be long-running, ensure `jobTimeout` is sufficient
3. **Monitor Dependencies** - Ensure source systems are accessible before pipeline runs
4. **Test Manually First** - Run pipeline manually before adding to automation
5. **Handle Failures** - Set up email notifications for pipeline failures

---

## SQL Query Task Type

Execute one or more SQL queries against a database connection.

### Purpose

The SQL query task type allows you to execute SQL statements against any connected database. This is ideal for data transformation, validation, cleanup, and other SQL operations that need to run as part of an automation.

### Required Fields

| Field                   | Type          | Description                       |
| ----------------------- | ------------- | --------------------------------- |
| `taskType`              | String        | Must be `"sql"`                   |
| `taskName`              | String        | Descriptive name for this task    |
| `sqlTargetConnectionID` | Integer       | The connection ID of the database |
| `sqlQueryMap`           | Array[String] | Array of SQL queries to execute   |
| `automationOrderNumber` | Integer       | Execution order (1-based)         |
| `isActive`              | Boolean       | Whether this task is enabled      |

### Optional Fields

| Field            | Type   | Default | Description                                            |
| ---------------- | ------ | ------- | ------------------------------------------------------ |
| `notebookParams` | Object | null    | Optional parameters (not typically used for SQL tasks) |

### Complete JSON Example

```json
{
	"taskType": "sql",
	"taskName": "Clean Staging Tables",
	"sqlTargetConnectionID": 58,
	"sqlQueryMap": [
		"DELETE FROM staging.customers WHERE processed = true",
		"UPDATE staging.orders SET status = 'ready' WHERE valid = true",
		"INSERT INTO audit_log (table_name, action, timestamp) VALUES ('staging.customers', 'cleanup', CURRENT_TIMESTAMP)"
	],
	"automationOrderNumber": 2,
	"isActive": true,
	"notebookParams": null
}
```

### Query Array Structure

The `sqlQueryMap` field is an **array of SQL query strings**. Each query is executed in sequence.

**Single Query:**

```json
{
	"sqlQueryMap": ["UPDATE sales SET processed = true WHERE date = CURRENT_DATE"]
}
```

**Multiple Sequential Queries:**

```json
{
	"sqlQueryMap": [
		"CREATE TEMP TABLE temp_sales AS SELECT * FROM sales WHERE date = CURRENT_DATE",
		"UPDATE temp_sales SET region = 'UNKNOWN' WHERE region IS NULL",
		"INSERT INTO sales_archive SELECT * FROM temp_sales",
		"DROP TABLE temp_sales"
	]
}
```

**Complex Transformations:**

```json
{
	"sqlQueryMap": [
		"DELETE FROM staging.data WHERE status = 'invalid'",
		"UPDATE staging.data SET normalized = UPPER(TRIM(name)) WHERE normalized IS NULL",
		"INSERT INTO production.data SELECT id, normalized, date FROM staging.data WHERE status = 'valid'",
		"UPDATE staging.data SET status = 'archived' WHERE status = 'valid'"
	]
}
```

### Multiple Query Execution

Queries in the `sqlQueryMap` array are executed **sequentially** in the order they appear. If any query fails, execution stops and the task is marked as failed.

**Execution Flow:**

1. Query 1 executes → Success → Continue
2. Query 2 executes → Success → Continue
3. Query 3 executes → **Failure** → Stop, mark task as failed
4. Query 4 is **not executed**

**Best Practice:** Order queries from least to most critical, with cleanup/logging queries at the end.

### Complete Multi-Task Example

```json
{
	"automationName": "Daily Data Transformation",
	"internalID": "proj-001",
	"jobRunSchedule": "0 3 * * *",
	"isActive": 1,
	"jobDetails": {
		"jobRunSchedule": "0 3 * * *",
		"jobRunTimeZone": "America/New_York",
		"jobClusterSize": "S",
		"jobTimeout": "1800",
		"tags": ["sql", "transformation"],
		"emailNotifications": ["data-team@example.com"]
	},
	"automationTask": [
		{
			"taskType": "pipeline",
			"taskName": "Load Raw Data",
			"jobID": "pipeline-100",
			"automationOrderNumber": 1,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "Validate and Transform",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": [
				"UPDATE staging.customers SET email = LOWER(TRIM(email))",
				"DELETE FROM staging.customers WHERE email IS NULL OR email = ''",
				"UPDATE staging.customers SET status = 'validated' WHERE email LIKE '%@%'"
			],
			"automationOrderNumber": 2,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "Load to Production",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": [
				"INSERT INTO production.customers SELECT * FROM staging.customers WHERE status = 'validated'",
				"UPDATE staging.customers SET processed = true WHERE status = 'validated'"
			],
			"automationOrderNumber": 3,
			"isActive": true
		}
	]
}
```

### Common Patterns

**Data Validation:**

```json
{
	"taskType": "sql",
	"taskName": "Validate Data Quality",
	"sqlTargetConnectionID": 58,
	"sqlQueryMap": [
		"UPDATE staging.data SET valid = false WHERE email NOT LIKE '%@%'",
		"UPDATE staging.data SET valid = false WHERE phone IS NULL",
		"UPDATE staging.data SET valid = true WHERE email LIKE '%@%' AND phone IS NOT NULL"
	],
	"automationOrderNumber": 1,
	"isActive": true
}
```

**Incremental Processing:**

```json
{
	"taskType": "sql",
	"taskName": "Process New Records",
	"sqlTargetConnectionID": 58,
	"sqlQueryMap": [
		"INSERT INTO production.sales SELECT * FROM staging.sales WHERE processed = false",
		"UPDATE staging.sales SET processed = true, processed_at = CURRENT_TIMESTAMP WHERE processed = false"
	],
	"automationOrderNumber": 2,
	"isActive": true
}
```

**Cleanup and Archival:**

```json
{
	"taskType": "sql",
	"taskName": "Archive and Clean",
	"sqlTargetConnectionID": 58,
	"sqlQueryMap": [
		"INSERT INTO archive.old_data SELECT * FROM production.data WHERE date < CURRENT_DATE - INTERVAL '90 days'",
		"DELETE FROM production.data WHERE date < CURRENT_DATE - INTERVAL '90 days'",
		"VACUUM production.data"
	],
	"automationOrderNumber": 3,
	"isActive": true
}
```

### Error Handling

**Common Errors:**

1. **Connection Not Found**

   ```
   Error: Connection ID 58 not found
   Solution: Verify connection exists using `databasin connectors list`
   ```

2. **SQL Syntax Error**

   ```
   Error: Syntax error at line 1: unexpected token 'FORM'
   Solution: Review SQL syntax, ensure queries are valid for target database
   ```

3. **Permission Denied**

   ```
   Error: User does not have permission to execute UPDATE on table 'sales'
   Solution: Grant necessary permissions to database user
   ```

4. **Query Timeout**
   ```
   Error: Query execution timeout after 1800 seconds
   Solution: Optimize query performance or increase jobTimeout in automation
   ```

### Best Practices

1. **Use Transactions** - Wrap related queries in transactions for atomicity
2. **Add Logging** - Include INSERT statements to audit/log tables
3. **Validate First** - Put validation queries before data modification
4. **Order Carefully** - Execute queries in logical sequence
5. **Test Queries** - Run queries manually in SQL editor before automation
6. **Use Comments** - Add SQL comments to complex queries for clarity
7. **Handle NULLs** - Explicitly handle NULL values in WHERE clauses
8. **Set Timeouts** - Ensure `jobTimeout` is appropriate for query complexity
9. **Monitor Performance** - Track query execution times and optimize slow queries
10. **Use Parameters** - Consider notebook tasks if you need parameterized queries

---

## Notebook Task Type

Execute a Databricks notebook as part of an automation.

### Purpose

The notebook task type allows you to execute Databricks notebooks containing Python, Scala, R, or SQL code. This is ideal for complex analytics, machine learning, custom transformations, and any operations that require the full power of Apache Spark.

### Required Fields

| Field                   | Type    | Description                                   |
| ----------------------- | ------- | --------------------------------------------- |
| `taskType`              | String  | Must be `"notebook"`                          |
| `taskName`              | String  | Descriptive name for this task                |
| `notebookPath`          | String  | Full path to notebook in Databricks workspace |
| `automationOrderNumber` | Integer | Execution order (1-based)                     |
| `isActive`              | Boolean | Whether this task is enabled                  |

### Optional Fields

| Field                        | Type    | Default | Description                                           |
| ---------------------------- | ------- | ------- | ----------------------------------------------------- |
| `notebookTargetConnectionID` | Integer | -1      | Databricks connection ID                              |
| `notebookParams`             | Object  | null    | Parameters to pass to notebook                        |
| `databricksRuntime`          | String  | null    | Databricks runtime version (e.g., "13.3.x-scala2.12") |
| `notebookPermissions`        | String  | null    | JSON string array of permission objects               |
| `gitRepository`              | Object  | null    | Git repository configuration for notebook source      |

### Complete JSON Example

```json
{
	"taskType": "notebook",
	"taskName": "Generate Daily Analytics",
	"notebookPath": "/analytics/daily_summary",
	"notebookTargetConnectionID": 45,
	"notebookParams": {
		"date": "2024-11-23",
		"environment": "production",
		"output_table": "analytics.daily_summary"
	},
	"databricksRuntime": "13.3.x-scala2.12",
	"automationOrderNumber": 3,
	"isActive": true,
	"gitRepository": null,
	"notebookPermissions": null
}
```

### File Path Specifications

The `notebookPath` must be the **full path** to the notebook in your Databricks workspace.

**Valid Path Formats:**

```
/Users/user@example.com/notebooks/my_notebook
/Shared/analytics/daily_report
/Repos/my-org/my-repo/notebooks/etl_process
/analytics/customer_segmentation
```

**Invalid Paths:**

```
my_notebook              ❌ Missing leading slash
notebooks/my_notebook    ❌ Relative path
~/my_notebook            ❌ Home directory notation not supported
```

### Parameter Passing

The `notebookParams` field accepts a JSON object where keys are parameter names and values are parameter values passed to the notebook.

**Simple Parameters:**

```json
{
	"notebookParams": {
		"start_date": "2024-01-01",
		"end_date": "2024-12-31",
		"region": "US"
	}
}
```

**Complex Parameters:**

```json
{
	"notebookParams": {
		"source_table": "staging.raw_data",
		"target_table": "production.processed_data",
		"partition_column": "date",
		"partition_value": "2024-11-23",
		"mode": "overwrite",
		"enable_caching": "true",
		"max_retries": "3"
	}
}
```

**Accessing in Notebook:**

Python:

```python
# Access parameters in Python notebook
start_date = dbutils.widgets.get("start_date")
region = dbutils.widgets.get("region")
```

Scala:

```scala
// Access parameters in Scala notebook
val startDate = dbutils.widgets.get("start_date")
val region = dbutils.widgets.get("region")
```

### Complete Multi-Task Example

```json
{
	"automationName": "ML Model Training Pipeline",
	"internalID": "proj-001",
	"jobRunSchedule": "0 4 * * *",
	"isActive": 1,
	"jobDetails": {
		"jobRunSchedule": "0 4 * * *",
		"jobRunTimeZone": "America/New_York",
		"jobClusterSize": "L",
		"jobTimeout": "7200",
		"tags": ["ml", "training"],
		"emailNotifications": ["ml-team@example.com"]
	},
	"automationTask": [
		{
			"taskType": "pipeline",
			"taskName": "Load Training Data",
			"jobID": "pipeline-200",
			"automationOrderNumber": 1,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "Prepare Features",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": [
				"CREATE OR REPLACE TABLE ml.features AS SELECT * FROM staging.raw_features WHERE date >= CURRENT_DATE - 30",
				"UPDATE ml.features SET normalized_score = score / 100.0"
			],
			"automationOrderNumber": 2,
			"isActive": true
		},
		{
			"taskType": "notebook",
			"taskName": "Train Model",
			"notebookPath": "/ml/model_training",
			"notebookTargetConnectionID": 45,
			"notebookParams": {
				"feature_table": "ml.features",
				"model_name": "customer_churn_v2",
				"training_date": "2024-11-23",
				"test_split": "0.2",
				"enable_mlflow": "true"
			},
			"databricksRuntime": "13.3.x-scala2.12",
			"automationOrderNumber": 3,
			"isActive": true
		},
		{
			"taskType": "notebook",
			"taskName": "Evaluate and Deploy",
			"notebookPath": "/ml/model_evaluation",
			"notebookTargetConnectionID": 45,
			"notebookParams": {
				"model_name": "customer_churn_v2",
				"threshold": "0.8",
				"deploy_if_better": "true"
			},
			"databricksRuntime": "13.3.x-scala2.12",
			"automationOrderNumber": 4,
			"isActive": true
		}
	]
}
```

### Git Repository Integration

If your notebook is stored in a Git repository, you can specify repository details:

```json
{
	"taskType": "notebook",
	"taskName": "Run Notebook from Git",
	"notebookPath": "/Repos/my-org/analytics/notebooks/daily_report",
	"gitRepository": {
		"url": "https://github.com/my-org/analytics",
		"branch": "main",
		"provider": "github"
	},
	"automationOrderNumber": 1,
	"isActive": true
}
```

### Databricks Runtime Versions

Specify the runtime version if your notebook requires specific Spark or library versions:

**Common Runtime Versions:**

- `"13.3.x-scala2.12"` - Standard Spark 3.4.1
- `"13.3.x-cpu-ml-scala2.12"` - Machine Learning (CPU)
- `"13.3.x-gpu-ml-scala2.12"` - Machine Learning (GPU)
- `"13.3.x-photon-scala2.12"` - Photon-enabled for performance

```json
{
	"databricksRuntime": "13.3.x-cpu-ml-scala2.12"
}
```

### Notebook Permissions

Set permissions for the notebook execution:

```json
{
	"notebookPermissions": "[{\"email\": \"user@example.com\", \"permission\": \"CAN_VIEW\"}, {\"email\": \"admin@example.com\", \"permission\": \"CAN_MANAGE\"}]"
}
```

**Permission Levels:**

- `CAN_VIEW` - View notebook and results
- `CAN_RUN` - Run notebook
- `CAN_EDIT` - Edit notebook
- `CAN_MANAGE` - Full management permissions

### Common Patterns

**Data Processing Pipeline:**

```json
{
	"taskType": "notebook",
	"taskName": "Process Customer Data",
	"notebookPath": "/etl/customer_processing",
	"notebookParams": {
		"source_table": "staging.customers",
		"target_table": "production.customers",
		"partition_date": "{{ current_date }}",
		"mode": "overwrite"
	},
	"automationOrderNumber": 2,
	"isActive": true
}
```

**Analytics Report Generation:**

```json
{
	"taskType": "notebook",
	"taskName": "Generate Weekly Report",
	"notebookPath": "/reports/weekly_summary",
	"notebookParams": {
		"week_start": "{{ week_start }}",
		"week_end": "{{ week_end }}",
		"output_format": "html",
		"email_recipients": "team@example.com"
	},
	"automationOrderNumber": 1,
	"isActive": true
}
```

**ML Model Inference:**

```json
{
	"taskType": "notebook",
	"taskName": "Run Predictions",
	"notebookPath": "/ml/batch_inference",
	"notebookParams": {
		"model_name": "sales_forecast_v3",
		"input_table": "production.sales",
		"output_table": "predictions.sales_forecast",
		"forecast_days": "30"
	},
	"databricksRuntime": "13.3.x-cpu-ml-scala2.12",
	"automationOrderNumber": 3,
	"isActive": true
}
```

### Error Handling

**Common Errors:**

1. **Notebook Not Found**

   ```
   Error: Notebook not found at path '/analytics/missing_notebook'
   Solution: Verify notebook exists in Databricks workspace at specified path
   ```

2. **Connection Not Found**

   ```
   Error: Databricks connection ID 45 not found
   Solution: Verify connection exists and is configured for Databricks
   ```

3. **Runtime Version Not Supported**

   ```
   Error: Runtime version '13.3.x-scala2.12' not available
   Solution: Check available runtime versions in your Databricks workspace
   ```

4. **Parameter Error**

   ```
   Error: Required parameter 'start_date' not provided
   Solution: Add missing parameter to notebookParams object
   ```

5. **Permission Denied**
   ```
   Error: User does not have permission to run notebook
   Solution: Grant necessary permissions in Databricks workspace
   ```

### Best Practices

1. **Use Parameters** - Make notebooks reusable with parameters instead of hard-coded values
2. **Set Appropriate Runtime** - Choose runtime version matching notebook requirements
3. **Handle Errors in Notebook** - Implement error handling and logging within notebooks
4. **Test Independently** - Run notebook manually before adding to automation
5. **Document Parameters** - Clearly document expected parameters in notebook comments
6. **Use Widgets** - Use `dbutils.widgets` for parameter input in notebooks
7. **Set Timeouts** - Ensure `jobTimeout` is sufficient for notebook execution
8. **Monitor Resource Usage** - Use appropriate cluster size for notebook workload
9. **Version Control** - Store notebooks in Git for version tracking
10. **Log Results** - Write execution logs and results for debugging

---

## Job Task Type

Trigger an existing Databricks job as part of an automation.

### Purpose

The job task type allows you to execute pre-configured Databricks jobs. This is useful when you have existing Databricks job definitions that you want to incorporate into an automation workflow.

### Required Fields

| Field                   | Type    | Description                      |
| ----------------------- | ------- | -------------------------------- |
| `taskType`              | String  | Must be `"job"`                  |
| `taskName`              | String  | Descriptive name for this task   |
| `jobID`                 | String  | The Databricks job ID to execute |
| `automationOrderNumber` | Integer | Execution order (1-based)        |
| `isActive`              | Boolean | Whether this task is enabled     |

### Optional Fields

| Field                   | Type    | Default | Description                                |
| ----------------------- | ------- | ------- | ------------------------------------------ |
| `jobTargetConnectionID` | Integer | -1      | Databricks connection ID for job execution |

### Complete JSON Example

```json
{
	"taskType": "job",
	"taskName": "Run Databricks ETL Job",
	"jobID": "job-456",
	"jobTargetConnectionID": 45,
	"automationOrderNumber": 2,
	"isActive": true
}
```

### Job Reference

The `jobID` refers to an existing Databricks job ID. You must create and configure the job in Databricks before referencing it in an automation.

**Finding Job IDs:**

1. Open Databricks workspace
2. Navigate to Workflows → Jobs
3. Select your job
4. Job ID is shown in the URL: `https://your-workspace.databricks.com/jobs/123456`
5. Use `job-123456` as the `jobID` value

### Complete Multi-Task Example

```json
{
	"automationName": "Nightly Processing Workflow",
	"internalID": "proj-001",
	"jobRunSchedule": "0 1 * * *",
	"isActive": 1,
	"jobDetails": {
		"jobRunSchedule": "0 1 * * *",
		"jobRunTimeZone": "America/New_York",
		"jobClusterSize": "M",
		"jobTimeout": "5400",
		"tags": ["nightly", "processing"],
		"emailNotifications": ["ops-team@example.com"]
	},
	"automationTask": [
		{
			"taskType": "pipeline",
			"taskName": "Extract Source Data",
			"jobID": "pipeline-100",
			"automationOrderNumber": 1,
			"isActive": true
		},
		{
			"taskType": "job",
			"taskName": "Run Databricks Processing Job",
			"jobID": "job-789",
			"jobTargetConnectionID": 45,
			"automationOrderNumber": 2,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "Update Status Tables",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": [
				"UPDATE job_status SET completed = true, completed_at = CURRENT_TIMESTAMP WHERE job_id = 'job-789'"
			],
			"automationOrderNumber": 3,
			"isActive": true
		}
	]
}
```

### Common Patterns

**Sequential Job Execution:**

```json
{
	"automationTask": [
		{
			"taskType": "job",
			"taskName": "Stage 1: Data Ingestion",
			"jobID": "job-100",
			"automationOrderNumber": 1,
			"isActive": true
		},
		{
			"taskType": "job",
			"taskName": "Stage 2: Data Transformation",
			"jobID": "job-101",
			"automationOrderNumber": 2,
			"isActive": true
		},
		{
			"taskType": "job",
			"taskName": "Stage 3: Data Validation",
			"jobID": "job-102",
			"automationOrderNumber": 3,
			"isActive": true
		}
	]
}
```

**Job with Pre/Post Processing:**

```json
{
	"automationTask": [
		{
			"taskType": "sql",
			"taskName": "Pre-process: Create Staging",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": ["CREATE TABLE IF NOT EXISTS staging.temp_data (id INT, data STRING)"],
			"automationOrderNumber": 1,
			"isActive": true
		},
		{
			"taskType": "job",
			"taskName": "Execute Main Processing Job",
			"jobID": "job-500",
			"jobTargetConnectionID": 45,
			"automationOrderNumber": 2,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "Post-process: Cleanup",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": ["DROP TABLE staging.temp_data"],
			"automationOrderNumber": 3,
			"isActive": true
		}
	]
}
```

### Error Handling

**Common Errors:**

1. **Job Not Found**

   ```
   Error: Databricks job 'job-456' not found
   Solution: Verify job exists in Databricks workspace
   ```

2. **Job Already Running**

   ```
   Error: Job is already running (concurrent execution not allowed)
   Solution: Wait for previous run to complete or enable concurrent runs in job settings
   ```

3. **Connection Error**

   ```
   Error: Cannot connect to Databricks workspace
   Solution: Verify jobTargetConnectionID points to valid Databricks connection
   ```

4. **Job Failed**
   ```
   Error: Databricks job failed with error: <error_message>
   Solution: Check job logs in Databricks workspace for detailed error information
   ```

### Best Practices

1. **Use Meaningful Names** - Task name should describe what the job does
2. **Configure Jobs First** - Set up and test job in Databricks before adding to automation
3. **Set Appropriate Cluster** - Ensure automation cluster size matches job requirements
4. **Monitor Concurrent Runs** - Be aware of Databricks job concurrency settings
5. **Handle Dependencies** - Ensure prerequisite tasks complete before job execution
6. **Review Job Logs** - Check Databricks job logs for execution details
7. **Set Timeouts** - Ensure automation `jobTimeout` exceeds expected job duration
8. **Use Job Parameters** - Configure job parameters in Databricks for flexibility

---

## File Drop Task Type

Move or copy files between storage locations (connectors).

### Purpose

The file drop task type allows you to move or copy files from one storage location to another. This is useful for archiving processed files, distributing files to multiple destinations, or organizing files based on processing results.

### Required Fields

| Field                        | Type    | Description                                            |
| ---------------------------- | ------- | ------------------------------------------------------ |
| `taskType`                   | String  | Must be `"file"`                                       |
| `taskName`                   | String  | Descriptive name for this task                         |
| `fileDropSourceConnectionID` | Integer | Source connector ID (where files are located)          |
| `fileDropTargetConnectionID` | Integer | Target connector ID (where files will be copied/moved) |
| `automationOrderNumber`      | Integer | Execution order (1-based)                              |
| `isActive`                   | Boolean | Whether this task is enabled                           |

### Optional Fields

| Field              | Type          | Default | Description                         |
| ------------------ | ------------- | ------- | ----------------------------------- |
| `fileDropQueryMap` | Array[Object] | null    | Array of file operation definitions |

### Complete JSON Example

```json
{
	"taskType": "file",
	"taskName": "Archive Processed Files",
	"fileDropSourceConnectionID": 12,
	"fileDropTargetConnectionID": 15,
	"fileDropQueryMap": [
		{
			"query": "SELECT file_path FROM processing_log WHERE status = 'completed'",
			"auditIdentifier": "file_id",
			"fileDropName": "processed_files_archive"
		}
	],
	"automationOrderNumber": 4,
	"isActive": true
}
```

### File Drop Query Map Structure

The `fileDropQueryMap` array contains objects that define which files to move/copy and how to track them.

**Query Map Object Structure:**

```json
{
	"query": "SQL query to select files",
	"auditIdentifier": "field name for audit tracking",
	"fileDropName": "descriptive name for this file operation"
}
```

### Path Monitoring

File drop tasks can monitor specific paths for new files and trigger actions when files appear.

**Monitor for CSV Files:**

```json
{
	"taskType": "file",
	"taskName": "Move New CSV Files",
	"fileDropSourceConnectionID": 20,
	"fileDropTargetConnectionID": 25,
	"fileDropQueryMap": [
		{
			"query": "SELECT file_path FROM files WHERE extension = 'csv' AND processed = false",
			"auditIdentifier": "file_id",
			"fileDropName": "csv_ingestion"
		}
	],
	"automationOrderNumber": 1,
	"isActive": true
}
```

**Monitor Specific Folder:**

```json
{
	"taskType": "file",
	"taskName": "Archive Daily Reports",
	"fileDropSourceConnectionID": 30,
	"fileDropTargetConnectionID": 35,
	"fileDropQueryMap": [
		{
			"query": "SELECT file_path FROM files WHERE folder = '/daily_reports' AND date = CURRENT_DATE",
			"auditIdentifier": "file_id",
			"fileDropName": "daily_report_archive"
		}
	],
	"automationOrderNumber": 2,
	"isActive": true
}
```

### Complete Multi-Task Example

```json
{
	"automationName": "File Processing and Archival",
	"internalID": "proj-001",
	"jobRunSchedule": "0 */6 * * *",
	"isActive": 1,
	"jobDetails": {
		"jobRunSchedule": "0 */6 * * *",
		"jobRunTimeZone": "America/New_York",
		"jobClusterSize": "S",
		"jobTimeout": "1800",
		"tags": ["file-processing"],
		"emailNotifications": ["file-ops@example.com"]
	},
	"automationTask": [
		{
			"taskType": "pipeline",
			"taskName": "Process Incoming Files",
			"jobID": "pipeline-300",
			"automationOrderNumber": 1,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "Update File Status",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": [
				"UPDATE file_registry SET status = 'processed' WHERE processed_at IS NOT NULL"
			],
			"automationOrderNumber": 2,
			"isActive": true
		},
		{
			"taskType": "file",
			"taskName": "Archive Processed Files",
			"fileDropSourceConnectionID": 12,
			"fileDropTargetConnectionID": 15,
			"fileDropQueryMap": [
				{
					"query": "SELECT file_path FROM file_registry WHERE status = 'processed'",
					"auditIdentifier": "file_id",
					"fileDropName": "processed_archive"
				}
			],
			"automationOrderNumber": 3,
			"isActive": true
		},
		{
			"taskType": "file",
			"taskName": "Move Failed Files to Error Folder",
			"fileDropSourceConnectionID": 12,
			"fileDropTargetConnectionID": 18,
			"fileDropQueryMap": [
				{
					"query": "SELECT file_path FROM file_registry WHERE status = 'failed'",
					"auditIdentifier": "file_id",
					"fileDropName": "error_files"
				}
			],
			"automationOrderNumber": 4,
			"isActive": true
		}
	]
}
```

### S3/ADLS Patterns

**S3 to S3 Archive:**

```json
{
	"taskType": "file",
	"taskName": "S3 Archive",
	"fileDropSourceConnectionID": 40,
	"fileDropTargetConnectionID": 41,
	"fileDropQueryMap": [
		{
			"query": "SELECT s3_key FROM s3_files WHERE age_days > 30",
			"auditIdentifier": "s3_key",
			"fileDropName": "s3_monthly_archive"
		}
	],
	"automationOrderNumber": 1,
	"isActive": true
}
```

**ADLS to ADLS Distribution:**

```json
{
	"taskType": "file",
	"taskName": "Distribute Reports to Teams",
	"fileDropSourceConnectionID": 50,
	"fileDropTargetConnectionID": 51,
	"fileDropQueryMap": [
		{
			"query": "SELECT file_path FROM reports WHERE type = 'daily' AND published = true",
			"auditIdentifier": "report_id",
			"fileDropName": "daily_report_distribution"
		}
	],
	"automationOrderNumber": 2,
	"isActive": true
}
```

**Cross-Platform File Transfer:**

```json
{
	"taskType": "file",
	"taskName": "S3 to ADLS Transfer",
	"fileDropSourceConnectionID": 60,
	"fileDropTargetConnectionID": 61,
	"fileDropQueryMap": [
		{
			"query": "SELECT file_location FROM cross_platform_files WHERE transfer_needed = true",
			"auditIdentifier": "transfer_id",
			"fileDropName": "s3_to_adls_migration"
		}
	],
	"automationOrderNumber": 1,
	"isActive": true
}
```

### Trigger Configuration

File drop tasks can be configured to trigger based on file arrival:

**Event-Driven Pattern:**

```json
{
	"automationName": "File Arrival Processing",
	"internalID": "proj-001",
	"jobRunSchedule": "0 * * * *",
	"isActive": 1,
	"jobDetails": {
		"jobRunSchedule": "0 * * * *",
		"jobRunTimeZone": "America/New_York",
		"jobClusterSize": "S",
		"jobTimeout": "900"
	},
	"automationTask": [
		{
			"taskType": "file",
			"taskName": "Detect New Files",
			"fileDropSourceConnectionID": 70,
			"fileDropTargetConnectionID": 71,
			"fileDropQueryMap": [
				{
					"query": "SELECT file_path FROM incoming_files WHERE created_at >= CURRENT_TIMESTAMP - INTERVAL '1 hour'",
					"auditIdentifier": "file_id",
					"fileDropName": "new_file_detection"
				}
			],
			"automationOrderNumber": 1,
			"isActive": true
		}
	]
}
```

### Error Handling

**Common Errors:**

1. **Source Connection Not Found**

   ```
   Error: Source connection ID 12 not found
   Solution: Verify source connector exists using `databasin connectors list`
   ```

2. **Target Connection Not Found**

   ```
   Error: Target connection ID 15 not found
   Solution: Verify target connector exists and has write permissions
   ```

3. **Permission Denied**

   ```
   Error: No permission to read from source or write to target
   Solution: Verify connector credentials have necessary permissions
   ```

4. **File Not Found**

   ```
   Error: File path '/data/file.csv' not found in source
   Solution: Verify files exist at source location before file drop task
   ```

5. **Query Error**
   ```
   Error: SQL query in fileDropQueryMap failed
   Solution: Test query independently, ensure it returns valid file paths
   ```

### Best Practices

1. **Verify Connections** - Test both source and target connectors before automation
2. **Use Audit Identifiers** - Always include audit identifiers for tracking
3. **Handle Missing Files** - Design queries to handle cases where files don't exist
4. **Set Appropriate Timeouts** - Large file transfers may need longer timeouts
5. **Monitor Storage** - Ensure target storage has sufficient space
6. **Use Descriptive Names** - Make `fileDropName` meaningful for audit logs
7. **Test Queries** - Validate SQL queries return expected file paths
8. **Consider Network** - Account for network bandwidth when transferring large files
9. **Implement Cleanup** - Consider deleting source files after successful transfer
10. **Log Operations** - Use SQL tasks to log file operations for audit trail

---

## Docker Task Type

Execute a Docker container as part of an automation.

### Purpose

The docker task type allows you to run containerized applications as part of an automation workflow. This is useful for running custom tools, legacy applications, or third-party software that isn't available in Databricks.

### Required Fields

| Field                      | Type    | Description                              |
| -------------------------- | ------- | ---------------------------------------- |
| `taskType`                 | String  | Must be `"docker"`                       |
| `taskName`                 | String  | Descriptive name for this task           |
| `dockerSourceConnectionID` | Integer | Connection ID for Docker registry/source |
| `automationOrderNumber`    | Integer | Execution order (1-based)                |
| `isActive`                 | Boolean | Whether this task is enabled             |

### Optional Fields

| Field                    | Type   | Default | Description                            |
| ------------------------ | ------ | ------- | -------------------------------------- |
| `dockerCommandOverride`  | String | null    | Override command to run in container   |
| `dockerArgumentOverride` | String | null    | Override arguments passed to container |

### Complete JSON Example

```json
{
	"taskType": "docker",
	"taskName": "Run Custom Data Validator",
	"dockerSourceConnectionID": 80,
	"dockerCommandOverride": "python /app/validate.py",
	"dockerArgumentOverride": "--input /data/input.csv --output /data/output.csv --strict",
	"automationOrderNumber": 5,
	"isActive": true
}
```

### Docker Image Reference

The Docker image is referenced through the `dockerSourceConnectionID`, which should point to a connector configured with:

- Docker registry URL
- Image name and tag
- Authentication credentials (if required)

**Example Docker Connector Configuration:**

```json
{
	"connectorName": "Custom Validator Image",
	"connectorType": "Docker Registry",
	"connectorHost": "docker.io",
	"imageName": "my-org/data-validator:latest",
	"connectorUsername": "registry_user",
	"connectorPassword": "registry_token"
}
```

### Environment Variables

Environment variables can be passed to containers through the Docker connector configuration or as part of the automation setup.

**Via Connector:**

```json
{
	"dockerSourceConnectionID": 80,
	"dockerEnvironmentVariables": {
		"ENV": "production",
		"LOG_LEVEL": "INFO",
		"API_KEY": "${SECURE_API_KEY}"
	}
}
```

**Via Command Override:**

```json
{
	"dockerCommandOverride": "sh -c 'export ENV=production && python /app/main.py'"
}
```

### Resource Limits

Resource limits for Docker containers are controlled by the automation's `jobClusterSize` setting:

| Cluster Size | CPU Cores | Memory (GB) | Typical Use           |
| ------------ | --------- | ----------- | --------------------- |
| XS           | 1         | 2           | Lightweight tools     |
| S            | 2         | 4           | Small processing jobs |
| M            | 4         | 8           | Medium workloads      |
| L            | 8         | 16          | Large processing      |
| XL           | 16        | 32          | Heavy computation     |

### Volume Mounts

Volume mounts allow containers to access data from storage connectors:

```json
{
	"taskType": "docker",
	"taskName": "Process Files with Custom Tool",
	"dockerSourceConnectionID": 85,
	"dockerCommandOverride": "python /app/processor.py",
	"dockerArgumentOverride": "--mount /mnt/data:/data --mount /mnt/output:/output",
	"automationOrderNumber": 2,
	"isActive": true
}
```

### Complete Multi-Task Example

```json
{
	"automationName": "Custom Docker Processing Workflow",
	"internalID": "proj-001",
	"jobRunSchedule": "0 5 * * *",
	"isActive": 1,
	"jobDetails": {
		"jobRunSchedule": "0 5 * * *",
		"jobRunTimeZone": "America/New_York",
		"jobClusterSize": "M",
		"jobTimeout": "3600",
		"tags": ["docker", "custom-processing"],
		"emailNotifications": ["ops@example.com"]
	},
	"automationTask": [
		{
			"taskType": "pipeline",
			"taskName": "Extract Data to Staging",
			"jobID": "pipeline-400",
			"automationOrderNumber": 1,
			"isActive": true
		},
		{
			"taskType": "file",
			"taskName": "Move Files to Processing Folder",
			"fileDropSourceConnectionID": 90,
			"fileDropTargetConnectionID": 91,
			"fileDropQueryMap": [
				{
					"query": "SELECT file_path FROM staging WHERE ready_for_processing = true",
					"auditIdentifier": "file_id",
					"fileDropName": "staging_to_processing"
				}
			],
			"automationOrderNumber": 2,
			"isActive": true
		},
		{
			"taskType": "docker",
			"taskName": "Run Legacy Validation Tool",
			"dockerSourceConnectionID": 85,
			"dockerCommandOverride": "/app/legacy_validator",
			"dockerArgumentOverride": "--input-dir /data/processing --output-dir /data/validated --config /config/rules.xml",
			"automationOrderNumber": 3,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "Update Processing Status",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": [
				"UPDATE processing_log SET status = 'validated', validated_at = CURRENT_TIMESTAMP WHERE status = 'processing'"
			],
			"automationOrderNumber": 4,
			"isActive": true
		},
		{
			"taskType": "docker",
			"taskName": "Generate Custom Report",
			"dockerSourceConnectionID": 86,
			"dockerCommandOverride": "python /app/report_generator.py",
			"dockerArgumentOverride": "--data /data/validated --template /templates/summary.html --output /reports/daily_summary.pdf",
			"automationOrderNumber": 5,
			"isActive": true
		}
	]
}
```

### Container Registry Configuration

**Docker Hub:**

```json
{
	"dockerSourceConnectionID": 100,
	"dockerImageReference": "username/image:tag"
}
```

**Private Registry:**

```json
{
	"dockerSourceConnectionID": 101,
	"dockerImageReference": "registry.company.com/team/image:v1.2.3"
}
```

**AWS ECR:**

```json
{
	"dockerSourceConnectionID": 102,
	"dockerImageReference": "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest"
}
```

**Azure Container Registry:**

```json
{
	"dockerSourceConnectionID": 103,
	"dockerImageReference": "myregistry.azurecr.io/my-app:v2.0"
}
```

### Common Patterns

**Data Transformation with Custom Tool:**

```json
{
	"taskType": "docker",
	"taskName": "Apply Proprietary Algorithm",
	"dockerSourceConnectionID": 110,
	"dockerCommandOverride": "/usr/local/bin/transform",
	"dockerArgumentOverride": "--input /data/raw --output /data/transformed --algorithm proprietary-v3",
	"automationOrderNumber": 2,
	"isActive": true
}
```

**Legacy Application Integration:**

```json
{
	"taskType": "docker",
	"taskName": "Run Legacy COBOL Export",
	"dockerSourceConnectionID": 111,
	"dockerCommandOverride": "/legacy/export_tool",
	"dockerArgumentOverride": "--config /config/mainframe.conf --output /exports/daily_extract.dat",
	"automationOrderNumber": 1,
	"isActive": true
}
```

**Third-Party Tool Execution:**

```json
{
	"taskType": "docker",
	"taskName": "PDF Generation",
	"dockerSourceConnectionID": 112,
	"dockerCommandOverride": "wkhtmltopdf",
	"dockerArgumentOverride": "/data/report.html /output/report.pdf",
	"automationOrderNumber": 4,
	"isActive": true
}
```

### Error Handling

**Common Errors:**

1. **Image Not Found**

   ```
   Error: Docker image 'my-org/my-app:latest' not found
   Solution: Verify image exists in registry and connector has correct image reference
   ```

2. **Registry Authentication Failed**

   ```
   Error: Failed to authenticate with Docker registry
   Solution: Verify connector credentials are correct and have pull permissions
   ```

3. **Container Execution Failed**

   ```
   Error: Container exited with code 1
   Solution: Check container logs, verify command and arguments are correct
   ```

4. **Resource Limits Exceeded**

   ```
   Error: Container killed due to OOM (out of memory)
   Solution: Increase automation jobClusterSize or optimize container memory usage
   ```

5. **Volume Mount Error**
   ```
   Error: Failed to mount volume /data
   Solution: Verify storage connector is accessible and has correct permissions
   ```

### Best Practices

1. **Use Specific Tags** - Avoid `:latest` tag, use specific version tags for reproducibility
2. **Test Containers Locally** - Run containers locally before adding to automation
3. **Set Resource Limits** - Configure appropriate cluster size for container requirements
4. **Handle Secrets Securely** - Use secure connector configuration for sensitive data
5. **Log Output** - Ensure containers log to stdout/stderr for debugging
6. **Use Health Checks** - Implement container health checks for reliability
7. **Minimize Image Size** - Use slim base images to reduce pull time
8. **Version Control** - Tag images with version numbers for tracking
9. **Clean Up** - Ensure containers exit cleanly and don't leave orphaned processes
10. **Monitor Performance** - Track container execution time and resource usage

---

## Task Sequencing

Multiple tasks can be combined in a single automation to create complex workflows. Tasks execute sequentially in the order defined by `automationOrderNumber`.

### Execution Order

Tasks are executed in ascending order of `automationOrderNumber`:

```json
{
	"automationTask": [
		{
			"automationOrderNumber": 1,
			"taskName": "First Task"
		},
		{
			"automationOrderNumber": 2,
			"taskName": "Second Task"
		},
		{
			"automationOrderNumber": 3,
			"taskName": "Third Task"
		}
	]
}
```

**Important:**

- Order numbers must be unique within an automation
- Order numbers should be consecutive (1, 2, 3...) for clarity
- Tasks execute in strict sequential order
- If a task fails, subsequent tasks do not execute

### Dependency Handling

Tasks can depend on outputs from previous tasks:

**Pipeline → SQL → Notebook Pattern:**

```json
{
	"automationTask": [
		{
			"taskType": "pipeline",
			"taskName": "Load Raw Data",
			"jobID": "pipeline-100",
			"automationOrderNumber": 1,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "Transform and Validate",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": [
				"UPDATE staging.data SET clean = TRIM(raw_value)",
				"DELETE FROM staging.data WHERE clean IS NULL"
			],
			"automationOrderNumber": 2,
			"isActive": true
		},
		{
			"taskType": "notebook",
			"taskName": "Generate Analytics",
			"notebookPath": "/analytics/daily_report",
			"notebookParams": {
				"source_table": "staging.data"
			},
			"automationOrderNumber": 3,
			"isActive": true
		}
	]
}
```

**File Processing Workflow:**

```json
{
	"automationTask": [
		{
			"taskType": "file",
			"taskName": "Move New Files to Processing",
			"fileDropSourceConnectionID": 10,
			"fileDropTargetConnectionID": 11,
			"automationOrderNumber": 1,
			"isActive": true
		},
		{
			"taskType": "docker",
			"taskName": "Process Files with Custom Tool",
			"dockerSourceConnectionID": 80,
			"dockerCommandOverride": "/app/processor",
			"automationOrderNumber": 2,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "Import Processed Data",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": ["COPY INTO production.data FROM '/processed' FILE_FORMAT = (TYPE = 'CSV')"],
			"automationOrderNumber": 3,
			"isActive": true
		},
		{
			"taskType": "file",
			"taskName": "Archive Processed Files",
			"fileDropSourceConnectionID": 11,
			"fileDropTargetConnectionID": 12,
			"automationOrderNumber": 4,
			"isActive": true
		}
	]
}
```

### Error Propagation

When a task fails:

1. Task execution stops immediately
2. Error is logged with task details
3. Subsequent tasks are **not executed**
4. Automation status is set to "Failed"
5. Email notifications are sent (if configured)

**Example Error Flow:**

```
Task 1: Pipeline ✅ Success → Continue to Task 2
Task 2: SQL ❌ Failed → Stop execution
Task 3: Notebook ⏭️ Not executed
Task 4: File Drop ⏭️ Not executed
```

**Handling Errors:**

1. **Use Try-Catch in Notebooks:**

```python
# In notebook task
try:
    # Your processing logic
    process_data()
except Exception as e:
    # Log error but don't fail
    log_error(e)
    # Exit successfully
    dbutils.notebook.exit("error_handled")
```

2. **Use Conditional SQL:**

```json
{
	"sqlQueryMap": [
		"UPDATE data SET status = 'error' WHERE validation_failed = true",
		"INSERT INTO error_log SELECT * FROM data WHERE status = 'error'",
		"DELETE FROM data WHERE status = 'error'"
	]
}
```

3. **Enable Audit Logging:**

```json
{
	"auditEnabled": 1,
	"auditInformation": {
		"purpose": "Track task failures for compliance"
	}
}
```

### Complex Workflow Example

Complete ETL workflow with all task types:

```json
{
	"automationName": "Complete ETL Workflow",
	"internalID": "proj-001",
	"jobRunSchedule": "0 2 * * *",
	"isActive": 1,
	"auditEnabled": 1,
	"jobDetails": {
		"jobRunSchedule": "0 2 * * *",
		"jobRunTimeZone": "America/New_York",
		"jobClusterSize": "L",
		"jobTimeout": "10800",
		"tags": ["etl", "production", "daily"],
		"emailNotifications": ["data-team@example.com", "ops@example.com"]
	},
	"automationTask": [
		{
			"taskType": "sql",
			"taskName": "1. Initialize Staging Environment",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": [
				"TRUNCATE TABLE staging.daily_import",
				"CREATE TABLE IF NOT EXISTS staging.processing_log (task_id INT, start_time TIMESTAMP, status STRING)",
				"INSERT INTO staging.processing_log VALUES (1, CURRENT_TIMESTAMP, 'started')"
			],
			"automationOrderNumber": 1,
			"isActive": true
		},
		{
			"taskType": "pipeline",
			"taskName": "2. Extract Data from Multiple Sources",
			"jobID": "pipeline-500",
			"automationOrderNumber": 2,
			"isActive": true
		},
		{
			"taskType": "file",
			"taskName": "3. Move Extracted Files to Processing",
			"fileDropSourceConnectionID": 20,
			"fileDropTargetConnectionID": 21,
			"fileDropQueryMap": [
				{
					"query": "SELECT file_path FROM extracted_files WHERE extract_date = CURRENT_DATE",
					"auditIdentifier": "file_id",
					"fileDropName": "extract_to_processing"
				}
			],
			"automationOrderNumber": 3,
			"isActive": true
		},
		{
			"taskType": "docker",
			"taskName": "4. Validate with Legacy Tool",
			"dockerSourceConnectionID": 85,
			"dockerCommandOverride": "/app/validator",
			"dockerArgumentOverride": "--input /data/processing --output /data/validated",
			"automationOrderNumber": 4,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "5. Import Validated Data",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": [
				"COPY INTO staging.daily_import FROM '/data/validated' FILE_FORMAT = (TYPE = 'PARQUET')",
				"UPDATE staging.processing_log SET status = 'imported' WHERE task_id = 1"
			],
			"automationOrderNumber": 5,
			"isActive": true
		},
		{
			"taskType": "notebook",
			"taskName": "6. Transform and Enrich Data",
			"notebookPath": "/etl/transform_enrich",
			"notebookParams": {
				"source_table": "staging.daily_import",
				"target_table": "staging.enriched",
				"date": "{{ current_date }}"
			},
			"databricksRuntime": "13.3.x-scala2.12",
			"automationOrderNumber": 6,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "7. Data Quality Checks",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": [
				"UPDATE staging.enriched SET quality_score = CASE WHEN all_fields_valid THEN 100 ELSE 0 END",
				"INSERT INTO quality_log SELECT date, COUNT(*), AVG(quality_score) FROM staging.enriched GROUP BY date"
			],
			"automationOrderNumber": 7,
			"isActive": true
		},
		{
			"taskType": "job",
			"taskName": "8. Run Production Load Job",
			"jobID": "job-1000",
			"jobTargetConnectionID": 45,
			"automationOrderNumber": 8,
			"isActive": true
		},
		{
			"taskType": "notebook",
			"taskName": "9. Generate Analytics Report",
			"notebookPath": "/reports/daily_summary",
			"notebookParams": {
				"date": "{{ current_date }}",
				"output_format": "html",
				"email_recipients": "executives@example.com"
			},
			"automationOrderNumber": 9,
			"isActive": true
		},
		{
			"taskType": "file",
			"taskName": "10. Archive Processed Files",
			"fileDropSourceConnectionID": 21,
			"fileDropTargetConnectionID": 22,
			"fileDropQueryMap": [
				{
					"query": "SELECT file_path FROM validated_files WHERE process_date = CURRENT_DATE",
					"auditIdentifier": "file_id",
					"fileDropName": "daily_archive"
				}
			],
			"automationOrderNumber": 10,
			"isActive": true
		},
		{
			"taskType": "sql",
			"taskName": "11. Finalize and Cleanup",
			"sqlTargetConnectionID": 58,
			"sqlQueryMap": [
				"UPDATE staging.processing_log SET status = 'completed', end_time = CURRENT_TIMESTAMP WHERE task_id = 1",
				"DELETE FROM staging.daily_import WHERE process_date < CURRENT_DATE - INTERVAL '7 days'",
				"OPTIMIZE production.data"
			],
			"automationOrderNumber": 11,
			"isActive": true
		}
	]
}
```

---

## Quick Reference Table

### All Task Types Summary

| Task Type  | Key Required Fields                                        | Primary Use Case                | Typical Duration |
| ---------- | ---------------------------------------------------------- | ------------------------------- | ---------------- |
| `pipeline` | `jobID`                                                    | Data movement, ingestion        | 5-30 minutes     |
| `sql`      | `sqlTargetConnectionID`, `sqlQueryMap`                     | Data transformation, validation | 1-10 minutes     |
| `notebook` | `notebookPath`                                             | Complex analytics, ML           | 10-60 minutes    |
| `job`      | `jobID`                                                    | Pre-configured Databricks jobs  | Varies           |
| `file`     | `fileDropSourceConnectionID`, `fileDropTargetConnectionID` | File management, archival       | 1-5 minutes      |
| `docker`   | `dockerSourceConnectionID`                                 | Custom containerized workloads  | 5-30 minutes     |

### Required Fields by Task Type

| Field                        | pipeline | sql | notebook | job | file | docker |
| ---------------------------- | -------- | --- | -------- | --- | ---- | ------ |
| `taskType`                   | ✅       | ✅  | ✅       | ✅  | ✅   | ✅     |
| `taskName`                   | ✅       | ✅  | ✅       | ✅  | ✅   | ✅     |
| `automationOrderNumber`      | ✅       | ✅  | ✅       | ✅  | ✅   | ✅     |
| `isActive`                   | ✅       | ✅  | ✅       | ✅  | ✅   | ✅     |
| `jobID`                      | ✅       |     |          | ✅  |      |        |
| `sqlTargetConnectionID`      |          | ✅  |          |     |      |        |
| `sqlQueryMap`                |          | ✅  |          |     |      |        |
| `notebookPath`               |          |     | ✅       |     |      |        |
| `fileDropSourceConnectionID` |          |     |          |     | ✅   |        |
| `fileDropTargetConnectionID` |          |     |          |     | ✅   |        |
| `dockerSourceConnectionID`   |          |     |          |     |      | ✅     |

### Use Case Summary

**Data Ingestion & Movement:**

- `pipeline` - Extract data from external sources
- `file` - Move files between storage locations

**Data Transformation:**

- `sql` - SQL-based transformations
- `notebook` - Complex transformations with Spark
- `docker` - Custom transformation tools

**Analytics & Reporting:**

- `notebook` - Generate reports, run analytics
- `docker` - Custom reporting tools

**Job Orchestration:**

- `job` - Trigger existing Databricks jobs
- `pipeline` - Execute Databasin workflows

**File Operations:**

- `file` - Archive, distribute, organize files
- `docker` - Process files with custom tools

---

## General Best Practices

### Task Naming

- Use descriptive, action-oriented names
- Include step number for complex workflows: "1. Extract", "2. Transform", "3. Load"
- Indicate what the task does, not just the type

### Order Numbers

- Use consecutive integers (1, 2, 3...)
- Leave gaps (10, 20, 30...) if you plan to insert tasks later
- Document dependencies in task names

### Error Handling

- Set up email notifications for all production automations
- Enable audit logging for compliance tracking
- Design tasks to be idempotent (safe to re-run)
- Add SQL logging tasks to track execution

### Performance

- Set appropriate `jobClusterSize` based on workload
- Set realistic `jobTimeout` values (don't make them too short)
- Consider splitting large tasks into smaller ones
- Monitor task execution times and optimize slow tasks

### Testing

- Test each task independently before automation
- Run automation manually before activating schedule
- Verify all connections are active and accessible
- Test with sample data before production data

### Maintenance

- Document complex workflows in task names
- Use tags to categorize automations
- Review and update automations regularly
- Archive unused automations instead of deleting

### Security

- Use secure connection configurations for sensitive data
- Avoid hard-coding credentials in SQL or notebook parameters
- Enable audit logging for compliance requirements
- Review permissions on all connectors

### Monitoring

- Set up email notifications for failures
- Review execution logs regularly
- Track automation performance over time
- Alert on abnormal execution times or failures

---

## Summary

Databasin automations support **6 powerful task types** that can be combined to create sophisticated data workflows:

1. **Pipeline** - Execute Databasin pipelines for data movement
2. **SQL** - Run SQL queries for transformation and validation
3. **Notebook** - Execute Databricks notebooks for analytics
4. **Job** - Trigger pre-configured Databricks jobs
5. **File** - Move files between storage locations
6. **Docker** - Run custom containerized applications

Each task type has specific required and optional fields, and tasks execute sequentially based on `automationOrderNumber`. By combining these task types, you can create complete end-to-end data workflows that handle ingestion, transformation, validation, analytics, and distribution.

For additional help:

- Review the automation SKILL.md for CLI usage
- Check connector references for connection setup
- Test tasks independently before combining
- Use the Databasin CLI for validation and testing
