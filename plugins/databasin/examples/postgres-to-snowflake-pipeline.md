# Complete Workflow: PostgreSQL to Snowflake Data Pipeline

This example demonstrates a complete end-to-end workflow for extracting customer data from PostgreSQL and loading it into Snowflake using the Databasin CLI.

## Prerequisites

- Databasin CLI installed
- Access to a Databasin project
- PostgreSQL source database credentials
- Snowflake destination credentials

## Step 1: Authentication

Always start by authenticating and verifying your session:

```bash
# Login via browser
databasin auth login

# Verify authentication and view available projects
databasin auth whoami

# Example output:
# User: john.doe@company.com
# Organizations:
#   - Acme Corp (ID: 123)
# Projects:
#   - Production Data Warehouse (ID: N1r8Do)  ← Use this project ID
#   - Development Environment (ID: K9mPx2)
```

**IMPORTANT:** Note your project's **internal ID** (e.g., `N1r8Do` in the example above). You'll need this for `--project` arguments throughout this workflow.

## Step 2: List Available Connectors

Check existing connectors in your project:

```bash
# Get count of connectors (efficient)
databasin connectors list

# List all connectors with key details (use project ID from Step 1)
databasin connectors list --full --fields connectorID,connectorName,connectorType --project N1r8Do

# Example output:
# ┌─────────────┬──────────────────────┬────────────────┐
# │ connectorID │ connectorName        │ connectorType  │
# ├─────────────┼──────────────────────┼────────────────┤
# │ 5459        │ Production PostgreSQL│ Postgres       │
# │ 5765        │ Analytics Snowflake  │ Snowflake      │
# └─────────────┴──────────────────────┴────────────────┘
```

## Step 3: Create PostgreSQL Source Connector (if needed)

If you don't have a PostgreSQL connector, create one:

```bash
# First, get the connector configuration template
databasin connectors config Postgres --screens

# Create a connector configuration file
cat > postgres-connector.json << EOF
{
  "name": "Production PostgreSQL",
  "type": "Postgres",
  "config": {
    "host": "db.company.com",
    "port": 5432,
    "database": "production",
    "username": "databasin_ro",
    "password": "\${POSTGRES_PASSWORD}",
    "ssl": true
  },
  "projectID": "N1r8Do"
}
EOF

# Create the connector (use your project ID)
databasin connectors create postgres-connector.json --project N1r8Do

# Test the connection
databasin connectors test 5459
```

## Step 4: Explore Source Data Structure

Discover what data is available in your PostgreSQL database:

```bash
# List all catalogs
databasin sql catalogs 5459

# List schemas in the production catalog
databasin sql schemas 5459 --catalog production

# List tables in the public schema
databasin sql tables 5459 --catalog production --schema public

# Example output:
# Tables in production.public:
# - customers
# - orders
# - products
# - user_activity
```

## Step 5: Sample the Source Data

Examine the customers table structure and sample data:

```bash
# View sample records
databasin sql exec 5459 "SELECT * FROM customers LIMIT 5"

# Check record count
databasin sql exec 5459 "SELECT COUNT(*) as total_customers FROM customers"

# View column information
databasin sql exec 5459 "
  SELECT column_name, data_type, is_nullable
  FROM information_schema.columns
  WHERE table_name = 'customers'
  ORDER BY ordinal_position
"
```

## Step 6: Create Snowflake Destination Connector (if needed)

```bash
# Get Snowflake connector template
databasin connectors config Snowflake --screens

# Create connector configuration
cat > snowflake-connector.json << EOF
{
  "name": "Analytics Snowflake",
  "type": "Snowflake",
  "config": {
    "account": "acme-prod",
    "warehouse": "ANALYTICS_WH",
    "database": "ANALYTICS_DB",
    "schema": "PUBLIC",
    "username": "databasin_user",
    "password": "\${SNOWFLAKE_PASSWORD}",
    "role": "DATABASIN_ROLE"
  },
  "projectID": "N1r8Do"
}
EOF

# Create the connector (use your project ID)
databasin connectors create snowflake-connector.json --project N1r8Do

# Test the connection
databasin connectors test 5765
```

## Step 7: Create the Pipeline Configuration

Generate a pipeline configuration template and customize it:

```bash
# Generate template
databasin pipelines template > customer-sync-pipeline.json

# Edit the configuration (example below)
cat > customer-sync-pipeline.json << EOF
{
  "name": "Daily Customer Sync to Snowflake",
  "description": "Extracts active customers from PostgreSQL and loads into Snowflake analytics warehouse",
  "projectID": "N1r8Do",
  "sourceConnectorID": 5459,
  "targetConnectorID": 5765,
  "artifacts": [
    {
      "name": "Active Customers Extract",
      "sourceQuery": "SELECT customer_id, email, first_name, last_name, created_at, last_login, status FROM customers WHERE status = 'active'",
      "targetTable": "customers",
      "targetSchema": "public",
      "writeMode": "REPLACE",
      "schedule": {
        "enabled": true,
        "cron": "0 6 * * *",
        "timezone": "America/New_York"
      }
    }
  ],
  "notifications": {
    "onSuccess": ["data-team@company.com"],
    "onFailure": ["data-team@company.com", "ops@company.com"]
  }
}
EOF
```

