# Databasin Plugin Usage Guide

This guide explains how to install and use the Databasin Claude Code plugin for data integration, pipeline management, and connector configuration.

## What is This Plugin?

The Databasin plugin is a **Claude Code plugin** that extends Claude Code with specialized capabilities for working with the Databasin data platform. It provides:

- **slash commands** for common operations
- **export agents** for pipeline creation
- **specialized skills** for connectors, pipelines, automations, and CLI operations

## Installation

### Option 1: Install from Claude Code Marketplace (Recommended)

1. Open Claude Code CLI
2. Type `/plugin marketplace add databasin-ai/agent-plugins` or use the marketplace command
3. Click "Install" or follow the installation prompts
4. Restart Claude Code

### Option 2: Local Installation

1. Clone or download this plugin to your project:
   ```bash
   cd /path/to/your/project
   mkdir -p .claude-plugin
   cp -r /path/to/databasin .claude-plugin/
   ```

2. Verify the plugin structure exists:
   ```bash
   ls .claude-plugin/databasin/.claude-plugin/plugin.json
   ```

3. Restart Claude Code to load the plugin

### Verify Installation

After installation, verify the plugin is loaded:

```
You: /help
```

You should see the databasin commands listed in the available commands section.

## Using Slash Commands

The plugin provides 5 slash commands for common Databasin operations. All commands are prefixed with `databasin:` to avoid conflicts with other plugins.

### Available Commands

#### 1. List Projects
```
/databasin:list-projects
```
Lists all Databasin projects accessible to the current user. Uses the `@skill-databasin-cli` to fetch project data.

**Example:**
```
You: /databasin:list-projects
Claude: [Lists all your projects with IDs and details]
```

#### 2. List Connectors
```
/databasin:list-connectors
```
Shows all available data source connectors (250+ types including PostgreSQL, MySQL, Salesforce, S3, etc.).

**Example:**
```
You: /databasin:list-connectors
Claude: [Lists available connectors with types and configurations]
```

#### 3. Create Connector
```
/databasin:create-connector
```
Guides you through creating a new data source connector with appropriate configuration.

**Example:**
```
You: /databasin:create-connector
Claude: What type of connector would you like to create?
You: PostgreSQL
Claude: [Walks through PostgreSQL connection configuration]
```

#### 4. Create Pipeline
```
/databasin:create-pipeline
```
Initiates the pipeline creation workflow to set up data integration pipelines.

**Example:**
```
You: /databasin:create-pipeline
Claude: [Guides you through source, destination, transformations, and scheduling]
```

#### 5. Create Report
```
/databasin:create-report
```
Helps you create reports and analytics in the Reportbasin module.

**Example:**
```
You: /databasin:create-report
Claude: [Guides you through report configuration]
```

## Using Skills

Skills are automatically invoked by Claude when relevant to your request, or you can explicitly reference them using the `@skill-name` syntax.

### Available Skills

#### @skill-databasin-cli
Expert skill for using the Databasin CLI tool. Handles data connector management, pipeline operations, SQL queries, automations, and comprehensive data engineering workflows.

**Automatic Invocation Examples:**
```
You: Show me all my Databasin projects
Claude: [Automatically uses @skill-databasin-cli to list projects]

You: How many connectors do we have?
Claude: [Uses @skill-databasin-cli to query connector count]

You: Create a SQL query to find customers in New York
Claude: [Uses @skill-databasin-cli to execute SQL query]
```

**Explicit Invocation:**
```
You: @skill-databasin-cli help me troubleshoot this pipeline failure
Claude: [Directly invokes the CLI skill for troubleshooting]
```

#### @skill-databasin-connectors
Specialized skill for data connector creation, configuration, and management. Knows about 250+ connector types including authentication requirements, field mappings, and best practices.

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

#### @skill-databasin-pipelines
Expert skill for pipeline creation, execution, and monitoring. Understands pipeline configuration, transformations, scheduling, and troubleshooting.

**Use Cases:**
- Building ETL/ELT pipelines
- Configuring data transformations
- Setting up pipeline schedules
- Troubleshooting pipeline failures

**Example:**
```
You: @skill-databasin-pipelines create a pipeline from MySQL to Snowflake
Claude: [Guides through pipeline creation with source/destination configuration]
```

#### @skill-databasin-automations
Specialized skill for creating and managing Databasin automations including scheduled tasks, event-driven workflows, and complex orchestration patterns.

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

The plugin includes one specialized agent that can be invoked for complex, multi-step workflows.

### @agent-databasin-pipeline-creator

