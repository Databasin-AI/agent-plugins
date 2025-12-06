# Advanced Databasin CLI Workflows

Comprehensive guide for complex data engineering workflows using the Databasin CLI.

---

## Schema Discovery and Data Exploration

### Complete Schema Discovery Workflow

Use this systematic approach to fully understand a new data source:

```bash
#!/bin/bash
# schema-discovery.sh - Complete schema exploration workflow

CONNECTOR_ID="$1"

if [ -z "$CONNECTOR_ID" ]; then
  echo "Usage: $0 <connector-id>"
  exit 1
fi

echo "=== Schema Discovery for Connector: $CONNECTOR_ID ==="

# Step 1: Verify connectivity
echo -e "\n[1/5] Testing connectivity..."
databasin sql exec $CONNECTOR_ID "SELECT 1 AS connection_test"

# Step 2: List all catalogs/databases
echo -e "\n[2/5] Discovering catalogs..."
databasin sql catalogs $CONNECTOR_ID --json > catalogs.json
cat catalogs.json | jq -r '.[]'

# Step 3: For each catalog, list schemas
echo -e "\n[3/5] Discovering schemas..."
for catalog in $(cat catalogs.json | jq -r '.[]'); do
  echo "  Catalog: $catalog"
  databasin sql schemas $CONNECTOR_ID --catalog "$catalog" --json > "schemas_${catalog}.json"
  cat "schemas_${catalog}.json" | jq -r '.[] | "    - \(.)"'
done

# Step 4: For each schema, list tables
echo -e "\n[4/5] Discovering tables..."
for catalog in $(cat catalogs.json | jq -r '.[]'); do
  for schema in $(cat "schemas_${catalog}.json" | jq -r '.[]'); do
    echo "  $catalog.$schema:"
    databasin sql tables $CONNECTOR_ID \
      --catalog "$catalog" \
      --schema "$schema" \
      --json > "tables_${catalog}_${schema}.json"
    cat "tables_${catalog}_${schema}.json" | jq -r '.[] | "    - \(.)"'
  done
done

# Step 5: Generate schema documentation
echo -e "\n[5/5] Generating schema documentation..."
cat > "schema_inventory_${CONNECTOR_ID}.md" << 'EOF'
# Schema Inventory

## Connector Information
- **Connector ID:** ${CONNECTOR_ID}
- **Discovery Date:** $(date)

## Database Structure

EOF

for catalog in $(cat catalogs.json | jq -r '.[]'); do
  echo "### Catalog: $catalog" >> "schema_inventory_${CONNECTOR_ID}.md"
  for schema in $(cat "schemas_${catalog}.json" | jq -r '.[]'); do
    echo "#### Schema: $schema" >> "schema_inventory_${CONNECTOR_ID}.md"
    echo '```' >> "schema_inventory_${CONNECTOR_ID}.md"
    cat "tables_${catalog}_${schema}.json" | jq -r '.[]' >> "schema_inventory_${CONNECTOR_ID}.md"
    echo '```' >> "schema_inventory_${CONNECTOR_ID}.md"
  done
done

echo "Schema inventory saved to: schema_inventory_${CONNECTOR_ID}.md"
```

### Interactive Schema Explorer

Explore table structures with detailed column information:

```bash
#!/bin/bash
# explore-table.sh - Deep dive into table structure

CONNECTOR_ID="$1"
TABLE_NAME="$2"
CATALOG="${3:-public}"
SCHEMA="${4:-public}"

# Get detailed column information
databasin sql exec $CONNECTOR_ID "
SELECT
  column_name,
  data_type,
  character_maximum_length,
  is_nullable,
  column_default,
  ordinal_position
FROM information_schema.columns
WHERE table_catalog = '$CATALOG'
  AND table_schema = '$SCHEMA'
  AND table_name = '$TABLE_NAME'
ORDER BY ordinal_position
" --csv > "${TABLE_NAME}_structure.csv"

# Get row count
ROW_COUNT=$(databasin sql exec $CONNECTOR_ID \
  "SELECT COUNT(*) as count FROM ${CATALOG}.${SCHEMA}.${TABLE_NAME}" \
  --json | jq -r '.[0].count')

# Get sample data
databasin sql exec $CONNECTOR_ID \
  "SELECT * FROM ${CATALOG}.${SCHEMA}.${TABLE_NAME} LIMIT 5" \
  --csv > "${TABLE_NAME}_sample.csv"

