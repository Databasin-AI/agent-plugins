# Databasin AI Agent Plugins

A collection of Claude Code plugins and integrations for extending AI agent capabilities with Databasin specific knowledge, skills, and automation.

## Overview

This repository contains production-ready Claude Code plugins that enable AI agents to interact with external systems, APIs, and services. Each plugin provides specialized agents, slash commands, and skills for seamless integration into your AI-powered workflows.

### Install Claude Code Marketplace

`/plugin marketplace add databasin-ai/agent-plugins`

## Available Plugins

### Databasin Plugin

Complete integration plugin for the Databasin data platform, providing authenticated API access, JWT management, and specialized agents for data operations.

**Location:** `.claude-plugins/databasin/`

**Key Features:**

- Project and organization management
- Data connector operations
- Pipeline and automation control
- Report generation and analytics
- Specialized AI agents for API interaction

**Available Commands:**

```bash
# Project and Connector Management
/databasin:list-projects       # List all accessible projects
/databasin:list-connectors     # View all data source connectors

# Creation Workflows
/databasin:create-connector    # Create and test a new data connector with guided configuration
/databasin:create-pipeline     # Create a DataBasin pipeline using interactive wizard
/databasin:create-report       # Create a Reportbasin report with the report builder agent
```

**Specialized Agents:**

- **reportbasin-report-builder** - Expert data visualization architect for creating and iterating on Reportbasin reports with Apache ECharts

**Available Skills:**

- **databasin-automations** - Create, manage, and troubleshoot Databasin automations with scheduled and triggered tasks
- **databasin-cli** - Comprehensive CLI tool expertise for connectors, pipelines, SQL queries, and data engineering workflows
- **databasin-connectors** - Create, manage, and troubleshoot data connectors for 250+ data source types
- **databasin-pipelines** - Create, modify, and manage data pipelines through natural language conversation

**Documentation:**

- [Plugin README](.claude-plugins/databasin/README.md) - Complete setup and usage guide
- [Plugin Usage Guide](.claude-plugins/databasin/PLUGIN-USAGE.md) - SDK integration details

## Getting Started

### Prerequisites

- Claude Code
- Node.js or Bun runtime
- Plugin-specific dependencies (see individual plugin documentation)

### Installation

1. Clone this repository:

```bash
git clone https://github.com/databasin-ai/agent-plugins.git
cd agent-plugins
```

2. Choose a plugin and follow its setup instructions:

```bash
cd .claude-plugins/databasin
# Follow README.md for plugin-specific setup
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Follow the plugin architecture** described above
3. **Include comprehensive documentation** for all components
4. **Test thoroughly** before submitting
5. **Submit a pull request** with a clear description of changes

### Contribution Areas

- New plugin integrations
- Enhanced agent capabilities
- Additional slash commands
- Improved documentation
- Bug fixes and optimizations

## License

This repository is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) - see individual plugin licenses for specific terms.

## Resources

- [Anthropic Agent SDK](https://github.com/anthropics/anthropic-sdk-typescript)
- [Claude Code Documentation](https://docs.anthropic.com/claude/docs/claude-code)
- [Plugin Development Guide](https://docs.anthropic.com/claude/docs/plugins)

## Support

For issues, questions, or contributions:

- **Issues:** [GitHub Issues](https://github.com/Databasin-AI/agent-plugins/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Databasin-AI/agent-plugins/discussions)
- **Documentation:** See individual plugin README files

## Maintained By

[Databasin](https://databasin.ai) - Modern data platform for analytics and automation.
