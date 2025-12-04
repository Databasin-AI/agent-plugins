# SQL Assistant Guide

**Last Updated:** 2025-11-20
**Purpose:** Generate, execute, and fix SQL queries using Databasin LLM connectors and warehouse proxies

---

## Table of Contents

- [Quick Start](#quick-start)
- [Workflow Examples](#workflow-examples)
- [Script Reference](#script-reference)
- [Database Types](#database-types)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

1. **LLM Connector** - For SQL generation/fixing (e.g., Claude connector)
2. **Warehouse Connector** - For SQL execution (Trino or Databricks lakehouse connector)
3. **JWT Token** - In `.token` file (use `refresh-databasin-jwt` skill)

### Basic Workflow

```bash
# 1. Get schema context
bun run scripts/get-schema-context.ts <warehouseConnectorID> --summary

# 2. Save full schema context to file
bun run scripts/get-schema-context.ts <warehouseConnectorID> > schema.json

# 3. Generate SQL from natural language
bun run scripts/generate-sql.ts <llmConnectorID> "Get top 10 customers by revenue" \
  --schema-file=schema.json --database-type=databricks

# 4. Execute the SQL
bun run scripts/execute-sql.ts <warehouseConnectorID> "SELECT ..." --format=table

# 5. If SQL fails, fix it
bun run scripts/fix-sql.ts <llmConnectorID> "SELECT ..." "Error message" \
  --schema-file=schema.json --database-type=databricks
```

---

## Workflow Examples

### Example 1: Simple Query Generation and Execution

**Scenario:** Generate and execute a query to count users

```bash
# Step 1: Get connector IDs
# - llmConnectorID: 456 (Claude connector)
# - warehouseConnectorID: 123 (Lakehouse Trino connector)

# Step 2: Get schema context
bun run scripts/get-schema-context.ts 123 \
  --catalog=hive --schema=default > schema.json

# Step 3: Generate SQL
bun run scripts/generate-sql.ts 456 "Count all users" \
  --schema-file=schema.json --raw > query.sql

# Step 4: Execute SQL
bun run scripts/execute-sql.ts 123 --file=query.sql --format=table
```

**Expected Output:**

```
| count |
|-------|
| 1,532 |

1 row in 234ms
```

---

### Example 2: Complex Query with Error Fixing

**Scenario:** Generate complex query, encounter error, fix it

```bash
# Step 1: Generate SQL for complex query
bun run scripts/generate-sql.ts 456 \
  "Show top 10 products by revenue in each category" \
  --schema-file=schema.json --raw > query.sql

# Step 2: Try to execute (fails with error)
bun run scripts/execute-sql.ts 123 --file=query.sql 2> error.txt

# Error: "Table not found: products"

# Step 3: Fix the SQL
SQL=$(cat query.sql)
ERROR=$(cat error.txt)
bun run scripts/fix-sql.ts 456 "$SQL" "$ERROR" \
  --schema-file=schema.json --raw > query-fixed.sql

# Step 4: Execute fixed SQL
bun run scripts/execute-sql.ts 123 --file=query-fixed.sql --format=table
```

---

### Example 3: Databricks-Specific Query

**Scenario:** Work with Databricks warehouse requiring backtick syntax

```bash
# Step 1: Get Databricks schema
bun run scripts/get-schema-context.ts 789 \
  --catalog=hubspot --schema=schema_hubspot > hubspot-schema.json

# Step 2: Generate SQL (Databricks-specific)
bun run scripts/generate-sql.ts 456 \
  "Count deals by pipeline stage" \
  --schema-file=hubspot-schema.json \
  --database-type=databricks \
  --raw

# Output will use backticks:
# SELECT `pipeline_stage`, COUNT(*) as deal_count
# FROM `hubspot`.`schema_hubspot`.`deals`
# GROUP BY `pipeline_stage`
```

---

### Example 4: Iterative Schema Exploration

**Scenario:** Explore schema step-by-step

```bash
# Step 1: List all catalogs
bun run scripts/get-schema-context.ts 123

# Output: { "catalogs": ["hive", "lakehouse", "hubspot"] }

# Step 2: Explore specific catalog
bun run scripts/get-schema-context.ts 123 --catalog=lakehouse

# Output: { "schemas": { "lakehouse": ["default", "analytics", "staging"] } }

# Step 3: List tables in schema
bun run scripts/get-schema-context.ts 123 \
  --catalog=lakehouse --schema=analytics

# Output: { "tables": { "lakehouse.analytics": [
#   {"name": "customers", "type": "TABLE"},
#   {"name": "orders", "type": "TABLE"}
# ]}}

# Step 4: Get columns for table
bun run scripts/get-schema-context.ts 123 \
  --catalog=lakehouse --schema=analytics --table=customers

# Output: { "columns": {
#   "lakehouse.analytics.customers": [
#     {"name": "id", "type": "bigint"},
#     {"name": "name", "type": "varchar"},
#     {"name": "email", "type": "varchar"}
#   ]
# }}
```

---

## Script Reference

### get-schema-context.ts

**Purpose:** Retrieve schema information for SQL generation

**Usage:**

```bash
bun run scripts/get-schema-context.ts <connectorID> [options]
```

**Options:**

- `--catalog=name` - Specific catalog
- `--schema=name` - Specific schema (requires `--catalog`)
- `--table=name` - Specific table (requires `--catalog` and `--schema`)
- `--summary` - Summary view with counts and samples
- `--compact` - Compact JSON output

**Examples:**

```bash
# Get all catalogs
bun run scripts/get-schema-context.ts 123

# Get summary (efficient for large schemas)
bun run scripts/get-schema-context.ts 123 --summary

# Save full context to file
bun run scripts/get-schema-context.ts 123 > schema.json

# Get specific catalog/schema
bun run scripts/get-schema-context.ts 123 --catalog=hive --schema=default
```

**Token Usage:**

- Summary mode: ~500-1,000 tokens
- Full catalogs only: ~100-500 tokens
- Single schema: ~1,000-5,000 tokens
- Full context with columns: **VERY HIGH** (~50,000-200,000 tokens)
  - ⚠️ Always use `--summary` first or target specific schemas

---

### generate-sql.ts

**Purpose:** Convert natural language to SQL using LLM

**Usage:**

```bash
bun run scripts/generate-sql.ts <llmConnectorID> <query> [options]
```

**Options:**

- `--schema-file=path` - Schema context JSON file (from get-schema-context.ts)
- `--connector-id=N` - Warehouse connector ID (alternative to schema-file)
- `--catalog=name` - Catalog name (with connector-id)
- `--schema=name` - Schema name (with connector-id)
- `--database-type=type` - Database: `trino` (default) or `databricks`
- `--model=name` - Model name (default: `claude-sonnet-4-20250514`)
- `--raw` - Output only SQL (no JSON)

**Examples:**

```bash
# With schema file (recommended)
bun run scripts/generate-sql.ts 456 "Get top 10 customers" \
  --schema-file=schema.json --raw

# With inline context
bun run scripts/generate-sql.ts 456 "Count orders" \
  --connector-id=123 --catalog=hive --schema=default

# Databricks-specific
bun run scripts/generate-sql.ts 456 "List all deals" \
  --schema-file=hubspot.json --database-type=databricks
```

**Token Usage:**

- Small schema (<10 tables): ~2,000-5,000 tokens
- Medium schema (10-50 tables): ~5,000-15,000 tokens
- Large schema (50+ tables): ~15,000-50,000+ tokens

**⚠️ Important:** Use targeted schema files (specific catalogs/schemas) to minimize token usage

---

### execute-sql.ts

**Purpose:** Execute SQL queries via warehouse proxy

**Usage:**

```bash
bun run scripts/execute-sql.ts <connectorID> <sql> [options]
bun run scripts/execute-sql.ts <connectorID> --file=query.sql [options]
```

**Options:**

- `--file=path` - Read SQL from file
- `--limit=N` - Limit results to N rows (default: 100)
- `--timeout=N` - Timeout in seconds (default: 30)
- `--format=type` - Output: `json` (default), `csv`, `table`
- `--compact` - Compact JSON
- `--fields=field1,...` - Return only specific fields

**Examples:**

```bash
# Execute inline SQL
bun run scripts/execute-sql.ts 123 "SELECT * FROM users LIMIT 10"

# Execute from file (table format)
bun run scripts/execute-sql.ts 123 --file=query.sql --format=table

# Execute with field filter
bun run scripts/execute-sql.ts 123 "SELECT * FROM orders" \
  --fields=id,customer_name,total --limit=20

# CSV export
bun run scripts/execute-sql.ts 123 --file=report.sql --format=csv > output.csv
```

**Token Usage:**

- Execution itself: ~500-1,000 tokens
- JSON results (10 rows): ~1,000-3,000 tokens
- JSON results (100 rows): ~10,000-30,000 tokens
- Table/CSV format: ~500-5,000 tokens (more compact)

**⚠️ Tip:** Use `--format=table` or `--format=csv` for large result sets

---

### fix-sql.ts

**Purpose:** Fix SQL queries based on error messages using LLM

**Usage:**

```bash
bun run scripts/fix-sql.ts <llmConnectorID> <sql> <error> [options]
bun run scripts/fix-sql.ts <llmConnectorID> --file=query.sql --error="..." [options]
```

**Options:**

- `--file=path` - Read SQL from file
- `--error=message` - Error message from failed query
- `--schema-file=path` - Schema context JSON
- `--database-type=type` - Database: `trino` or `databricks`
- `--model=name` - Model name (default: `claude-sonnet-4-20250514`)
- `--raw` - Output only fixed SQL

**Examples:**

```bash
# Fix inline SQL
bun run scripts/fix-sql.ts 456 \
  "SELECT * FROM users" \
  "Table not found: users" \
  --schema-file=schema.json --raw

# Fix SQL from file
bun run scripts/fix-sql.ts 456 --file=query.sql \
  --error="Syntax error at line 5" \
  --schema-file=schema.json

# Databricks-specific fix
bun run scripts/fix-sql.ts 456 \
  'SELECT "deals"."stage" FROM "hubspot"."schema_hubspot"."deals"' \
  "Syntax error: unexpected character: \"" \
  --database-type=databricks --raw

# Output: SELECT `deals`.`stage` FROM `hubspot`.`schema_hubspot`.`deals`
```

**Token Usage:**

- Small fix (~1 table): ~1,000-3,000 tokens
- Medium fix (~5 tables): ~3,000-8,000 tokens
- Large fix (full schema): ~8,000-30,000+ tokens

---

## Database Types

### Trino (Apache Trino)

**Identifier Syntax:** Double quotes `"` (only for special characters)

```sql
SELECT "column-name" FROM "catalog"."schema"."table-name"
```

**Data Types:**

- `VARCHAR` for text
- `REGEXP_LIKE()` for regex
- `CAST(column AS INTEGER)`

**Generated SQL Example:**

```sql
SELECT customer_id, name, SUM(order_total) as revenue
FROM hive.default.orders
WHERE order_date >= DATE '2025-01-01'
GROUP BY customer_id, name
ORDER BY revenue DESC
LIMIT 10
```

---

### Databricks

**Identifier Syntax:** Backticks `` ` `` (ALWAYS, even for simple names)

```sql
SELECT `column_name` FROM `catalog`.`schema`.`table_name`
```

**🔴 CRITICAL:** Databricks requires backticks for ALL identifiers, never double quotes

**Data Types:**

- `STRING` (not VARCHAR)
- `RLIKE` for regex
- `CAST(column AS STRING)`

**Generated SQL Example:**

```sql
SELECT `customer_id`, `name`, SUM(`order_total`) as revenue
FROM `hubspot`.`schema_hubspot`.`orders`
WHERE `order_date` >= '2025-01-01'
GROUP BY `customer_id`, `name`
ORDER BY revenue DESC
LIMIT 10
```

---

## Best Practices

### Schema Context Management

**✅ DO:**

- Use `--summary` first to understand schema size
- Save schema context to files for reuse
- Target specific catalogs/schemas when possible
- Use compact format for programmatic usage

**❌ DON'T:**

- Fetch full schema with all columns unless necessary
- Re-fetch schema for every query
- Include unused catalogs in context

**Example Efficient Workflow:**

```bash
# 1. Initial exploration (summary)
bun run scripts/get-schema-context.ts 123 --summary

# 2. Save targeted context
bun run scripts/get-schema-context.ts 123 \
  --catalog=lakehouse --schema=analytics > lakehouse-analytics.json

# 3. Reuse context file for multiple queries
bun run scripts/generate-sql.ts 456 "Query 1" --schema-file=lakehouse-analytics.json --raw
bun run scripts/generate-sql.ts 456 "Query 2" --schema-file=lakehouse-analytics.json --raw
bun run scripts/generate-sql.ts 456 "Query 3" --schema-file=lakehouse-analytics.json --raw
```

---

### SQL Generation

**✅ DO:**

- Provide clear, specific natural language queries
- Include schema context whenever possible
- Specify database type (Trino vs Databricks)
- Use `--raw` when piping to execution

**❌ DON'T:**

- Generate SQL without schema context (will guess table names)
- Mix Trino and Databricks syntax
- Skip error handling

**Example Clear Queries:**

```bash
# ✅ Good - specific and clear
"Get the top 10 customers by total revenue in 2025"
"Count active deals by pipeline stage"
"Show monthly order trends for the last 12 months"

# ❌ Bad - vague or ambiguous
"Get some data"
"Show me stuff about customers"
"Query the database"
```

---

### SQL Execution

**✅ DO:**

- Use `--format=table` for readability
- Use `--limit` to avoid huge result sets
- Use `--fields` to filter columns
- Set appropriate `--timeout` for long queries

**❌ DON'T:**

- Execute queries without LIMIT clauses on unknown tables
- Request full JSON for 1000+ rows
- Ignore timeouts on complex queries

**Example Safe Execution:**

```bash
# Explore new table safely
bun run scripts/execute-sql.ts 123 \
  "SELECT * FROM new_table LIMIT 10" \
  --format=table

# Large aggregation with timeout
bun run scripts/execute-sql.ts 123 --file=complex-query.sql \
  --timeout=300 --format=csv > results.csv
```

---

### Error Fixing

**✅ DO:**

- Provide full error message
- Include schema context
- Specify correct database type
- Try fixed SQL immediately

**❌ DON'T:**

- Truncate error messages
- Skip schema context
- Mix database types

**Example Fix Workflow:**

```bash
# 1. Execute and capture error
bun run scripts/execute-sql.ts 123 "$SQL" 2> error.txt

# 2. Fix with full context
SQL=$(cat query.sql)
ERROR=$(cat error.txt)
bun run scripts/fix-sql.ts 456 "$SQL" "$ERROR" \
  --schema-file=schema.json --database-type=databricks --raw > query-fixed.sql

# 3. Re-execute
bun run scripts/execute-sql.ts 123 --file=query-fixed.sql --format=table
```

---

## Troubleshooting

### "Table not found" Errors

**Cause:** Missing catalog/schema prefix

**Solution:**

1. Get schema context: `bun run scripts/get-schema-context.ts 123 --summary`
2. Use fully qualified names: `catalog.schema.table`
3. Fix SQL with context: `bun run scripts/fix-sql.ts 456 "$SQL" "$ERROR" --schema-file=schema.json`

---

### "Syntax error" in Databricks

**Cause:** Using Trino syntax (double quotes) instead of backticks

**Solution:**

1. Regenerate with `--database-type=databricks`
2. Or fix existing SQL:

```bash
bun run scripts/fix-sql.ts 456 "$SQL" "Syntax error: unexpected \" " \
  --database-type=databricks --raw
```

---

### LLM API Errors (401, 403, 500)

**Cause:** Invalid JWT token or wrong LLM connector ID

**Solution:**

1. Refresh token: Use `refresh-databasin-jwt` skill
2. Verify connector ID:

```bash
bun run scripts/api-call.ts GET /api/connector/<llmConnectorID>
```

3. Check connector is LLM-enabled (look for `connectorType` containing "claude" or "openai")

---

### Warehouse Proxy Errors

**Cause:** Connector not lakehouse-enabled or invalid credentials

**Solution:**

1. Verify connector type:

```bash
bun run scripts/api-call.ts GET /api/connector/<connectorID> \
  --fields=connectorID,connectorName,connectorType,connectorSubType
```

2. Look for `connectorSubType` = "trino" or "databricks"
3. Check auth:

```bash
bun run scripts/api-call.ts GET "/api/connector/auth?connectorID=<connectorID>"
```

---

### High Token Usage

**Cause:** Large schema context or result sets

**Solution:**

1. Use `--summary` mode for schema exploration
2. Target specific catalogs/schemas
3. Use `--fields` and `--limit` for execution
4. Use `--format=table` or `--format=csv` for results

**Token Reduction Example:**

```bash
# ❌ High tokens (~100,000+)
bun run scripts/get-schema-context.ts 123 > full-schema.json

# ✅ Low tokens (~1,000)
bun run scripts/get-schema-context.ts 123 --summary
bun run scripts/get-schema-context.ts 123 --catalog=hive --schema=default > targeted.json
```

---

## Advanced Patterns

### Automated Query-Execute-Fix Loop

```bash
#!/usr/bin/env bash

LLM_CONNECTOR=456
WAREHOUSE_CONNECTOR=123
SCHEMA_FILE="schema.json"
MAX_RETRIES=3

QUERY="$1"
DATABASE_TYPE="${2:-trino}"

# Generate SQL
echo "Generating SQL..."
SQL=$(bun run scripts/generate-sql.ts $LLM_CONNECTOR "$QUERY" \
  --schema-file=$SCHEMA_FILE --database-type=$DATABASE_TYPE --raw)

echo "SQL: $SQL"

# Try to execute with retries
for i in $(seq 1 $MAX_RETRIES); do
  echo "Attempt $i..."

  if bun run scripts/execute-sql.ts $WAREHOUSE_CONNECTOR "$SQL" --format=table 2>error.txt; then
    echo "✅ Success!"
    exit 0
  fi

  ERROR=$(cat error.txt)
  echo "❌ Error: $ERROR"

  if [ $i -lt $MAX_RETRIES ]; then
    echo "Fixing SQL..."
    SQL=$(bun run scripts/fix-sql.ts $LLM_CONNECTOR "$SQL" "$ERROR" \
      --schema-file=$SCHEMA_FILE --database-type=$DATABASE_TYPE --raw)
    echo "Fixed SQL: $SQL"
  fi
done

echo "❌ Failed after $MAX_RETRIES attempts"
exit 1
```

**Usage:**

```bash
chmod +x query-loop.sh
./query-loop.sh "Get top 10 customers by revenue" "databricks"
```

---

## Support

**Issues or questions?**

1. Check this guide for examples
2. Check [Working Endpoints](./working-endpoints.md) for connector APIs
3. Check [Error Handling](./error-handling.md) for troubleshooting

---

**Last Updated:** 2025-11-20
**Scripts Version:** 1.0
**Status:** ✅ Production Ready
