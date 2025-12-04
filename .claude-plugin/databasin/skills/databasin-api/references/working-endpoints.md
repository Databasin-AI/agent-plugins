# Databasin API - Working Endpoints Cheatsheet

**Last Updated:** 2025-11-20
**Purpose:** Quick reference for common API endpoints with usage examples and scenarios

---

## Table of Contents

- [Projects & Organizations](#projects--organizations)
- [Connectors](#connectors)
- [Pipelines](#pipelines)
- [Users](#users)
- [System](#system)
- [Governance](#governance)
- [Automations](#automations)
- [SQL & Lakebasin](#sql--lakebasin)
- [Metadata](#metadata)

---

## Projects & Organizations

### GET `/api/my/projects`

**Description:** Get all projects accessible to the current user
**Token Usage:** ~20,000 tokens for 18 projects (full data)
**Auth:** Required
**Scenarios:**

- List all user projects for project selection
- Get project counts and stats
- Find project by name
- Check project access

**Examples:**

```bash
# Count projects only (minimal tokens)
bun run scripts/api-call.ts GET /api/my/projects --count

# Get summary (total + first 3 samples)
bun run scripts/api-call.ts GET /api/my/projects --summary

# Get specific fields only
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalID,description --limit=10

# Full data (use sparingly)
bun run scripts/api-call.ts GET /api/my/projects
```

**Response Fields:**

- `id`: Project ID (integer)
- `internalID`: Project short code (string, e.g., "N1r8Do")
- `name`: Project name
- `description`: Project description
- `organizationId`: Parent organization ID
- `organizationName`: Parent organization name
- `administratorId`: User ID of project administrator
- `createdDate`: ISO timestamp
- `deleted`: Boolean flag
- `favorited`: Boolean flag for current user

---

### GET `/api/my/organizations`

**Description:** Get all organizations accessible to the current user
**Token Usage:** ~5,000 tokens for 7 organizations (full data)
**Auth:** Required
**Scenarios:**

- List all user organizations
- Get organization count
- Find organization by name

**Examples:**

```bash
# Count organizations
bun run scripts/api-call.ts GET /api/my/organizations --count

# Get specific fields
bun run scripts/api-call.ts GET /api/my/organizations --fields=id,name,description --limit=10
```

**Response Fields:**

- `id`: Organization ID (integer)
- `name`: Organization name
- `description`: Organization description
- `createdDate`: ISO timestamp
- `administrator`: User object
- `projects`: Array of project objects with roles

---

### GET `/api/my/account`

**Description:** Get current logged-in user profile
**Token Usage:** ~2,000 tokens
**Auth:** Required
**Scenarios:**

- Get current user details
- Display user profile
- Get user ID for other API calls
- Check user roles and permissions

**Examples:**

```bash
# Full user profile
bun run scripts/api-call.ts GET /api/my/account

# Specific fields only
bun run scripts/api-call.ts GET /api/my/account --fields=id,firstName,lastName,email
```

**Response Fields:**

- `id`: User ID (integer)
- `firstName`: User first name
- `lastName`: User last name
- `email`: User email address
- `organizationMemberships`: Array of org memberships with roles
- `projectMemberships`: Array of project memberships with roles

---

## Connectors

### GET `/api/connector`

**Description:** Get all connectors OR connectors for a specific project
**Token Usage:** ~200,000+ tokens for 434 connectors (HUGE!)
**Auth:** Required
**Parameters:**

- `internalID` (optional): Project internal ID to filter connectors

**Scenarios:**

- List available connector types
- Get connectors for a specific project
- Find connector by name or type
- Check connector configuration

**Examples:**

```bash
# ⚠️ NEVER do this - returns 434 connectors with full data!
# bun run scripts/api-call.ts GET /api/connector

# ✅ ALWAYS use count or filters
bun run scripts/api-call.ts GET /api/connector --count

# Get connectors for a project
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --count
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --fields=connectorID,connectorName,connectorType --limit=10

# Get specific connector types
bun run scripts/api-call.ts GET /api/connector --fields=connectorID,connectorName,connectorType,status --limit=20
```

**Response Fields:**

- `connectorID`: Connector ID (string)
- `connectorName`: Connector name
- `connectorType`: Type category (database, app, file & api, etc.)
- `status`: Connector status
- `configuration`: Full connector configuration object

**⚠️ Token Warning:** This endpoint can return 200,000+ tokens for all connectors. ALWAYS use `--count`, `--fields`, or `--limit` options!

---

## Pipelines

### GET `/api/pipeline`

**Description:** Get pipelines for a specific project
**Token Usage:** Variable based on pipeline count
**Auth:** Required
**Required Parameters:**

- `internalID`: Project internal ID (required!)

**Scenarios:**

- List pipelines in a project
- Get pipeline count
- Find pipeline by name
- Check pipeline status

**Examples:**

```bash
# ⚠️ This will fail - internalID is required
# bun run scripts/api-call.ts GET /api/pipeline

# ✅ Correct usage with project ID
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do" --count
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do" --fields=pipelineID,pipelineName,status --limit=10
```

**Response Fields:**

- `pipelineID`: Pipeline ID (integer)
- `pipelineName`: Pipeline name
- `status`: Pipeline status
- `enabled`: Boolean enabled state
- `lastRunDate`: ISO timestamp
- `artifacts`: Array of pipeline artifacts

**Error:** Returns 400 Bad Request if `internalID` parameter is missing

---

## Users

### GET `/api/users`

**Description:** Get all system users (admin only)
**Token Usage:** Variable based on user count
**Auth:** Required (admin role)
**Scenarios:**

- List all users in the system
- Find user by email
- Get user count
- Audit user accounts

**Examples:**

```bash
# Count users
bun run scripts/api-call.ts GET /api/users --count

# Get user summary
bun run scripts/api-call.ts GET /api/users --fields=id,firstName,lastName,email --limit=20
```

**Response Fields:**

- `id`: User ID (integer)
- `firstName`: First name
- `lastName`: Last name
- `email`: Email address
- `enabled`: Boolean status
- `roles`: Array of user roles

---

### GET `/api/project/{projectId}/users`

**Description:** Get users assigned to a specific project
**Token Usage:** Variable based on user count
**Auth:** Required
**Scenarios:**

- List project team members
- Get user count for a project
- Check user roles in project

**Examples:**

```bash
# Count project users
bun run scripts/api-call.ts GET "/api/project/12/users" --count

# Get user details
bun run scripts/api-call.ts GET "/api/project/12/users" --fields=id,firstName,lastName,email,role
```

---

### GET `/api/organizations/users/{organizationId}`

**Description:** Get users in an organization
**Token Usage:** Variable based on user count
**Auth:** Required
**Scenarios:**

- List organization members
- Get member count
- Check user roles in organization

**Examples:**

```bash
# Count org users
bun run scripts/api-call.ts GET "/api/organizations/users/17" --count

# Get user details
bun run scripts/api-call.ts GET "/api/organizations/users/17" --fields=id,firstName,lastName,email,role --limit=20
```

---

## System

### GET `/api/ping`

**Description:** Health check endpoint to verify API availability and authentication
**Token Usage:** ~100 tokens
**Auth:** Optional (returns different response based on auth)
**Scenarios:**

- Check if API is running
- Verify JWT token is valid
- Get system configuration status
- Get API version

**Examples:**

```bash
bun run scripts/api-call.ts GET /api/ping
```

**Response Fields:**

- `isLoggedIn`: Boolean authentication status
- `hasProfile`: Boolean profile completion status
- `isSystemConfigured`: Boolean system setup status
- `message`: Status message (usually "pong")
- `version`: API version string

---

### GET `/api/config`

**Description:** Get system configuration including available connectors
**Token Usage:** ~50,000 tokens (returns full connector configuration)
**Auth:** Required
**Scenarios:**

- Get list of available connector types
- Check connector configurations
- Get system hosting environment
- Check feature flags

**Examples:**

```bash
# This returns a LOT of data - use sparingly
bun run scripts/api-call.ts GET /api/config --summary

# Get specific connector configs
bun run scripts/api-call.ts GET /api/config --fields=key,hostingEnvironment,sourceConnectors,targetConnectors
```

**Response Fields:**

- `key`: System configuration key
- `hostingEnvironment`: Hosting environment (Azure, AWS, etc.)
- `sourceConnectors`: Array of source connector configurations
- `targetConnectors`: Array of target connector configurations

---

### GET `/api/project/{projectId}/stats`

**Description:** Get project statistics
**Token Usage:** ~500 tokens
**Auth:** Required
**Scenarios:**

- Get project metrics
- Display project dashboard stats

**Examples:**

```bash
bun run scripts/api-call.ts GET "/api/project/12/stats"
```

**Note:** May return empty object `{}` if project has no statistics data

---

## Automations

### GET `/api/automations`

**Description:** Get automations for a specific project
**Token Usage:** Variable based on automation count (~1,000-5,000 tokens per 10 automations)
**Auth:** Required
**Required Parameters:**

- `internalID`: Project internal ID (REQUIRED - endpoint returns null without it!)

**⚠️ CRITICAL:** This endpoint returns `null` when called without `internalID` parameter. Always include the project's `internalID` to get automation data.

**Scenarios:**

- List automations in a project
- Get automation count (total and active)
- Check automation status and schedules
- View automation tasks and configurations

**Examples:**

```bash
# ❌ BAD: Without internalID returns null (count shows 0)
bun run scripts/api-call.ts GET /api/automations --count
# Returns: {"count": 0}

# ✅ GOOD: Get automation count for specific project
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --count
# Returns: {"count": 17}

# ✅ Get all automations with key fields only (token-efficient)
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" \
  --fields=automationID,automationName,isActive,lastRunStatus \
  --limit=10

# ✅ Get only active automations (filter in shell)
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" \
  --fields=automationID,automationName,isActive | grep '"isActive": true'

# ✅ Get summary of automations
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --summary

# ✅ Get full automation details (use sparingly - high token usage)
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do"
```

**Response Fields:**

- `automationID`: Automation ID (integer)
- `automationName`: Automation name (string)
- `isActive`: Boolean - whether automation is currently active
- `isPrivate`: Boolean - whether automation is private to owner
- `currentlyRunning`: Boolean - whether automation is currently executing
- `lastRunStatus`: String - "Successful", "Failed", "Running", "Stopped", etc.
- `lastRunErrorMessage`: String - error message if last run failed
- `automationTasks`: Array - list of task types (e.g., ["sql", "pipeline", "notebook"])
- `jobRunSchedule`: String - cron schedule (e.g., "0 10 \* \* \*")
- `jobClusterSize`: String - cluster size ("s", "M", "L")
- `jobTimeout`: String - timeout in seconds
- `institutionID`: Integer - organization ID
- `internalID`: String - project internal ID (with braces, e.g., "{N1r8Do}")
- `ownerID`: Integer - user ID of automation owner
- `jobName`: String - internal job name
- `jobTags`: Array - custom tags for the automation
- `lastUpdatedDateTime`: String - timestamp of last update
- `auditEnabled`: Boolean - whether audit logging is enabled
- `auditInformation`: Object - audit metadata (IRB numbers, PI names, etc.)

**Common Patterns:**

```bash
# Count active vs inactive automations
ACTIVE=$(bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" \
  --fields=isActive | grep -c '"isActive": true')
TOTAL=$(bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --count | jq -r '.count')
echo "Active: $ACTIVE / Total: $TOTAL"

# Find currently running automations
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" \
  --fields=automationID,automationName,currentlyRunning,lastRunStatus | \
  grep -B2 '"currentlyRunning": true'

# Get automations with failed last run
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" \
  --fields=automationID,automationName,lastRunStatus,lastRunErrorMessage | \
  grep -A3 '"lastRunStatus": "Failed"'
```

---

## SQL & Lakebasin

### GET `/api/v2/connector/catalogs/:connectorID`

**Description:** Get available catalogs for a lakehouse-enabled connector
**Token Usage:** ~100-500 tokens (depends on catalog count)
**Auth:** Required
**Scenarios:**

- List catalogs for Trino/Databricks connector
- Explore schema structure
- Build SQL generation context

**Examples:**

```bash
# Get all catalogs
bun run scripts/api-call.ts GET /api/v2/connector/catalogs/123

# Or use get-schema-context.ts script
bun run scripts/get-schema-context.ts 123
```

**Response Format:**

```json
{
	"catalogs": ["hive", "lakehouse", "hubspot"]
}
```

---

### GET `/api/v2/connector/schemas/:connectorID`

**Description:** Get available schemas for a specific catalog
**Token Usage:** ~100-1,000 tokens (depends on schema count)
**Auth:** Required
**Query Parameters:**

- `catalog` (required) - Catalog name

**Examples:**

```bash
# Get schemas for catalog
bun run scripts/api-call.ts GET "/api/v2/connector/schemas/123?catalog=hive"

# Or use get-schema-context.ts script
bun run scripts/get-schema-context.ts 123 --catalog=hive
```

**Response Format:**

```json
{
	"schemas": ["default", "analytics", "staging"]
}
```

---

### GET `/api/v2/connector/tables/:connectorID`

**Description:** Get available tables for a specific catalog and schema
**Token Usage:** ~500-5,000 tokens (depends on table count)
**Auth:** Required
**Query Parameters:**

- `catalog` (required) - Catalog name
- `schema` (required) - Schema name

**Examples:**

```bash
# Get tables for schema
bun run scripts/api-call.ts GET \
  "/api/v2/connector/tables/123?catalog=hive&schema=default"

# Or use get-schema-context.ts script
bun run scripts/get-schema-context.ts 123 --catalog=hive --schema=default
```

**Response Format:**

```json
{
	"tables": [
		{ "name": "customers", "type": "TABLE" },
		{ "name": "orders", "type": "TABLE" }
	]
}
```

---

### POST `/api/connector/columns`

**Description:** Get columns for a specific table
**Token Usage:** ~500-5,000 tokens (depends on column count)
**Auth:** Required
**Body Parameters:**

- `connectorID` (required) - Connector ID
- `tableName` (required) - Table name
- `schemaCatalog` (required) - Format: `catalog.schema`

**Examples:**

```bash
# Get columns for table
bun run scripts/api-call.ts POST /api/connector/columns '{
  "connectorID": 123,
  "tableName": "customers",
  "schemaCatalog": "hive.default"
}'

# Or use get-schema-context.ts script
bun run scripts/get-schema-context.ts 123 \
  --catalog=hive --schema=default --table=customers
```

**Response Format:**

```json
[
	{ "name": "id", "type": "bigint" },
	{ "name": "name", "type": "varchar" },
	{ "name": "email", "type": "varchar" },
	{ "name": "created_at", "type": "timestamp" }
]
```

---

### POST `/api/data-warehouse/proxy`

**Description:** Proxy requests to Trino/Databricks warehouse for SQL execution
**Token Usage:** ~1,000-30,000+ tokens (depends on result size)
**Auth:** Required
**Body Parameters:**

- `url` (required) - Warehouse URL (e.g., `https://trino-host:443/v1/statement`)
- `method` (required) - HTTP method (usually POST for queries)
- `headers` (required) - Request headers (authentication, catalog, etc.)
- `data` (required) - Request body (SQL query)

**Examples:**

```bash
# Execute SQL via proxy (use execute-sql.ts script instead)
bun run scripts/execute-sql.ts 123 "SELECT * FROM users LIMIT 10" --format=table
```

**Response Format:** Returns warehouse-specific response (Trino or Databricks format)

**⚠️ Important:**

- This endpoint is complex - use `execute-sql.ts` script instead
- Requires proper warehouse authentication headers
- Different formats for Trino vs Databricks

---

### LLM Connector Endpoints for SQL Generation

**Pattern:** `/:connectorID/openai/v1/chat/completions`

**Description:** Generate SQL from natural language using LLM connector
**Token Usage:** ~2,000-50,000+ tokens (depends on schema context size)
**Auth:** Required (JWT token)
**Body Parameters:**

- `model` - Model name (e.g., `claude-sonnet-4-20250514`)
- `messages` - Message array with system prompt and user query
- `max_tokens` - Maximum response tokens (default: 2048)
- `temperature` - Temperature (default: 0.2 for SQL generation)

**Examples:**

```bash
# Generate SQL (use generate-sql.ts script instead)
bun run scripts/generate-sql.ts 456 "Get top 10 customers by revenue" \
  --schema-file=schema.json --raw

# Fix SQL (use fix-sql.ts script instead)
bun run scripts/fix-sql.ts 456 "SELECT * FROM users" \
  "Table not found: users" --schema-file=schema.json --raw
```

**⚠️ Important:**

- Use `generate-sql.ts` and `fix-sql.ts` scripts for easier usage
- Always provide schema context for best results
- Specify `--database-type=databricks` for Databricks warehouses

**See [SQL Assistant Guide](./sql-assistant.md) for complete SQL workflows**

---

## Metadata

### GET `/api/databasin-modules`

**Description:** Get available Databasin modules (Flowbasin, Lakebasin, Reportbasin, etc.)
**Token Usage:** ~2,000 tokens
**Auth:** Required
**Scenarios:**

- Get enabled modules
- Check module configuration
- Get module count

**Examples:**

```bash
# Count modules
bun run scripts/api-call.ts GET /api/databasin-modules --count

# Get module details
bun run scripts/api-call.ts GET /api/databasin-modules --fields=id,name,enabled,order
```

**Response Fields:**

- `id`: Module ID (integer)
- `name`: Module name
- `displayName`: Display name
- `enabled`: Boolean enabled state
- `order`: Display order
- `icon`: Icon identifier

---

## Reports

### GET `/api/reports`

**Description:** Get reports created by or shared with current user
**Token Usage:** Variable based on report count
**Auth:** Required
**Scenarios:**

- List user reports
- Get report count
- Find report by name

**Examples:**

```bash
# Count reports
bun run scripts/api-call.ts GET /api/reports --count

# Get report summary
bun run scripts/api-call.ts GET /api/reports --fields=id,name,createdDate,shared --limit=10
```

---

## ⚠️ Endpoints Requiring Special Parameters

**These endpoints return 400 Bad Request without required parameters:**

1. **`/api/pipeline`** - Requires `internalID` parameter
2. **`/api/automations`** - Recommended to use `internalID` parameter
3. **`/api/lakebasin/connections`** - Requires `projectId` parameter

**Always check API client implementations for required parameters!**

---

## Token Efficiency Tips

1. **Always use `--count`** when you only need to know quantity
2. **Use `--summary`** to get total + 3 sample items
3. **Use `--fields`** to limit returned fields
4. **Use `--limit`** to cap result size
5. **Combine options** for maximum efficiency: `--fields=id,name --limit=10`

**Token Usage Examples:**

- Full connectors: ~200,000 tokens
- Connectors with --count: ~50 tokens
- Connectors with --fields and --limit=10: ~1,000 tokens

---

**Testing Completed:** 2025-11-16
**Endpoints Tested:** 15+ core endpoints
**Status:** ✅ Documented and verified
