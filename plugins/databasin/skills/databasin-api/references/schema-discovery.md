# Schema Discovery Guide

When working with SQL queries against connectors, you need to know the schema structure first. This guide shows you how to discover schemas, tables, and columns before writing SQL queries.

## Discovery Workflow

```
1. List Schemas → 2. List Tables → 3. Describe Table → 4. Query Data
```

---

## Step 1: List Available Schemas

**When to use:** You need to know what schemas/databases exist in a connector.

### Command

```bash
bun run scripts/list-schemas.ts <connectorID> [catalog]
```

### Examples

```bash
# List all schemas for connector 5459
bun run scripts/list-schemas.ts 5459

# List schemas in a specific catalog (for lakehouse connectors)
bun run scripts/list-schemas.ts 5459 hive
```

### Output

```
📚 Available Schemas:

  • backup
  • current
  • extensions
  • history
  • main
  • real_estate

✅ Found 6 schema(s) in 450ms

💡 Next Steps:
   List tables: bun run scripts/list-tables.ts 5459 <schema>
```

### Common Errors

**Token Expired (401)**

```
❌ Error: Failed to list schemas (401)

💡 Token expired. Get a fresh token:
   1. Log into http://localhost:3000
   2. Open DevTools → Application → Local Storage
   3. Copy token value and paste into .token file
```

**Connector Not Found (404)**

```
❌ Error: Failed to list schemas (404)

💡 Connector not found or no permission
   Check connector ID and your permissions
```

---

## Step 2: List Tables in a Schema

**When to use:** You know the schema and need to see what tables are available.

### Command

```bash
bun run scripts/list-tables.ts <connectorID> <schema> [catalog]
```

### Examples

```bash
# List tables in the 'main' schema
bun run scripts/list-tables.ts 5459 main

# List tables with catalog prefix
bun run scripts/list-tables.ts 5459 default hive
```

### Output

```
📋 Tables in Schema: main

  TABLES:
    • pipeline
    • pipeline_artifact
    • pipeline_connection
    • pipeline_notification
    • pipeline_validation
    • users_favorite_pipelines

✅ Found 6 table(s) in 890ms

💡 Next Steps:
   Describe table: bun run scripts/describe-table.ts 5459 main <table>
   Query table: bun run scripts/execute-sql.ts 5459 "SELECT * FROM main.<table> LIMIT 10"
```

### Common Errors

**Schema Not Found**

```
❌ Error: Schema "nonexistent" not found

💡 Schema "nonexistent" not found. List available schemas:
   bun run scripts/list-schemas.ts 5459
```

---

## Step 3: Describe Table Structure

**When to use:** You need to know the columns, data types, and structure of a table.

### Command

```bash
bun run scripts/describe-table.ts <connectorID> <schema> <table> [catalog]
```

### Examples

```bash
# Describe the pipeline table
bun run scripts/describe-table.ts 5459 main pipeline

# Describe with catalog
bun run scripts/describe-table.ts 5459 default customers hive
```

### Output

```
🔍 Describing Table: main.pipeline

┌─────────────────────────┬────────────────────────┬──────────┬────────────┐
│ Column Name             │ Data Type              │ Nullable │ Default    │
├─────────────────────────┼────────────────────────┼──────────┼────────────┤
│ id                      │ integer                │ NO       │            │
│ pipeline_name           │ character varying      │ NO       │            │
│ description             │ text                   │ YES      │            │
│ created_at              │ timestamp              │ NO       │ now()      │
│ updated_at              │ timestamp              │ NO       │ now()      │
│ project_id              │ integer                │ NO       │            │
│ source_connector_id     │ integer                │ YES      │            │
│ target_connector_id     │ integer                │ YES      │            │
└─────────────────────────┴────────────────────────┴──────────┴────────────┘

✅ Found 8 column(s) in 1230ms

💡 Next Steps:
   Sample data: bun run scripts/execute-sql.ts 5459 "SELECT * FROM main.pipeline LIMIT 5" --format=table
   Count rows: bun run scripts/execute-sql.ts 5459 "SELECT COUNT(*) FROM main.pipeline"
```

### Common Errors

**Table Not Found**

```
❌ Error: relation "main.wrong_table" does not exist

💡 Table "wrong_table" not found in schema "main"
   List tables: bun run scripts/list-tables.ts 5459 main
```

---

## Step 4: Query Table Data

**When to use:** You know the table structure and want to query or count data.

### Command

```bash
bun run scripts/execute-sql.ts <connectorID> "<SQL>" [--format=table|json|csv]
```

### Examples

```bash
# Get sample data
bun run scripts/execute-sql.ts 5459 "SELECT * FROM main.pipeline LIMIT 5" --format=table

# Count records
bun run scripts/execute-sql.ts 5459 "SELECT COUNT(*) as pipeline_count FROM main.pipeline"

# Filter and aggregate
bun run scripts/execute-sql.ts 5459 "SELECT project_id, COUNT(*) as count FROM main.pipeline GROUP BY project_id"

# Join tables
bun run scripts/execute-sql.ts 5459 "
  SELECT p.pipeline_name, c.connector_name
  FROM main.pipeline p
  JOIN main.pipeline_connection c ON p.source_connector_id = c.id
  LIMIT 10
"
```

---

## Quick Reference Commands

