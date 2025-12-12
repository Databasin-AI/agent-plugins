---
name: databasin-cli
description: General-purpose expert skill for using the Databasin CLI tool to assist with CLI usage, documentation access, and and advanced databasin command usage. Use when users or agents need help with Databasin CLI operations, accessing documentation, troubleshooting failures, or when more specific Databasin skills are not available or unsuccessful.
---

# Databasin CLI Expert (General Purpose)

General-purpose expert skill for using the Databasin CLI tool to manage data connectors, pipelines, automations, SQL queries, documentation access, and comprehensive data engineering workflows on the Databasin platform.

## When to use this skill

**This is a general-purpose Databasin CLI skill.** Use this skill when users need help with:
- Creating, managing, or troubleshooting data connectors (250+ types available)
- Building and running data pipelines for ETL/ELT workflows
- Executing SQL queries and exploring database structures
- Setting up automations for data workflows
- Finding specific data using natural language descriptions
- Troubleshooting pipeline failures by analyzing logs
- Managing Databasin projects, users, and permissions
- **Accessing and searching Databasin documentation efficiently**
- **Fetching and indexing documentation from GitHub**
- Any data engineering, data science, data administration, or data visualization task using Databasin
- **When more specific Databasin skills are not available or unsuccessful** (fallback skill)

## 📚 Real-World Examples

For comprehensive, step-by-step workflow examples, see the plugin's `examples/` directory:

- **[PostgreSQL to Snowflake Pipeline](../../examples/postgres-to-snowflake-pipeline.md)** - Complete end-to-end workflow for building a production data pipeline with authentication, connector setup, data exploration, pipeline creation, and monitoring
- **[Troubleshooting Failed Pipelines](../../examples/troubleshooting-failed-pipeline.md)** - Systematic approach to diagnosing and fixing pipeline failures including log analysis, common scenarios, and preventive monitoring
- **[Connector Inspection and Cloning](../../examples/connector-inspection-and-cloning.md)** - Advanced techniques using `connectors inspect` and `pipelines clone` for environment promotion and rapid deployment

**See [../../examples/README.md](../../examples/README.md) for a complete guide to all available examples and common patterns.**

**CRITICAL REMINDER:** Always use project internal IDs (alphanumeric strings like "N1r8Do") with `--project` arguments, never project names. Find your project ID with `databasin auth whoami`.

## Core CLI Capabilities

The Databasin CLI (`databasin`) provides comprehensive data platform management:

### Authentication
```bash
databasin auth login      # Login via browser (always required first)
databasin auth whoami     # View current user, and their projects and organizations
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
# IMPORTANT: connectors list defaults to COUNT MODE for efficiency
databasin connectors list                              # Count connectors (default, efficient)
databasin connectors list --full                       # List all connector objects (use with caution)
databasin connectors list --full --fields id,name,type --limit 20  # Token-efficient listing
databasin connectors get <connector-id>                # Get connector details
databasin connectors inspect <id-or-name>              # Comprehensive analysis (connection, metadata, structure, pipelines, quick actions)
databasin connectors create <config.json>              # Create new connector
databasin connectors update <id> <config.json>         # Update connector
databasin connectors delete <connector-id>             # Delete connector
databasin connectors test <connector-id>               # Test connector connection
databasin connectors config <subtype>                  # Get connector workflow screens (e.g., Postgres, MySQL)
databasin connectors config --all                      # List all available connector types
databasin connectors config <subtype> --screens        # Show detailed screen workflow
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
databasin pipelines template                           # Generate pipeline configuration template (RECOMMENDED)
databasin pipelines list --project <project-id>        # List pipelines (project required)
databasin pipelines get <pipeline-id>                  # Get pipeline details
databasin pipelines create <config.json> -p <project>  # Create pipeline from file
databasin pipelines clone <pipeline-id>                # Clone existing pipeline with optional overrides
databasin pipelines clone <id> --name "New Name"       # Clone with custom name
databasin pipelines clone <id> --source <conn-id>      # Clone with different source
databasin pipelines clone <id> --target <conn-id>      # Clone with different target
databasin pipelines clone <id> --schedule "0 3 * * *"  # Clone with different schedule
databasin pipelines clone <id> --dry-run               # Preview changes without creating
databasin pipelines run <pipeline-id>                  # Run pipeline
databasin pipelines logs <pipeline-id>                 # View logs (critical for troubleshooting)
databasin pipelines history <pipeline-id>              # View execution history
databasin pipelines history <id> --limit 10            # Recent 10 runs
databasin pipelines history <id> --count               # Count total runs
databasin pipelines artifacts logs <artifact-id>       # View artifact logs
databasin pipelines artifacts history <artifact-id>    # View artifact execution history
```

