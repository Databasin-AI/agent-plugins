# Troubleshooting a Failed Pipeline

This example demonstrates how to diagnose and fix a pipeline that's failing using the Databasin CLI.

## Scenario

Your "Daily Sales Sync" pipeline (ID: 7234) is showing as failed in the dashboard. You need to investigate and resolve the issue.

## Step 1: Check Pipeline Status and Recent Runs

```bash
# Get pipeline details including status
databasin pipelines get 7234

# View recent execution history
databasin pipelines history 7234 --limit 10

# Example output showing failures:
# ┌────────┬─────────────────────┬────────┬──────────────────────┐
# │ Run ID │ Started At          │ Status │ Duration             │
# ├────────┼─────────────────────┼────────┼──────────────────────┤
# │ 15234  │ 2025-12-11 06:00:00 │ FAILED │ 0:02:15              │
# │ 15233  │ 2025-12-10 06:00:00 │ FAILED │ 0:02:18              │
# │ 15232  │ 2025-12-09 06:00:00 │ FAILED │ 0:02:12              │
# │ 15231  │ 2025-12-08 06:00:00 │ SUCCESS│ 0:15:43              │
# └────────┴─────────────────────┴────────┴──────────────────────┘
```

**Observation:** Pipeline started failing on Dec 9. It was working fine on Dec 8.

## Step 2: Examine Pipeline Logs

**CRITICAL:** Always check logs first when troubleshooting:

```bash
# View latest pipeline logs
databasin pipelines logs 7234

# Example error output:
# [2025-12-11 06:00:01] Pipeline execution started
# [2025-12-11 06:00:05] Connected to source: Production MySQL
# [2025-12-11 06:00:06] Executing query: SELECT order_id, customer_id...
# [2025-12-11 06:00:12] ERROR: Column 'payment_method' does not exist in table 'orders'
# [2025-12-11 06:00:12] Pipeline execution failed
# [2025-12-11 06:00:15] Sending failure notification to sales-team@company.com
```

**Root Cause Identified:** The query references a column `payment_method` that no longer exists.

## Step 3: Investigate Source Schema Changes

Verify what changed in the source database:

```bash
# Get current schema of the orders table
databasin sql exec 5678 "
  SELECT column_name, data_type
  FROM information_schema.columns
  WHERE table_name = 'orders'
  ORDER BY ordinal_position
"

# Example output:
# column_name       | data_type
# ------------------|----------
# order_id          | integer
# customer_id       | integer
# order_date        | timestamp
# total_amount      | numeric
# payment_type      | varchar    ← CHANGED from 'payment_method'
# status            | varchar
```

**Finding:** Column was renamed from `payment_method` to `payment_type`.

## Step 4: Review Current Pipeline Configuration

```bash
# Get full pipeline configuration
databasin pipelines get 7234 --json | jq '.artifacts[0].sourceQuery'

# Output:
# "SELECT order_id, customer_id, order_date, total_amount, payment_method, status FROM orders WHERE order_date >= CURRENT_DATE - INTERVAL '1 day'"
```

## Step 5: Update Pipeline Configuration

Create an updated configuration file:

```bash
# First, get the current config as a starting point
databasin pipelines get 7234 --json > pipeline-7234.json

# Edit the configuration file to fix the column name
# Change "payment_method" to "payment_type" in the sourceQuery

cat > pipeline-7234-fixed.json << EOF
{
  "name": "Daily Sales Sync",
  "description": "Sync yesterday's sales orders to analytics warehouse",
  "projectID": "N1r8Do",
  "sourceConnectorID": 5678,
  "targetConnectorID": 5765,
  "artifacts": [
    {
      "name": "Daily Orders Extract",
      "sourceQuery": "SELECT order_id, customer_id, order_date, total_amount, payment_type, status FROM orders WHERE order_date >= CURRENT_DATE - INTERVAL '1 day'",
      "targetTable": "daily_orders",
      "targetSchema": "sales",
      "writeMode": "APPEND",
      "schedule": {
        "enabled": true,
        "cron": "0 6 * * *",
        "timezone": "America/New_York"
      }
    }
  ]
}
EOF
```

**IMPORTANT:** Use the project's internal ID (N1r8Do) when updating the pipeline configuration.

## Step 6: Validate the Fixed Configuration

```bash
# Always validate before updating
databasin pipelines validate pipeline-7234-fixed.json

# Expected output:
# ✓ Pipeline configuration is valid
# ✓ Source connector exists and is accessible
# ✓ Target connector exists and is accessible
# ✓ SQL query syntax is valid
# ✓ All referenced columns exist in source table
```

## Step 7: Update the Pipeline

```bash
# Update the pipeline with fixed configuration (use project ID)
databasin pipelines update 7234 pipeline-7234-fixed.json --project N1r8Do

# Confirm update
# Pipeline 7234 updated successfully
```

## Step 8: Test the Fixed Pipeline

```bash
# Run the pipeline manually to test
databasin pipelines run 7234

# Monitor the logs in real-time
databasin pipelines logs 7234

# Expected successful output:
# [2025-12-11 08:15:01] Pipeline execution started
# [2025-12-11 08:15:05] Connected to source: Production MySQL
# [2025-12-11 08:15:06] Executing query: SELECT order_id, customer_id...
# [2025-12-11 08:15:12] Extracted 1,247 rows
# [2025-12-11 08:15:15] Connected to target: Analytics Snowflake
# [2025-12-11 08:15:45] Loaded 1,247 rows to sales.daily_orders table
# [2025-12-11 08:15:46] Pipeline execution completed successfully
```

