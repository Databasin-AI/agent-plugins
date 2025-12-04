# Databasin API Skill - Improvements and Lessons Learned

## Session Date: 2025-11-20

### Overview

This document captures lessons learned from implementing and testing the `/api/connector/:id/query` endpoint and improving the JWT token refresh workflow.

---

## 1. JWT Token Refresh Improvements

### Current Issues

#### Popup Authentication Flow

- **Problem**: Azure AD authentication uses a popup window that Playwright can't easily access in headless mode
- **Symptoms**:
  - "Cross-Origin-Opener-Policy policy would block the window.closed call" errors
  - Token never appears in localStorage after button click
  - Script waits 30 seconds then fails
  - `msal.version` appears in localStorage but `token` does not

#### localStorage Token Format

- **Discovery**: Databasin stores JWT token in wrapped JSON format: `{value: "...", expires: null}`
- **Current script**: Checks multiple keys but didn't prioritize the correct format
- **Impact**: Even when token exists, extraction logic may miss it

### Recommended Improvements

#### 1. Add Fallback Authentication Methods

```typescript
// Priority 1: Manual token paste
// If refresh script fails, provide clear instructions:
console.error(`
Manual token extraction:
1. Open http://localhost:3000 in your browser
2. Sign in with Azure AD
3. Open DevTools (F12) → Application → Local Storage
4. Copy value from 'token' key (inside JSON: {"value": "..."})
5. Paste into .token file
`);

// Priority 2: Browser extension or API endpoint
// Consider implementing a /api/auth/refresh endpoint that can be called
// with existing credentials to get a fresh token
```

#### 2. Improve Token Extraction Logic

```typescript
// Prioritize Databasin's specific format
async function extractJWT(page: Page): Promise<string | null> {
	// Try Databasin format first (most likely)
	const token = await page.evaluate(() => {
		const item = localStorage.getItem('token');
		if (item) {
			try {
				const parsed = JSON.parse(item);
				return parsed.value || null;
			} catch {}
		}
		return null;
	});

	if (token) return token;

	// Fallback to other formats...
}
```

#### 3. Better Popup Handling

```typescript
// Option A: Intercept popup and handle in same context
const context = await browser.newContext({
  viewport: { width: 1280, height: 720 }
});

// Listen for new pages (popups)
context.on('page', async (popup) => {
  console.error('🪟 Popup detected, monitoring authentication...');
  // Handle Azure AD form in popup
});

// Option B: Use MSAL redirect flow instead of popup
// Modify Azure AD config in .auth-config.json to use redirect
{
  "authMethod": "redirect", // instead of "popup"
  "username": "...",
  "password": "..."
}
```

#### 4. Add Token Validation

```typescript
// Before saving token, verify it's valid
async function validateToken(jwt: string): Promise<boolean> {
	try {
		const response = await fetch('http://localhost:9000/api/ping', {
			headers: { Authorization: `Bearer ${jwt}` }
		});
		return response.ok;
	} catch {
		return false;
	}
}
```

---

## 2. SQL Execution Improvements

### Current State

- ✅ `/api/connector/:id/query` endpoint working
- ✅ Executes SQL against any RDBMS connector
- ✅ Returns proper JSON with rows, columns, metadata
- ✅ Permission checking via `connectionPermissionService`

### Recommended Enhancements

#### 1. Add Schema Discovery Helper

```typescript
// scripts/explore-schema.ts
async function exploreSchema(connectorID: number) {
	// List all schemas
	const schemas = await executeSQL(
		connectorID,
		`
    SELECT schema_name
    FROM information_schema.schemata
    ORDER BY schema_name
  `
	);

	// For each schema, list tables
	for (const schema of schemas.rows) {
		const tables = await executeSQL(
			connectorID,
			`
      SELECT table_name, table_type
      FROM information_schema.tables
      WHERE table_schema = '${schema.schema_name}'
      ORDER BY table_name
    `
		);

		console.log(`Schema: ${schema.schema_name}`);
		tables.rows.forEach((t) => console.log(`  - ${t.table_name} (${t.table_type})`));
	}
}
```

#### 2. Add Query Templates

```typescript
// scripts/query-templates.ts
const QUERY_TEMPLATES = {
	countTable: (schema: string, table: string) => `SELECT COUNT(*) as count FROM ${schema}.${table}`,

	tableInfo: (schema: string, table: string) => `
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_schema = '${schema}' AND table_name = '${table}'
    ORDER BY ordinal_position
  `,

	sampleData: (schema: string, table: string, limit: number = 10) =>
		`SELECT * FROM ${schema}.${table} LIMIT ${limit}`,

	searchTables: (pattern: string) => `
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_name ILIKE '%${pattern}%'
    ORDER BY table_schema, table_name
  `
};
```

