# Databasin CLI Expert Skill for Claude Code

A comprehensive Claude Code skill that makes Claude an expert at using the Databasin CLI tool for data engineering, data science, data administration, and data visualization workflows.

## What This Skill Does

This skill empowers Claude to:

- **Manage Data Connectors:** Create, configure, and troubleshoot connections to 250+ data sources including databases, cloud storage, SaaS apps, data warehouses, and streaming platforms
- **Build Data Pipelines:** Design and run ETL/ELT workflows with transformations, scheduling, and monitoring
- **Explore Data:** Navigate database structures (catalogs, schemas, tables) and execute SQL queries
- **Translate Natural Language to SQL:** Convert user data requests into proper SQL queries
- **Troubleshoot Failures:** Analyze logs, diagnose issues, and provide solutions
- **Execute Automations:** Manage complex data workflows and business logic
- **Assist with Data Discovery:** Help users find the data they need by querying metadata and sampling data

## Installation

### For Claude Code Users

1. **Copy this skill to your Claude Code skills directory:**
   ```bash
   # If you're using user skills
   cp -r databasin-cli-skill ~/.claude/skills/user/databasin-cli
   
   # Or if you have a custom skills location
   cp -r databasin-cli-skill /path/to/your/skills/databasin-cli
   ```

2. **Restart Claude Code or reload skills** (if applicable)

3. **The skill will activate automatically** when you mention Databasin CLI operations

### Prerequisites

You'll need the Databasin CLI installed:

```bash
# Quick install
curl -fsSL https://raw.githubusercontent.com/Databasin-AI/databasin-cli/main/install.sh | bash

# Or download and inspect first
curl -fsSL https://raw.githubusercontent.com/Databasin-AI/databasin-cli/main/install.sh -o install.sh
chmod +x install.sh
./install.sh
```

## Usage Examples

### Example 1: Data Discovery
```
You: "I need to find all customer emails from users who signed up in the last month from the production database"

Claude with this skill will:
1. List available connectors
2. Explore the database structure
3. Sample the users table to understand schema
4. Craft and execute the appropriate SQL query
5. Return the results in your preferred format
```

### Example 2: Building a Pipeline
```
You: "Create a pipeline that syncs active users from our PostgreSQL database to our Snowflake analytics warehouse every 6 hours"

Claude with this skill will:
1. Verify both connectors exist and are working
2. Create a proper pipeline configuration
3. Test the source connection
4. Build the pipeline with appropriate transformations
5. Schedule it to run every 6 hours
6. Monitor the first run and check logs
```

### Example 3: Troubleshooting
```
You: "My daily customer sync pipeline is failing with errors"

Claude with this skill will:
1. Check the pipeline logs for detailed errors
2. Verify source and target connector status
3. Test connectivity with simple queries
4. Identify the root cause
5. Provide specific commands to fix the issue
6. Suggest preventive measures
```

### Example 4: SQL Translation
```
You: "Show me the top 10 products by revenue this quarter"

Claude with this skill will:
1. Identify the relevant tables (products, orders)
2. Craft a JOIN query with aggregation
3. Apply date filters for the current quarter
4. Order by revenue and limit to 10
5. Execute and display results
6. Offer to export to CSV if needed
```

## Key Features

### 🎯 Comprehensive CLI Coverage
- All authentication operations
- Project management
- Connector CRUD operations
- SQL interface and data exploration
- Pipeline creation, execution, and monitoring
- Automation management
- Generic API access

### 🔍 Intelligent Data Discovery
- Systematic exploration of data hierarchy
- Natural language to SQL translation
- Smart sampling before full queries
- Schema comparison capabilities

### 🛠️ Advanced Troubleshooting
- Log analysis and interpretation
- Common error pattern recognition
- Systematic diagnostic workflows
- Debug mode guidance

### 📊 Multiple Output Formats
- Table format for viewing
- JSON for scripting/automation
- CSV for data exports
- Field filtering

### 🚀 Best Practices Built-In
- Authentication verification
- Incremental testing approaches
- Security-conscious configurations
- Performance optimization tips

## What Makes This Skill Powerful

1. **Context-Aware Assistance:** The skill knows when to use which commands based on the user's goal
2. **Error Prevention:** Guides users through proper sequences (e.g., always authenticate first)
3. **Troubleshooting Expertise:** Systematic approaches to diagnosing and fixing issues
4. **Natural Language Processing:** Translates plain English data requests into SQL
5. **Complete Workflow Coverage:** From initial setup through ongoing maintenance

## Supported Operations

### Authentication & Setup
- Browser-based login
- Token verification
- Configuration management

### Data Sources (250+ Connector Types)
- Databases: PostgreSQL, MySQL, SQL Server, Oracle, MongoDB
- Cloud Storage: S3, Azure Blob, GCS
- Data Warehouses: Snowflake, BigQuery, Redshift, Databricks
- SaaS: Salesforce, HubSpot, Zendesk, ServiceNow
- Streaming: Kafka, Event Hubs, Kinesis

### Workflows
- ETL/ELT pipelines
- Data transformations
- Scheduled jobs
- Event-driven automations
- Data quality checks

### Data Operations
- Schema exploration
- SQL query execution
- Data sampling
- Export to CSV/JSON
- Batch operations

## Tips for Best Results

1. **Be Specific:** "Find customer emails from New York who ordered last month" is better than "get customer data"

2. **Mention Constraints:** "I need this to run daily at 6 AM" helps Claude configure schedules properly

3. **Provide Context:** "The pipeline failed with a timeout error" gives Claude more to work with

4. **Ask for Explanations:** "Explain this SQL query" - Claude will break down what each part does

5. **Request Validation:** "Check if this pipeline configuration is correct" - Claude will review it

## Common Workflows Supported

- ✅ Setting up new data sources
- ✅ Creating data synchronization pipelines
- ✅ Exploring unfamiliar databases
- ✅ Writing SQL queries from natural language
- ✅ Troubleshooting failed pipelines
- ✅ Comparing data between sources
- ✅ Validating data quality
- ✅ Exporting data for analysis
- ✅ Scheduling automated workflows
- ✅ Managing user permissions

## Contributing

Found an issue or have suggestions? This skill can be extended with:
- Additional troubleshooting patterns
- More SQL translation examples
- Pipeline template library
- Connector-specific best practices

## Resources

- [Databasin CLI Repository](https://github.com/Databasin-AI/databasin-cli)
- [Databasin Platform](https://databasin.ai)
- [CLI Documentation](https://github.com/Databasin-AI/databasin-cli/blob/main/README.md)

## License

This skill follows the same license as the Databasin CLI tool (CC-BY-4.0).

---

**Built for Claude Code users who work with data pipelines, connectors, and SQL workflows on the Databasin platform.**
