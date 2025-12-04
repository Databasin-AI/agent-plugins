# Databasin Claude Code Plugin

Complete plugin for Databasin API integration, providing authenticated API access, JWT management, and specialized agents for working with Databasin data.

## Plugin Structure

```
.claude/plugins/databasin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/                 # Slash commands for common operations
│   ├── list-projects.md
│   ├── list-connectors.md
│   ├── get-user-info.md
│   ├── refresh-token.md
│   └── api-health.md
├── agents/                   # Specialized subagents
│   └── databasin-api-expert.md
└── README.md                 # This file
```

## Associated Skills

This plugin works with these skills located in `.claude/skills/`:

- **`databasin-api`** - API client for making authenticated requests to Databasin
  - Location: `.claude/skills/databasin-api/`
  - Script: `scripts/api-call.ts`
  - Documentation: `references/working-endpoints.md`
  - Purpose: Execute API calls with token efficiency options

- **`refresh-databasin-jwt`** - JWT token refresh automation
  - Location: `.claude/skills/refresh-databasin-jwt/`
  - Script: `refresh-jwt.ts`
  - Purpose: Obtain fresh JWT token and save to `.token` file

## Quick Start

### 1. Setup Authentication

Create `.auth-config.json` in project root:

```json
{
	"username": "your-email@company.com",
	"password": "your-password",
	"loginUrl": "http://localhost:3000"
}
```

### 2. Refresh JWT Token

```bash
bun run .claude/skills/refresh-databasin-jwt/refresh-jwt.ts
```

This saves the token to `.token` in the project root.

### 3. Use Slash Commands

The plugin provides these commands (use with `databasin:` prefix):

- **`/databasin:list-projects`** - List all accessible projects
- **`/databasin:list-connectors`** - List available data source connectors
- **`/databasin:get-user-info`** - Show current user profile
- **`/databasin:refresh-token`** - Refresh JWT authentication token
- **`/databasin:api-health`** - Check API server status

### 4. Use the API Expert Agent

When you need to interact with Databasin data, the `databasin-api-expert` agent automatically:

1. Consults endpoint documentation
2. Applies token-efficient options
3. Handles authentication errors
4. Formats responses clearly
5. Chains multi-step operations

## Available Commands

### List Projects

```bash
/databasin:list-projects
```

Displays all projects accessible to the current user with IDs, organization info, and status.

### List Connectors

```bash
/databasin:list-connectors
```

Shows available data source connectors. Automatically uses token-efficient options since there are 434 connectors.

### Get User Info

```bash
/databasin:get-user-info
```

Displays current user profile including organizations, roles, and permissions.

### Refresh Token

```bash
/databasin:refresh-token
```

Refreshes the JWT authentication token using automated browser login.

### API Health Check

```bash
/databasin:api-health
```

Verifies the Databasin API is running and accessible.

## Direct API Access

For advanced usage, call the API directly using the skill:

```bash
# Get projects
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/my/projects

# Get connector count (token-efficient)
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/connector --count

# Get specific fields only
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/connector \
  --fields=connectorID,connectorName \
  --limit=20
```

## Token Efficiency

**CRITICAL:** Some endpoints return massive amounts of data. Always use these options:

- **`--count`** - Get count only (reduces 50,000+ tokens to ~50)
- **`--summary`** - Get total + 3 samples
- **`--fields=field1,field2`** - Limit returned fields
- **`--limit=N`** - Limit number of results
- **`--offset=N`** - Skip first N results

**Example: Heavy endpoint**

```bash
# ❌ BAD - Returns 200,000+ tokens
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/connector

# ✅ GOOD - Returns ~50 tokens
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/connector --count

# ✅ GOOD - Returns ~5,000 tokens
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/connector \
  --fields=connectorID,connectorName --limit=20
```

## Endpoint Documentation

Before calling any endpoint, consult the reference documentation:

```bash
# Read working endpoints guide
cat .claude/skills/databasin-api/references/working-endpoints.md

# Check deprecated endpoints to avoid
cat .claude/skills/databasin-api/references/deprecated-endpoints.md

# Quick start guide
cat .claude/skills/databasin-api/references/README.md
```

## Common Workflows

### Workflow 1: Setup and Test

```bash
# 1. Create auth config
cp .auth-config.example.json .auth-config.json
# Edit .auth-config.json with your credentials

# 2. Refresh token
bun run .claude/skills/refresh-databasin-jwt/refresh-jwt.ts

# 3. Test API
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/ping
```

### Workflow 2: Explore Your Data

```bash
# Get account info
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/my/account

# List projects
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/my/projects

# Count connectors
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/connector --count
```

### Workflow 3: Handle Token Expiration

```bash
# If you get 401 Unauthorized:

# 1. Refresh token
bun run .claude/skills/refresh-databasin-jwt/refresh-jwt.ts

# 2. Retry your API call
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/my/projects
```

## Error Handling

### 401 Unauthorized

Your JWT token has expired. Run the token refresh command.

### 404 Not Found

The endpoint doesn't exist. Check `working-endpoints.md` for correct endpoints.

### 500 Internal Server Error

Backend API issue. Check API server logs.

## Configuration Files

### `.auth-config.json` (project root)

```json
{
	"username": "your-email@company.com",
	"password": "your-password",
	"loginUrl": "http://localhost:3000"
}
```

**Status:** Git-ignored for security

### `.token` (project root)

Contains the current JWT token (plain text).

**Status:** Git-ignored for security

### `.claude/skills/databasin-api/.local.config.json`

```json
{
	"baseUrl": "http://localhost:9000"
}
```

**Status:** Git-ignored for local overrides

## Security Notes

These files are automatically git-ignored:

- `.auth-config.json` - Contains credentials
- `.token` - Contains JWT token
- `.claude/skills/databasin-api/.local.config.json` - Local overrides

**Never commit credentials or tokens to version control.**

## Dependencies

- **Bun** >= 1.0.0 - JavaScript runtime
- **Playwright** >= 1.40.0 - Browser automation for token refresh

Install dependencies:

```bash
bun install
bun add -d playwright
bunx playwright install chromium
```

## Plugin Capabilities

This plugin provides:

1. **API Client** - Authenticated HTTP client for Databasin API
2. **Authentication** - Automated JWT token refresh
3. **Data Integration** - Access to projects, pipelines, connectors
4. **Pipeline Management** - Query and manage data pipelines
5. **SQL Execution** - Access to SQL query results via Lakebasin
6. **Reporting** - Access to Reportbasin reports and analytics

## Support

For issues or questions:

1. Check endpoint documentation in `.claude/skills/databasin-api/references/`
2. Review the skill README files
3. Consult the Databasin API swagger documentation
4. Use the `databasin-api-expert` agent for guided assistance

## Version History

### v1.0.0 (2024-11-16)

- Initial plugin structure
- 5 slash commands for common operations
- databasin-api-expert specialized agent
- Integration with databasin-api and refresh-databasin-jwt skills
- Comprehensive documentation and examples