**Key Configuration Points:**
- `projectID`: Your project's internal ID from Step 1 (N1r8Do in this example)
- `sourceConnectorID`: PostgreSQL connector ID (5459)
- `targetConnectorID`: Snowflake connector ID (5765)
- `schedule.cron`: "0 6 * * *" = Daily at 6:00 AM
- `writeMode`: "REPLACE" overwrites data, "APPEND" adds to existing data

## Step 8: Validate the Pipeline Configuration

Before creating, validate your configuration:

```bash
databasin pipelines validate customer-sync-pipeline.json

# If validation passes, you'll see:
# ✓ Pipeline configuration is valid
# ✓ Source connector exists and is accessible
# ✓ Target connector exists and is accessible
# ✓ SQL query syntax is valid
# ✓ Schedule cron expression is valid
```

## Step 9: Create the Pipeline

```bash
# Create the pipeline (use your project ID)
databasin pipelines create customer-sync-pipeline.json --project N1r8Do

# Example output:
# Pipeline created successfully
# Pipeline ID: 8901
# Pipeline Name: Daily Customer Sync to Snowflake
```

## Step 10: Test Run the Pipeline

Execute the pipeline immediately to verify it works:

```bash
# Run the pipeline
databasin pipelines run 8901

# Monitor execution
databasin pipelines logs 8901

# Check execution history
databasin pipelines history 8901 --limit 5
```

## Step 11: Monitor Pipeline Logs

View detailed logs to ensure successful execution:

```bash
# View latest logs
databasin pipelines logs 8901

# View logs with verbose output
databasin pipelines logs 8901 --verbose

# Example successful output:
# [2025-12-11 06:00:01] Pipeline execution started
# [2025-12-11 06:00:05] Connected to source: Production PostgreSQL
# [2025-12-11 06:00:06] Executing query: SELECT customer_id, email...
# [2025-12-11 06:00:12] Extracted 15,432 rows
# [2025-12-11 06:00:15] Connected to target: Analytics Snowflake
# [2025-12-11 06:00:45] Loaded 15,432 rows to customers table
# [2025-12-11 06:00:46] Pipeline execution completed successfully
```

## Step 12: Verify Data in Snowflake

Confirm the data was loaded correctly:

```bash
# Query the target Snowflake table
databasin sql exec 5765 "SELECT COUNT(*) as customer_count FROM customers"

# Sample the loaded data
databasin sql exec 5765 "SELECT * FROM customers LIMIT 10"

# Compare counts between source and target
echo "Source count:" && databasin sql exec 5459 "SELECT COUNT(*) FROM customers WHERE status = 'active'" --json | jq '.[0]'
echo "Target count:" && databasin sql exec 5765 "SELECT COUNT(*) FROM customers" --json | jq '.[0]'
```

## Troubleshooting

### Pipeline Fails with "Connection Timeout"

```bash
# Test connectors individually
databasin connectors test 5459
databasin connectors test 5765

# Check connector configuration
databasin connectors get 5459
```

### Data Count Mismatch

```bash
# View pipeline artifact logs for details
databasin pipelines artifacts logs <artifact-id>

# Check for data quality issues in source
databasin sql exec 5459 "
  SELECT
    COUNT(*) as total,
    COUNT(*) - COUNT(email) as missing_emails,
    COUNT(DISTINCT email) as unique_emails
  FROM customers
  WHERE status = 'active'
"
```

### Schedule Not Running

```bash
# Verify pipeline configuration
databasin pipelines get 8901 --json | jq '.artifacts[0].schedule'

# Check recent execution history
databasin pipelines history 8901 --limit 20
```

## Advanced: Clone Pipeline for Different Environment

Once you have a working pipeline, clone it for staging or development:

```bash
# Clone to development environment with different connectors
databasin pipelines clone 8901 \
  --name "Dev Customer Sync" \
  --source 5555 \
  --target 6666 \
  --schedule "0 */6 * * *" \
  --project K9mPx2

# Preview clone changes before creating
databasin pipelines clone 8901 --dry-run --project K9mPx2
```

## Summary

This workflow demonstrated:

1. ✅ Authentication and project identification **using internal project IDs**
2. ✅ Creating and testing data connectors
3. ✅ Exploring source data structure
4. ✅ Building a pipeline configuration **with proper projectID references**
5. ✅ Validating before deployment
6. ✅ Creating and testing the pipeline **using the --project argument**
7. ✅ Monitoring execution
8. ✅ Troubleshooting common issues
9. ✅ Cloning for different environments

## Key Takeaways

- **Always use project internal IDs**: Use the numeric ID from `databasin auth whoami`, not the project name
- **Test connectors before pipelines**: Verify each connector works independently
- **Validate configurations**: Use `databasin pipelines validate` before creating
- **Monitor logs**: Always check `databasin pipelines logs` after execution
- **Start simple**: Test with small data samples before full production runs
- **Use cloning**: Duplicate working pipelines for new environments instead of recreating from scratch