# Get primary key information
databasin sql exec $CONNECTOR_ID "
SELECT
  kcu.column_name,
  tc.constraint_type
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
  ON tc.constraint_name = kcu.constraint_name
WHERE tc.table_name = '$TABLE_NAME'
  AND tc.constraint_type IN ('PRIMARY KEY', 'FOREIGN KEY')
" --csv > "${TABLE_NAME}_constraints.csv"

echo "Table: $TABLE_NAME"
echo "Rows: $ROW_COUNT"
echo "Structure saved to: ${TABLE_NAME}_structure.csv"
echo "Sample data saved to: ${TABLE_NAME}_sample.csv"
echo "Constraints saved to: ${TABLE_NAME}_constraints.csv"
```

### Automated Data Profiling

Profile data quality and statistics for a table:

```bash
# data-profile.sh - Generate data quality profile

CONNECTOR_ID="$1"
TABLE_NAME="$2"

# Get all column names
COLUMNS=$(databasin sql exec $CONNECTOR_ID "
SELECT column_name
FROM information_schema.columns
WHERE table_name = '$TABLE_NAME'
" --json | jq -r '.[].column_name')

# Build comprehensive profiling query
PROFILE_QUERY="SELECT
  COUNT(*) as total_rows,
  COUNT(DISTINCT *) as unique_rows"

for col in $COLUMNS; do
  PROFILE_QUERY="$PROFILE_QUERY,
  COUNT($col) as ${col}_non_null,
  COUNT(DISTINCT $col) as ${col}_distinct,
  MIN($col) as ${col}_min,
  MAX($col) as ${col}_max"
done

PROFILE_QUERY="$PROFILE_QUERY FROM $TABLE_NAME"

# Execute profiling query
databasin sql exec $CONNECTOR_ID "$PROFILE_QUERY" --csv > "${TABLE_NAME}_profile.csv"

echo "Data profile saved to: ${TABLE_NAME}_profile.csv"
```

---

## Complex Pipeline Creation

### Pipeline Creation Workflow

Complete workflow for creating production-ready data pipelines:

```bash
#!/bin/bash
# create-pipeline.sh - Comprehensive pipeline creation workflow

SOURCE_CONNECTOR="$1"
TARGET_CONNECTOR="$2"
SOURCE_TABLE="$3"
TARGET_TABLE="$4"

echo "=== Pipeline Creation Workflow ==="

# Step 1: Verify source and target connectivity
echo -e "\n[1/7] Verifying source connectivity..."
databasin sql exec $SOURCE_CONNECTOR "SELECT 1 AS test" || exit 1

echo "[2/7] Verifying target connectivity..."
databasin sql exec $TARGET_CONNECTOR "SELECT 1 AS test" || exit 1

# Step 2: Analyze source schema
echo "[3/7] Analyzing source schema..."
databasin sql exec $SOURCE_CONNECTOR "
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = '$SOURCE_TABLE'
ORDER BY ordinal_position
" --csv > source_schema.csv

# Step 3: Analyze target schema
echo "[4/7] Analyzing target schema..."
databasin sql exec $TARGET_CONNECTOR "
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = '$TARGET_TABLE'
ORDER BY ordinal_position
" --csv > target_schema.csv

# Step 4: Compare schemas and identify transformations needed
echo "[5/7] Comparing schemas..."
diff source_schema.csv target_schema.csv || echo "Schema differences detected"

# Step 5: Sample source data to understand content
echo "[6/7] Sampling source data..."
databasin sql exec $SOURCE_CONNECTOR \
  "SELECT * FROM $SOURCE_TABLE LIMIT 10" \
  --csv > source_sample.csv

# Step 6: Create pipeline configuration
echo "[7/7] Creating pipeline configuration..."
cat > pipeline-config.json << EOF
{
  "name": "Sync ${SOURCE_TABLE} to ${TARGET_TABLE}",
  "description": "Automated sync from source to target",
  "sourceConnector": "$SOURCE_CONNECTOR",
  "targetConnector": "$TARGET_CONNECTOR",
  "sourceQuery": "SELECT * FROM $SOURCE_TABLE WHERE updated_at > :last_run_time",
  "targetTable": "$TARGET_TABLE",
  "transformations": [
    {
      "type": "filter",
      "condition": "id IS NOT NULL"
    },
    {
      "type": "map",
      "fields": {
        "id": "id",
        "name": "name",
        "email": "LOWER(email)",
        "created_at": "created_at",
        "updated_at": "updated_at"
      }
    }
  ],
  "loadStrategy": "upsert",
  "upsertKey": ["id"],
  "schedule": "0 */6 * * *",
  "enabled": true
}
EOF

# Create the pipeline
PIPELINE_ID=$(databasin pipelines create pipeline-config.json --json | jq -r '.id')
echo "Pipeline created: $PIPELINE_ID"

# Test run the pipeline
echo "Running initial pipeline test..."
databasin pipelines run $PIPELINE_ID

# Monitor the run
sleep 5
databasin pipelines logs $PIPELINE_ID

echo "Pipeline setup complete!"
echo "Pipeline ID: $PIPELINE_ID"
echo "Configuration saved to: pipeline-config.json"
```

### Incremental ETL Pipeline

Pipeline for incremental data loading with watermark tracking:

```json
{
  "name": "Incremental Customer Sync",
  "description": "Sync new/updated customers since last run",
  "sourceConnector": "source-mysql-prod",
  "targetConnector": "target-snowflake-warehouse",
  "sourceQuery": "SELECT * FROM customers WHERE updated_at > :watermark ORDER BY updated_at",
  "targetTable": "analytics.customers",
  "transformations": [
    {
      "type": "filter",
      "description": "Remove test accounts",
      "condition": "email NOT LIKE '%@test.com' AND status != 'deleted'"
    },
    {
      "type": "map",
      "description": "Standardize and enrich fields",
      "fields": {
        "customer_id": "id",
        "full_name": "CONCAT(first_name, ' ', last_name)",
        "email_normalized": "LOWER(TRIM(email))",
        "phone_formatted": "REGEXP_REPLACE(phone, '[^0-9]', '')",
        "signup_date": "created_at",
        "last_updated": "updated_at",
        "customer_lifetime_value": "COALESCE(total_orders_value, 0)",
        "is_premium": "subscription_tier IN ('premium', 'enterprise')"
      }
    },
    {
      "type": "deduplicate",
      "description": "Remove duplicates based on email",
      "keys": ["email_normalized"],
      "keepFirst": false
    }
  ],
  "loadStrategy": "upsert",
  "upsertKey": ["customer_id"],
  "watermarkColumn": "updated_at",
  "schedule": "*/15 * * * *",
  "enabled": true,
  "errorHandling": {
    "onFailure": "retry",
    "maxRetries": 3,
    "retryDelay": 300
  }
}
```

### Complex Multi-Stage Pipeline

Pipeline with multiple stages for data validation and enrichment:

```json
{
  "name": "E-commerce Order Processing Pipeline",
  "description": "Multi-stage order data processing with validation and enrichment",
  "stages": [
    {
      "name": "extract_orders",
      "sourceConnector": "prod-postgresql",
      "sourceQuery": "SELECT o.*, c.email, c.name as customer_name FROM orders o JOIN customers c ON o.customer_id = c.id WHERE o.created_at >= CURRENT_DATE - INTERVAL '1 day'",
      "transformations": [
        {
          "type": "validate",
          "rules": {
            "order_id": "NOT NULL",
            "customer_id": "NOT NULL",
            "total_amount": "> 0",
            "status": "IN ('pending', 'processing', 'completed', 'cancelled')"
          },
          "onValidationFailed": "quarantine"
        }
      ]
    },
    {
      "name": "enrich_with_product_data",
      "sourceConnector": "prod-postgresql",
      "sourceQuery": "SELECT oi.order_id, p.category, p.brand, SUM(oi.quantity) as total_items FROM order_items oi JOIN products p ON oi.product_id = p.id WHERE oi.order_id IN (:order_ids) GROUP BY oi.order_id, p.category, p.brand",
      "joinOn": "order_id"
    },
    {
      "name": "calculate_metrics",
      "transformations": [
        {
          "type": "map",
          "fields": {
            "order_id": "order_id",
            "customer_id": "customer_id",
            "customer_email": "email",
            "customer_name": "customer_name",
            "order_total": "total_amount",
            "order_date": "created_at",
            "order_status": "status",
            "product_category": "category",
            "product_brand": "brand",
            "total_items": "total_items",
            "avg_item_price": "total_amount / NULLIF(total_items, 0)",
            "is_high_value": "total_amount > 1000",
            "processing_timestamp": "CURRENT_TIMESTAMP"
          }
        }
      ]
    },
    {
      "name": "load_to_warehouse",
      "targetConnector": "snowflake-analytics",
      "targetTable": "analytics.enriched_orders",
      "loadStrategy": "append"
    }
  ],
  "schedule": "0 2 * * *",
  "enabled": true
}
```

---

## Advanced SQL Patterns

### Data Deduplication Strategy

Identify and remove duplicate records with sophisticated logic:

```bash
# Find duplicates with ranking
databasin sql exec $CONNECTOR_ID "
WITH ranked_duplicates AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY email
      ORDER BY updated_at DESC, created_at DESC
    ) as row_num
  FROM users
)
SELECT
  email,
  COUNT(*) as duplicate_count,
  MAX(CASE WHEN row_num = 1 THEN id END) as keep_id,
  STRING_AGG(
    CASE WHEN row_num > 1 THEN id::text END,
    ','
    ORDER BY updated_at DESC
  ) as delete_ids
