# Connector Inspection and Pipeline Cloning

This example demonstrates how to use the `databasin connectors inspect` command for comprehensive connector analysis and the `databasin pipelines clone` command for rapid pipeline deployment across environments.

## Part 1: Comprehensive Connector Inspection

The `inspect` command provides an all-in-one view of a connector's status, configuration, database structure, and usage.

### Basic Connector Inspection

```bash
# Inspect by connector ID
databasin connectors inspect 5459

# Inspect by name (finds first match)
databasin connectors inspect "production postgres"

# Example output:
# ════════════════════════════════════════════════════════════════
# CONNECTOR INSPECTION REPORT
# ════════════════════════════════════════════════════════════════
#
# 📋 BASIC INFORMATION
# ────────────────────────────────────────────────────────────────
# ID:              5459
# Name:            Production PostgreSQL
# Type:            Postgres
# Status:          Active
# Created:         2024-11-15 14:23:45
# Last Modified:   2025-12-10 09:15:22
# Project ID:      456
#
# 🔌 CONNECTION STATUS
# ────────────────────────────────────────────────────────────────
# ✓ Connection Test: PASSED
# ✓ Response Time: 45ms
# ✓ Database Version: PostgreSQL 14.5
#
# ⚙️  CONFIGURATION
# ────────────────────────────────────────────────────────────────
# Host:            db.prod.company.com
# Port:            5432
# Database:        production_db
# Username:        databasin_ro
# SSL Enabled:     Yes
# Connection Pool: 10
#
# 🗄️  DATABASE STRUCTURE
# ────────────────────────────────────────────────────────────────
# Catalogs:        1 (production_db)
# Schemas:         5 (public, sales, inventory, hr, analytics)
# Tables:          47 total
#   └─ public:     23 tables
#   └─ sales:      12 tables
#   └─ inventory:  8 tables
#   └─ hr:         3 tables
#   └─ analytics:  1 table
#
# 📊 TOP TABLES BY SIZE
# ────────────────────────────────────────────────────────────────
# 1. public.user_activity        2.3M rows
# 2. public.transactions         1.8M rows
# 3. sales.orders                892K rows
# 4. public.customers            156K rows
# 5. inventory.stock_movements   89K rows
#
# 🔗 PIPELINE USAGE
# ────────────────────────────────────────────────────────────────
# Used in 12 pipelines:
#   └─ As Source:  8 pipelines
#   └─ As Target:  4 pipelines
#
# Active Pipelines:
# • Pipeline 7234: Daily Sales Sync (Source)
# • Pipeline 7856: Inventory Updates (Source)
# • Pipeline 8901: Customer Data Export (Source)
# • Pipeline 9102: Analytics Refresh (Target)
#
# 💡 QUICK ACTIONS
# ────────────────────────────────────────────────────────────────
# Explore database:
#   databasin sql discover 5459
#
# List all tables:
#   databasin sql tables 5459 --catalog production_db --schema public
#
# View pipelines using this connector:
#   databasin pipelines list --project N1r8Do --json | jq '.[] | select(.sourceConnectorID==5459 or .targetConnectorID==5459)'
#
# Create new pipeline from this connector:
#   databasin pipelines wizard --source 5459 --project N1r8Do
```

### Using Inspect for Troubleshooting

When a connector is experiencing issues:

```bash
# Inspect to see connection status
databasin connectors inspect 5678

# Example output showing problems:
# 🔌 CONNECTION STATUS
# ────────────────────────────────────────────────────────────────
# ✗ Connection Test: FAILED
# ✗ Error: Connection timeout after 30s
# ✗ Last Successful Connection: 2025-12-09 15:30:00 (2 days ago)
#
# 💡 TROUBLESHOOTING STEPS:
# 1. Verify database is running:
#    ping db.prod.company.com
#
# 2. Check credentials:
#    databasin connectors get 5678 --json | jq '.config'
#
# 3. Test with manual connection:
#    psql -h db.prod.company.com -U databasin_ro -d production_db
#
# 4. Review connector configuration:
#    databasin connectors update 5678 updated-config.json
```

### Inspect Before Building Pipelines

Use inspect to understand available data before creating pipelines:

```bash
# Step 1: Inspect source connector
databasin connectors inspect 5459

# Review the "DATABASE STRUCTURE" and "TOP TABLES BY SIZE" sections
# to identify relevant tables

# Step 2: Get detailed table information
databasin sql tables 5459 --catalog production_db --schema sales

# Step 3: Sample data from identified tables
databasin sql exec 5459 "SELECT * FROM sales.orders LIMIT 5"

# Step 4: Check if connector is already used in similar pipelines
# (shown in "PIPELINE USAGE" section of inspect output)
databasin pipelines get 7234  # Review existing pipeline configuration
```

