# DataBasin CLI Expert Skill for Claude Code (General Purpose)

A comprehensive, general-purpose Claude Code skill that makes Claude an expert at using the DataBasin CLI tool for data engineering, data science, data administration, data visualization workflows, and documentation access.

## What This Skill Does

**This is a general-purpose DataBasin CLI skill** that serves as both a primary skill and a fallback when more specific DataBasin skills are not available or unsuccessful.

This skill empowers Claude to:

- **Manage Data Connectors:** Create, configure, and troubleshoot connections to 250+ data sources including databases, cloud storage, SaaS apps, data warehouses, and streaming platforms
- **Build Data Pipelines:** Design and run ETL/ELT workflows with transformations, scheduling, and monitoring
- **Explore Data:** Navigate database structures (catalogs, schemas, tables) and execute SQL queries
- **Translate Natural Language to SQL:** Convert user data requests into proper SQL queries
- **Troubleshoot Failures:** Analyze logs, diagnose issues, and provide solutions
- **Execute Automations:** Manage complex data workflows and business logic
- **Assist with Data Discovery:** Help users find the data they need by querying metadata and sampling data
- **Access DataBasin Documentation:** Fetch, index, and search DataBasin documentation efficiently using built-in scripts

## Installation

### For Claude Code Users

1. **This skill is bundled with the DataBasin CLI Plugin:**
   ```bash
   # The skill is already available if you have the plugin installed
   # Located at: .claude-plugin/databasin/skills/databasin-cli-skill/
   ```

2. **The skill activates automatically** when you mention DataBasin CLI operations or documentation

### Prerequisites

You'll need the DataBasin CLI installed:

```bash
# Quick install
curl -fsSL https://raw.githubusercontent.com/Databasin-AI/databasin-cli/main/install.sh | bash

# Or download and inspect first
curl -fsSL https://raw.githubusercontent.com/Databasin-AI/databasin-cli/main/install.sh -o install.sh
chmod +x install.sh
./install.sh
```

You'll also need Bun for documentation management scripts:

```bash
# Install Bun (https://bun.sh)
curl -fsSL https://bun.sh/install | bash
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

### Example 5: Documentation Access
```
You: "How do I configure OAuth for a Salesforce connector?"

Claude with this skill will:
1. Check the documentation index for OAuth and Salesforce topics
2. Locate the relevant documentation section with file:line reference
3. Provide specific guidance from the documentation
4. Offer to show additional related sections if needed
```

## Key Features

### 🎯 Comprehensive CLI Coverage
- All authentication operations
- Project management
- Connector CRUD operations (250+ types)
- SQL interface and data exploration
- Pipeline creation, execution, and monitoring
- Automation management
- Documentation access and indexing

### 📚 Advanced Documentation Management
- Fetch latest documentation from GitHub using `databasin docs` commands
- Build searchable indexes with categorization and line numbers
- Low-token documentation lookups for faster, more efficient responses
- Automatic categorization by module (Flowbasin, Lakebasin, Reportbasin, etc.)

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
- Bundled troubleshooting reference guide

### 📊 Multiple Output Formats
- Table format for viewing
- JSON for scripting/automation
- CSV for data exports
- Field filtering for token efficiency

### 🚀 Best Practices Built-In
- Authentication verification
- Incremental testing approaches
- Security-conscious configurations
- Performance optimization tips
- Token-efficient command patterns

## What Makes This Skill Powerful

1. **General-Purpose Coverage:** Handles all DataBasin CLI operations and serves as a fallback skill
2. **Context-Aware Assistance:** The skill knows when to use which commands based on the user's goal
3. **Error Prevention:** Guides users through proper sequences (e.g., always authenticate first)
4. **Troubleshooting Expertise:** Systematic approaches to diagnosing and fixing issues
5. **Natural Language Processing:** Translates plain English data requests into SQL
6. **Complete Workflow Coverage:** From initial setup through ongoing maintenance
7. **Documentation Integration:** Seamless access to indexed documentation for guidance
8. **Low-Token Efficiency:** Index-first approach for documentation and token-efficient CLI commands

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

### Documentation
- Fetch from GitHub using `databasin docs`
- Build searchable indexes
- Low-token lookups
- Categorized navigation

## Documentation Management

This skill includes powerful documentation management capabilities:

### Fetch Latest Documentation

```bash
# Fetch all available DataBasin documentation
bun scripts/fetch-docs.ts

