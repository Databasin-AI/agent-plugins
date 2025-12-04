# Databasin Plugin Usage Guide

This guide explains how to load and use the Databasin Claude Code plugin.

## Loading the Plugin

To use this plugin with the Claude Code Agent SDK, add it to your agent configuration:

```typescript
import { createAgent } from '@anthropic/agent-sdk';

const agent = await createAgent({
	plugins: [
		{
			type: 'local',
			path: './.claude/plugins/databasin'
		}
	]
});
```

### Relative vs Absolute Paths

**Relative path** (recommended):

```typescript
path: './.claude/plugins/databasin'; // Relative to current working directory
```

**Absolute path**:

```typescript
path: '/home/founder3/code/tpi/databasin-sv/.claude/plugins/databasin';
```

## Verifying Plugin Load

After loading, verify the plugin appears in initialization:

```typescript
const response = await agent.sendMessage('Hello');

// Check loaded plugins
console.log('Loaded plugins:', response.plugins);
// Expected: ['databasin']

// Check available commands
console.log('Available commands:', response.slash_commands);
// Expected: [
//   'databasin:list-projects',
//   'databasin:list-connectors',
//   'databasin:get-user-info',
//   'databasin:refresh-token',
//   'databasin:api-health'
// ]
```

## Using Slash Commands

Commands are namespaced with `databasin:` prefix to avoid conflicts:

```typescript
// List projects
await agent.sendMessage('/databasin:list-projects');

// List connectors
await agent.sendMessage('/databasin:list-connectors');

// Get user info
await agent.sendMessage('/databasin:get-user-info');

// Refresh token
await agent.sendMessage('/databasin:refresh-token');

// Check API health
await agent.sendMessage('/databasin:api-health');
```

## Using the Databasin API Expert Agent

The plugin includes a specialized agent that automatically handles Databasin API interactions:

```typescript
// The agent automatically invokes the databasin-api-expert when appropriate
await agent.sendMessage('Show me all my Databasin projects');
await agent.sendMessage('How many connectors are available?');
await agent.sendMessage('What is my account information?');
```

The expert agent will:

1. Consult endpoint documentation
2. Apply token-efficient options
3. Handle authentication errors
4. Format responses clearly
5. Chain multi-step operations

## Direct Skill Access

You can also invoke the underlying skills directly:

### databasin-api Skill

```bash
# Get projects
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/my/projects

# Get connector count
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/connector --count
```

### refresh-databasin-jwt Skill

```bash
# Refresh JWT token
bun run .claude/skills/refresh-databasin-jwt/refresh-jwt.ts
```

## Configuration Requirements

Before using the plugin, ensure these files exist:

### 1. Authentication Config

Create `.auth-config.json` in project root:

```json
{
	"username": "your-email@company.com",
	"password": "your-password",
	"loginUrl": "http://localhost:3000"
}
```

### 2. API Config

The plugin uses `.claude/skills/databasin-api/.local.config.json`:

```json
{
	"baseUrl": "http://localhost:9000"
}
```

### 3. JWT Token

Run the refresh script to create `.token` file:

```bash
bun run .claude/skills/refresh-databasin-jwt/refresh-jwt.ts
```

## Example Workflows

### Workflow 1: First-Time Setup

```typescript
// 1. Create auth config (manual step)
// Create .auth-config.json with credentials

// 2. Refresh token
await agent.sendMessage('/databasin:refresh-token');

// 3. Verify API access
await agent.sendMessage('/databasin:api-health');

// 4. Get your projects
await agent.sendMessage('/databasin:list-projects');
```

### Workflow 2: Explore Data

```typescript
// Get account info
await agent.sendMessage('/databasin:get-user-info');

// List projects
await agent.sendMessage('Show me all my projects');

// Count connectors
await agent.sendMessage('How many connectors are available?');

// Find specific connector
await agent.sendMessage('Do we have a PostgreSQL connector?');
```

### Workflow 3: Handle Token Expiration

