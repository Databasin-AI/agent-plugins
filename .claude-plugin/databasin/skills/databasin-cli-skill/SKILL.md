---
name: databasin-cli
description: Expert skill for using the Databasin CLI tool to manage data connectors, pipelines, automations, SQL queries, and comprehensive data engineering workflows. This skill should be used when users need help with creating/managing data connectors (250+ types), building ETL/ELT pipelines, executing SQL queries, exploring database structures, troubleshooting pipeline failures, managing Databasin projects, or any data engineering/administration task using Databasin.
---

# Databasin CLI Expert

Expert skill for using the Databasin CLI tool to manage data connectors, pipelines, automations, SQL queries, and comprehensive data engineering workflows on the Databasin platform.

## When to use this skill

Use this skill when users need help with:
- Creating, managing, or troubleshooting data connectors (250+ types available)
- Building and running data pipelines for ETL/ELT workflows
- Executing SQL queries and exploring database structures
- Setting up automations for data workflows
- Finding specific data using natural language descriptions
- Troubleshooting pipeline failures by analyzing logs
- Managing Databasin projects, users, and permissions
- Any data engineering, data science, data administration, or data visualization task using Databasin

## Core CLI Capabilities

The Databasin CLI (`databasin`) provides comprehensive data platform management:

### Authentication
```bash
databasin auth login      # Login via browser (always required first)
databasin auth whoami     # View current user
databasin auth verify     # Check token validity
```

### Project Management
```bash
databasin projects list                    # List all projects
databasin projects get <project-id>        # Get project details
databasin projects users <project-id>      # View project users
databasin projects stats <project-id>      # Show statistics
```

### Connector Operations
```bash
databasin connectors list                              # List all connectors
databasin connectors get <connector-id>                # Get connector details
databasin connectors create <config.json>              # Create new connector
databasin connectors update <id> <config.json>         # Update connector
databasin connectors delete <connector-id>             # Delete connector
```

### SQL Interface & Data Exploration
```bash
databasin sql catalogs <connector-id>                                      # List catalogs
databasin sql schemas <connector-id> --catalog <name>                      # List schemas
databasin sql tables <connector-id> --catalog <name> --schema <name>       # List tables
databasin sql exec <connector-id> "<SQL query>"                            # Execute SQL
databasin sql exec <connector-id> "<query>" --csv > output.csv             # Export to CSV
```

### Pipeline Operations
```bash
databasin pipelines list --project <project-id>        # List pipelines
databasin pipelines get <pipeline-id>                  # Get pipeline details
databasin pipelines create <config.json>               # Create pipeline
databasin pipelines run <pipeline-id>                  # Run pipeline
databasin pipelines logs <pipeline-id>                 # View logs (critical for troubleshooting)
```

### Automation Management
```bash
databasin automations list                             # List automations
databasin automations list --project <project-id>      # List by project
databasin automations get <automation-id>              # Get details
databasin automations run <automation-id>              # Run automation
databasin automations logs <automation-id>             # View logs
```

### Output Formatting
```bash
--json                    # JSON output
--csv                     # CSV output
--fields field1,field2    # Select specific fields
```

## Critical Usage Patterns

### 1. Always Verify Authentication First
Before ANY operation:
```bash
databasin auth whoami
# If not logged in: databasin auth login
```

### 2. Data Discovery Workflow (VERY IMPORTANT)
When users ask "find data" or "show me data about X":

```bash
# Step 1: List available connectors
databasin connectors list

# Step 2: Explore data hierarchy
databasin sql catalogs <connector-id>
databasin sql schemas <connector-id> --catalog <catalog>
databasin sql tables <connector-id> --catalog <catalog> --schema <schema>

# Step 3: Sample data to understand structure
databasin sql exec <connector-id> "SELECT * FROM <table> LIMIT 5"

# Step 4: Craft query based on user's natural language request
# Example: "customer emails from New York"
databasin sql exec <connector-id> "SELECT email FROM customers WHERE state = 'NY'"

# Step 5: Export if needed
databasin sql exec <connector-id> "<query>" --csv > results.csv
```