### Automation Management
```bash
databasin automations list                             # List automations
databasin automations list --project <project-id>      # List by project
databasin automations list --active                    # Filter to active automations
databasin automations list --running                   # Filter to currently running automations
databasin automations get <automation-id>              # Get details
databasin automations create <config.json>             # Create automation
databasin automations run <automation-id>              # Run automation
databasin automations stop <automation-id>             # Stop running automation
databasin automations logs <automation-id>             # View logs
databasin automations logs <id> --run-id <run-id>      # View logs for specific run
databasin automations history <automation-id>          # View execution history
databasin automations history <id> --limit 20          # Recent 20 runs
databasin automations tasks logs <task-id>             # View task logs
databasin automations tasks history <task-id>          # View task execution history
```

### Documentation Access (CRITICAL FEATURE)
```bash
databasin docs                                         # List all available documentation
databasin docs quickstart                              # View quickstart guide
databasin docs connectors-guide                        # View connectors guide
databasin docs pipelines-guide                         # View pipelines guide
databasin docs automations-guide                       # View automations guide
databasin docs <name> --pretty                         # View with rich formatting
```

**This skill includes scripts to fetch, index, and search documentation efficiently:**
- Fetch latest docs from GitHub using `databasin docs` commands
- Build searchable indexes with categorization and line numbers
- Low-token documentation lookups for faster responses


### Output Formatting
```bash
--json                    # JSON output
--csv                     # CSV output
--fields field1,field2    # Select specific fields
--limit N                 # Limit number of results
--count                   # Return count only
--no-color                # Disable colored output
--verbose                 # Enable verbose logging
--debug                   # Enable debug mode with stack traces
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
# Step 1: Count available connectors (fast, efficient)
databasin connectors list
# Output: 143 connectors

# Step 2: List connector details if needed (with token efficiency)
databasin connectors list --full --fields connectorID,connectorName,connectorType --limit 20

# Step 2a (NEW): Use inspect for comprehensive connector analysis
# This command provides connection testing, metadata, configuration, database structure,
# pipeline usage, and quick action suggestions in a single command
databasin connectors inspect <id-or-name>
# Example: databasin connectors inspect 5459
# Example: databasin connectors inspect "postgres"

# Step 3: Explore data hierarchy
databasin sql catalogs <connector-id>
databasin sql schemas <connector-id> --catalog <catalog>
databasin sql tables <connector-id> --catalog <catalog> --schema <schema>

# Step 4: Sample data to understand structure
databasin sql exec <connector-id> "SELECT * FROM <table> LIMIT 5"

# Step 5: Craft query based on user's natural language request
# Example: "customer emails from New York"
databasin sql exec <connector-id> "SELECT email FROM customers WHERE state = 'NY'"

# Step 6: Export if needed
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

### 4. Building New Pipelines (FILE-BASED APPROACH)

**IMPORTANT: Interactive wizards are not supported in AI agent workflows. Always use file-based configuration.**

**Option A: Create from scratch**

```bash
# Step 1: Verify source connector works
databasin sql exec <source-id> "SELECT 1"

