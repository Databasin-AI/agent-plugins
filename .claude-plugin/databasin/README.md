# Databasin Claude Code Plugin

Complete plugin for Databasin CLI integration, providing authenticated access, pipeline management, connector configuration, and specialized agents for data engineering workflows.

## Plugin Structure

```
.claude-plugin/databasin/
├── plugin.json              # Plugin manifest
├── commands/                 # Slash commands for common operations
│   ├── list-projects.md
│   ├── list-connectors.md
│   ├── create-connector.md
│   ├── create-pipeline.md
│   └── create-report.md
├── agents/                   # Specialized subagents
│   └── databasin-pipeline-creator.md
├── skills/                   # Expert skills
│   ├── databasin-cli-skill/
│   ├── databasin-connectors/
│   ├── databasin-pipelines/
│   └── databasin-automations/
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