FROM ranked_duplicates
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC
" --csv > duplicates_to_clean.csv

# Remove duplicates keeping most recent
databasin sql exec $CONNECTOR_ID "
DELETE FROM users
WHERE id IN (
  SELECT id
  FROM (
    SELECT
      id,
      ROW_NUMBER() OVER (
        PARTITION BY email
        ORDER BY updated_at DESC
      ) as row_num
    FROM users
  ) ranked
  WHERE row_num > 1
)
"
```

### Data Migration with Validation

Complete data migration workflow with pre and post validation:

```bash
#!/bin/bash
# data-migration.sh - Safe data migration with validation

SOURCE_CONN="$1"
TARGET_CONN="$2"
TABLE_NAME="$3"

echo "=== Data Migration with Validation ==="

# Pre-migration validation
echo "[1/6] Pre-migration validation..."

# Count source records
SOURCE_COUNT=$(databasin sql exec $SOURCE_CONN \
  "SELECT COUNT(*) as count FROM $TABLE_NAME" \
  --json | jq -r '.[0].count')
echo "Source records: $SOURCE_COUNT"

# Get source schema
databasin sql exec $SOURCE_CONN "
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = '$TABLE_NAME'
ORDER BY ordinal_position
" --csv > source_schema.csv

# Verify target table exists and schema matches
echo "[2/6] Verifying target schema..."
databasin sql exec $TARGET_CONN "
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = '$TABLE_NAME'
ORDER BY ordinal_position
" --csv > target_schema.csv