# Step 2: Explore source data
databasin sql catalogs <source-id>
databasin sql tables <source-id> --catalog <catalog> --schema <schema>
databasin sql exec <source-id> "SELECT * FROM <table> LIMIT 5"

# Step 3: Generate template
databasin pipelines template > pipeline.json

# Step 4: Edit configuration (add source, target, artifacts, schedule)
# Modify pipeline.json with appropriate configuration

# Step 5: Create pipeline from configuration
databasin pipelines create pipeline.json -p <project-id>

# Step 6: Test
databasin pipelines run <pipeline-id>
databasin pipelines logs <pipeline-id>
```

**Option B: Clone existing pipeline (NEW)**

```bash
# Step 1: Identify pipeline to clone
databasin pipelines list --project <project-id>

# Step 2: Preview clone (optional, recommended)
databasin pipelines clone <pipeline-id> --dry-run

# Step 3: Clone with optional modifications
# Clone with default name (adds " (Clone)" suffix)
databasin pipelines clone <pipeline-id>

# Or clone with customizations:
databasin pipelines clone <pipeline-id> \
  --name "Dev Pipeline" \
  --source <new-source-id> \
  --target <new-target-id> \
  --schedule "0 */6 * * *"

# Step 4: Test the cloned pipeline
databasin pipelines run <new-pipeline-id>
databasin pipelines logs <new-pipeline-id>
```

**Use cases for cloning:**
- Environment promotion (dev → staging → prod)
- Testing with different connectors
- Schedule variations (hourly vs daily)
- Creating backups before major modifications

### 5. Documentation Lookup Workflow (EFFICIENT REFERENCE)

When users need documentation or guidance:

```bash
# Step 1: Check what documentation is available
databasin docs

# Step 2: View specific documentation
databasin docs <name>

# Step 3: For indexed documentation (if available)
# Read references/documentation-index.md for quick lookups
# Then read the specific file section as needed
```

## Documentation Management

This skill provides powerful documentation management capabilities for efficient, low-token lookups.

### 1. Fetch Latest Documentation

Retrieve the most current Databasin documentation directly from GitHub.

**When to use:**
- Setting up documentation for the first time
- Updating to the latest documentation version
- After significant documentation changes in the repository

**How to fetch:**

```bash
bun scripts/fetch-docs.ts
```

This command:
- Executes `databasin docs` to get the list of available documentation
- Fetches each individual document using `databasin docs [name]`
- Saves all documentation to `references/databasin-docs/`
- Creates a documentation index file at `references/databasin-docs/00-documentation-index.md`

**Custom output location:**

```bash
bun scripts/fetch-docs.ts /path/to/custom/output
```

### 2. Build Searchable Index

Generate a consolidated index from fetched documentation with categorization, line numbers, and descriptions.

**When to use:**
- After fetching documentation for the first time
- After documentation updates
- When the index needs to be regenerated

**How to build:**

```bash
bun scripts/build-index.ts
```

This command:
- Scans all markdown files in `references/databasin-docs/`
- Extracts headers and their line numbers
- Categorizes content by module (Flowbasin, Lakebasin, Reportbasin, etc.)
- Generates a consolidated index at `references/documentation-index.md`

**Custom paths:**

```bash
bun scripts/build-index.ts /path/to/docs /path/to/output/index.md
```

**Index structure:**

The generated index includes:
- **Table of Contents** - Quick navigation to each category
- **Categorized sections** - Organized by module/topic (Flowbasin, Lakebasin, API, Frontend, Backend, etc.)
- **File locations** - Relative paths with line numbers (e.g., `docs/api-guide.md:42`)
- **Descriptions** - Brief content previews for context

### 3. Search Documentation Efficiently

Use the index for low-token documentation lookups.

**Workflow:**

1. **Search the index first** - Read `references/documentation-index.md` to find relevant topics
2. **Identify file location** - Note the file path and line number from index entry
3. **Read specific section** - Use the Read tool with the file path and line number to load only the relevant content

**Example search pattern:**

```
User asks: "How do Flowbasin pipelines handle errors?"

