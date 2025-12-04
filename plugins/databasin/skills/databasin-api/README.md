# Databasin API Skill

Call Databasin API endpoints using BunJS with configurable base URL and JWT authentication.

**⚠️ CRITICAL:** Always check `references/working-endpoints.md` BEFORE calling any endpoint to ensure proper usage, token efficiency, and avoid broken endpoints.

---

## What's New

### 🎯 Recent Major Additions

#### Schema Discovery & SQL Assistant (Nov 2024)

- **Schema Discovery Scripts** - Explore database schemas before querying
  - `list-schemas.ts` - List all available schemas in a connector
  - `list-tables.ts` - List tables in a specific schema
  - `describe-table.ts` - Get detailed column information
  - `get-schema-context.ts` - Get full schema context for LLM prompts

- **SQL Assistant Scripts** - AI-powered SQL generation and execution
  - `generate-sql.ts` - Generate SQL from natural language queries
  - `execute-sql.ts` - Execute SQL against Trino/Databricks connectors
  - `fix-sql.ts` - Automatically fix failed SQL queries

- **User Context Script** - Get comprehensive user context
  - `get-user-context.ts` - Fetch account, organizations, and projects in one call

#### Token Efficiency Features

- `--count` - Get just the count of results (~50 tokens vs 200,000+)
- `--summary` - Count + first 3 samples (~500-2,000 tokens)
- `--fields` - Return only specific fields (saves 50-80% tokens)
- `--limit` - Limit number of results returned
- `--compact` - Remove JSON formatting (saves ~30% tokens)

#### Comprehensive Documentation (15+ reference guides)

- Topic-specific guides for projects, connectors, pipelines, automations
- SQL assistant guide with natural language to SQL workflows
- Schema discovery guide for exploratory data analysis
- Token efficiency guide with best practices
- Security, error handling, and programmatic usage guides
- Working endpoints reference (15+ tested endpoints)
- Deprecated endpoints documentation (avoid common pitfalls)

---

## Quick Start

### Authentication

The skill reads JWT authentication token from a `.token` file in the current working directory.

**See:** `references/security.md` for token management best practices

### Essential Examples

```bash
# Get user context (account + organizations + projects)
bun run scripts/get-user-context.ts

# Make API calls with token efficiency
bun run scripts/api-call.ts GET /api/my/projects --count
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --summary

# Schema discovery workflow
bun run scripts/list-schemas.ts 123
bun run scripts/list-tables.ts 123 main
bun run scripts/describe-table.ts 123 main users

# SQL assistant workflow
bun run scripts/generate-sql.ts 456 "Get top 10 customers by revenue" --schema-file=schema.json
bun run scripts/execute-sql.ts 123 "SELECT * FROM users LIMIT 10" --format=table
bun run scripts/fix-sql.ts 456 "SELECT * FROM users" "Table not found" --schema-file=schema.json

# Traditional API calls
bun run scripts/api-call.ts POST /api/connector '{
  "connectorName": "my-db",
  "connectorType": "database",
  "institutionID": 1,
  "ownerID": 5
}'
```

---

## Complete Documentation

**📖 Start Here:** `SKILL.md` - Comprehensive skill documentation with:

- Task-based "I'm working on..." quick navigation
- 15+ topic-specific reference guides
- Best practices and common workflows
- Troubleshooting quick help

**📚 Reference Documentation:** `references/` directory contains:

- **getting-started.md** - Setup and first API calls
- **sql-assistant.md** - Natural language to SQL workflows ⭐ NEW
- **schema-discovery.md** - Database exploration workflows ⭐ NEW
- **token-efficiency.md** - Optimize API usage and reduce costs
- **projects-and-organizations.md** - User context management
- **connectors.md** - Data source operations
- **pipelines.md** - Pipeline management
- **automations.md** - Scheduling and triggers
- **error-handling.md** - Troubleshooting guide
- **security.md** - Token and credential management
- **programmatic-usage.md** - Using the API in your code
- **working-endpoints.md** - 15+ tested endpoint reference
- **deprecated-endpoints.md** - Broken endpoints to avoid

---

## Files & Scripts

### Core Scripts

- **scripts/api-call.ts** - HTTP client for making API requests
- **scripts/get-user-context.ts** - Get account, organizations, and projects ⭐ NEW
- **scripts/fetch-swagger.ts** - Helper to fetch latest OpenAPI spec

### Schema Discovery Scripts ⭐ NEW

- **scripts/list-schemas.ts** - List all schemas in a connector
- **scripts/list-tables.ts** - List tables in a schema
- **scripts/describe-table.ts** - Describe table columns and types
- **scripts/get-schema-context.ts** - Get full schema context for LLM

### SQL Assistant Scripts ⭐ NEW

- **scripts/generate-sql.ts** - Generate SQL from natural language
- **scripts/execute-sql.ts** - Execute SQL queries against connectors
- **scripts/fix-sql.ts** - Auto-fix failed SQL queries

### Documentation

- **SKILL.md** - Main skill documentation
- **references/** - 15+ comprehensive reference guides

---

## Key Features

✅ **Token-Efficient API Calls** - Count, summary, fields, limit, compact options

✅ **Natural Language to SQL** - AI-powered SQL generation
✅ **Schema Discovery** - Explore databases before querying
✅ **SQL Execution** - Direct Trino/Databricks query execution
✅ **Automatic SQL Fixing** - Retry failed queries with corrections
✅ **User Context Management** - Unified account/org/project access
✅ **Comprehensive Error Handling** - Detailed troubleshooting guides
✅ **15+ Tested Endpoints** - Production-ready endpoint reference
✅ **Security Best Practices** - JWT token management and protection

---

## Requirements

- Bun >= 1.0.0
- Databasin API access
- Valid JWT token in `.token` file
- For SQL features: Trino or Databricks connector access

---

## Support

**Issues or questions?**

1. Check `SKILL.md` for task-based navigation
2. Consult topic-specific guides in `references/`
3. Review `references/working-endpoints.md` for endpoint examples
4. Check `references/deprecated-endpoints.md` for known issues

---

**Last Updated:** 2025-11-21
**Status:** ✅ Production Ready
**Scripts:** 12 (5 schema discovery, 3 SQL assistant, 4 core)
**Reference Guides:** 15+
**Tested Endpoints:** 15+
