# Databasin Plugin Usage Guide

This guide explains how to use the Databasin Claude Code plugin for data integration, pipeline management, and connector configuration.

## What is This Plugin?

The Databasin plugin extends Claude Code with specialized capabilities for working with the Databasin data platform through the **Databasin CLI**. It provides:

- **Slash commands** for common operations
- **Expert agents** for pipeline creation
- **Specialized skills** for connectors, pipelines, automations, and CLI operations
- **Token-efficient workflows** optimized for AI interactions

## Prerequisites

### 1. Install Databasin CLI

Ensure the Databasin CLI is installed:

```bash
# Check if installed
databasin --version

# View all available commands
databasin --help
```

If not installed, follow your organization's Databasin CLI installation guide.

### 2. Authenticate

```bash
# Browser-based authentication (one-time setup)
databasin auth login

# Verify authentication
databasin auth whoami
```

The CLI opens your browser for secure authentication. Tokens are stored in `~/.databasin/config.json` and refreshed automatically.

### 3. Optional: Enable Shell Completions

For better CLI experience with tab completion:

```bash
# Bash
databasin completion install bash

# Zsh
databasin completion install zsh

# Fish
databasin completion install fish
```

## Installation

### Option 1: Install from Claude Code Marketplace (Recommended)

1. Open Claude Code CLI
2. Type `/plugin marketplace add databasin-ai/agent-plugins`
3. Click "Install" or follow prompts
4. Restart Claude Code

### Option 2: Local Installation

```bash
cd /path/to/your/project
mkdir -p .claude-plugin
cp -r /path/to/databasin .claude-plugin/
```

Verify installation:
```bash
ls .claude-plugin/databasin/.claude-plugin/plugin.json
```

Restart Claude Code to load the plugin.

## Using Slash Commands

The plugin provides 5 slash commands for common operations. All use the `databasin:` prefix.

### 1. List Projects

```
/databasin:list-projects
```

Lists all Databasin projects accessible to the current user.

**Example:**
```
You: /databasin:list-projects
Claude: [Shows all your projects with IDs and details]
```

**CLI Equivalent:**
```bash
databasin projects list
```

### 2. List Connectors

```
/databasin:list-connectors
```

Shows count of available data source connectors (250+ types). Uses token-efficient count mode by default.

**Example:**
```
You: /databasin:list-connectors
Claude: Total connectors: 434
  Use --full flag to see full connector list
```

**CLI Equivalent:**
```bash
# Count only (default, ~50 tokens)
databasin connectors list -p <project-id>

# Full list with specific fields (~5,000 tokens)
databasin connectors list -p <project-id> --full --fields "connectorID,connectorName,connectorType"
```

### 3. Create Connector

```
/databasin:create-connector
```

Guides you through creating a new data source connector.

**Example:**
```
You: /databasin:create-connector
Claude: What type of connector would you like to create?
You: PostgreSQL
Claude: [Walks through PostgreSQL connection configuration]
```

**CLI Equivalent:**
```bash
# Get connector configuration requirements
databasin connectors config PostgreSQL

# Create connector
databasin connectors create postgres-config.json -p <project-id>

# Test connection
databasin connectors test <connector-id>
```

### 4. Create Pipeline

```
/databasin:create-pipeline
```

Creates a pipeline from JSON configuration file.

**Example:**
```
You: /databasin:create-pipeline
Claude: [Guides through creating pipeline configuration and executes creation command]
```

**CLI Equivalent:**
```bash
# Generate template first
databasin pipelines template > pipeline-config.json

# Create from configuration file
databasin pipelines create pipeline-config.json -p <project-id>
```

### 5. Create Report

```
/databasin:create-report
```

Helps create reports and analytics in Reportbasin.

**Example:**
```
You: /databasin:create-report
Claude: [Guides through report configuration]
```

## Using Skills

Skills are automatically invoked by Claude when relevant, or you can explicitly reference them using `@skill-name`.

### @skill-databasin-cli

Expert skill for using the Databasin CLI. Handles data connector management, pipeline operations, SQL queries, and automations.

**Automatic Invocation:**
```
You: Show me all my Databasin projects
Claude: [Uses @skill-databasin-cli to list projects]

You: How many connectors do we have?
Claude: [Uses CLI skill to get connector count]
```

**Explicit Invocation:**
```
You: @skill-databasin-cli help me troubleshoot this pipeline failure
Claude: [Directly invokes CLI skill for troubleshooting]
```

