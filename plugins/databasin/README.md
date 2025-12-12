# Databasin Claude Code Plugin

Complete plugin for Databasin CLI integration, providing authenticated access, pipeline management, connector configuration, and specialized agents for data engineering workflows.

## Platform Overview

**Databasin** is an enterprise data integration platform that provides three integrated modules for comprehensive data management:

### Flowbasin - Data Integration & Pipeline Management
The core data integration engine that connects to 250+ data sources and orchestrates ETL/ELT workflows.

**Key capabilities:**
- **Connector Management**: Create and configure connections to databases, cloud storage, SaaS applications, and streaming platforms
- **Pipeline Orchestration**: Build, schedule, and monitor data pipelines for automated data movement
- **Transformation Engine**: Apply data transformations, validations, and enrichments during pipeline execution
- **Artifact Management**: Configure granular data artifacts within pipelines for complex workflows

**Common use cases:**
- Sync data from operational databases to analytics warehouses
- Integrate CRM data (Salesforce, HubSpot) with internal systems
- Consolidate data from multiple sources into a unified data lake
- Automate recurring data exports and imports

### Lakebasin - Interactive SQL Query Engine
Direct SQL access to connected data sources using Trino-powered distributed query execution.

**Key capabilities:**
- **Schema Discovery**: Explore catalogs, schemas, and tables across all connected sources
- **SQL Execution**: Run ad-hoc SQL queries against any connected database
- **Direct Connections**: Optional browser-based direct connections to Trino clusters
- **Data Exploration**: Sample data, validate schemas, and perform data quality checks

**Common use cases:**
- Explore unfamiliar databases to understand structure and content
- Run ad-hoc queries for analysis without building pipelines
- Validate data quality before and after pipeline executions
- Perform schema comparisons between source and target systems

### Reportbasin - AI-Powered Analytics & Reporting
LLM-integrated reporting system that generates insights from your data.

**Key capabilities:**
- **Natural Language Queries**: Describe what you want to analyze in plain language
- **Automated Data Collection**: AI gathers relevant data from connected sources
- **Intelligent Analysis**: LLM-powered insights and pattern detection
- **Report Generation**: Automated report creation with visualizations and recommendations

**Common use cases:**
- Generate executive summaries from complex datasets
- Identify trends and anomalies automatically
- Create recurring analytical reports
- Answer business questions through natural language

## Integration Architecture

The Databasin CLI provides unified access to all three modules:

```
┌─────────────────────────────────────────────────────┐
│              Databasin CLI                           │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌───────────────┐  ┌───────────────┐  ┌──────────┐│
│  │  Flowbasin    │  │  Lakebasin    │  │ Reportbasin│
│  │  Commands     │  │  Commands     │  │ Commands   │
│  ├───────────────┤  ├───────────────┤  ├──────────┤│
│  │ • connectors  │  │ • sql exec    │  │ • reports │ │
│  │ • pipelines   │  │ • sql tables  │  │ • analyze │ │
│  │ • automations │  │ • sql discover│  │ • insights│ │
│  └───────────────┘  └───────────────┘  └──────────┘│
│                                                       │
├─────────────────────────────────────────────────────┤
│            Authentication & Projects                  │
│     • auth login  • auth whoami  • projects list    │
└─────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│        Databasin API (Backend Services)              │
│   • REST API  • Authentication  • Module Guard       │
└─────────────────────────────────────────────────────┘
```

## Plugin Structure

```
.claude-plugin/databasin/
├── plugin.json              # Plugin manifest
├── LICENSE                  # CC-BY-4.0 License
├── commands/                 # Slash commands for common operations
│   ├── list-projects.md
│   ├── list-connectors.md
│   ├── create-connector.md
│   ├── create-pipeline.md
│   └── create-report.md
├── agents/                   # Specialized subagents
│   └── databasin-pipeline-creator.md
├── skills/                   # Expert skills
│   ├── databasin-cli-skill/       # General CLI expertise
│   ├── databasin-connectors/      # Connector management
│   ├── databasin-pipelines/       # Pipeline workflows
│   ├── databasin-automations/     # Automation scheduling
│   └── databasin-query-assistant/ # SQL query assistance
├── examples/                 # Real-world workflow examples
│   ├── README.md
│   ├── postgres-to-snowflake-pipeline.md
│   ├── troubleshooting-failed-pipeline.md
│   └── connector-inspection-and-cloning.md
└── README.md                 # This file
```

## Associated Skills

This plugin works with specialized skills in the `skills/` directory:

- **databasin-cli-skill** - Expert skill for using the Databasin CLI
  - Commands for connectors, pipelines, automations, SQL queries
  - Token-efficient data exploration
  - Comprehensive troubleshooting guides

- **databasin-connectors** - Data connector management skill
  - Create, configure, test 250+ connector types
  - OAuth and credential authentication
  - Connection troubleshooting

- **databasin-pipelines** - Pipeline creation and management
  - File-based pipeline configuration
  - Artifact configuration
  - Pipeline monitoring and logs

- **databasin-automations** - Workflow automation management
  - Scheduled task creation
  - Event-driven workflows
  - Automation monitoring

## 🔑 Critical: Always Use Project Internal IDs

**IMPORTANT:** Many Databasin CLI commands require a `--project` (or `-p`) argument. Always use the project's **internal ID (alphanumeric string)**, not the project name.

### Finding Your Project ID

```bash
# Login first
databasin auth login

# View your projects with their internal IDs
databasin auth whoami

# Example output:
# User: john.doe@company.com
# Organizations:
#   - Acme Corp (ID: 123)
# Projects:
#   - Production Data Warehouse (ID: N1r8Do)  ← Use this ID
#   - Development Environment (ID: K9mPx2)    ← Or this ID
```

### Using Project IDs Correctly

```bash
# ✅ CORRECT - using internal ID
databasin connectors list --project N1r8Do
databasin pipelines create config.json --project N1r8Do
databasin pipelines clone 8901 --project N1r8Do

# ❌ WRONG - using project name (will fail)
databasin connectors list --project "Production Data Warehouse"
```

**Why this matters:** The Databasin API uses internal IDs for all resource references. Project names can change, but IDs remain stable. Always reference projects by their ID for reliable automation.

## Quick Start

### 1. Install the Databasin CLI

Ensure the Databasin CLI is installed and accessible:

```bash
# Verify CLI installation
databasin --version

# View available commands
databasin --help
```

If not installed, follow your organization's Databasin CLI installation guide.

### 2. Authenticate

Use browser-based authentication (recommended):

```bash
# Open browser for secure authentication
databasin auth login

# Verify authentication
databasin auth whoami
```

Authentication tokens are stored securely in `~/.databasin/config.json` and refreshed automatically.

### 3. Optional: Enable Shell Completions

Enable tab completion for better CLI experience:

```bash
# Bash
databasin completion install bash

# Zsh
databasin completion install zsh

# Fish
databasin completion install fish
```

### 4. Use Slash Commands

The plugin provides these commands (use with `databasin:` prefix):

- **/databasin:list-projects** - List all accessible projects
- **/databasin:list-connectors** - List available data source connectors
- **/databasin:create-connector** - Create new data connector from JSON configuration
- **/databasin:create-pipeline** - Create pipeline from JSON configuration
- **/databasin:create-report** - Create reports and analytics

### 5. Use Skills and Agents

Skills are automatically invoked based on your requests, or you can explicitly reference them:

- **@skill-databasin-cli** - CLI commands and data operations
- **@skill-databasin-connectors** - Connector creation and management
- **@skill-databasin-pipelines** - Pipeline workflows
- **@skill-databasin-automations** - Automation scheduling
- **@agent-databasin-pipeline-creator** - Complete pipeline setup assistant

## Available Commands

### List Projects

```bash
/databasin:list-projects
```

Displays all projects accessible to the current user with IDs, organization info, and status.

**CLI Equivalent:**
```bash
databasin projects list
```

### List Connectors

```bash
/databasin:list-connectors
```

Shows count of available data source connectors. Uses token-efficient count mode by default.

**CLI Equivalent:**
```bash
# Count only (default, token-efficient)
databasin connectors list -p <project-id>

# Full list with specific fields
databasin connectors list -p <project-id> --full --fields "connectorID,connectorName,connectorType"
```

### Create Connector

```bash
/databasin:create-connector
```

Guides you through creating a new data source connector with appropriate configuration.

**CLI Equivalent:**
```bash
# Get connector configuration requirements
databasin connectors config PostgreSQL

# Create connector from config file
databasin connectors create postgres-config.json -p <project-id>

# Test connection
databasin connectors test <connector-id>
```

### Create Pipeline

```bash
/databasin:create-pipeline
```

Creates a data integration pipeline from JSON configuration file.

**CLI Equivalent:**
```bash
# Create from configuration file
databasin pipelines create pipeline-config.json -p <project-id>

# Generate template first
databasin pipelines template > pipeline-config.json

# View pipeline details
databasin pipelines get <pipeline-id>
```

### Create Report

```bash
/databasin:create-report
```