diff source_schema.csv target_schema.csv || {
  echo "ERROR: Schema mismatch!"
  exit 1
}

# Create backup of target (if data exists)
echo "[3/6] Creating target backup..."
TARGET_COUNT=$(databasin sql exec $TARGET_CONN \
  "SELECT COUNT(*) as count FROM $TABLE_NAME" \
  --json | jq -r '.[0].count')

if [ "$TARGET_COUNT" -gt 0 ]; then
  databasin sql exec $TARGET_CONN \
    "CREATE TABLE ${TABLE_NAME}_backup_$(date +%Y%m%d_%H%M%S) AS SELECT * FROM $TABLE_NAME"
fi

# Perform migration in batches
echo "[4/6] Migrating data in batches..."
BATCH_SIZE=10000
OFFSET=0

while [ $OFFSET -lt $SOURCE_COUNT ]; do
  echo "  Migrating batch: $OFFSET to $((OFFSET + BATCH_SIZE))"

  # Extract batch
  databasin sql exec $SOURCE_CONN \
    "SELECT * FROM $TABLE_NAME ORDER BY id LIMIT $BATCH_SIZE OFFSET $OFFSET" \
    --csv > batch_${OFFSET}.csv

  # Load batch (implementation depends on target connector)
  # For now, create SQL INSERT statements

  OFFSET=$((OFFSET + BATCH_SIZE))
done

# Post-migration validation
echo "[5/6] Post-migration validation..."

# Count target records
TARGET_COUNT_FINAL=$(databasin sql exec $TARGET_CONN \
  "SELECT COUNT(*) as count FROM $TABLE_NAME" \
  --json | jq -r '.[0].count')

echo "Target records after migration: $TARGET_COUNT_FINAL"