**Key Features:**
- Token-efficient data exploration (count mode, field filtering)
- SQL query execution and data discovery
- Pipeline and automation management
- Comprehensive troubleshooting

### @skill-databasin-connectors

Specialized skill for data connector creation, configuration, and management. Knows about 250+ connector types.

**Use Cases:**
- Creating new connectors
- Understanding connector configuration options
- Troubleshooting connector authentication
- Finding the right connector for your data source

**Example:**
```
You: @skill-databasin-connectors I need to connect to Salesforce, what do I need?
Claude: [Provides Salesforce connector configuration guide including OAuth setup]
```

### @skill-databasin-pipelines

Expert skill for pipeline creation, execution, and monitoring.

**Use Cases:**
- Building ETL/ELT pipelines
- Generating pipeline configuration files
- Configuring data transformations
- Setting up pipeline schedules
- Troubleshooting pipeline failures

**Example:**
```
You: @skill-databasin-pipelines create a pipeline from MySQL to Snowflake
Claude: [Guides through creating pipeline configuration file and executing creation command]
```

### @skill-databasin-automations

Specialized skill for creating and managing automations including scheduled tasks and event-driven workflows.

**Use Cases:**
- Setting up scheduled data loads
- Creating event-triggered workflows
- Configuring automation schedules with cron expressions
- Troubleshooting automation failures

**Example:**
```
You: @skill-databasin-automations set up a daily data sync at 6am
Claude: [Helps configure automation with cron schedule]
```

## Using the Agent

### @agent-databasin-pipeline-creator

Elite pipeline architect agent for designing, configuring, and deploying data integration pipelines.

**When to Use:**
- Creating pipelines from scratch
- Configuring complex multi-step pipelines
- Setting up source-to-destination data flows
- Troubleshooting pipeline creation issues

**Automatic Invocation:**
```
You: I need to create a pipeline from Salesforce to PostgreSQL
Claude: [Automatically invokes @agent-databasin-pipeline-creator]
```

**Explicit Invocation:**
```
You: @agent-databasin-pipeline-creator create a multi-step pipeline with transformations
Claude: [Directly invokes the pipeline creator agent]
```

**Agent Capabilities:**
- Requirements gathering for pipeline design
- Connector validation and selection
- Step-by-step pipeline configuration guidance
- Field mapping and transformation setup
- Pipeline testing and troubleshooting
- Production deployment assistance

## Common Workflows

### Workflow 1: First-Time Setup

```
You: /databasin:list-projects
Claude: [Shows all accessible projects]

You: /databasin:list-connectors
Claude: Total connectors: 434

You: Show me how to connect to PostgreSQL
Claude: [Uses @skill-databasin-connectors to explain PostgreSQL setup]
```

**CLI Commands:**
```bash
# Authenticate
databasin auth login

# List projects
databasin projects list

# Get connector count
databasin connectors list -p <project-id>

# Get connector configuration requirements
databasin connectors config PostgreSQL
```

### Workflow 2: Create a Data Pipeline

```
You: I want to sync data from MySQL to Snowflake daily
Claude: I'll help you create this pipeline using file-based configuration.

[Agent creates pipeline configuration:]
1. Identify source connector (MySQL)
2. Identify destination connector (Snowflake)
3. Generate pipeline configuration JSON
4. Configure schedule (daily at 2 AM)
5. Create pipeline from configuration
```

**CLI Commands:**
```bash
# Generate template
databasin pipelines template > pipeline.json

# Create pipeline from configuration
databasin pipelines create pipeline.json -p <project-id>
```

The file-based approach provides:
- Full control over configuration
- Version-controllable pipeline definitions
- Reusable templates
- Automated pipeline creation

### Workflow 3: Create Multiple Pipelines Programmatically

```
You: Create a pipeline from connector-123 to connector-456
Claude: [Uses @skill-databasin-pipelines]

Claude: Let me create this pipeline...
[Executes:]
1. Verify connectors exist
2. Explore source schema
3. Configure pipeline
4. Create and test
```

**CLI Commands:**
```bash
# Verify connectors
databasin connectors test 123
databasin connectors test 456

# Create pipeline from config file
databasin pipelines create pipeline-config.json -p <project-id>

# Run pipeline
databasin pipelines run <pipeline-id>

# Monitor execution
databasin pipelines logs <pipeline-id>
databasin pipelines history <pipeline-id>
```