Helps you create reports and analytics in the Reportbasin module.

## Common Workflows

### Workflow 1: First-Time Setup

```bash
# 1. Authenticate
databasin auth login

# 2. Verify authentication
databasin auth whoami

# 3. List your projects
databasin projects list

# 4. Enable shell completions (optional)
databasin completion install bash
```

### Workflow 2: Explore Your Data

```bash
# List projects
databasin projects list

# Get connector count (token-efficient)
databasin connectors list -p <project-id>

# Explore SQL data sources
databasin sql catalogs <connector-id>
databasin sql schemas <connector-id> --catalog <catalog-name>
databasin sql tables <connector-id> --catalog <catalog> --schema <schema>

# Execute SQL query
databasin sql exec <connector-id> "SELECT * FROM users LIMIT 10"
```

### Workflow 3: Create a Data Pipeline

```bash
# Step 1: Verify connectors exist
databasin connectors list -p <project-id> --full --fields "connectorID,connectorName"

# Step 2: Generate pipeline template
databasin pipelines template > pipeline-config.json

# Step 3: Edit configuration (add source, target, artifacts, schedule)
# Edit pipeline-config.json with your preferred editor

# Step 4: Create pipeline from configuration
databasin pipelines create pipeline-config.json -p <project-id>

# Step 5: Run pipeline
databasin pipelines run <pipeline-id>

# Step 6: Monitor execution
databasin pipelines logs <pipeline-id>
databasin pipelines history <pipeline-id>
```

### Workflow 4: Set Up Automation

```bash
# Create scheduled automation
databasin automations create automation-config.json -p <project-id>

# View automation status
databasin automations list -p <project-id>

# Check execution history
databasin automations history <automation-id>
```

## Token Efficiency

The CLI is designed for optimal token usage in AI workflows:

### Count Mode (Default)

Many commands return counts by default to save tokens:

```bash
# Returns count only (~50 tokens vs ~50,000+)
databasin connectors list -p <project-id>
# Output: "Total connectors: 434"

# Use --full flag when you need full objects
databasin connectors list -p <project-id> --full
```

### Field Filtering

Limit response size by selecting specific fields:

```bash
# Only fetch fields you need
databasin connectors list -p <project-id> --full --fields "connectorID,connectorName,connectorType"
```

### Result Limiting

Limit number of results:

```bash
# Fetch in batches
databasin connectors list -p <project-id> --full --limit 20
```

### Token Efficiency Best Practices

1. **Start with count mode** - Check counts before fetching full data
2. **Use field filtering** - Only request fields you need
3. **Filter by project** - Always specify `-p <project-id>` when available
4. **Use pagination** - Fetch large result sets in batches

**Example: Token-Efficient Workflow**

```bash
# Step 1: Get count (~50 tokens)
databasin connectors list -p proj-001

# Step 2: Get limited fields for subset (~5,000 tokens)
databasin connectors list -p proj-001 --full --fields "connectorID,connectorName" --limit 20

# Step 3: Get full details only for specific items (~2,000 tokens each)
databasin connectors get <connector-id>
```

## Access Documentation

The CLI includes built-in documentation access:

```bash
# List all available docs
databasin docs

# View specific documentation
databasin docs sql-queries        # SQL query patterns
databasin docs pipelines          # Pipeline creation guide
databasin docs connectors         # Connector configuration
databasin docs troubleshooting    # Troubleshooting guide
```

## Error Handling

### Authentication Errors

```
Error: Authentication required
Solution: Run 'databasin auth login'
```

### Connector Not Found

```
Error: Connector not found (404)
Solution: Run 'databasin connectors list -p <project> --full' to see available connectors
```

### Pipeline Failures

```bash
# Check pipeline logs
databasin pipelines logs <pipeline-id>

# View execution history
databasin pipelines history <pipeline-id>

# Re-run with debug mode
DATABASIN_DEBUG=true databasin pipelines run <pipeline-id>
```

### Connection Test Failures

```bash
# Test connector
databasin connectors test <connector-id>

# Get connector details
databasin connectors get <connector-id>

# Update connector configuration
databasin connectors update <connector-id> updated-config.json
```

## Plugin Capabilities

This plugin provides:

1. **Data Integration** - 250+ prebuilt connectors to any data source
2. **Pipeline Management** - Create, run, monitor ETL/ELT workflows
3. **SQL Execution** - Query and explore data via SQL interface
4. **Automation** - Schedule recurring data workflows
5. **Token Efficiency** - Optimized for AI agent interactions
6. **File-based Configuration** - JSON-based pipeline and connector creation