#### 3. Add Interactive SQL REPL

```typescript
// scripts/sql-repl.ts
// Interactive SQL shell for exploring connectors
import readline from 'readline';

async function sqlREPL(connectorID: number) {
	const rl = readline.createInterface({
		input: process.stdin,
		output: process.stdout,
		prompt: `[Connector ${connectorID}]> `
	});

	rl.prompt();

	rl.on('line', async (line) => {
		if (line.trim().startsWith('.')) {
			// Handle special commands
			switch (line.trim()) {
				case '.schemas':
					await listSchemas(connectorID);
					break;
				case '.tables':
					await listTables(connectorID);
					break;
				case '.quit':
					process.exit(0);
			}
		} else {
			// Execute SQL
			const result = await executeSQL(connectorID, line);
			console.table(result.rows);
		}
		rl.prompt();
	});
}
```

#### 4. Better Error Messages

```typescript
// In execute-sql.ts, improve error handling
try {
	const result = await executeSQL(connectorID, sql, jwt, timeout);
	// ...
} catch (error) {
	if (error.message.includes('relation') && error.message.includes('does not exist')) {
		console.error('❌ Table not found. Try these commands:');
		console.error(
			'   List schemas: bun run scripts/execute-sql.ts <id> "SELECT schema_name FROM information_schema.schemata"'
		);
		console.error(
			'   Search tables: bun run scripts/execute-sql.ts <id> "SELECT table_schema, table_name FROM information_schema.tables WHERE table_name LIKE \'%pipeline%\'"'
		);
	} else if (error.message.includes('401')) {
		console.error('❌ Token expired. Run: bun run ../../refresh-databasin-jwt/refresh-jwt.ts');
	} else {
		console.error('❌ Error:', error.message);
	}
}
```

---

## 3. Documentation Improvements

### Add Quick Start Examples

Create `references/sql-assistant.md` with:

```markdown
# SQL Assistant Quick Start

## Setup

1. Ensure you have a valid JWT token in `.token` file
2. Find your connector ID from the UI or API

## Common Queries

### Count Records

\`\`\`bash
bun run scripts/execute-sql.ts 5459 "SELECT COUNT(\*) FROM main.pipeline"
\`\`\`

### Explore Schema

\`\`\`bash

# List all schemas

bun run scripts/execute-sql.ts 5459 "SELECT schema_name FROM information_schema.schemata"

# Find tables with 'pipeline' in name

bun run scripts/execute-sql.ts 5459 "SELECT table_schema, table_name FROM information_schema.tables WHERE table_name LIKE '%pipeline%'"
\`\`\`

### Sample Data

\`\`\`bash
bun run scripts/execute-sql.ts 5459 "SELECT \* FROM main.pipeline LIMIT 5" --format=table
\`\`\`

## Troubleshooting

### Token Expired (401 Error)

Refresh your token manually:

1. Log into http://localhost:3000
2. Open DevTools → Application → Local Storage
3. Copy value from 'token' key
4. Paste into `.token` file

### Table Not Found

Use schema exploration queries above to find the correct table name.
```

---

## 4. Testing Improvements

### Add Integration Tests

```typescript
// tests/connector-query.test.ts
describe('Connector Query Endpoint', () => {
	test('executes simple SELECT query', async () => {
		const result = await executeSQL(5459, 'SELECT 1 as test');
		expect(result.success).toBe(true);
		expect(result.rows[0].test).toBe(1);
	});

	test('handles invalid SQL gracefully', async () => {
		const result = await executeSQL(5459, 'INVALID SQL');
		expect(result.success).toBe(false);
		expect(result.error).toContain('syntax error');
	});

	test('enforces permission checks', async () => {
		const result = await executeSQL(9999, 'SELECT 1'); // Non-existent connector
		expect(result.success).toBe(false);
		expect(result.error).toContain('not authorized');
	});
});
```

---

## 5. User Experience Improvements

### 1. Add Progress Indicators

```typescript
// For long-running queries
console.error('⏳ Executing query...');
const startTime = Date.now();

// Show progress every 2 seconds
const interval = setInterval(() => {
	const elapsed = Math.floor((Date.now() - startTime) / 1000);
	console.error(`   Still running... (${elapsed}s)`);
}, 2000);

const result = await executeSQL(connectorID, sql, jwt, timeout);
clearInterval(interval);
```

### 2. Add Query History

