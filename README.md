# Databasin CLI Plugin for Claude Code

A comprehensive Claude Code plugin that provides expert assistance for using the Databasin CLI tool to manage data connectors, pipelines, automations, SQL queries, and data engineering workflows.

## Overview

This plugin extends Claude Code with specialized knowledge and skills for working with the Databasin platform CLI. It includes expert agents, slash commands, and comprehensive reference documentation to help you efficiently create connectors, build pipelines, execute queries, and manage your data infrastructure.

## Installation

Install directly from the Claude Code Marketplace:

```
/plugin marketplace add databasin-ai/agent-plugins
```

Or clone this repository to your Claude Code plugins directory.

## What This Plugin Provides

### Slash Commands

Quick-access commands for common Databasin CLI workflows:

- `/databasin:list-projects` - List all accessible Databasin projects
- `/databasin:list-connectors` - View all data source connectors in your project
- `/databasin:create-connector` - Create and configure a new data connector with guided setup
- `/databasin:create-pipeline` - Build a data pipeline using interactive wizard or CLI workflow
- `/databasin:create-report` - Create a Reportbasin report with expert guidance

### Expert Skills

Specialized skills that provide deep expertise in specific areas:

- **databasin-cli** - Comprehensive CLI tool expertise covering authentication, projects, connectors, pipelines, SQL queries, automations, and data engineering workflows
- **databasin-connectors** - Expert guidance for creating, configuring, and troubleshooting data connectors for 250+ data source types (databases, SaaS apps, cloud storage, APIs)
- **databasin-pipelines** - Pipeline creation, modification, and management through natural language conversation with full CLI integration
- **databasin-automations** - Create, schedule, and troubleshoot Databasin automations with cron scheduling and task orchestration

### Specialized Agent

- **databasin-pipeline-creator** - Elite pipeline architect agent that guides you through the complete pipeline creation lifecycle, from requirements gathering to deployment

## Key Capabilities

This plugin helps you:

- Authenticate with Databasin and manage CLI sessions
- Create and configure data connectors for 250+ source types
- Build ETL/ELT data pipelines with field mapping and transformations
- Execute SQL queries against Trino-connected data sources
- Explore database schemas and metadata
- Set up scheduled automations and workflows
- Troubleshoot pipeline failures using log analysis
- Manage projects, users, and permissions
- Find specific data using natural language queries

## Quick Start

1. Install the plugin from the Claude Code Marketplace
2. Ensure you have the Databasin CLI installed and configured
3. Use slash commands like `/databasin:list-projects` to get started
4. Ask Claude for help with any Databasin CLI task

## Example Usage

```
User: I need to create a connector to Salesforce
Claude: I'll help you create a Salesforce connector using the databasin CLI...
[Uses databasin-connectors skill to guide through setup]

User: /databasin:create-pipeline
Claude: [Launches databasin-pipelines skill for interactive pipeline creation]

User: How do I query data from my PostgreSQL connector?
Claude: [Uses databasin-cli skill to explain SQL query syntax and provide examples]
```

## Requirements

- Claude Code
- Databasin CLI tool installed and accessible in your PATH
- Active Databasin account with appropriate permissions

## Documentation

- [Plugin Usage Guide](.claude-plugin/databasin/PLUGIN-USAGE.md) - Detailed usage instructions and examples
- [Plugin README](.claude-plugin/databasin/README.md) - Complete plugin documentation

## Contributing

Contributions are welcome! Please:

1. Fork the repository and create a feature branch
2. Include comprehensive documentation for any new features
3. Test thoroughly before submitting
4. Submit a pull request with a clear description of changes

## License

This plugin is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).

## Support

- **Issues:** [GitHub Issues](https://github.com/Databasin-AI/agent-plugins/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Databasin-AI/agent-plugins/discussions)
- **Documentation:** [Databasin Documentation](https://databasin.ai/docs)

## Maintained By

[Databasin](https://databasin.ai) - Modern data platform for analytics and automation.