## CLI Command Categories

### Authentication
- `databasin auth login` - Browser-based authentication
- `databasin auth whoami` - View current user
- `databasin auth verify` - Check token validity

### Projects
- `databasin projects list` - List all projects
- `databasin projects get <id>` - Get project details

### Connectors
- `databasin connectors list -p <project>` - List connectors (count mode default)
- `databasin connectors get <id>` - Get connector details
- `databasin connectors config <subtype>` - Get connector configuration requirements
- `databasin connectors create <file> -p <project>` - Create connector
- `databasin connectors update <id> <file>` - Update connector
- `databasin connectors test <id>` - Test connection
- `databasin connectors delete <id>` - Delete connector

### SQL Interface
- `databasin sql catalogs <connector-id>` - List catalogs
- `databasin sql schemas <connector-id> --catalog <name>` - List schemas
- `databasin sql tables <connector-id> --catalog <cat> --schema <sch>` - List tables
- `databasin sql exec <connector-id> "<query>"` - Execute SQL query

### Pipelines
- `databasin pipelines template` - Generate pipeline configuration template
- `databasin pipelines list -p <project>` - List pipelines (requires project ID)
- `databasin pipelines get <id>` - Get pipeline details
- `databasin pipelines create <file> -p <project>` - Create pipeline
- `databasin pipelines run <id>` - Execute pipeline
- `databasin pipelines logs <id>` - View execution logs
- `databasin pipelines history <id>` - View execution history

### Automations
- `databasin automations list` - List automations
- `databasin automations get <id>` - Get automation details
- `databasin automations create <file> -p <project>` - Create automation
- `databasin automations run <id>` - Execute automation
- `databasin automations history <id>` - View execution history

### Documentation & Help
- `databasin docs [name]` - Access GitHub documentation
- `databasin completion install <shell>` - Install shell completions
- `databasin --help` - View all available commands

## Output Formats

All commands support multiple output formats:

```bash
# Table format (default, human-readable)
databasin projects list

# JSON format (for scripting)
databasin projects list --json

# CSV format (for spreadsheets)
databasin projects list --csv

# Specific fields only
databasin projects list --fields "projectID,projectName,status"
```

## Important Notes for AI Agents

**Interactive features are not supported in agent workflows.** Always provide all required arguments explicitly:

```bash
# Always specify required arguments
databasin connectors list -p <project-id>
databasin connectors get <connector-id>
databasin pipelines list -p <project-id>

# Use file-based configuration instead of interactive wizards
databasin pipelines template > pipeline.json
# Edit pipeline.json
databasin pipelines create pipeline.json -p <project-id>
```

## 📚 Comprehensive Examples

The `examples/` directory contains detailed, real-world workflow examples with step-by-step instructions:

### [PostgreSQL to Snowflake Pipeline](./examples/postgres-to-snowflake-pipeline.md)
Complete end-to-end workflow for building a production data pipeline.

**Covers:**
- Authentication and project ID discovery
- Connector creation and testing
- Source data exploration
- Pipeline configuration and validation
- Deployment and monitoring
- Environment cloning strategies

**Perfect for:** First-time users setting up their first pipeline

---

### [Troubleshooting Failed Pipelines](./examples/troubleshooting-failed-pipeline.md)
Systematic approach to diagnosing and fixing pipeline failures.

**Covers:**
- Reading and interpreting logs
- Common failure scenarios (schema changes, permissions, timeouts)
- Testing fixes safely
- Debug mode usage
- Preventive monitoring

**Perfect for:** Users experiencing pipeline issues or building monitoring automation

---

### [Connector Inspection and Pipeline Cloning](./examples/connector-inspection-and-cloning.md)
Advanced techniques for connector analysis and rapid deployment.

**Covers:**
- Using `connectors inspect` for comprehensive analysis
- Understanding database structure before building pipelines
- Environment promotion workflows (dev → staging → prod)
- Testing configuration variations
- Creating pipeline backups

**Perfect for:** Advanced users managing multiple environments or promoting tested pipelines

---

**See [examples/README.md](./examples/README.md) for a complete guide to all available examples.**

## 🔧 Troubleshooting Guide

### Authentication Issues

**Problem:** "Authentication required" or "Token expired" errors

**Solution:**
```bash
# Re-authenticate
databasin auth login

# Verify token validity
databasin auth verify

# Check current user context
databasin auth whoami
```

---

### Pipeline Failures

**Problem:** Pipeline execution fails or shows errors

