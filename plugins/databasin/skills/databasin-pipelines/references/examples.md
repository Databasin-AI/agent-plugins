# Databasin Pipeline Configuration Examples

This document provides example configurations for common pipeline scenarios.

## Example 1: MySQL to Snowflake (Data Warehouse Pattern)

```json
{
	"institutionID": 1,
	"internalID": "project-123",
	"ownerID": 42,
	"pipelineName": "MySQL Users & Orders",
	"isPrivate": 0,
	"connectorTechnology": ["mysql"],
	"targetCatalogName": "analytics",
	"targetSchemaName": "",
	"ingestionPattern": "data warehouse",
	"createCatalogs": false,
	"sourceNamingConvention": true,
	"jobDetails": {
		"tags": ["production", "analytics"],
		"jobClusterSize": "M",
		"emailNotifications": ["data-team@company.com"],
		"jobRunSchedule": "0 2 * * *",
		"jobRunTimeZone": "UTC",
		"jobTimeout": "43200"
	},
	"items": [
		{
			"sourceConnectionID": 101,
			"targetConnectionID": 201,
			"artifactType": 1,
			"sourceDatabaseName": "production",
			"sourceSchemaName": "public",
			"sourceTableName": "users",
			"sourceColumnNames": null,
			"targetDatabaseName": "analytics",
			"targetSchemaName": "staging",
			"targetTableName": "users",
			"ingestionType": "delta",
			"watermarkColumnName": ["updated_at"],
			"mergeColumns": ["user_id"],
			"backloadNumDays": 7,
			"snapshotRetentionPeriod": 3,
			"detectDeletes": true,
			"autoExplode": false
		},
		{
			"sourceConnectionID": 101,
			"targetConnectionID": 201,
			"artifactType": 1,
			"sourceDatabaseName": "production",
			"sourceSchemaName": "public",
			"sourceTableName": "orders",
			"sourceColumnNames": null,
			"targetDatabaseName": "analytics",
			"targetSchemaName": "staging",
			"targetTableName": "orders",
			"ingestionType": "delta",
			"watermarkColumnName": ["created_at"],
			"mergeColumns": ["order_id"],
			"backloadNumDays": 30,
			"snapshotRetentionPeriod": 3,
			"detectDeletes": false,
			"autoExplode": false
		}
	]
}
```

## Example 2: S3 CSV Files to Databricks (Datalake Pattern)

```json
{
	"institutionID": 1,
	"internalID": "project-456",
	"ownerID": 42,
	"pipelineName": "S3 Sales Data",
	"isPrivate": 0,
	"connectorTechnology": ["s3"],
	"targetCatalogName": "",
	"targetSchemaName": "bronze",
	"ingestionPattern": "datalake",
	"createCatalogs": true,
	"sourceNamingConvention": false,
	"jobDetails": {
		"tags": ["bronze", "raw-data"],
		"jobClusterSize": "L",
		"emailNotifications": ["data-eng@company.com"],
		"jobRunSchedule": "0 */6 * * *",
		"jobRunTimeZone": "America/New_York",
		"jobTimeout": "43200"
	},
	"items": [
		{
			"sourceConnectionID": 102,
			"targetConnectionID": 202,
			"artifactType": 3,
			"sourceDatabaseName": "",
			"sourceSchemaName": "",
			"sourceTableName": "sales_*.csv",
			"sourceFileName": "data/sales/sales_*.csv",
			"sourceFileFormat": "csv",
			"sourceFileDelimiter": ",",
			"containsHeader": true,
			"columnHeaderLineNumber": 1,
			"targetDatabaseName": "main",
			"targetSchemaName": "bronze",
			"targetTableName": "sales_raw",
			"ingestionType": "full",
			"watermarkColumnName": [],
			"mergeColumns": [],
			"backloadNumDays": 0,
			"snapshotRetentionPeriod": 3,
			"detectDeletes": false,
			"autoExplode": false
		}
	]
}
```

## Example 3: PostgreSQL Specific Tables with Column Selection

```json
{
	"institutionID": 1,
	"internalID": "project-789",
	"ownerID": 42,
	"pipelineName": "PG Customer Analytics",
	"isPrivate": 0,
	"connectorTechnology": ["postgresql"],
	"targetCatalogName": "warehouse",
	"targetSchemaName": "",
	"ingestionPattern": "data warehouse",
	"createCatalogs": false,
	"sourceNamingConvention": true,
	"jobDetails": {
		"tags": ["customers", "pii"],
		"jobClusterSize": "S",
		"emailNotifications": ["analytics@company.com"],
		"jobRunSchedule": "0 10 * * *",
		"jobRunTimeZone": "UTC",
		"jobTimeout": "21600"
	},
	"items": [
		{
			"sourceConnectionID": 103,
			"targetConnectionID": 203,
			"artifactType": 1,
			"sourceDatabaseName": "app_db",
			"sourceSchemaName": "public",
			"sourceTableName": "customers",
			"sourceColumnNames": ["customer_id", "email", "created_at", "country", "subscription_tier"],
			"targetDatabaseName": "warehouse",
			"targetSchemaName": "analytics",
			"targetTableName": "customers",
			"ingestionType": "snapshot",
			"watermarkColumnName": [],
			"mergeColumns": [],
			"backloadNumDays": 0,
			"snapshotRetentionPeriod": 7,
			"detectDeletes": false,
			"autoExplode": false
		}
	]
}
```