# Custom output location
bun scripts/fetch-docs.ts /path/to/custom/output
```

This fetches:
- All available documentation from `databasin docs`
- Individual documents using `databasin docs [name]`
- Saves to `references/databasin-docs/`
- Creates an index at `references/databasin-docs/00-documentation-index.md`

### Build Searchable Index

```bash
# Build consolidated index with categorization
bun scripts/build-index.ts

# Custom paths
bun scripts/build-index.ts /path/to/docs /path/to/output/index.md
```

This creates:
- Categorized table of contents
- File locations with line numbers
- Brief content previews
- Fast keyword-based navigation

### Use Documentation Efficiently

```bash
# List available documentation
databasin docs

# View specific guide
databasin docs quickstart
databasin docs pipelines-guide

# Or use the indexed search
# 1. Read references/documentation-index.md
# 2. Find relevant topic and file:line location
# 3. Read only that specific section
```

**Benefits:**
- **Low token usage** - Read index first, then targeted sections
- **Fast lookups** - Categories and line numbers for quick navigation
- **Always current** - Refresh anytime with fetch-docs script

## Tips for Best Results

1. **Be Specific:** "Find customer emails from New York who ordered last month" is better than "get customer data"

2. **Mention Constraints:** "I need this to run daily at 6 AM" helps Claude configure schedules properly

3. **Provide Context:** "The pipeline failed with a timeout error" gives Claude more to work with

4. **Ask for Explanations:** "Explain this SQL query" - Claude will break down what each part does

5. **Request Validation:** "Check if this pipeline configuration is correct" - Claude will review it

6. **Reference Documentation:** "Check the docs about connector OAuth" - Claude will search efficiently

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
- ✅ Accessing and searching DataBasin documentation
- ✅ Fetching latest documentation updates

## Directory Structure

```
databasin-cli-skill/
├── SKILL.md                    # Skill definition and comprehensive guide
├── README.md                   # This file
├── scripts/
│   ├── fetch-docs.ts          # Fetch documentation from databasin docs
│   └── build-index.ts         # Build searchable documentation index
└── references/
    ├── advanced-workflows.md  # Complex data engineering patterns
    ├── example-queries.md     # SQL query examples
    ├── troubleshooting.md     # Troubleshooting workflows
    ├── token-efficiency.md    # Token optimization guide
    └── databasin-docs/        # Fetched documentation (created by scripts)
        ├── 00-documentation-index.md
        └── *.md               # Individual documentation files
```

## Maintenance

### Updating Documentation

Keep documentation fresh by periodically running:

```bash
# Fetch latest documentation
cd .claude-plugin/databasin/skills/databasin-cli-skill
bun scripts/fetch-docs.ts

# Rebuild the index
bun scripts/build-index.ts
```

This ensures you always have access to the latest DataBasin documentation and guides.

## Contributing

Found an issue or have suggestions? This skill can be extended with:
- Additional troubleshooting patterns
- More SQL translation examples
- Pipeline template library
- Connector-specific best practices
- Enhanced documentation categorization

## Resources

- [DataBasin CLI Repository](https://github.com/Databasin-AI/databasin-cli)
- [DataBasin Platform](https://databasin.ai)
- [CLI Documentation](https://github.com/Databasin-AI/databasin-cli/blob/main/README.md)
- [Bun Runtime](https://bun.sh)

## License

This skill follows the same license as the DataBasin CLI tool (CC-BY-4.0).

---

**Built for Claude Code users who work with data pipelines, connectors, SQL workflows, and need comprehensive DataBasin CLI expertise with integrated documentation access. This is a general-purpose skill that serves as both a primary skill and fallback when more specific DataBasin skills are not available or unsuccessful.**