## Step 9: Verify Data in Target

```bash
# Check that data was loaded
databasin sql exec 5765 "
  SELECT COUNT(*) as loaded_today
  FROM sales.daily_orders
  WHERE DATE(order_date) = CURRENT_DATE - INTERVAL '1 day'
"

# Verify payment_type column has data
databasin sql exec 5765 "
  SELECT payment_type, COUNT(*) as count
  FROM sales.daily_orders
  WHERE DATE(order_date) = CURRENT_DATE - INTERVAL '1 day'
  GROUP BY payment_type
"
```

## Common Pipeline Failure Scenarios

### Scenario 1: Connection Timeout

**Error:** "Connection to source connector timed out"

```bash
# Test source connector
databasin connectors test 5678

# If test fails, check connector config
databasin connectors get 5678

# Possible solutions:
# - Verify credentials haven't expired
# - Check network connectivity
# - Verify database is running and accessible
```

### Scenario 2: Permission Denied

**Error:** "Permission denied for table 'customers'"

```bash
# Test with a simple query
databasin sql exec 5678 "SELECT 1"  # Works

databasin sql exec 5678 "SELECT * FROM customers LIMIT 1"  # Fails

# Solution: Contact database admin to grant READ permissions
# Or update connector to use an account with proper permissions
```

### Scenario 3: Target Table Doesn't Exist

**Error:** "Table 'analytics.customers' does not exist"

```bash
# Check if table exists
databasin sql tables 5765 --catalog analytics --schema public

# Create the table first, then re-run pipeline
databasin sql exec 5765 "
  CREATE TABLE analytics.customers (
    customer_id INT,
    email VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP
  )
"
```

### Scenario 4: Data Type Mismatch

**Error:** "Cannot insert value of type VARCHAR into column of type INTEGER"

```bash
# Check source data types
databasin sql exec 5678 "
  SELECT column_name, data_type
  FROM information_schema.columns
  WHERE table_name = 'source_table'
"

# Check target data types
databasin sql exec 5765 "
  SELECT column_name, data_type
  FROM information_schema.columns
  WHERE table_name = 'target_table'
"

# Solution: Either:
# 1. Cast in the source query: CAST(column AS VARCHAR)
# 2. Alter target table schema to match source
```

### Scenario 5: Schedule Not Executing

**Problem:** Pipeline configured to run daily, but hasn't executed

```bash
# Check pipeline schedule configuration
databasin pipelines get 7234 --json | jq '.artifacts[0].schedule'

# Verify schedule is enabled
# {
#   "enabled": false,  ← Problem: schedule is disabled
#   "cron": "0 6 * * *",
#   "timezone": "America/New_York"
# }

# Solution: Update configuration to enable schedule
```

## Debugging Workflow Checklist

When a pipeline fails, follow this systematic approach:

1. **Check execution history** - `databasin pipelines history <id>`
2. **Read the logs** - `databasin pipelines logs <id>` (ALWAYS DO THIS FIRST)
3. **Test source connector** - `databasin connectors test <source-id>`
4. **Test target connector** - `databasin connectors test <target-id>`
5. **Verify source query** - Run the query directly with `databasin sql exec`
6. **Check schema compatibility** - Compare source and target schemas
7. **Review recent changes** - What changed since it last worked?
8. **Update and validate** - Fix config and validate before updating
9. **Test the fix** - Run manually before re-enabling schedule
10. **Monitor next scheduled run** - Confirm it works automatically

## Enable Debug Mode

For more detailed diagnostics:

```bash
# Run with debug enabled
DATABASIN_DEBUG=true databasin pipelines run 7234

# Debug output includes:
# - Full SQL queries with parameters
# - Detailed connection information
# - Stack traces for errors
# - API request/response details
```

## Preventive Monitoring

Set up monitoring to catch failures quickly:

```bash
# Create a monitoring script
cat > check-pipelines.sh << 'EOF'
#!/bin/bash

# Get all pipelines in project (use your project ID)
PIPELINES=$(databasin pipelines list --project N1r8Do --json | jq -r '.[].pipelineID')

for PIPELINE_ID in $PIPELINES; do
  # Get latest run status
  STATUS=$(databasin pipelines history $PIPELINE_ID --limit 1 --json | jq -r '.[0].status')

  if [ "$STATUS" = "FAILED" ]; then
    echo "⚠️  Pipeline $PIPELINE_ID FAILED"
    databasin pipelines logs $PIPELINE_ID | grep ERROR
  fi
done
EOF

chmod +x check-pipelines.sh

# Run daily via cron
# 0 7 * * * /path/to/check-pipelines.sh
```

## Summary

This workflow demonstrated:

1. ✅ Systematic troubleshooting using logs
2. ✅ Identifying schema changes as root cause
3. ✅ Validating fixes before deployment
4. ✅ Testing pipelines after updates
5. ✅ Common failure scenarios and solutions
6. ✅ Debug mode for detailed diagnostics
7. ✅ Preventive monitoring scripts

## Key Takeaways

- **Always check logs first**: `databasin pipelines logs <id>` is your best diagnostic tool
- **Test connectors individually**: Isolate whether the issue is source, target, or transformation
- **Validate before updating**: Use `databasin pipelines validate` to catch errors early
- **Use project IDs consistently**: Always pass `--project <internal-id>` when working with pipelines
- **Monitor proactively**: Set up automated checks to catch failures quickly
- **Enable debug mode when stuck**: `DATABASIN_DEBUG=true` provides detailed diagnostics
