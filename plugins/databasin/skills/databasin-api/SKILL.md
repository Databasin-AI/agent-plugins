---
name: databasin-api
description: Call Databasin API endpoints using the CLI with configurable base URL and JWT authentication. **IMPORTANT - Always consult references/working-endpoints.md BEFORE calling any endpoint** to ensure proper usage, token efficiency, and avoid broken endpoints. Use when making HTTP requests to the Databasin API for pipelines, connectors, projects, reports, governance, or any other Databasin resources.
---

# Databasin API Client

> **Migration Complete:** This skill now uses the `databasin` CLI exclusively.
> All script-based examples have been replaced with CLI commands.

Call Databasin API endpoints using the `databasin` CLI with JWT authentication.

**⚠️ CRITICAL: Always check [references/working-endpoints.md](./references/working-endpoints.md) before calling any endpoint!**

---

## Quick Start

### Authentication

JWT token required in `.token` file in current working directory.

→ **[Security Guide](./references/security.md)** - Token setup and management (lines 14-58)

### Your First API Call

```bash
# Get user context (account + organizations + projects)
databasin auth whoami

# Count projects (token-efficient)
databasin api GET /api/my/projects --count
```

→ **[Getting Started Guide](./references/getting-started.md)** - Complete setup walkthrough (lines 1-217)

---

## I'm Working On... What Should I Read?

### 🚀 "I'm just getting started"

→ **[Getting Started Guide](./references/getting-started.md)**

Essential commands, authentication, first API calls, common workflows

### 📊 "I need to work with projects and organizations"

→ **[Projects & Organizations Guide](./references/projects-and-organizations.md)**

Get user context, list projects, understand internalID, find organization details

**Quick commands:**

```bash
# Get all my projects
databasin auth whoami --fields=projects
databasin api GET /api/my/projects --summary

# Get organizations
databasin api GET /api/my/organizations
```

### 🔌 "I need to work with connectors"

→ **[Connectors Guide](./references/connectors.md)**

List connectors, create/update/delete, connector types, filter by project

**Quick commands:**

```bash
# Count connectors in project
databasin api GET "/api/connector?internalID=N1r8Do" --count

# Get connector details
databasin api GET "/api/connector?internalID=N1r8Do" \
  --fields=connectorID,connectorName,connectorType
```

### 🔄 "I need to work with pipelines"

→ **[Pipelines Guide](./references/pipelines.md)**

List pipelines, create/run pipelines, monitor status, view logs

**Quick commands:**

```bash
# Count pipelines in project
databasin api GET "/api/pipeline?internalID=N1r8Do" --count

# Run a pipeline
databasin api POST /api/pipeline/run '{"pipelineID": 123}'
```

### ⏰ "I need to work with automations"

→ **[Automations Guide](./references/automations.md)**

Schedule pipelines, create cron/interval automations, manage triggers, monitor execution

**Quick commands:**

```bash
# Count automations in project
databasin api GET "/api/automations?internalID=N1r8Do" --count

# Create daily automation
databasin api POST /api/automations '{
  "automationName": "Daily Sync",
  "pipelineID": 123,
  "scheduleType": "cron",
  "cronExpression": "0 2 * * *",
  "institutionID": 1,
  "internalID": "N1r8Do",
  "ownerID": 5,
  "isActive": 1
}'
```

### 💬 "I need to generate SQL from natural language or execute queries"

→ **[SQL Assistant Guide](./references/sql-assistant.md)**

Generate SQL from natural language, execute queries, fix SQL errors, work with Trino/Databricks

**Quick commands:**

```bash
# Get schema context
databasin sql schemas 123

# Execute SQL
databasin sql exec 123 "SELECT * FROM users LIMIT 10"

# Note: SQL generation and fixing features are planned for future releases
```

### 🔍 "I need to discover schemas, tables, or columns before querying"

→ **[Schema Discovery Guide](./references/schema-discovery.md)**

Discover database schemas, list tables, describe columns, exploratory workflow

**Quick commands:**