### Workflow 4: Troubleshooting

```
You: My pipeline keeps failing, how do I debug it?
Claude: [Uses @skill-databasin-cli to check logs]

Claude: Let me check the pipeline logs...
[Analyzes errors and provides solutions]
```

**CLI Commands:**
```bash
# Check pipeline logs
databasin pipelines logs <pipeline-id>

# View execution history
databasin pipelines history <pipeline-id>

# Test connectors
databasin connectors test <connector-id>
```

### Workflow 5: Data Discovery

```
You: Find all customers who ordered in the last month
Claude: [Uses @skill-databasin-cli for data discovery]

Claude: Let me explore your data structure...
[Executes:]
1. List available connectors
2. Explore database schemas
3. Find customer and order tables
4. Generate SQL query
5. Execute and show results
```

**CLI Commands:**
```bash
# Explore data hierarchy
databasin sql catalogs <connector-id>
databasin sql schemas <connector-id> --catalog <catalog>
databasin sql tables <connector-id> --catalog <catalog> --schema <schema>

# Execute SQL query
databasin sql exec <connector-id> "
SELECT c.*
FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o
  WHERE o.customer_id = c.id
  AND o.created_at > CURRENT_DATE - INTERVAL '1 month'
)
"
```

### Workflow 6: Create Automation

```
You: Set up a daily sync job at 6 AM
Claude: [Uses @skill-databasin-automations]

Claude: I'll create a scheduled automation...
[Sets up cron schedule: "0 6 * * *"]
```

**CLI Commands:**
```bash
# Create automation from config
databasin automations create automation-config.json -p <project-id>

# View automations
databasin automations list -p <project-id>

# Check execution history
databasin automations history <automation-id>
```

## Natural Language Usage

You don't need to memorize commands. Claude automatically determines the right tools based on your requests:

**Data Exploration:**
```
You: What data sources do I have access to?
Claude: [Uses CLI to list connectors]

You: Show me the schema of my production database
Claude: [Explores database schema using SQL commands]
```

**Pipeline Operations:**
```
You: Create a pipeline that moves data from Salesforce to our warehouse
Claude: [Invokes @agent-databasin-pipeline-creator ]

You: Why did my pipeline fail last night?
Claude: [Checks logs and provides diagnosis]
```

**Connector Management:**
```
You: How do I connect to AWS S3?
Claude: [Uses @skill-databasin-connectors for S3 configuration]

You: What authentication does Salesforce require?
Claude: [Explains OAuth setup]
```

## Token Efficiency Features

The plugin is optimized for AI interactions with minimal token usage:

### Count Mode (Default)

```bash
# Returns count only (~50 tokens vs ~50,000+)
databasin connectors list -p <project-id>
# Output: "Total connectors: 434"
```

**When to use --full flag:**
```bash
# When you need full objects
databasin connectors list -p <project-id> --full --fields "connectorID,connectorName,connectorType"
```

### Field Filtering

```bash
# Only fetch fields you need (saves 80%+ tokens)
databasin pipelines list -p <project-id> --fields "pipelineID,pipelineName,status"
```

### Result Limiting

```bash
# Fetch in batches
databasin connectors list -p <project-id> --full --limit 20
```

### Important for AI Agents

**Interactive prompts are not supported in agent workflows.** Always provide all required arguments:

```bash
# ❌ Will fail in agent context (prompts for missing args)
databasin connectors list

# ✅ Correct - provide all required arguments
databasin connectors list -p <project-id>
databasin connectors get <connector-id>
databasin pipelines list -p <project-id>
```

## Access Documentation

The CLI includes built-in documentation:

```bash
# List all docs
databasin docs

# View specific docs
databasin docs sql-queries
databasin docs pipelines
databasin docs connectors
databasin docs troubleshooting
```

Claude can also reference these docs automatically when helping you.

## Troubleshooting

### Plugin Not Loading

**Problem:** Commands don't appear in `/help`

**Solutions:**
1. Verify: `.claude-plugin/databasin/.claude-plugin/plugin.json` exists
2. Restart Claude Code
3. Run `/plugins` to see loaded plugins

### CLI Not Found

**Problem:** "databasin command not found"

**Solution:**
```bash
# Verify CLI installation
which databasin

# Check version
databasin --version

# If not installed, follow your organization's installation guide
```

### Authentication Errors

**Problem:** "Unauthorized" or "Authentication required"