## Example 4: JSON Files with Auto-Explode

```json
{
	"institutionID": 1,
	"internalID": "project-321",
	"ownerID": 42,
	"pipelineName": "API Logs Ingestion",
	"isPrivate": 0,
	"connectorTechnology": ["azure_blob"],
	"targetCatalogName": "",
	"targetSchemaName": "logs",
	"ingestionPattern": "datalake",
	"createCatalogs": true,
	"sourceNamingConvention": false,
	"jobDetails": {
		"tags": ["logs", "monitoring"],
		"jobClusterSize": "M",
		"emailNotifications": ["ops@company.com"],
		"jobRunSchedule": "0 * * * *",
		"jobRunTimeZone": "UTC",
		"jobTimeout": "7200"
	},
	"items": [
		{
			"sourceConnectionID": 104,
			"targetConnectionID": 204,
			"artifactType": 3,
			"sourceDatabaseName": "",
			"sourceSchemaName": "",
			"sourceTableName": "api-logs-*.json",
			"sourceFileName": "logs/api/api-logs-*.json",
			"sourceFileFormat": "json",
			"sourceFileDelimiter": null,
			"containsHeader": false,
			"columnHeaderLineNumber": null,
			"targetDatabaseName": "main",
			"targetSchemaName": "logs",
			"targetTableName": "api_requests",
			"ingestionType": "full",
			"watermarkColumnName": [],
			"mergeColumns": [],
			"backloadNumDays": 0,
			"snapshotRetentionPeriod": 1,
			"detectDeletes": false,
			"autoExplode": true
		}
	]
}
```

## Example 5: Minimal Configuration (Single Table, Full Load)

```json
{
	"institutionID": 1,
	"internalID": "project-999",
	"ownerID": 42,
	"pipelineName": "Simple Product Sync",
	"isPrivate": 0,
	"connectorTechnology": ["mysql"],
	"targetCatalogName": "staging",
	"targetSchemaName": "",
	"ingestionPattern": "data warehouse",
	"createCatalogs": false,
	"sourceNamingConvention": true,
	"jobDetails": {
		"tags": [],
		"jobClusterSize": "S",
		"emailNotifications": ["user@company.com"],
		"jobRunSchedule": "0 0 * * *",
		"jobRunTimeZone": "UTC",
		"jobTimeout": "43200"
	},
	"items": [
		{
			"sourceConnectionID": 105,
			"targetConnectionID": 205,
			"artifactType": 1,
			"sourceDatabaseName": "ecommerce",
			"sourceSchemaName": "public",
			"sourceTableName": "products",
			"sourceColumnNames": null,
			"targetDatabaseName": "staging",
			"targetSchemaName": "public",
			"targetTableName": "products",
			"ingestionType": "full",
			"watermarkColumnName": [],
			"mergeColumns": [],
			"backloadNumDays": 0,
			"snapshotRetentionPeriod": 3,
			"detectDeletes": false,
			"autoExplode": false
		}
	]
}
```

## Common Patterns

### Ingestion Types

**Full Load:**

- Replaces entire target table on each run
- No watermark needed
- Good for small dimension tables

**Delta Load:**

- Only ingests new/changed records
- Requires watermark column (e.g., `updated_at`, `created_at`)
- Requires merge columns (primary key)
- `detectDeletes` can identify removed records

**Snapshot:**

- Creates versioned snapshots of data
- `snapshotRetentionPeriod` controls how many snapshots to keep
- Good for tracking historical changes

### File Formats

**CSV/TXT:**

- Set `containsHeader: true/false`
- Set `columnHeaderLineNumber: 1` if header present
- Specify `sourceFileDelimiter` (e.g., `,`, `\t`, `|`)

**JSON:**

- Set `autoExplode: true` to flatten nested structures
- No delimiter or header needed

**Parquet:**

- Binary columnar format
- No delimiter or header needed
- Good for large datasets

### Wildcard Patterns

Use wildcards for file-based sources:

- `*.csv` - All CSV files
- `data_*.json` - Files starting with "data\_"
- `logs/2024/*.parquet` - All parquet files in logs/2024/

### Column Selection

- `"sourceColumnNames": null` - Ingest all columns
- `"sourceColumnNames": ["col1", "col2"]` - Ingest specific columns only

### Schedule Patterns

Common cron expressions:

- `0 2 * * *` - Daily at 2 AM
- `0 */6 * * *` - Every 6 hours
- `0 0 * * 0` - Weekly on Sunday midnight
- `0 0 1 * *` - Monthly on the 1st