## Part 2: Pipeline Cloning for Environment Promotion

The `clone` command allows you to quickly duplicate pipelines with modifications, perfect for promoting tested pipelines from dev → staging → production.

### Basic Pipeline Cloning

```bash
# Clone with default name (adds " (Clone)" suffix)
databasin pipelines clone 8901 --project N1r8Do

# Example output:
# Pipeline cloned successfully
# Original Pipeline ID: 8901
# New Pipeline ID: 9234
# New Pipeline Name: Customer Data Export (Clone)
```

### Clone with Custom Name

```bash
# Clone with a descriptive name
databasin pipelines clone 8901 \
  --name "Customer Data Export - Staging" \
  --project N1r8Do

# Output:
# Pipeline cloned successfully
# Original Pipeline ID: 8901
# New Pipeline ID: 9235
# New Pipeline Name: Customer Data Export - Staging
```

### Clone with Different Connectors

Promote a pipeline from dev to production with different connectors:

```bash
# List available connectors to find prod IDs
databasin connectors list --full --fields connectorID,connectorName,connectorType --project N1r8Do

# Example output:
# Dev Environment:
#   5111 - Dev PostgreSQL (Source)
#   5222 - Dev Snowflake (Target)
#
# Prod Environment:
#   5459 - Production PostgreSQL (Source)
#   5765 - Production Snowflake (Target)

# Clone dev pipeline to prod with prod connectors
databasin pipelines clone 7777 \
  --name "Customer Sync - Production" \
  --source 5459 \
  --target 5765 \
  --project N1r8Do

# Output:
# Pipeline cloned successfully
# Changes applied:
#   • Name: Customer Sync - Production
#   • Source Connector: 5111 → 5459 (Dev PostgreSQL → Production PostgreSQL)
#   • Target Connector: 5222 → 5765 (Dev Snowflake → Production Snowflake)
# Original Pipeline ID: 7777
# New Pipeline ID: 9236
```

### Clone with Modified Schedule

```bash
# Clone and change schedule from hourly to daily
databasin pipelines clone 8901 \
  --name "Customer Sync - Less Frequent" \
  --schedule "0 6 * * *" \
  --project N1r8Do

# Schedule examples:
# "0 6 * * *"      = Daily at 6:00 AM
# "0 */6 * * *"    = Every 6 hours
# "0 0 * * 0"      = Weekly on Sunday at midnight
# "0 0 1 * *"      = Monthly on the 1st at midnight
# "*/15 * * * *"   = Every 15 minutes
```

### Preview Clone Changes (Dry Run)

Always preview changes before creating the clone:

```bash
# Dry run to see what would be created
databasin pipelines clone 8901 \
  --name "Test Clone" \
  --source 5555 \
  --target 6666 \
  --schedule "0 */2 * * *" \
  --dry-run \
  --project N1r8Do

# Example output:
# DRY RUN - Pipeline would be created with these changes:
# ═══════════════════════════════════════════════════════════
# Original Pipeline: 8901 - Customer Data Export
#
# PROPOSED CHANGES:
# ├─ Name: "Customer Data Export" → "Test Clone"
# ├─ Source Connector: 5459 → 5555
# ├─ Target Connector: 5765 → 6666
# └─ Schedule: "0 6 * * *" → "0 */2 * * *"
#
# UNCHANGED:
# ├─ Description: "Daily export of customer data..."
# ├─ Artifacts: 1 artifact (Active Customers Extract)
# ├─ Transformations: 2 transformations
# └─ Notifications: 3 recipients
#
# To create this pipeline, remove the --dry-run flag
```

### Complete Environment Promotion Workflow

**Scenario:** Promote a tested dev pipeline to staging and production

```bash
# Step 1: Verify dev pipeline works
databasin pipelines get 7001  # Dev pipeline
databasin pipelines history 7001 --limit 5  # Check recent runs

# Step 2: Identify connector IDs for staging
databasin connectors search "staging" --project N1r8Do

# Staging connectors:
#   5333 - Staging PostgreSQL
#   5444 - Staging Snowflake

# Step 3: Clone to staging with preview
databasin pipelines clone 7001 \
  --name "Customer Sync - Staging" \
  --source 5333 \
  --target 5444 \
  --dry-run \
  --project N1r8Do

# Step 4: Create staging pipeline
databasin pipelines clone 7001 \
  --name "Customer Sync - Staging" \
  --source 5333 \
  --target 5444 \
  --project N1r8Do

# Output: Pipeline cloned successfully, New Pipeline ID: 7002

# Step 5: Test staging pipeline
databasin pipelines run 7002
databasin pipelines logs 7002

# Step 6: After staging validation, clone to production
databasin connectors search "production" --project N1r8Do

# Production connectors:
#   5459 - Production PostgreSQL
#   5765 - Production Snowflake

databasin pipelines clone 7001 \
  --name "Customer Sync - Production" \
  --source 5459 \
  --target 5765 \
  --project N1r8Do

# Output: Pipeline cloned successfully, New Pipeline ID: 7003

# Step 7: Verify production pipeline
databasin pipelines get 7003
databasin pipelines run 7003
databasin pipelines logs 7003
```

