# Pipeline Creation Guide

This document provides a comprehensive guide for creating data pipelines using the Databasin CLI. Pipelines move data between connectors with optional transformations, scheduling, and automation.

## Understanding Pipeline Creation

Creating a pipeline in Databasin involves several steps that vary based on the source and target connector types. The CLI provides both interactive and file-based approaches to pipeline creation.

### Key Concepts

**Pipeline Components:**
- **Source Connector** - Where data comes from (must support egress)
- **Target Connector** - Where data goes to (must support ingress)
- **Artifacts** - The data objects being moved (tables, files, API endpoints)
- **Ingestion Pattern** - How data is stored: "datalake" or "data warehouse"
- **Schedule** - When the pipeline runs (cron format)

**Connector Requirements:**
- Source connectors must have `egressTargetSupport: true`
- Target connectors must have `ingressTargetSupport: true`
- Use `databasin connectors config <type>` to verify connector capabilities

## Pipeline Creation Workflow

The pipeline creation process follows a multi-step workflow that adapts based on connector types. Understanding this workflow helps you gather the right information before creating a pipeline.

### Step 0: Prerequisites

Before creating a pipeline, gather the following information:

1. **Project Information**
   ```bash
   # List available projects
   databasin projects list
   ```

2. **Available Connectors**
   ```bash
   # List connectors in your project
   databasin connectors list --project <projectId> --full

   # View connector details
   databasin connectors get <connectorId>

   # Check connector configuration
   databasin connectors config <connectorType>
   ```

3. **Pipeline Configuration Settings**
   - Pipeline name (max 27 characters)
   - Ingestion pattern (datalake or data warehouse)
   - Target catalog/schema names
   - Schedule (cron format)
   - Cluster size (S, M, L, XL)

### Step 1: Initial Configuration

**Required Information:**
- `pipelineName` - String, max 27 characters
- `sourceConnectorId` - Connector ID with egress support
- `targetConnectorId` - Connector ID with ingress support
- `ingestionPattern` - "datalake" or "data warehouse"
- `targetCatalogName` - Required for data warehouse pattern
- `targetSchemaName` - Required for datalake pattern
- `createCatalogs` - Auto-create catalogs (boolean)
- `sourceNamingConvention` - true = short names, false = long names

**Discovery Commands:**

```bash
# Find connectors that support egress (source)
databasin connectors list --project <projectId> --full --json | \
  jq '.[] | select(.egressTargetSupport == true)'

# Find connectors that support ingress (target)
databasin connectors list --project <projectId> --full --json | \
  jq '.[] | select(.ingressTargetSupport == true)'

# View connector workflow requirements
databasin connectors config <connectorType> --screens
```

### Step 2: Connector-Specific Workflows

Different connector types require different discovery steps. The CLI helps you navigate these based on the connector configuration.

#### Database Connectors (MySQL, PostgreSQL, SQL Server)

**Typical Workflow:** Catalogs → Schemas → Tables → Columns → Ingestion Options

**Discovery Process:**

1. **List Available Catalogs/Databases**
   - Some databases organize objects in catalogs (databases)
   - Others use schemas directly
   - Check connector config to understand the hierarchy

2. **List Schemas**
   - Schemas contain the actual tables
   - Select the schema that contains your target tables

3. **Select Tables (Artifacts)**
   - Choose which tables to include in the pipeline
   - Can select multiple tables in a single pipeline

4. **Select Columns**
   - For each table, choose which columns to ingest
   - Omitting this step includes all columns
   - Useful for excluding sensitive data

5. **Configure Ingestion Options**
   - **Ingestion Type:**
     - `full` - Complete table replacement each run
     - `delta` - Only new/changed records (requires watermark column)
     - `snapshot` - Point-in-time copies with retention
   - **Watermark Column** - Column for delta tracking (e.g., `updated_at`)
   - **Merge Columns** - Primary key columns for delta merges
   - **Backload Days** - How many days to backfill initially
   - **Snapshot Retention** - How many snapshots to keep
   - **Detect Deletes** - Track deleted records (delta mode with merge)
   - **Auto Explode** - Automatically flatten nested data structures

**Example: Database Pipeline Configuration**