### 3. Troubleshooting Failures (CRITICAL)
When pipelines or automations fail:

```bash
# Step 1: Get logs (ALWAYS DO THIS FIRST)
databasin pipelines logs <pipeline-id>
# or
databasin automations logs <automation-id>

# Step 2: Check resource details
databasin pipelines get <pipeline-id>

# Step 3: Verify connectors are working
databasin connectors get <connector-id>
databasin sql exec <connector-id> "SELECT 1"

# Step 4: Enable debug mode if needed
DATABASIN_DEBUG=true databasin pipelines run <pipeline-id>
```

### 4. Building New Pipelines
```bash
# Step 1: Verify source connector works
databasin sql exec <source-id> "SELECT 1"

# Step 2: Explore source data
databasin sql catalogs <source-id>
databasin sql tables <source-id> --catalog <catalog> --schema <schema>
databasin sql exec <source-id> "SELECT * FROM <table> LIMIT 5"

# Step 3: Create pipeline config file
cat > pipeline.json << 'EOF'
{
  "name": "My Pipeline",
  "sourceConnector": "<source-id>",
  "targetConnector": "<target-id>",
  "transformations": [],
  "schedule": "0 6 * * *"
}
EOF

# Step 4: Create and test
databasin pipelines create pipeline.json
databasin pipelines run <pipeline-id>
databasin pipelines logs <pipeline-id>
```

## Natural Language to SQL Translation

When users describe data needs in natural language, translate systematically:

**Example 1:**
- User: "Show me customers who ordered in the last month"
- Translation: Identify entities (customers, orders), relationships (customer_id), filters (date)
- Query:
```sql
SELECT c.* 
FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o 
  WHERE o.customer_id = c.id 
  AND o.created_at > CURRENT_DATE - INTERVAL '1 month'
)
```

**Example 2:**
- User: "Find duplicate emails in the users table"
- Translation: GROUP BY with HAVING for duplicates
- Query:
```sql
SELECT email, COUNT(*) as count
FROM users
GROUP BY email
HAVING COUNT(*) > 1
```

**Example 3:**
- User: "Top 10 products by revenue this year"
- Translation: JOIN orders and products, SUM revenue, filter by year, ORDER BY and LIMIT
- Query:
```sql
SELECT p.name, SUM(o.amount) as total_revenue
FROM products p
JOIN orders o ON p.id = o.product_id
WHERE YEAR(o.created_at) = YEAR(CURRENT_DATE)
GROUP BY p.id, p.name
ORDER BY total_revenue DESC
LIMIT 10
```

## Connector Types & Use Cases

Databasin supports 250+ prebuilt connectors:

**Databases:**
- PostgreSQL, MySQL, SQL Server, Oracle, MongoDB
- Use for: Primary data sources, transactional data

**Cloud Storage:**
- AWS S3, Azure Blob Storage, Google Cloud Storage
- Use for: File-based data, backups, data lakes

**Data Warehouses:**
- Snowflake, BigQuery, Redshift, Databricks
- Use for: Analytics targets, aggregated data

**SaaS Applications:**
- Salesforce, HubSpot, Zendesk, ServiceNow
- Use for: CRM data, customer support data

**Streaming:**
- Kafka, Event Hubs, Kinesis
- Use for: Real-time data ingestion

## Common Error Patterns & Solutions

| Error Message | Cause | Solution |
|--------------|-------|----------|
| "Token expired" | Auth token invalid | `databasin auth login` |
| "Project not found" | Invalid project ID | `databasin projects list` to get valid IDs |
| "Connector failed" | Connection config issue | `databasin connectors get <id>` to check config |
| "Permission denied" | Insufficient access | `databasin projects users <project-id>` to verify permissions |
| "SQL execution failed" | Invalid query or schema | Test with `SELECT 1`, check table existence |
| "Pipeline failed" | Data transformation error | `databasin pipelines logs <id>` to see detailed error |