**Solution:**
```bash
# Step 1: Always check logs FIRST
databasin pipelines logs <pipeline-id>

# Step 2: Review execution history
databasin pipelines history <pipeline-id> --limit 10

# Step 3: Test connectors individually
databasin connectors test <source-connector-id>
databasin connectors test <target-connector-id>

# Step 4: Verify source query
databasin sql exec <source-id> "SELECT 1"

# Step 5: Enable debug mode for detailed diagnostics
DATABASIN_DEBUG=true databasin pipelines run <pipeline-id>
```

---

### Connector Connection Failures

**Problem:** "Connection timeout" or "Connection refused" errors

**Solution:**
```bash
# Test the connector
databasin connectors test <connector-id>

# Inspect comprehensive status
databasin connectors inspect <connector-id>

# Review connector configuration
databasin connectors get <connector-id>

# Common fixes:
# 1. Verify credentials haven't expired
# 2. Check network connectivity to host
# 3. Ensure database/service is running
# 4. Verify firewall rules allow access
```

---

### "Resource Not Found" Errors

**Problem:** "Connector not found" or "Pipeline not found" (404 errors)

**Solution:**
```bash
# For connectors:
databasin connectors list --project <project-id> --full --fields "connectorID,connectorName"

# For pipelines:
databasin pipelines list --project <project-id> --json | jq '.[] | {id: .pipelineID, name: .name}'

# Ensure you're using the correct project ID:
databasin auth whoami  # Check your project IDs
```

---

### SQL Query Errors

**Problem:** "Syntax error" or "Column does not exist" in queries

**Solution:**
```bash
# Verify table structure
databasin sql tables <connector-id> --catalog <cat> --schema <sch>

# Check column names
databasin sql exec <connector-id> "
  SELECT column_name, data_type
  FROM information_schema.columns
  WHERE table_name = 'your_table'
"

# Test with simple query first
databasin sql exec <connector-id> "SELECT 1"
```

---

### Schedule Not Executing

**Problem:** Pipeline configured to run on schedule, but not executing

**Solution:**
```bash
# Check schedule configuration
databasin pipelines get <id> --json | jq '.artifacts[0].schedule'

# Verify schedule is enabled
# Look for: "enabled": true

# Check recent execution history
databasin pipelines history <id> --limit 20

# If enabled but not running:
# 1. Verify cron expression is valid
# 2. Check timezone setting
# 3. Confirm pipeline isn't in error state
# 4. Contact administrator if issue persists
```

---

### Performance Issues

**Problem:** Pipelines running slowly or timing out

**Solution:**
```bash
# Check pipeline execution time trends
databasin pipelines history <id> --json | jq '.[] | {run: .runID, duration: .duration, status: .status}'

# Review logs for slow steps
databasin pipelines logs <id> | grep -i "duration\|elapsed\|time"

# Common performance fixes:
# 1. Add WHERE clauses to limit data volume
# 2. Use incremental loads instead of full refreshes
# 3. Optimize source queries with proper indexes
# 4. Consider parallel pipeline execution for large datasets
```

---

### Getting More Help

1. **Enable Debug Mode:**
   ```bash
   DATABASIN_DEBUG=true databasin <command>
   ```

2. **Check CLI Documentation:**
   ```bash
   databasin docs troubleshooting
   databasin <command> --help
   ```

3. **Use Skills for Guided Assistance:**
   - `@skill-databasin-cli` - General CLI help
   - Review `skills/*/references/troubleshooting.md` files

4. **Consult Examples:**
   - See `examples/troubleshooting-failed-pipeline.md` for detailed troubleshooting workflows

## Support

For issues or questions:

1. Check built-in documentation: `databasin docs`
2. Review skill reference documentation in `skills/*/references/`
3. Use skills explicitly: `@skill-databasin-cli help with <task>`
4. Consult the Databasin CLI help: `databasin <command> --help`
5. Contact your Databasin administrator

## Version History

### v1.1.0 (2025-12-07)

- Updated all documentation to reflect current CLI capabilities
- Added `databasin connectors config` command for discovering workflow requirements
- Added `databasin docs` command for accessing documentation
- Added `databasin pipelines template` for generating configuration templates
- Added shell completion support
- Documented count mode as default for connector list
- Removed outdated script-based workflows
- Added token efficiency guidance throughout
- Updated authentication to use `databasin auth login`
- Clarified that interactive features are not supported for AI agents
- Added file-based workflow patterns for agent automation

### v1.0.0 (2024-11-16)

- Initial plugin structure
- 5 slash commands for common operations
- databasin-pipeline-creator specialized agent
- Integration with databasin CLI
- Comprehensive documentation and examples