```json
{
  "pipelineName": "MySQL to Snowflake",
  "sourceConnectorId": "mysql-prod-123",
  "targetConnectorId": "snowflake-dw-456",
  "ingestionPattern": "data warehouse",
  "targetCatalogName": "analytics",
  "createCatalogs": false,
  "sourceNamingConvention": true,
  "jobDetails": {
    "tags": ["production", "daily"],
    "jobClusterSize": "M",
    "emailNotifications": ["team@example.com"],
    "jobRunSchedule": "0 2 * * *",
    "jobRunTimeZone": "UTC",
    "jobTimeout": "43200"
  },
  "items": [
    {
      "sourceConnectionID": "mysql-prod-123",
      "targetConnectionID": "snowflake-dw-456",
      "sourceDatabaseName": "production",
      "sourceSchemaName": "public",
      "sourceTableName": "users",
      "sourceColumnNames": ["id", "email", "created_at", "updated_at"],
      "targetDatabaseName": "analytics",
      "targetSchemaName": "staging",
      "targetTableName": "users",
      "ingestionType": "delta",
      "watermarkColumnName": ["updated_at"],
      "mergeColumns": ["id"],
      "backloadNumDays": 7,
      "detectDeletes": true,
      "autoExplode": false
    }
  ]
}
```

#### File Storage Connectors (S3, Azure Blob, Google Cloud Storage)

**Typical Workflow:** Files/Patterns → Ingestion Options

**Discovery Process:**

1. **Identify File Patterns**
   - Use wildcard patterns (e.g., `*.csv`, `data_*.json`)
   - Or specify individual file paths
   - File connector configurations determine available paths

2. **Configure File Ingestion**
   - **Source File Name** - File path or pattern
   - **Source File Format** - csv, json, parquet, xml, avro, etc.
   - **Contains Header** - For CSV files, first row is header
   - **Column Header Line** - Which line contains column names (CSV)
   - **File Delimiter** - Delimiter character (CSV/TXT)
   - **Auto Explode** - Flatten nested JSON structures
   - **Row Tag** - XML element that represents a row
   - **XSD Path** - XML schema definition file location

**Example: S3 CSV Pipeline Configuration**

```json
{
  "pipelineName": "S3 CSV Ingestion",
  "sourceConnectorId": "s3-bucket-123",
  "targetConnectorId": "snowflake-dw-456",
  "ingestionPattern": "datalake",
  "targetSchemaName": "raw_data",
  "createCatalogs": true,
  "sourceNamingConvention": false,
  "jobDetails": {
    "tags": ["s3", "csv"],
    "jobClusterSize": "L",
    "emailNotifications": ["data-team@example.com"],
    "jobRunSchedule": "0 */4 * * *",
    "jobRunTimeZone": "America/New_York",
    "jobTimeout": "21600"
  },
  "items": [
    {
      "sourceConnectionID": "s3-bucket-123",
      "targetConnectionID": "snowflake-dw-456",
      "sourceFileName": "sales/daily_*.csv",
      "sourceFileFormat": "csv",
      "containsHeader": true,
      "columnHeaderLineNumber": 1,
      "sourceFileDelimiter": ",",
      "targetSchemaName": "raw_data",
      "targetTableName": "daily_sales",
      "ingestionType": "full",
      "autoExplode": false
    }
  ]
}
```

#### Cloud Data Warehouse Connectors (Snowflake, Databricks)

**Typical Workflow:** Databases → Schemas → Tables → Columns → Ingestion Options

Similar to database connectors, but may have additional hierarchy levels:
- **Databases** - Top-level organizational unit
- **Schemas** - Second-level organizational unit
- **Tables** - Actual data objects

**Discovery Tips:**

```bash
# View the required workflow for a connector
databasin connectors config Snowflake --screens

# Example output shows:
# 1. [6] Database - Choose database/catalog
# 2. [7] Schemas - Choose schema
# 3. [2] Artifacts - Select tables
# 4. [3] Columns - Select columns
# 5. [4] Data Ingestion Options - Configure ingestion
# 6. [5] Final Configuration - Schedule and cluster
```

#### API Connectors

**Typical Workflow:** API Configuration → Authentication → Ingestion Options

**Configuration Requirements:**
- **API Endpoint URL** - The full URL to the API endpoint
- **API Call Type** - GET, POST, PUT, DELETE
- **Authentication Method** - OAuth, token, basic auth
- **Request Payload** - Body for POST/PUT requests
- **Response Format** - JSON, XML, CSV