```typescript
// Save query history to ~/.databasin-sql-history
import fs from 'fs';
import os from 'os';

const historyFile = path.join(os.homedir(), '.databasin-sql-history');

function saveToHistory(connectorID: number, sql: string, success: boolean) {
	const entry = {
		timestamp: new Date().toISOString(),
		connectorID,
		sql,
		success
	};

	fs.appendFileSync(historyFile, JSON.stringify(entry) + '\n');
}

// Add command to view history
// bun run scripts/sql-history.ts --last 10
```

### 3. Add Output Formatting Options

```typescript
// Add to execute-sql.ts options
--format=json     # JSON output (default)
--format=csv      # CSV output
--format=table    # Pretty table (current)
--format=markdown # Markdown table
--format=html     # HTML table

// Example markdown output
function formatMarkdown(result: ExecutionResult): string {
  const columns = result.columns || [];
  const rows = result.rows || [];

  let output = '| ' + columns.join(' | ') + ' |\n';
  output += '| ' + columns.map(() => '---').join(' | ') + ' |\n';

  rows.forEach(row => {
    output += '| ' + columns.map(col => row[col] ?? '').join(' | ') + ' |\n';
  });

  return output;
}
```

---

## 6. Performance Improvements

### 1. Add Query Result Caching

```typescript
// Cache results for repeated queries
import crypto from 'crypto';

const queryCache = new Map<string, ExecutionResult>();

function getCacheKey(connectorID: number, sql: string): string {
	return crypto.createHash('md5').update(`${connectorID}:${sql}`).digest('hex');
}

async function executeSQLWithCache(
	connectorID: number,
	sql: string,
	jwt: string,
	useCache: boolean = true
): Promise<ExecutionResult> {
	if (useCache) {
		const key = getCacheKey(connectorID, sql);
		const cached = queryCache.get(key);
		if (cached) {
			console.error('📦 Using cached result');
			return cached;
		}
	}

	const result = await executeSQL(connectorID, sql, jwt);

	if (result.success && useCache) {
		queryCache.set(getCacheKey(connectorID, sql), result);
	}

	return result;
}
```

### 2. Add Query Explain Plan

```typescript
// Add --explain flag to show query execution plan
if (options.explain) {
	const explainSQL = `EXPLAIN ${sql}`;
	const plan = await executeSQL(connectorID, explainSQL, jwt);
	console.error('\n📊 Query Plan:');
	console.table(plan.rows);
}
```

---

## Priority Implementation Order

1. **Immediate** (Next Session)
   - Add manual token extraction instructions to error messages
   - Add schema exploration helper queries to README
   - Improve error messages for common issues

2. **Short Term** (This Week)
   - Implement query templates
   - Add integration tests
   - Create interactive SQL REPL

3. **Medium Term** (Next Sprint)
   - Fix popup authentication in refresh script
   - Add query history tracking
   - Add result caching

4. **Long Term** (Future Enhancement)
   - Build web UI for SQL execution
   - Add query performance monitoring
   - Implement query result export to various formats

---

## Lessons Learned Summary

### What Worked Well

- ✅ Direct API endpoint approach for SQL execution
- ✅ Using existing JDBC infrastructure
- ✅ Jackson ObjectMapper for JSON serialization
- ✅ Permission-based access control
- ✅ CLI script with multiple output formats

### What Needs Improvement

- ❌ JWT token refresh automation (popup auth issues)
- ❌ Schema discovery (need helper tools)
- ❌ Error messages (need more context)
- ❌ Documentation (need more examples)
- ❌ User workflow (too many manual steps)

### Key Takeaways

1. **Azure AD popup authentication is tricky in headless browsers** - need fallback to manual token extraction
2. **Schema exploration is essential** - users need to discover table names before querying
3. **Error messages should be actionable** - tell users exactly what to do next
4. **Token lifecycle management matters** - expiration, refresh, validation all need smooth UX
5. **SQL execution is powerful** - having direct database access enables many use cases beyond the API

---

## Related Files

- `/home/founder3/code/tpi/databasin-sv/.claude-plugin/plugins/databasin/skills/databasin-api/scripts/execute-sql.ts`
- `/home/founder3/code/tpi/databasin-sv/.claude-plugin/plugins/databasin/skills/refresh-databasin-jwt/refresh-jwt.ts`
- `/home/founder3/code/tpi/tpi-datalake-api/app/com/databasin/platform/ConnectorService.scala:1174-1280`
- `/home/founder3/code/tpi/tpi-datalake-api/app/controllers/api/ConnectorsController.scala:933-1000`
- `/home/founder3/code/tpi/tpi-datalake-api/conf/routes:68`