1. Read references/documentation-index.md
2. Search for "pipeline" or "error" in the Flowbasin category
3. Find entry: "Pipeline Error Handling (flowbasin-architecture.md:156)"
4. Read references/databasin-docs/flowbasin-architecture.md starting at line 156
```

**Benefits:**
- Minimal token usage - load only the index first
- Targeted reading - fetch only relevant documentation sections
- Fast lookups - categories and line numbers enable quick navigation

### Documentation Categories

The index organizes content into these categories:

- **Flowbasin** - Pipeline management, data integration, connectors
- **Lakebasin** - SQL queries, Trino connections, query execution
- **Reportbasin** - AI reporting, LLM integration, report generation
- **API** - API endpoints, request/response patterns, authentication
- **Frontend** - Svelte components, ViewModels, UI patterns
- **Backend** - Scala services, controllers, business logic
- **Connectors** - Data source integrations, OAuth flows
- **Authentication** - Auth flows, token management, security
- **Configuration** - Setup, environment variables, deployment
- **General** - Uncategorized documentation

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

### 5. When Accessing Documentation
- **Use indexed search first:** Check documentation-index.md before fetching full docs
- **Fetch targeted sections:** Read only the specific file:line needed
- **Update as needed:** Refresh documentation when Databasin updates
- **Provide context:** Include file locations when referencing docs

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

## Scripts Directory

### scripts/fetch-docs.ts
TypeScript/Bun script that fetches documentation using `databasin docs` commands:
- Lists all available documentation
- Fetches each document individually
- Saves to `references/databasin-docs/`
- Creates documentation index

### scripts/build-index.ts
TypeScript/Bun script that builds the consolidated searchable index:
- Scans all markdown files in documentation directory
- Extracts headers with line numbers
- Categorizes by module/topic
- Generates `references/documentation-index.md`

## Typical Workflow Examples

### Initial Setup with Documentation
1. Fetch documentation from GitHub:
   ```bash
   bun scripts/fetch-docs.ts
   ```

2. Build the searchable index:
   ```bash
   bun scripts/build-index.ts
   ```

3. Reference available at `references/documentation-index.md`

### Regular Usage
1. When a documentation question arises, read the index:
   ```
   Read references/documentation-index.md
   ```

2. Search for relevant keywords in the category structure

3. Locate the file path and line number from the index entry

4. Read the specific documentation section:
   ```
   Read references/databasin-docs/[file-name].md (starting at line X)
   ```

### Updating Documentation
1. Re-fetch latest documentation:
   ```bash
   bun scripts/fetch-docs.ts
   ```

2. Rebuild the index:
   ```bash
   bun scripts/build-index.ts
   ```

## Summary

The Databasin CLI is your comprehensive tool for:
- **Data Integration:** 250+ prebuilt connectors to any source
- **Data Discovery:** SQL interface to explore and query data
- **Pipeline Management:** Build, run, and monitor ETL/ELT workflows
- **Automation:** Execute complex business logic and orchestration
- **Troubleshooting:** Detailed logs and debug capabilities
- **Data Administration:** Manage projects, permissions, and infrastructure
- **Documentation Access:** Fetch, index, and search Databasin documentation efficiently

**Golden Rules:**
1. Always authenticate first: `databasin auth login`
2. Always check logs when troubleshooting: `databasin <resource> logs <id>`
3. Always explore before querying: catalogs → schemas → tables → sample
4. Always test connectors individually before building pipelines
5. Always use appropriate output format: --json for scripts, --csv for exports, table for viewing
6. Use indexed documentation search first: `references/documentation-index.md`
7. Fetch targeted documentation sections: only read what you need

To assist users effectively, leverage all Databasin CLI capabilities, translate their data needs into proper commands and SQL queries, troubleshoot issues systematically using the bundled troubleshooting guide, access documentation efficiently using the index, and guide them through building robust data workflows.