```bash
# Discovery workflow
bun run scripts/list-schemas.ts 5459
bun run scripts/list-tables.ts 5459 main
bun run scripts/describe-table.ts 5459 main pipeline
bun run scripts/execute-sql.ts 5459 "SELECT * FROM main.pipeline LIMIT 5" --format=table

# Search for tables containing 'pipeline'
bun run scripts/execute-sql.ts 5459 "
  SELECT table_schema, table_name
  FROM information_schema.tables
  WHERE table_name LIKE '%pipeline%'
  ORDER BY table_schema, table_name
" --format=table

# Get row counts for all tables in a schema
bun run scripts/execute-sql.ts 5459 "
  SELECT
    schemaname,
    tablename,
    n_live_tup as row_count
  FROM pg_stat_user_tables
  WHERE schemaname = 'main'
  ORDER BY n_live_tup DESC
" --format=table
```

---

## Best Practices

### 1. Always Discover Before Querying

❌ **Don't guess table names:**

```bash
# This might fail with "relation does not exist"
bun run scripts/execute-sql.ts 5459 "SELECT * FROM automations.pipelines"
```

✅ **Discover first:**

```bash
# Step 1: List schemas
bun run scripts/list-schemas.ts 5459

# Step 2: List tables in correct schema
bun run scripts/list-tables.ts 5459 main

# Step 3: Query with correct name
bun run scripts/execute-sql.ts 5459 "SELECT * FROM main.pipeline LIMIT 5"
```

### 2. Use Limits on Exploratory Queries

❌ **Don't query entire tables:**

```bash
# Could return millions of rows
bun run scripts/execute-sql.ts 5459 "SELECT * FROM main.pipeline"
```

✅ **Use LIMIT:**

```bash
# Safe exploratory query
bun run scripts/execute-sql.ts 5459 "SELECT * FROM main.pipeline LIMIT 10" --format=table
```

### 3. Check Column Names Before Filtering

❌ **Don't assume column names:**

```bash
# Might fail if column doesn't exist
bun run scripts/execute-sql.ts 5459 "SELECT * FROM main.pipeline WHERE status = 'active'"
```

✅ **Describe table first:**

```bash
# See actual column names
bun run scripts/describe-table.ts 5459 main pipeline

# Then query with correct columns
bun run scripts/execute-sql.ts 5459 "SELECT * FROM main.pipeline WHERE pipeline_status = 'ACTIVE'"
```

### 4. Use Table Formatting for Readability

```bash
# JSON format (default) - good for programmatic use
bun run scripts/execute-sql.ts 5459 "SELECT * FROM main.pipeline LIMIT 5"

# Table format - good for visual inspection
bun run scripts/execute-sql.ts 5459 "SELECT * FROM main.pipeline LIMIT 5" --format=table

# CSV format - good for importing to Excel
bun run scripts/execute-sql.ts 5459 "SELECT * FROM main.pipeline LIMIT 5" --format=csv > pipelines.csv
```

---

## Troubleshooting

### Problem: "Token expired" errors

**Solution:** Refresh your JWT token

```bash
# Manual method (recommended):
1. Log into http://localhost:3000
2. Open DevTools (F12) → Application → Local Storage
3. Find the 'token' key and copy the value
4. Paste into /home/founder3/code/tpi/databasin-sv/.token file
```

### Problem: "Table does not exist" errors

**Solution:** Use schema discovery workflow

```bash
# 1. List all schemas
bun run scripts/list-schemas.ts 5459

# 2. Pick a schema and list its tables
bun run scripts/list-tables.ts 5459 main

# 3. Use the exact table name from the list
bun run scripts/execute-sql.ts 5459 "SELECT * FROM main.pipeline LIMIT 5"
```

### Problem: "Column does not exist" errors

**Solution:** Describe the table to see actual column names

```bash
# See all columns and their types
bun run scripts/describe-table.ts 5459 main pipeline

# Query with correct column names
bun run scripts/execute-sql.ts 5459 "SELECT id, pipeline_name, created_at FROM main.pipeline LIMIT 5"
```

### Problem: Query returns too much data

**Solution:** Always use LIMIT and filters

```bash
# Count first to see data volume
bun run scripts/execute-sql.ts 5459 "SELECT COUNT(*) FROM main.pipeline"

# Then limit your query
bun run scripts/execute-sql.ts 5459 "SELECT * FROM main.pipeline WHERE created_at > '2025-01-01' LIMIT 100"
```

---

## Advanced Techniques

### Finding Related Tables

```bash
# Find all tables with foreign keys to pipeline table
bun run scripts/execute-sql.ts 5459 "
  SELECT
    tc.table_schema,
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name
  FROM information_schema.table_constraints AS tc
  JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
  JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
  WHERE tc.constraint_type = 'FOREIGN KEY'
    AND ccu.table_name = 'pipeline'
" --format=table
```

### Schema Statistics

```bash
# Get size and row counts for all tables
bun run scripts/execute-sql.ts 5459 "
  SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    n_live_tup AS row_count
  FROM pg_stat_user_tables
  ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
  LIMIT 20
" --format=table
```

### Column Search

```bash
# Find all tables containing a column name
bun run scripts/execute-sql.ts 5459 "
  SELECT table_schema, table_name, column_name, data_type
  FROM information_schema.columns
  WHERE column_name LIKE '%created_at%'
  ORDER BY table_schema, table_name
" --format=table
```

---

## Related Documentation

- [SQL Assistant Reference](./sql-assistant.md)
- [Error Handling Guide](./error-handling.md)
- [Programmatic Usage](./programmatic-usage.md)
- [Working Endpoints](./working-endpoints.md)