```typescript
// If you get 401 Unauthorized errors:

// 1. Refresh token
await agent.sendMessage('/databasin:refresh-token');

// 2. Retry your request
await agent.sendMessage('/databasin:list-projects');
```

## Plugin Capabilities

Once loaded, the plugin provides:

### Commands (5 total)

- `/databasin:list-projects` - List accessible projects
- `/databasin:list-connectors` - List data source connectors
- `/databasin:get-user-info` - Show user profile
- `/databasin:refresh-token` - Refresh JWT token
- `/databasin:api-health` - Check API status

### Agents (1 total)

- `databasin-api-expert` - Specialized agent for API interactions

### Skills (2 total)

- `databasin-api` - API client with token efficiency
- `refresh-databasin-jwt` - Automated token refresh

## Token Efficiency

The plugin automatically applies token-efficient options for heavy endpoints:

```typescript
// ❌ Without plugin - Returns 200,000+ tokens
await fetch('http://localhost:9000/api/connector');

// ✅ With plugin - Returns ~50 tokens
await agent.sendMessage('How many connectors are there?');
// Plugin uses: --count option automatically
```

## Error Handling

The plugin handles common errors automatically:

### 401 Unauthorized

```typescript
await agent.sendMessage('/databasin:list-projects');
// If token expired, agent will guide you to refresh
// "❌ Your JWT token has expired. Run /databasin:refresh-token to get a fresh one."
```

### 404 Not Found

```typescript
// Plugin consults working-endpoints.md to use correct endpoints
// Won't use deprecated or broken endpoints
```

### 500 Server Error

```typescript
// Plugin provides troubleshooting guidance
// "❌ API server error. Check backend logs for details."
```

## Advanced Usage

### Custom API Calls

For endpoints not covered by commands:

```typescript
await agent.sendMessage(
	'Use the databasin-api skill to call GET /api/pipeline with internalID=123'
);
```

The expert agent will:

1. Read the working-endpoints.md documentation
2. Execute the API call with proper authentication
3. Format the response clearly

### Multi-Step Operations

```typescript
await agent.sendMessage('Show me all pipelines in my first project');
```

The expert agent will:

1. Get projects: `GET /api/my/projects --limit=1`
2. Extract project ID from response
3. Get pipelines: `GET /api/pipeline?internalID={id}`
4. Format and present results

## Troubleshooting

### Plugin Not Loading

Check the plugin path is correct:

```typescript
// ✅ Correct
path: './.claude/plugins/databasin';

// ❌ Wrong - missing .claude-plugin/plugin.json
path: './.claude/plugins/databasin-wrong';
```

### Commands Not Available

Verify plugin loaded:

```typescript
console.log('Plugins:', response.plugins);
// Should include 'databasin'
```

### Token Errors

Refresh your JWT token:

```bash
bun run .claude/skills/refresh-databasin-jwt/refresh-jwt.ts
```

Verify `.token` file exists:

```bash
ls -la .token
cat .token  # Should show JWT string
```

### API Connection Errors

Check API server is running:

```bash
curl http://localhost:9000/api/ping
# Should return: pong
```

Verify base URL config:

```bash
cat .claude/skills/databasin-api/.local.config.json
# Should show: {"baseUrl": "http://localhost:9000"}
```

## Security Notes

The plugin automatically excludes these files from git:

- `.auth-config.json` - Contains credentials
- `.token` - Contains JWT token

**Never commit these files to version control.**

## Dependencies

Ensure these are installed:

```bash
# Bun runtime
curl -fsSL https://bun.sh/install | bash

# Install project dependencies
bun install

# Playwright for token refresh
bun add -d playwright
bunx playwright install chromium
```

## Support

For issues or questions:

1. Check `.claude/plugins/databasin/README.md`
2. Review endpoint documentation in `.claude/skills/databasin-api/references/`
3. Consult skill documentation in respective SKILL.md files
4. Use the `databasin-api-expert` agent for guided help

## Version

Plugin version: 1.0.0
Last updated: 2024-11-16