### Clone for Testing Different Schedules

```bash
# Original pipeline runs daily
databasin pipelines get 8901 --json | jq '.artifacts[0].schedule.cron'
# Output: "0 6 * * *"

# Clone to test hourly execution
databasin pipelines clone 8901 \
  --name "Customer Sync - Hourly Test" \
  --schedule "0 * * * *" \
  --project N1r8Do

# Clone to test weekly execution
databasin pipelines clone 8901 \
  --name "Customer Sync - Weekly Test" \
  --schedule "0 6 * * 0" \
  --project N1r8Do
```

### Clone Multiple Pipelines in Bulk

Promote multiple dev pipelines to staging:

```bash
#!/bin/bash

# Get all dev pipelines (assuming they follow naming pattern)
DEV_PIPELINES=$(databasin pipelines list --project K9mPx2 --json | jq -r '.[] | select(.name | contains("Dev")) | .pipelineID')

# Staging connector IDs
STAGING_SOURCE=5333
STAGING_TARGET=5444

for PIPELINE_ID in $DEV_PIPELINES; do
  # Get original name
  ORIGINAL_NAME=$(databasin pipelines get $PIPELINE_ID --json | jq -r '.name')
  # Generate staging name
  STAGING_NAME="${ORIGINAL_NAME/Dev/Staging}"

  echo "Cloning pipeline $PIPELINE_ID: $ORIGINAL_NAME → $STAGING_NAME"

  # Clone with new connectors
  databasin pipelines clone $PIPELINE_ID \
    --name "$STAGING_NAME" \
    --source $STAGING_SOURCE \
    --target $STAGING_TARGET \
    --project N1r8Do

  echo "---"
done
```

## Advanced Use Cases

### Clone with Connector Inspection

Verify connectors before cloning:

```bash
# Step 1: Inspect original pipeline's connectors
ORIGINAL_PIPELINE=8901
SOURCE_ID=$(databasin pipelines get $ORIGINAL_PIPELINE --json | jq -r '.sourceConnectorID')
TARGET_ID=$(databasin pipelines get $ORIGINAL_PIPELINE --json | jq -r '.targetConnectorID')

# Step 2: Inspect both connectors
databasin connectors inspect $SOURCE_ID
databasin connectors inspect $TARGET_ID

# Step 3: Identify equivalent connectors in target environment
databasin connectors search "production postgres" --project N1r8Do
databasin connectors search "production snowflake" --project N1r8Do

# Step 4: Clone with new connectors
databasin pipelines clone $ORIGINAL_PIPELINE \
  --name "Migrated to Production" \
  --source 5459 \
  --target 5765 \
  --project N1r8Do
```

### Create Pipeline Backup Before Modifications

```bash
# Before making changes to a production pipeline, create a backup
databasin pipelines clone 9001 \
  --name "Production Customer Sync - BACKUP $(date +%Y%m%d)" \
  --project N1r8Do

# Now safe to modify the original
databasin pipelines update 9001 modified-config.json --project N1r8Do

# If update fails, you can clone the backup back
databasin pipelines clone 9002 \
  --name "Production Customer Sync" \
  --project N1r8Do
```

## Summary

This workflow demonstrated:

1. ✅ Using `connectors inspect` for comprehensive connector analysis
2. ✅ Understanding database structure before building pipelines
3. ✅ Troubleshooting connectors with inspect output
4. ✅ Basic pipeline cloning operations
5. ✅ Environment promotion workflows (dev → staging → prod)
6. ✅ Testing different schedules with clones
7. ✅ Previewing changes with `--dry-run`
8. ✅ Bulk cloning operations
9. ✅ Creating pipeline backups before modifications

## Key Takeaways

- **Use `inspect` first**: Get a comprehensive view of connectors before building pipelines
- **Always use project IDs**: Pass `--project <internal-id>` consistently throughout workflows
- **Preview with `--dry-run`**: Always check changes before creating clones
- **Clone for promotion**: Fastest way to move pipelines between environments
- **Clone for testing**: Test schedule/connector variations without affecting originals
- **Create backups**: Clone pipelines before making risky modifications
- **Inspect shows usage**: The "PIPELINE USAGE" section shows which pipelines use a connector
- **Inspect for troubleshooting**: Connection status and quick actions help diagnose issues quickly