**Solution:**
```bash
# Re-authenticate
databasin auth login

# Verify authentication
databasin auth whoami
```

### Connector List Returns Count Only

**This is expected behavior (token-efficient default)**

**Solution:**
```bash
# Use --full flag when you need full objects
databasin connectors list -p <project-id> --full

# Or get specific fields only
databasin connectors list -p <project-id> --full --fields "connectorID,connectorName,connectorType"
```

### Skill Not Responding

**Problem:** Skill doesn't activate when expected

**Solutions:**
1. Use explicit invocation: `@skill-databasin-cli your request`
2. Be more specific in your request
3. Check that Databasin CLI is installed and authenticated

## Getting Help

### Within Claude Code

```
You: How do I use the Databasin plugin?
Claude: [Provides overview of capabilities]

You: What can @skill-databasin-cli do?
Claude: [Lists CLI skill capabilities]

You: Show me examples of pipeline creation
Claude: [Provides examples  programmatic approaches]
```

### Documentation Resources

The plugin includes extensive reference documentation:

- **CLI Skill References:**
  - `skills/databasin-cli-skill/references/advanced-workflows.md`
  - `skills/databasin-cli-skill/references/example-queries.md`
  - `skills/databasin-cli-skill/references/troubleshooting.md`
  - `skills/databasin-cli-skill/references/token-efficiency.md`

- **Connector Skill References:**
  - `skills/databasin-connectors/references/connector-types-guide.md`
  - `skills/databasin-connectors/references/authentication-guide.md`
  - `skills/databasin-connectors/references/field-reference.md`

- **Pipeline Skill References:**
  - `skills/databasin-pipelines/references/examples.md`
  - `skills/databasin-pipelines/references/pipeline-automation.md`

- **Automation Skill References:**
  - `skills/databasin-automations/references/cron-schedule-guide.md`
  - `skills/databasin-automations/references/task-types-reference.md`

### Command Help

Get help for any command:

```bash
databasin --help
databasin connectors --help
databasin pipelines template --help
```

## Best Practices

### 1. Always Authenticate First

```bash
databasin auth whoami
# If not authenticated: databasin auth login
```

### 2. Use Natural Language

Don't worry about exact syntax:
```
You: I need to move data from MySQL to BigQuery every day
Claude: [Handles the complexity  programmatic approach]
```

### 3. Leverage the Interactive Wizard

For complex pipelines, use file-based configuration:
```bash
databasin pipelines template
```

Benefits:
- Step-by-step guidance
- Automatic schema discovery
- Field mapping recommendations
- Built-in validation
- No need to write JSON configs

### 4. Use Token-Efficient Commands

```bash
# Good: Check count first
databasin connectors list -p proj-001

# Then get limited fields if needed
databasin connectors list -p proj-001 --full --fields "connectorID,connectorName" --limit 10
```

### 5. Check Logs for Troubleshooting

```bash
# Always review logs when things go wrong
databasin pipelines logs <pipeline-id>
databasin pipelines history <pipeline-id>
```

## Summary

The Databasin Claude Code plugin transforms how you work with the Databasin platform:

- **Simple commands** for common operations
- **File-based configuration** for complex pipeline creation
- **Intelligent skills** that understand your data integration needs
- **Expert agents** for multi-step workflows
- **Natural language interface** - just describe what you need
- **Token-efficient** - optimized for AI interactions

**Get Started:**
```bash
# Authenticate
databasin auth login

# List projects
databasin projects list

# Create your first pipeline
databasin pipelines template
```

Then explore connectors, create pipelines, and automate your data workflows using natural conversation with Claude.

## Version & Updates

**Plugin Version:** 1.1.0
**Last Updated:** 2025-12-07

**Latest Updates:**
- Added `databasin pipelines template` for generating configuration
- Added `databasin connectors config` command
- Added `databasin docs` for accessing documentation
- Documented count mode as default for connector list
- Updated authentication to `databasin auth login`
- Removed outdated script-based workflows
- **Clarified that interactive features (wizards, prompts) are not supported for AI agents**
- Emphasized file-based configuration workflow for pipeline creation
- Added token efficiency guidance throughout

## Support

For issues, questions, or feature requests:

1. Ask Claude directly: `How do I [task] with Databasin?`
2. Use `databasin docs` to access documentation
3. Reference skill documentation for detailed guides
4. Check the Databasin CLI help: `databasin <command> --help`
5. Contact your Databasin administrator