## Configuration Files

### Connector Configuration Example
```json
{
  "name": "Production PostgreSQL",
  "type": "postgres",
  "config": {
    "host": "db.example.com",
    "port": 5432,
    "database": "production",
    "username": "databasin_user",
    "ssl": true
  }
}
```

### Pipeline Configuration Example
```json
{
  "name": "Daily User Sync",
  "description": "Sync active users to analytics warehouse",
  "sourceConnector": "conn-prod-db",
  "targetConnector": "conn-analytics-warehouse",
  "transformations": [
    {
      "type": "filter",
      "condition": "active = true"
    },
    {
      "type": "map",
      "fields": {
        "user_id": "id",
        "full_name": "CONCAT(first_name, ' ', last_name)",
        "signup_date": "created_at"
      }
    }
  ],
  "schedule": "0 6 * * *"
}
```

## Best Practices for User Assistance

### 1. When Users Ask About Data
- **Clarify:** What data? Which source? What format?
- **Explore:** Use catalogs → schemas → tables hierarchy
- **Sample:** Always show sample data before full queries
- **Export:** Provide results in requested format (--json, --csv)

### 2. When Troubleshooting
- **Always check logs first:** `databasin <resource> logs <id>`
- **Verify basics:** Authentication, resource exists, connectivity
- **Test incrementally:** Simple queries first, then complex
- **Enable debug mode:** `DATABASIN_DEBUG=true` for details

### 3. When Building Pipelines
- **Plan first:** Understand source, target, transformations
- **Test connectors individually:** Ensure both work before pipeline
- **Start simple:** Basic pipeline first, add complexity incrementally
- **Monitor closely:** Check logs after every run

### 4. When Helping with SQL
- **Understand the ask:** Break down natural language into SQL components
- **Explain the query:** Show users what each part does
- **Validate results:** Sample output before exporting large datasets
- **Optimize:** Use appropriate LIMIT, indexes, filters

## Environment Variables

```bash
# Set automatically by login, but can be set manually
export DATABASIN_TOKEN="your-token"

# Change API endpoint (default: http://localhost:9000)
export DATABASIN_API_URL="https://api.databasin.com"

# Enable detailed debug output
export DATABASIN_DEBUG=true
```

## Advanced Patterns

### Batch Operations
```bash
# Check status of all connectors
for id in $(databasin connectors list --json | jq -r '.[].id'); do
  echo "Testing $id..."
  databasin sql exec $id "SELECT 1" 2>&1 | grep -q "success" && echo "✓" || echo "✗"
done

# Export all tables from a schema
for table in $(databasin sql tables <conn-id> --catalog <cat> --schema <sch> --json | jq -r '.[].name'); do
  databasin sql exec <conn-id> "SELECT * FROM $table" --csv > "${table}.csv"
done
```

### Data Quality Checks
```bash
# Record counts with nulls
databasin sql exec <connector-id> "
  SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(*) - COUNT(email) as null_emails,
    MIN(created_at) as earliest,
    MAX(created_at) as latest
  FROM users
"

# Find duplicates
databasin sql exec <connector-id> "
  SELECT email, COUNT(*) as count
  FROM users
  GROUP BY email
  HAVING COUNT(*) > 1
"
```

### Schema Comparison
```bash
# Compare schemas between source and target
databasin sql exec <source-id> "
  SELECT column_name, data_type 
  FROM information_schema.columns 
  WHERE table_name = 'users'
  ORDER BY ordinal_position
" --csv > source_schema.csv

databasin sql exec <target-id> "
  SELECT column_name, data_type 
  FROM information_schema.columns 
  WHERE table_name = 'users'
  ORDER BY ordinal_position
" --csv > target_schema.csv

diff source_schema.csv target_schema.csv
```