```bash
# Step 1: List all catalogs and schemas
databasin sql catalogs 5459
databasin sql schemas 5459

# Step 2: List tables in a schema
databasin sql tables 5459 --schema main

# Step 3: Query the table directly
databasin sql exec 5459 "SELECT * FROM main.pipeline LIMIT 5"
```

**⚠️ ALWAYS discover before querying to avoid "table/column does not exist" errors!**

### ⚡ "My API calls are using too many tokens"

→ **[Token Efficiency Guide](./references/token-efficiency.md)**

Learn: `--count`, `--summary`, `--fields`, `--limit`, pagination, best practices

**Quick commands:**

```bash
# ✅ Count only (~50 tokens)
databasin api GET /api/connector --count

# ✅ Summary view (~2,000 tokens)
databasin api GET /api/connector --summary

# ✅ Specific fields with limit (~500 tokens)
databasin api GET /api/connector \
  --fields=connectorID,connectorName --limit=20
```

### ❌ "I'm getting errors or null responses"

→ **[Error Handling Guide](./references/error-handling.md)**

HTTP status codes, null responses, required parameters, debugging, troubleshooting

**Common issues:**

- 401 Unauthorized → Check JWT token (lines 14-43)
- 400 Bad Request → Missing required parameters (lines 45-72)
- null response → Missing `internalID` parameter (lines 74-103)
- Massive token usage → Use `--count` first (lines 161-193)

### 🎯 "I want to follow best practices and avoid common mistakes"

→ **[Best Practices Guide](./references/best-practices.md)**

When to ask for clarification, do's and don'ts, common workflows, decision trees, common mistakes

**Key sections:**

- When to Ask for Clarification (lines 11-52)
- DO's and DON'Ts (lines 58-100)
- Common Workflow Patterns (lines 106-189)
- Decision Trees (lines 195-257)
- Common Mistakes to Avoid (lines 319-386)

### 💻 "I want to use this in my code"

→ **[Programmatic Usage Guide](./references/programmatic-usage.md)**

Import client, make API calls, error handling, examples, best practices

**Quick example:**

```bash
# Use the CLI directly in scripts
databasin api GET /api/my/projects --json > projects.json

# Or call it programmatically (requires databasin CLI installed)
# The CLI handles authentication automatically
```

### 🔒 "I need to understand security"

→ **[Security Guide](./references/security.md)**

JWT token protection, file permissions, credential management, git ignore, best practices

**Key points:**

- JWT tokens in `.token` file (lines 14-29)
- Never commit `.token` to git (lines 31-58)
- Tokens expire after ~1 hour (lines 60-95)
- Use `chmod 600 .token` for permissions (lines 97-129)

---

## Complete Reference Documentation

### Endpoint References

**ALWAYS consult these before calling endpoints:**

→ **[Working Endpoints](./references/working-endpoints.md)** - 15+ tested endpoints with examples

→ **[Deprecated Endpoints](./references/deprecated-endpoints.md)** - Broken endpoints to avoid

### Topic-Specific Guides

| Guide                                                                      | When to Use                                | Quick Link  |
| -------------------------------------------------------------------------- | ------------------------------------------ | ----------- |
| **[Getting Started](./references/getting-started.md)**                     | First-time setup, learning basics          | Lines 1-217 |
| **[Best Practices](./references/best-practices.md)**                       | Clarifications, workflows, common mistakes | Lines 1-395 |
| **[Token Efficiency](./references/token-efficiency.md)**                   | Optimize API usage, reduce costs           | Lines 1-346 |
| **[Projects & Organizations](./references/projects-and-organizations.md)** | User context, projects, organizations      | Lines 1-287 |
| **[Connectors](./references/connectors.md)**                               | Data source management                     | Lines 1-274 |
| **[Pipelines](./references/pipelines.md)**                                 | Pipeline operations and monitoring         | Lines 1-286 |
| **[Automations](./references/automations.md)**                             | Scheduling, cron, triggers                 | Lines 1-422 |
| **[SQL Assistant](./references/sql-assistant.md)**                         | Natural language to SQL, query execution   | Lines 1-551 |
| **[Schema Discovery](./references/schema-discovery.md)**                   | Database exploration workflows             | Lines 1-360 |
| **[Error Handling](./references/error-handling.md)**                       | Troubleshooting errors and nulls           | Lines 1-293 |
| **[Security](./references/security.md)**                                   | Token security and credentials             | Lines 1-283 |
| **[Programmatic Usage](./references/programmatic-usage.md)**               | Using API client in code                   | Lines 1-372 |