**Example: REST API Pipeline Configuration**

```json
{
  "pipelineName": "Salesforce API Extract",
  "sourceConnectorId": "salesforce-api-123",
  "targetConnectorId": "snowflake-dw-456",
  "ingestionPattern": "datalake",
  "targetSchemaName": "salesforce_raw",
  "createCatalogs": true,
  "sourceNamingConvention": true,
  "jobDetails": {
    "tags": ["api", "salesforce"],
    "jobClusterSize": "S",
    "emailNotifications": ["integrations@example.com"],
    "jobRunSchedule": "0 1 * * *",
    "jobRunTimeZone": "UTC",
    "jobTimeout": "7200"
  },
  "items": [
    {
      "sourceConnectionID": "salesforce-api-123",
      "targetConnectionID": "snowflake-dw-456",
      "apiRoute": "/services/data/v52.0/query",
      "apiCallType": "GET",
      "apiPayload": "SELECT Id, Name, Email FROM Contact WHERE LastModifiedDate > YESTERDAY",
      "apiResponseFormat": "json",
      "targetSchemaName": "salesforce_raw",
      "targetTableName": "contacts",
      "ingestionType": "full",
      "autoExplode": true
    }
  ]
}
```

### Step 3: Final Configuration

**Job Details Required:**
- `tags` - Array of strings for categorization (optional)
- `jobClusterSize` - Compute resources: "S", "M", "L", or "XL"
- `emailNotifications` - Array of email addresses for alerts
- `jobRunSchedule` - Cron expression (e.g., "0 10 * * *")
- `jobRunTimeZone` - Timezone string (e.g., "UTC", "America/New_York")
- `jobTimeout` - Maximum runtime in seconds (default: 43200 = 12 hours)

**Cluster Size Guidelines:**
- **S (Small)** - Light workloads, small files, API calls
- **M (Medium)** - Standard database ingestion, moderate file sizes
- **L (Large)** - High-volume data transfers, large file processing
- **XL (Extra Large)** - Massive datasets, complex transformations

**Cron Schedule Examples:**
```bash
# Every day at 2 AM UTC
"0 2 * * *"

# Every 4 hours
"0 */4 * * *"

# Every Monday at 8 AM
"0 8 * * 1"

# First day of month at midnight
"0 0 1 * *"

# Every 15 minutes (for testing)
"*/15 * * * *"
```

### Step 4: Create the Pipeline

**Using CLI Commands:**

```bash
# Create from configuration file
databasin pipelines create pipeline-config.json

# Interactive creation (simplified)
databasin pipelines create --project <projectId>

# View created pipeline
databasin pipelines get <pipelineId>

# Run the pipeline
databasin pipelines run <pipelineId>
```

## Implementation Strategies

### Strategy 1: Interactive CLI Mode

Use the interactive wizard for simple pipelines:

```bash
# Start interactive creation
databasin pipelines create

# Prompts will guide you through:
# 1. Project selection
# 2. Pipeline name
# 3. Source connector
# 4. Target connector
# 5. Schedule configuration
```

**Best for:**
- Quick pipeline setup
- Learning the pipeline creation process
- Simple source-to-target data movement

**Limitations:**
- Limited artifact configuration support
- No advanced ingestion options
- Cannot specify column selection

### Strategy 2: Configuration File

Create a JSON file with complete pipeline configuration:

```bash
# 1. Create configuration file
cat > my-pipeline.json <<EOF
{
  "pipelineName": "My Data Pipeline",
  "sourceConnectorId": "source-123",
  "targetConnectorId": "target-456",
  ...
}
EOF

# 2. Create pipeline from file
databasin pipelines create my-pipeline.json

# 3. Verify and run
databasin pipelines get <pipelineId>
databasin pipelines run <pipelineId>
```

**Best for:**
- Complex pipeline configurations
- Repeatable pipeline creation
- Version-controlled pipeline definitions
- Automation and scripting

### Strategy 3: Programmatic Approach

Use the CLI in scripts for batch operations:

```bash
#!/bin/bash
# Create multiple similar pipelines

TABLES=("users" "orders" "products")
for table in "${TABLES[@]}"; do
  cat > "${table}-pipeline.json" <<EOF
  {
    "pipelineName": "Sync ${table}",
    "sourceConnectorId": "mysql-prod",
    "targetConnectorId": "snowflake-dw",
    "items": [{
      "sourceTableName": "${table}",
      "targetTableName": "${table}",
      ...
    }]
  }
EOF

  databasin pipelines create "${table}-pipeline.json"
done
```

**Best for:**
- Bulk pipeline creation
- Standardized pipeline patterns
- Multi-table synchronization
- Automated deployment

## Common Pipeline Patterns

### Pattern 1: Full Table Replication

Complete table replacement on each run:

```json
{
  "items": [{
    "sourceTableName": "customers",
    "targetTableName": "customers",
    "ingestionType": "full",
    "sourceColumnNames": null
  }]
}
```

**Use when:**
- Small to medium tables
- Source data changes frequently
- No reliable timestamp column
- Simplicity is preferred

### Pattern 2: Delta Ingestion

Capture only new or changed records:

```json
{
  "items": [{
    "sourceTableName": "orders",
    "targetTableName": "orders",
    "ingestionType": "delta",
    "watermarkColumnName": ["updated_at"],
    "mergeColumns": ["order_id"],
    "backloadNumDays": 7,
    "detectDeletes": true
  }]
}
```

**Use when:**
- Large tables
- Reliable timestamp/sequence column exists
- Need to detect deleted records
- Minimize data transfer volume

### Pattern 3: Snapshot Management

Maintain historical point-in-time copies:

```json
{
  "items": [{
    "sourceTableName": "inventory",
    "targetTableName": "inventory_snapshots",
    "ingestionType": "snapshot",
    "snapshotRetentionPeriod": 30
  }]
}
```

**Use when:**
- Need historical data views
- Tracking changes over time
- Compliance requirements
- Trend analysis

### Pattern 4: Multi-Table Synchronization

Single pipeline for related tables:

```json
{
  "pipelineName": "E-commerce Sync",
  "items": [
    {
      "sourceTableName": "customers",
      "targetTableName": "customers",
      "ingestionType": "delta",
      "watermarkColumnName": ["updated_at"]
    },
    {
      "sourceTableName": "orders",
      "targetTableName": "orders",
      "ingestionType": "delta",
      "watermarkColumnName": ["created_at"]
    },
    {
      "sourceTableName": "products",
      "targetTableName": "products",
      "ingestionType": "full"
    }
  ]
}
```

**Use when:**
- Related tables need consistent timing
- Maintaining referential integrity
- Simplifying pipeline management

### Pattern 5: File Pattern Processing

Process multiple files matching a pattern:

```json
{
  "items": [{
    "sourceFileName": "logs/app-*.json",
    "sourceFileFormat": "json",
    "targetTableName": "application_logs",
    "ingestionType": "full",
    "autoExplode": true
  }]
}
```

**Use when:**
- Regular file drops
- Consistent file naming convention
- Automated file processing

## Key Considerations

### 1. Data Type Handling

When creating pipeline configurations:
- Boolean fields should be JSON booleans: `true` or `false`
- Numeric fields should be numbers: `3306`, not `"3306"`
- Timeout values are strings: `"43200"`
- Arrays for watermark/merge columns: `["column_name"]`

### 2. Column Selection

**All Columns:**
```json
"sourceColumnNames": null
```

**Specific Columns:**
```json
"sourceColumnNames": ["id", "name", "email", "created_at"]
```

**When to limit columns:**
- Exclude sensitive data (SSN, passwords)
- Reduce data transfer volume
- Target schema has different structure
- Compliance requirements

### 3. Ingestion Type Selection

**Choose Full when:**
- Table is small (< 1M rows)
- Complete refresh is acceptable
- No reliable watermark column
- Simplicity is priority

**Choose Delta when:**
- Table is large (> 1M rows)
- Watermark column exists
- Minimize data transfer
- Need deleted record detection

**Choose Snapshot when:**
- Historical tracking required
- Need point-in-time analysis
- Regulatory compliance
- Change tracking

### 4. Schedule Optimization

**Considerations:**
- Avoid overlapping runs (timeout > typical runtime)
- Align with source system batch windows
- Consider timezone differences
- Balance freshness vs. resource usage