# Validate row counts match
if [ "$SOURCE_COUNT" -eq "$TARGET_COUNT_FINAL" ]; then
  echo "✓ Row count validation passed"
else
  echo "✗ Row count mismatch: Source=$SOURCE_COUNT, Target=$TARGET_COUNT_FINAL"
  exit 1
fi

# Sample data comparison
echo "[6/6] Comparing sample data..."
databasin sql exec $SOURCE_CONN \
  "SELECT * FROM $TABLE_NAME ORDER BY id LIMIT 100" \
  --csv > source_sample.csv

databasin sql exec $TARGET_CONN \
  "SELECT * FROM $TABLE_NAME ORDER BY id LIMIT 100" \
  --csv > target_sample.csv

diff source_sample.csv target_sample.csv && echo "✓ Sample data matches"

echo "Migration complete!"
```

### Data Quality Audit

Comprehensive data quality checks across multiple tables:

```bash
#!/bin/bash
# data-quality-audit.sh - Generate data quality report

CONNECTOR_ID="$1"
OUTPUT_DIR="quality_reports"
mkdir -p $OUTPUT_DIR

echo "=== Data Quality Audit ==="

# Get all tables
TABLES=$(databasin sql exec $CONNECTOR_ID "
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
" --json | jq -r '.[].table_name')

# For each table, generate quality report
for table in $TABLES; do
  echo "Auditing: $table"

  # Get columns
  COLUMNS=$(databasin sql exec $CONNECTOR_ID "
  SELECT column_name
  FROM information_schema.columns
  WHERE table_name = '$table'
  " --json | jq -r '.[].column_name')

  # Build quality check query
  QUALITY_SQL="SELECT
    '$table' as table_name,
    COUNT(*) as total_rows"

  for col in $COLUMNS; do
    QUALITY_SQL="$QUALITY_SQL,
    SUM(CASE WHEN $col IS NULL THEN 1 ELSE 0 END) as ${col}_nulls,
    COUNT(DISTINCT $col) as ${col}_distinct"
  done

  QUALITY_SQL="$QUALITY_SQL FROM $table"

  # Execute and save
  databasin sql exec $CONNECTOR_ID "$QUALITY_SQL" \
    --csv > "$OUTPUT_DIR/${table}_quality.csv"
done

# Generate summary report
cat > "$OUTPUT_DIR/quality_summary.md" << 'EOF'
# Data Quality Audit Report

Generated: $(date)

## Tables Audited

EOF

for table in $TABLES; do
  TOTAL=$(head -2 "$OUTPUT_DIR/${table}_quality.csv" | tail -1 | cut -d',' -f2)
  echo "- **$table**: $TOTAL rows" >> "$OUTPUT_DIR/quality_summary.md"
done

echo "Quality audit complete! Reports in: $OUTPUT_DIR/"
```

---

## Connector Configuration Examples

### PostgreSQL Connector

```json
{
  "name": "Production PostgreSQL",
  "type": "postgres",
  "config": {
    "host": "prod-db.company.com",
    "port": 5432,
    "database": "production",
    "username": "databasin_user",
    "password": "${POSTGRES_PASSWORD}",
    "ssl": true,
    "sslmode": "verify-full",
    "sslrootcert": "/path/to/ca-cert.pem",
    "connectionTimeout": 30000,
    "maxConnections": 10
  }
}
```

### Snowflake Connector

```json
{
  "name": "Snowflake Analytics Warehouse",
  "type": "snowflake",
  "config": {
    "account": "company.us-east-1",
    "username": "DATABASIN_SERVICE",
    "password": "${SNOWFLAKE_PASSWORD}",
    "warehouse": "ANALYTICS_WH",
    "database": "ANALYTICS_DB",
    "schema": "PUBLIC",
    "role": "DATABASIN_ROLE"
  }
}
```

### AWS S3 Connector

```json
{
  "name": "S3 Data Lake",
  "type": "s3",
  "config": {
    "region": "us-east-1",
    "bucket": "company-data-lake",
    "accessKeyId": "${AWS_ACCESS_KEY_ID}",
    "secretAccessKey": "${AWS_SECRET_ACCESS_KEY}",
    "prefix": "raw/",
    "format": "parquet"
  }
}
```

### MongoDB Connector

```json
{
  "name": "MongoDB Production",
  "type": "mongodb",
  "config": {
    "connectionString": "mongodb+srv://user:${MONGO_PASSWORD}@cluster.mongodb.net/",
    "database": "production",
    "authSource": "admin",
    "ssl": true,
    "replicaSet": "rs0"
  }
}
```

---

## Automation Workflows

### Scheduled Data Quality Checks

```json
{
  "name": "Daily Data Quality Monitoring",
  "description": "Run comprehensive data quality checks every morning",
  "trigger": {
    "type": "schedule",
    "schedule": "0 6 * * *"
  },
  "tasks": [
    {
      "name": "check_null_values",
      "type": "sql",
      "connector": "prod-database",
      "query": "SELECT table_name, column_name, COUNT(*) as null_count FROM information_schema.columns c JOIN (SELECT table_name FROM information_schema.tables WHERE table_schema = 'public') t USING(table_name) WHERE column_name IN (SELECT column_name FROM pg_stats WHERE null_frac > 0.05) GROUP BY table_name, column_name HAVING COUNT(*) > 100"
    },
    {
      "name": "check_duplicates",
      "type": "sql",
      "connector": "prod-database",
      "query": "SELECT 'users' as table_name, COUNT(*) as duplicates FROM (SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1) dups"
    },
    {
      "name": "alert_if_issues",
      "type": "notification",
      "condition": "tasks.check_null_values.row_count > 0 OR tasks.check_duplicates.duplicates > 0",
      "channels": ["email", "slack"]
    }
  ]
}
```

### Event-Driven Pipeline Trigger

```json
{
  "name": "Process New File Uploads",
  "description": "Automatically process files when uploaded to S3",
  "trigger": {
    "type": "event",
    "source": "s3-connector",
    "eventType": "file.created",
    "filter": {
      "path": "incoming/*.csv"
    }
  },
  "tasks": [
    {
      "name": "validate_file",
      "type": "sql",
      "connector": "s3-connector",
      "query": "SELECT COUNT(*) as row_count, COUNT(DISTINCT customer_id) as unique_customers FROM :event.file_path"
    },
    {
      "name": "load_to_staging",
      "type": "pipeline",
      "pipeline": "csv-to-staging-pipeline",
      "parameters": {
        "source_file": ":event.file_path"
      }
    },
    {
      "name": "archive_file",
      "type": "file_operation",
      "operation": "move",
      "source": ":event.file_path",
      "destination": "processed/:event.file_name"
    }
  ]
}
```

---

## Real-World Use Cases

### Use Case 1: Customer 360 View

Build a comprehensive customer view from multiple sources:

```bash
#!/bin/bash
# customer-360.sh - Build unified customer view

# Step 1: Extract customer data from CRM
databasin sql exec crm-salesforce "
SELECT
  id as customer_id,
  email,
  first_name,
  last_name,
  company,
  industry,
  created_date
FROM contacts
WHERE is_deleted = false
" --csv > customers_crm.csv

# Step 2: Extract order history from e-commerce database
databasin sql exec ecommerce-postgres "
SELECT
  customer_id,
  COUNT(*) as total_orders,
  SUM(total_amount) as lifetime_value,
  MAX(created_at) as last_order_date,
  AVG(total_amount) as avg_order_value
FROM orders
GROUP BY customer_id
" --csv > customers_orders.csv

# Step 3: Extract support tickets
databasin sql exec support-zendesk "
SELECT
  requester_id as customer_id,
  COUNT(*) as total_tickets,
  AVG(satisfaction_rating) as avg_satisfaction,
  MAX(created_at) as last_contact_date
FROM tickets
GROUP BY requester_id
" --csv > customers_support.csv

# Step 4: Merge data in target warehouse
# (This would typically be done via a pipeline, shown here for illustration)
databasin sql exec analytics-snowflake "
CREATE OR REPLACE TABLE customer_360 AS
SELECT
  c.customer_id,
  c.email,
  c.first_name,
  c.last_name,
  c.company,
  c.industry,
  c.created_date as customer_since,
  COALESCE(o.total_orders, 0) as total_orders,
  COALESCE(o.lifetime_value, 0) as lifetime_value,
  o.last_order_date,
  COALESCE(o.avg_order_value, 0) as avg_order_value,
  COALESCE(s.total_tickets, 0) as total_support_tickets,
  s.avg_satisfaction,
  s.last_contact_date,
  CASE
    WHEN o.lifetime_value > 10000 THEN 'VIP'
    WHEN o.lifetime_value > 5000 THEN 'Premium'
    WHEN o.total_orders > 5 THEN 'Regular'
    ELSE 'New'
  END as customer_tier
FROM customers c
LEFT JOIN orders_summary o ON c.customer_id = o.customer_id
LEFT JOIN support_summary s ON c.customer_id = s.customer_id
"
```

### Use Case 2: Real-Time Inventory Sync

Keep inventory in sync across systems:

```json
{
  "name": "Real-Time Inventory Sync",
  "description": "Sync inventory levels from warehouse to e-commerce platform in real-time",
  "sourceConnector": "warehouse-mysql",
  "targetConnector": "shopify-api",
  "sourceQuery": "SELECT sku, available_quantity, warehouse_location, last_updated FROM inventory WHERE last_updated > :watermark",
  "transformations": [
    {
      "type": "filter",
      "condition": "available_quantity >= 0"
    },
    {
      "type": "map",
      "fields": {
        "product_sku": "sku",
        "inventory_quantity": "available_quantity",
        "location": "warehouse_location",
        "sync_timestamp": "CURRENT_TIMESTAMP"
      }
    },
    {
      "type": "alert",
      "condition": "available_quantity < 10",
      "message": "Low stock alert for SKU: {sku}",
      "channels": ["email", "slack"]
    }
  ],
  "loadStrategy": "upsert",
  "upsertKey": ["product_sku"],
  "watermarkColumn": "last_updated",
  "schedule": "*/5 * * * *",
  "enabled": true
}
```

### Use Case 3: Financial Reporting Automation

Automated daily financial reporting:

```bash
#!/bin/bash
# financial-reporting.sh - Generate daily financial reports

REPORT_DATE=$(date +%Y-%m-%d)
CONNECTOR="finance-postgres"

# Revenue by product category
databasin sql exec $CONNECTOR "
SELECT
  DATE_TRUNC('day', order_date) as date,
  product_category,
  COUNT(DISTINCT order_id) as num_orders,
  SUM(total_amount) as revenue,
  AVG(total_amount) as avg_order_value
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE_TRUNC('day', order_date), product_category
ORDER BY date DESC, revenue DESC
" --csv > "revenue_by_category_${REPORT_DATE}.csv"

# Customer acquisition costs
databasin sql exec $CONNECTOR "
SELECT
  DATE_TRUNC('month', signup_date) as month,
  marketing_source,
  COUNT(*) as new_customers,
  SUM(acquisition_cost) as total_cac,
  AVG(acquisition_cost) as avg_cac,
  SUM(first_order_value) / NULLIF(COUNT(*), 0) as avg_first_order
FROM customers
WHERE signup_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', signup_date), marketing_source
ORDER BY month DESC
" --csv > "cac_analysis_${REPORT_DATE}.csv"

# Profit margins
databasin sql exec $CONNECTOR "
SELECT
  product_category,
  SUM(revenue) as total_revenue,
  SUM(cost_of_goods) as total_cogs,
  SUM(revenue - cost_of_goods) as gross_profit,
  (SUM(revenue - cost_of_goods) / NULLIF(SUM(revenue), 0)) * 100 as margin_percentage
FROM (
  SELECT
    p.category as product_category,
    oi.quantity * oi.unit_price as revenue,
    oi.quantity * p.cost as cost_of_goods
  FROM order_items oi
  JOIN products p ON oi.product_id = p.id
  JOIN orders o ON oi.order_id = o.id
  WHERE o.order_date >= CURRENT_DATE - INTERVAL '7 days'
) profit_calc
GROUP BY product_category
ORDER BY gross_profit DESC
" --csv > "profit_margins_${REPORT_DATE}.csv"

echo "Financial reports generated for $REPORT_DATE"
```

---

## Performance Optimization Patterns

### Batch Processing Strategy

Optimize large data transfers with batching:

```bash
#!/bin/bash
# batch-processor.sh - Process large datasets in optimal batches

CONNECTOR="$1"
TABLE="$2"
BATCH_SIZE=50000

# Get total row count
TOTAL_ROWS=$(databasin sql exec $CONNECTOR \
  "SELECT COUNT(*) as count FROM $TABLE" \
  --json | jq -r '.[0].count')

echo "Total rows to process: $TOTAL_ROWS"
echo "Batch size: $BATCH_SIZE"

BATCHES=$(( (TOTAL_ROWS + BATCH_SIZE - 1) / BATCH_SIZE ))
echo "Total batches: $BATCHES"

# Process each batch
for i in $(seq 0 $((BATCHES - 1))); do
  OFFSET=$((i * BATCH_SIZE))
  echo "Processing batch $((i + 1))/$BATCHES (offset: $OFFSET)"

  databasin sql exec $CONNECTOR "
  SELECT * FROM $TABLE
  ORDER BY id
  LIMIT $BATCH_SIZE
  OFFSET $OFFSET
  " --csv > "batch_${i}.csv"

  # Process the batch
  # (Your processing logic here)

  # Progress indicator
  PROGRESS=$(( (i + 1) * 100 / BATCHES ))
  echo "Progress: ${PROGRESS}%"
done

echo "Batch processing complete!"
```

### Parallel Pipeline Execution

Run multiple pipelines concurrently:

```bash
#!/bin/bash
# parallel-pipelines.sh - Execute multiple pipelines in parallel

# Array of pipeline IDs to run
PIPELINES=(
  "pipeline-customers"
  "pipeline-orders"
  "pipeline-products"
  "pipeline-inventory"
)

echo "Starting parallel pipeline execution..."

# Start all pipelines in parallel
for pipeline in "${PIPELINES[@]}"; do
  echo "Starting: $pipeline"
  databasin pipelines run $pipeline &
done

# Wait for all to complete
wait

# Check results
echo -e "\n=== Pipeline Results ==="
for pipeline in "${PIPELINES[@]}"; do
  STATUS=$(databasin pipelines get $pipeline --json | jq -r '.status')
  echo "$pipeline: $STATUS"

  if [ "$STATUS" == "failed" ]; then
    echo "  Logs:"
    databasin pipelines logs $pipeline | tail -20
  fi
done

echo "Parallel execution complete!"
```

---

## Monitoring and Alerting

### Pipeline Health Monitor

Monitor pipeline health and send alerts:

```bash
#!/bin/bash
# pipeline-health-monitor.sh - Monitor all pipelines and alert on failures

PROJECT_ID="$1"
SLACK_WEBHOOK="${SLACK_WEBHOOK_URL}"

# Get all pipelines
PIPELINES=$(databasin pipelines list --project $PROJECT_ID --json)

# Check each pipeline
echo "$PIPELINES" | jq -r '.[] | "\(.id)|\(.name)|\(.status)|\(.lastRun)"' | \
while IFS='|' read -r id name status last_run; do

  if [ "$status" == "failed" ]; then
    # Get failure details
    ERROR=$(databasin pipelines logs $id --json | \
      jq -r '.[] | select(.level=="error") | .message' | \
      tail -1)

    # Send alert
    curl -X POST $SLACK_WEBHOOK \
      -H 'Content-Type: application/json' \
      -d "{
        \"text\": \"🚨 Pipeline Failed: $name\",
        \"attachments\": [{
          \"color\": \"danger\",
          \"fields\": [
            {\"title\": \"Pipeline\", \"value\": \"$name\", \"short\": true},
            {\"title\": \"Status\", \"value\": \"$status\", \"short\": true},
            {\"title\": \"Last Run\", \"value\": \"$last_run\", \"short\": true},
            {\"title\": \"Error\", \"value\": \"$ERROR\", \"short\": false}
          ]
        }]
      }"

    echo "Alert sent for failed pipeline: $name"
  fi
done
```

---

## Best Practices Summary

### 1. Schema Discovery
- Always verify connectivity before schema exploration
- Document discovered schemas for reference
- Sample data before building pipelines

### 2. Pipeline Development
- Compare source and target schemas before creating pipelines
- Test with small datasets first
- Use incremental loading with watermarks
- Implement proper error handling

### 3. Data Quality
- Validate data before and after transformations
- Implement data quality checks in pipelines
- Monitor null rates and duplicates
- Profile data regularly

### 4. Performance
- Use batching for large datasets
- Run independent pipelines in parallel
- Optimize SQL queries with proper indexes
- Monitor execution times

### 5. Monitoring
- Set up health checks for all pipelines
- Implement alerting for failures
- Log all operations for troubleshooting
- Review logs regularly

---

**Last Updated:** 2025-12-06