---

### 🌐 "I need to call an arbitrary API endpoint"

→ **Generic API Command**

The `databasin api` command provides direct access to ANY Databasin API endpoint.

**Quick commands:**

```bash
# Count resources (most efficient)
databasin api GET /api/connector --count

# Get specific fields
databasin api GET /api/connector --fields=connectorID,connectorName,type --limit=10

# Summary view
databasin api GET /api/my/projects --summary

# POST/PUT/DELETE operations
databasin api POST /api/connector '{"connectorName":"test"}'
databasin api DELETE /api/connector/58
```

**Token Efficiency Options:**
- `--count` - Returns {count: N} only (most efficient, ~50 tokens)
- `--summary` - Returns {total: N, sample: [first 3]} (~2,000 tokens)
- `--fields` - Filter to specific fields only
- `--limit` / `--offset` - Pagination support

For full documentation: `databasin api --help`

---

## Quick Command Reference

### Most Common Commands

```bash
# User context
databasin auth whoami

# Token-efficient queries
databasin api GET "/api/connector?internalID=N1r8Do" --count
databasin api GET "/api/pipeline?internalID=N1r8Do" --summary
databasin api GET "/api/automations?internalID=N1r8Do" --fields=id,name

# Schema discovery
databasin sql catalogs <connectorID>
databasin sql schemas <connectorID> --catalog <catalog>
databasin sql tables <connectorID> --catalog <cat> --schema <schema>

# SQL operations
databasin sql exec <connectorID> "SELECT ..." --limit 100

# Generic API calls
databasin api <METHOD> <endpoint> [body] [options]

# Health check
databasin api GET /api/ping
```

---

## Troubleshooting Quick Help

| Problem                         | Solution                                          | Reference                                                                           |
| ------------------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Getting null responses          | Check required parameters (usually `internalID`)  | [Error Handling](./references/error-handling.md) lines 74-103                       |
| 401 Unauthorized                | Run `databasin auth verify` to check token        | [Security](./references/security.md) lines 60-95                                    |
| Too many tokens used            | Use `--count`, `--fields`, `--limit` flags        | [Token Efficiency](./references/token-efficiency.md) lines 61-133                   |
| Can't find endpoint             | Use `databasin api` generic command               | New command help                                                                    |
| Table doesn't exist             | Run schema discovery first with `databasin sql`   | [Schema Discovery](./references/schema-discovery.md) lines 21-134                   |
| Don't know project's internalID | Run `databasin auth whoami`                       | [Projects & Organizations](./references/projects-and-organizations.md) lines 76-123 |

---

## When to Use Each Guide

```text
New to API?                    → Getting Started
Following best practices?      → Best Practices
Working with projects?         → Projects & Organizations
Working with connectors?       → Connectors
Working with pipelines?        → Pipelines
Scheduling pipelines?          → Automations
Generate/execute SQL?          → SQL Assistant
Discover database schema?      → Schema Discovery
Using too many tokens?         → Token Efficiency
Getting errors?                → Error Handling
Need security info?            → Security
Writing code?                  → Programmatic Usage
Looking for endpoint?          → Working Endpoints
Endpoint not working?          → Deprecated Endpoints
```

---

## Support & Documentation

**Issues or questions?**

1. Check [Best Practices](./references/best-practices.md) for common patterns
2. Check [Working Endpoints](./references/working-endpoints.md) for tested examples
3. Check [Deprecated Endpoints](./references/deprecated-endpoints.md) for known issues
4. Consult topic-specific guide from table above
5. Review [Error Handling](./references/error-handling.md) for troubleshooting

---

**Last Updated:** 2025-11-21
**Status:** ✅ Production Ready
**Endpoints Documented:** 15+
**Topic Guides:** 13