**Monitoring:**
```bash
# Check pipeline status
databasin pipelines get <pipelineId>

# View recent executions (when available)
databasin pipelines logs <pipelineId>
```

### 5. Error Handling

Pipeline configuration validation happens at creation time. Common validation errors:

- **Missing required fields** - Check configuration completeness
- **Invalid connector IDs** - Verify connectors exist and have correct support
- **Invalid cron schedule** - Validate cron expression syntax
- **Column selection errors** - Ensure columns exist in source
- **Type mismatches** - Verify data types in configuration

### 6. Performance Tuning

**Cluster Size Selection:**
- Start with M (Medium) for most workloads
- Monitor execution time
- Scale up for slow pipelines
- Scale down to reduce costs

**Optimization Tips:**
- Use delta ingestion for large tables
- Limit columns to needed fields only
- Batch related tables in single pipeline
- Schedule during off-peak hours

## Workflow Reference

### Common Workflows by Connector Type

**RDBMS (MySQL, PostgreSQL, SQL Server):**
1. Select database/catalog
2. Select schema
3. Select tables (artifacts)
4. Select columns (optional)
5. Configure ingestion options
6. Set schedule and cluster size

**File Storage (S3, Azure Blob):**
1. Specify file patterns
2. Configure file format options
3. Configure ingestion options
4. Set schedule and cluster size

**Cloud Warehouse (Snowflake, Databricks):**
1. Select database
2. Select schema
3. Select tables (artifacts)
4. Select columns (optional)
5. Configure ingestion options
6. Set schedule and cluster size

**API Connectors:**
1. Configure API endpoint
2. Set authentication
3. Configure request/response
4. Configure ingestion options
5. Set schedule and cluster size

### Discovery Commands Reference

```bash
# View connector workflow requirements
databasin connectors config <type> --screens

# List all connector configurations
databasin connectors config --all

# Get specific connector details
databasin connectors get <connectorId>

# List connectors in project
databasin connectors list --project <projectId> --full

# View created pipelines
databasin pipelines list --project <projectId>

# Get pipeline details
databasin pipelines get <pipelineId>

# Execute pipeline
databasin pipelines run <pipelineId>
```

## Complete Configuration Example

Here's a comprehensive pipeline configuration showing all available options:

```json
{
  "pipelineName": "Complete Pipeline Example",
  "sourceConnectorId": "mysql-prod-123",
  "targetConnectorId": "snowflake-dw-456",
  "ingestionPattern": "data warehouse",
  "targetCatalogName": "analytics",
  "targetSchemaName": "staging",
  "createCatalogs": false,
  "sourceNamingConvention": true,
  "isPrivate": 0,
  "jobDetails": {
    "tags": ["production", "hourly", "critical"],
    "jobClusterSize": "L",
    "emailNotifications": [
      "data-team@example.com",
      "ops@example.com"
    ],
    "jobRunSchedule": "0 * * * *",
    "jobRunTimeZone": "America/New_York",
    "jobTimeout": "7200"
  },
  "items": [
    {
      "sourceConnectionID": "mysql-prod-123",
      "targetConnectionID": "snowflake-dw-456",
      "sourceDatabaseName": "production",
      "sourceSchemaName": "public",
      "sourceTableName": "user_events",
      "sourceColumnNames": [
        "event_id",
        "user_id",
        "event_type",
        "event_timestamp",
        "metadata"
      ],
      "targetDatabaseName": "analytics",
      "targetSchemaName": "staging",
      "targetTableName": "user_events",
      "ingestionType": "delta",
      "watermarkColumnName": ["event_timestamp"],
      "mergeColumns": ["event_id"],
      "backloadNumDays": 3,
      "snapshotRetentionPeriod": 0,
      "detectDeletes": false,
      "autoExplode": true
    }
  ]
}
```

## Next Steps

1. **Review connector documentation** - `databasin connectors config <type> --screens`
2. **Test connector connections** - `databasin connectors test <connectorId>`
3. **Create test pipeline** - Use interactive mode or simple JSON file
4. **Monitor execution** - Check pipeline status after creation
5. **Iterate and optimize** - Adjust cluster size and schedule as needed

For detailed CLI command reference, see:
- [Pipelines Commands Guide](../../../databasin-cli/docs/pipelines-guide.md)
- [Connectors Commands Guide](../../../databasin-cli/docs/connectors-guide.md)