Elite pipeline architect agent specializing in designing, configuring, and deploying data integration pipelines. This agent guides you through the complete pipeline creation lifecycle.

**When to Use:**
- Creating pipelines from scratch
- Configuring complex multi-step pipelines
- Setting up source-to-destination data flows
- Troubleshooting pipeline creation issues

**Automatic Invocation Examples:**
```
You: I need to create a pipeline from Salesforce to PostgreSQL
Claude: [Automatically invokes @agent-databasin-pipeline-creator]

You: Help me set up a new data integration pipeline
Claude: [Launches the pipeline creator agent]
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

## Prerequisites & Setup

### Databasin CLI Installation

Before using the plugin, ensure the Databasin CLI is installed:

```bash
# Install Databasin CLI (specific installation method depends on your setup)
npm install -g @databasin/cli
```

### Authentication

Authenticate with Databasin before using commands:

```bash
databasin auth login
```

This will open a browser window for authentication and store your credentials locally.

### Verify CLI Access

Test that the CLI is working:

```bash
databasin auth whoami
databasin projects list
```

## Common Workflows

### Workflow 1: First-Time Setup

```
You: /databasin:list-projects
Claude: [Shows all accessible projects]

You: /databasin:list-connectors
Claude: [Shows available connector types]

You: Show me how to connect to PostgreSQL
Claude: [Uses @skill-databasin-connectors to explain PostgreSQL setup]
```

### Workflow 2: Create a Data Pipeline

```
You: I want to sync data from MySQL to Snowflake daily
Claude: I'll help you create this pipeline. Let me invoke the pipeline creator agent.
[Automatically uses @agent-databasin-pipeline-creator]

Agent: Let's start by understanding your requirements...
- What MySQL tables do you want to sync?
- What's your Snowflake destination schema?
- Do you need any data transformations?
[Guides through complete pipeline setup]
```

### Workflow 3: Troubleshooting

```
You: My pipeline keeps failing, how do I debug it?
Claude: [Uses @skill-databasin-cli to check logs]

Claude: Let me check the pipeline logs for you...
[Executes: databasin pipelines logs <pipeline-id>]
[Analyzes errors and provides solutions]
```

### Workflow 4: Data Discovery

```
You: Find all customers who ordered in the last month
Claude: [Uses @skill-databasin-cli for data discovery]

Claude: Let me explore your data structure first...
[Lists available connectors]
[Explores database schemas and tables]
[Generates SQL query]
[Executes query and shows results]
```

### Workflow 5: Create Automation

```
You: Set up a daily sync job at 6 AM
Claude: [Uses @skill-databasin-automations]

Claude: I'll help you create a scheduled automation...
[Guides through automation configuration]
[Sets up cron schedule: "0 6 * * *"]
[Creates and tests automation]
```

## Natural Language Usage

You don't need to memorize commands or skill names. Claude automatically determines the right tools to use based on your natural language requests:

**Data Exploration:**
```
You: What data sources do I have access to?
Claude: [Uses @skill-databasin-cli to list connectors]

You: Show me the schema of my production database
Claude: [Uses CLI to explore database schema]
```

**Pipeline Operations:**
```
You: Create a pipeline that moves data from Salesforce to our warehouse
Claude: [Invokes @agent-databasin-pipeline-creator]

You: Why did my pipeline fail last night?
Claude: [Uses @skill-databasin-pipelines to check logs]
```

**Connector Management:**
```
You: How do I connect to AWS S3?
Claude: [Uses @skill-databasin-connectors for S3 configuration]

You: What authentication does Salesforce require?
Claude: [Explains OAuth setup using connector skill]
```

## Advanced Usage Tips

### 1. Combining Skills

Claude can automatically chain skills together for complex requests:

```
You: Create a pipeline from my PostgreSQL database to Snowflake,
     then set it to run every night at 2 AM

Claude: [Uses multiple skills in sequence:]
1. @skill-databasin-connectors - Verify PostgreSQL connector
2. @agent-databasin-pipeline-creator - Create pipeline
3. @skill-databasin-automations - Set up schedule
```

### 2. Explicit Skill Selection

When you want Claude to use a specific skill:

```
You: @skill-databasin-cli execute this SQL: SELECT * FROM users LIMIT 10
Claude: [Directly uses the CLI skill to run the query]
```

### 3. Context-Aware Assistance

The skills maintain context across the conversation:

```
You: List all my connectors
Claude: [Lists connectors]

You: Tell me more about the first one
Claude: [Remembers context and provides details on the first connector]

You: Test the connection
Claude: [Tests the connector from previous context]
```

### 4. Error Recovery

Skills automatically handle errors and provide actionable solutions:

```
You: Run this pipeline
Claude: [Attempts to run]
Error: Authentication token expired