## Quick Command Reference

```bash
# Essential workflow commands
databasin auth login
databasin projects list
databasin connectors list
databasin sql catalogs <conn-id>
databasin sql exec <conn-id> "<query>"
databasin pipelines list --project <proj-id>
databasin pipelines logs <pipeline-id>

# Common output options
--json                    # Machine-readable JSON
--csv                     # CSV export
--fields id,name,status   # Select specific fields

# Debugging
DATABASIN_DEBUG=true <command>
```

## Bundled References

The skill includes comprehensive reference documentation in the `references/` directory. Consult these files as needed for expert-level guidance:

### references/advanced-workflows.md
**Use for complex data engineering workflows.** Contains comprehensive guides for:
- **Schema Discovery**: Complete workflows for exploring unfamiliar databases, automated schema documentation, interactive table exploration, and data profiling
- **Pipeline Creation**: End-to-end pipeline development workflows, incremental ETL patterns, multi-stage pipelines, and production-ready configurations
- **Complex SQL Patterns**: Data deduplication strategies, migration workflows with validation, comprehensive data quality audits
- **Connector Configuration**: Production-ready examples for PostgreSQL, Snowflake, S3, MongoDB, and other data sources
- **Automation Workflows**: Scheduled data quality checks, event-driven triggers, file processing automation
- **Real-World Use Cases**: Customer 360 view, real-time inventory sync, financial reporting automation
- **Performance Optimization**: Batch processing strategies, parallel pipeline execution, monitoring and alerting patterns

### references/example-queries.md
**Use when users need SQL query patterns.** Contains comprehensive examples of:
- Data exploration queries (sampling, schema information, record counts)
- Data quality checks (finding NULLs, duplicates, outliers)
- Time-based queries and aggregations
- Joins and relationships
- Window functions and advanced analytics
- Text search and pattern matching
- Conditional logic with CASE statements
- Common Table Expressions (CTEs)
- Data transformation patterns

### references/troubleshooting.md
**Use when diagnosing issues or errors.** Contains systematic troubleshooting workflows for:
- Authentication failures (expired tokens, API connectivity)
- Connector issues (connection failed, permission denied)
- Pipeline failures (execution errors, schema mismatches, constraint violations)
- SQL query errors (syntax errors, timeout issues)
- Performance problems (slow execution, high memory usage)
- Data quality issues (duplicates, NULL values)
- Emergency procedures for stuck pipelines and data loss concerns
- Preventive measures and monitoring scripts

### references/token-efficiency.md
**Use when working with large datasets** to minimize token usage. Contains guidance on:
- Token-efficient command options (--json, --csv, --fields, --project)
- Filtering strategies to reduce result sets
- SQL query optimization for controlled data retrieval
- Batch operations with minimal token usage
- Advanced patterns for incremental data fetching

## Summary

The Databasin CLI is your comprehensive tool for:
- **Data Integration:** 250+ prebuilt connectors to any source
- **Data Discovery:** SQL interface to explore and query data
- **Pipeline Management:** Build, run, and monitor ETL/ELT workflows
- **Automation:** Execute complex business logic and orchestration
- **Troubleshooting:** Detailed logs and debug capabilities
- **Data Administration:** Manage projects, permissions, and infrastructure

**Golden Rules:**
1. Always authenticate first: `databasin auth login`
2. Always check logs when troubleshooting: `databasin <resource> logs <id>`
3. Always explore before querying: catalogs → schemas → tables → sample
4. Always test connectors individually before building pipelines
5. Always use appropriate output format: --json for scripts, --csv for exports, table for viewing

To assist users effectively, leverage all Databasin CLI capabilities, translate their data needs into proper commands and SQL queries, troubleshoot issues systematically using the bundled troubleshooting guide, and guide them through building robust data workflows.