Claude: Your authentication token has expired. Let me help you refresh it.
Run this command: databasin auth login
[Guides through re-authentication]
```

## Troubleshooting

### Plugin Not Loading

**Problem:** Commands don't appear in `/help`

**Solutions:**
1. Verify plugin is in correct location: `.claude-plugin/databasin/`
2. Check `plugin.json` exists: `.claude-plugin/databasin/.claude-plugin/plugin.json`
3. Restart Claude Code
4. Run `/plugins` to see loaded plugins

### CLI Not Found

**Problem:** "databasin command not found"

**Solution:**
```bash
# Verify CLI installation
which databasin

# If not installed, install it
npm install -g @databasin/cli
# OR follow your organization's installation guide
```

### Authentication Errors

**Problem:** "Unauthorized" or "Token expired" errors

**Solution:**
```bash
# Re-authenticate
databasin auth login

# Verify authentication
databasin auth whoami
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
Claude: [Provides overview of plugin capabilities]

You: What can @skill-databasin-cli do?
Claude: [Lists CLI skill capabilities]

You: Show me examples of pipeline creation
Claude: [Provides examples using the agent]
```

### Documentation Resources

The plugin includes extensive reference documentation:

- **CLI Skill References:**
  - `skills/databasin-cli-skill/references/advanced-workflows.md` - Complex workflows
  - `skills/databasin-cli-skill/references/example-queries.md` - SQL query patterns
  - `skills/databasin-cli-skill/references/troubleshooting.md` - Diagnostic guides
  - `skills/databasin-cli-skill/references/token-efficiency.md` - Performance optimization

- **Connector Skill References:**
  - `skills/databasin-connectors/references/connector-types-guide.md` - All connector types
  - `skills/databasin-connectors/references/authentication-guide.md` - Auth methods
  - `skills/databasin-connectors/references/field-reference.md` - Configuration fields
  - `skills/databasin-connectors/references/examples.md` - Example configurations

- **Pipeline Skill References:**
  - `skills/databasin-pipelines/references/api-endpoints.md` - Pipeline API reference
  - `skills/databasin-pipelines/references/examples.md` - Pipeline examples
  - `skills/databasin-pipelines/references/pipeline-automation.md` - Automation patterns

- **Automation Skill References:**
  - `skills/databasin-automations/references/cron-schedule-guide.md` - Cron syntax
  - `skills/databasin-automations/references/task-types-reference.md` - Task types
  - `skills/databasin-automations/references/troubleshooting-guide.md` - Debugging

### Command Help

Each command includes inline help:

```
You: /databasin:list-projects --help
You: /databasin:create-connector --help
```

## Best Practices

### 1. Start with Authentication
Always ensure you're authenticated before running commands:
```bash
databasin auth whoami
```

### 2. Use Natural Language
Don't worry about exact command syntax. Claude understands natural requests:
```
You: I need to move data from MySQL to BigQuery every day
[Claude handles the complexity]
```

### 3. Leverage Skills for Expertise
When you need deep expertise, reference skills explicitly:
```
You: @skill-databasin-connectors what's the best way to connect to Snowflake?
```

### 4. Let the Agent Guide Complex Workflows
For multi-step processes, let the pipeline creator agent lead:
```
You: Help me create a complex multi-stage pipeline
[Agent asks clarifying questions and guides step-by-step]
```

### 5. Check Logs for Troubleshooting
Always review logs when things go wrong:
```
You: Why did my pipeline fail?
Claude: [Automatically checks logs and provides diagnosis]
```

## Version & Updates

**Plugin Version:** 0.0.1
**Last Updated:** 2024-11-16

To update the plugin:
1. Check Claude Code Marketplace for updates
2. Run plugin update command (if available)
3. Or manually replace plugin files with latest version

## Support

For issues, questions, or feature requests:

1. Ask Claude directly: `How do I [task] with Databasin?`
2. Reference skill documentation for detailed guides
3. Check Databasin platform documentation
4. Contact your Databasin administrator

## Summary

The Databasin Claude Code plugin transforms how you work with the Databasin platform by providing:

- **Simple commands** for common operations
- **Intelligent skills** that understand your data integration needs
- **Expert agents** for complex pipeline creation workflows
- **Natural language interface** - just describe what you need

You don't need to memorize commands or syntax. Just tell Claude what you want to accomplish, and the plugin handles the complexity.

**Get Started:**
```
You: /databasin:list-projects
```

Then explore connectors, create pipelines, and automate your data workflows using natural conversation with Claude.
