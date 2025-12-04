# Databasin API Best Practices

**Purpose:** Guidelines for effective and efficient use of the Databasin API skill

---

## When to Ask for Clarification

**ALWAYS ask the user for clarification when:**

### 1. Missing Connector ID

User asks to query or work with a connector but doesn't specify which one.

**Ask:** "Which connector would you like to work with? Please provide the connector ID or name."

### 2. Ambiguous Table/Schema Names

User mentions a table that might not exist or schema is unclear.

**Do:** Run schema discovery first (list-schemas.ts, list-tables.ts)

**Ask:** "I found these schemas/tables: [list]. Which one would you like to query?"

### 3. Unclear Query Intent

User asks a vague question like "show me the data"

**Ask:** "What specific data would you like to see? For example:

- All records (with LIMIT)?
- A count of records?
- Filtered by specific criteria?
- Specific columns only?"

### 4. Multiple Possible Approaches

Task can be solved multiple ways (API endpoint vs SQL query)

**Ask:** "I can do this via [option 1] or [option 2]. Which would you prefer?"

### 5. Missing Context for SQL

User wants to query but you don't know the schema structure.

**Do:** Use schema discovery scripts first

**Explain:** "Let me first discover the schema structure to write the correct query."

---

## Development Best Practices

### ✅ DO

**Schema Discovery First**

- Use schema discovery scripts BEFORE writing SQL queries
- Never guess table or column names
- Always verify schema structure exists

**Clear Communication**

- Provide step-by-step explanations of what you're doing
- Show exact commands being run
- Give contextual error messages with solutions
- Suggest next steps after each operation

**Token Efficiency**

- Always use `--count` first to check data size
- Apply `--fields` and `--limit` for large datasets
- Use `--summary` for quick overviews
- Reference: [token-efficiency.md](./token-efficiency.md)

**Error Handling**

- Validate required parameters before calling
- Check for null responses and provide context
- Reference deprecated endpoints list
- Provide actionable error messages
- Reference: [error-handling.md](./error-handling.md)

**Security**

- Never expose JWT tokens in responses
- Use file permissions (chmod 600 .token)
- Check token expiration
- Reference: [security.md](./security.md)

---

### ❌ DON'T

**Don't Guess**

- Don't guess table or column names
- Don't assume connector IDs
- Don't skip schema discovery

**Don't Waste Tokens**

- Don't call `/api/connector` without filters (434 items!)
- Don't call `/api/config` without filters (50K+ tokens)
- Don't fetch full data when count suffices

**Don't Skip Validation**

- Don't run SQL without discovering schema first (unless user provides exact names)
- Don't skip error handling or assume success
- Don't ignore required parameters

---

## Common Workflow Patterns

### Pattern 1: Schema Discovery → Query

```bash
# Step 1: Discover schemas
bun run scripts/list-schemas.ts <connectorID>

# Step 2: List tables in target schema
bun run scripts/list-tables.ts <connectorID> <schemaName>

# Step 3: Describe table structure
bun run scripts/describe-table.ts <connectorID> <schemaName> <tableName>

# Step 4: Execute query with verified names
bun run scripts/execute-sql.ts <connectorID> "SELECT * FROM schema.table LIMIT 10"
```

### Pattern 2: Natural Language → SQL

```bash
# Step 1: Get schema context
bun run scripts/get-schema-context.ts <connectorID> --output=schema.json

# Step 2: Generate SQL from natural language
bun run scripts/generate-sql.ts <connectorID> "your question" --schema-file=schema.json

# Step 3: Execute generated SQL
bun run scripts/execute-sql.ts <connectorID> "<generated SQL>" --format=table

# Step 4: Fix if error occurs
bun run scripts/fix-sql.ts <connectorID> "<failed SQL>" "<error message>" --schema-file=schema.json
```

### Pattern 3: Project Resource Discovery

```bash
# Step 1: Get user context
bun run scripts/get-user-context.ts

# Step 2: Get project's internalID from output
# Then query project resources:

# Count connectors
bun run scripts/api-call.ts GET "/api/connector?internalID=<id>" --count

# Count pipelines
bun run scripts/api-call.ts GET "/api/pipeline?internalID=<id>" --count

# Count automations
bun run scripts/api-call.ts GET "/api/automations?internalID=<id>" --count
```

### Pattern 4: Token-Efficient Exploration

```bash
# Step 1: Count to check size
bun run scripts/api-call.ts GET /api/endpoint --count

# Step 2: If large, get summary (count + 3 samples)
bun run scripts/api-call.ts GET /api/endpoint --summary

# Step 3: If needed, get specific fields with limit
bun run scripts/api-call.ts GET /api/endpoint --fields=id,name --limit=20

# Step 4: Only get full data if absolutely necessary
bun run scripts/api-call.ts GET /api/endpoint
```

---

## Decision Trees

### "Should I use API endpoint or SQL query?"

```
User wants to...
├─ Get Databasin metadata (projects, connectors, pipelines)
│  └─ Use API endpoints (api-call.ts)
│
├─ Query data inside a connector/database
│  └─ Use SQL scripts (execute-sql.ts, generate-sql.ts)
│
├─ Create/update/delete Databasin resources
│  └─ Use API endpoints (POST/PUT/DELETE via api-call.ts)
│
└─ Analyze or transform data
   └─ Use SQL scripts with natural language generation
```

### "Which schema discovery script should I use?"

```
I need to...
├─ See what schemas are available
│  └─ list-schemas.ts <connectorID>
│
├─ See what tables are in a schema
│  └─ list-tables.ts <connectorID> <schemaName>
│
├─ See columns and types for a table
│  └─ describe-table.ts <connectorID> <schemaName> <tableName>
│
└─ Get full context for LLM to generate SQL
   └─ get-schema-context.ts <connectorID> --output=schema.json
```

### "How should I handle this error?"

```
Error type...
├─ 401 Unauthorized
│  └─ Check .token file, refresh JWT token
│
├─ 400 Bad Request
│  └─ Check required parameters, validate request body
│
├─ null response
│  └─ Add missing required parameter (usually internalID)
│
├─ "Table does not exist"
│  └─ Run schema discovery to find correct names
│
└─ Token limit exceeded
   └─ Use --count, --summary, --fields, --limit options
```

Reference: [error-handling.md](./error-handling.md)

---

## Quick Command Reference

### Most Common Commands

```bash
# Get user context (account + orgs + projects)
bun run scripts/get-user-context.ts

# Count resources token-efficiently
bun run scripts/api-call.ts GET /api/endpoint --count

# Get summary (count + 3 samples)
bun run scripts/api-call.ts GET /api/endpoint --summary

# Get specific fields with limit
bun run scripts/api-call.ts GET /api/endpoint --fields=id,name --limit=10

# Discover database schema
bun run scripts/list-schemas.ts <connectorID>
bun run scripts/list-tables.ts <connectorID> <schemaName>
bun run scripts/describe-table.ts <connectorID> <schemaName> <tableName>

# Generate and execute SQL
bun run scripts/generate-sql.ts <connectorID> "your question" --schema-file=schema.json
bun run scripts/execute-sql.ts <connectorID> "SELECT ..." --format=table
```

---

## Token Efficiency Tips

### Size Estimation Rules

| Dataset Size   | Best Option                  | Token Usage         |
| -------------- | ---------------------------- | ------------------- |
| Unknown        | `--count` first              | ~50 tokens          |
| < 10 items     | Full response                | ~500-2,000 tokens   |
| 10-100 items   | `--fields --limit=20`        | ~2,000-5,000 tokens |
| 100-1000 items | `--summary`                  | ~2,000 tokens       |
| 1000+ items    | `--count` + targeted queries | ~50 tokens          |

### Progressive Disclosure

```bash
# Step 1: Always start with count
--count (~50 tokens)

# Step 2: If count is reasonable, get summary
--summary (~500-2,000 tokens)

# Step 3: If needed, get specific data
--fields=field1,field2 --limit=N (~variable)

# Step 4: Only if absolutely necessary
Full response (potentially 100K+ tokens)
```

Reference: [token-efficiency.md](./token-efficiency.md)

---

## Security Checklist

- [ ] JWT token stored in `.token` file (not hardcoded)
- [ ] `.token` file has secure permissions (chmod 600)
- [ ] `.token` is in `.gitignore`
- [ ] Token expiration is monitored
- [ ] Never expose tokens in console output
- [ ] Use HTTPS endpoints only
- [ ] Validate all user inputs before API calls

Reference: [security.md](./security.md)

---

## Performance Tips

### Optimize API Calls

1. **Use filters** - Always add `internalID` or other filters when available
2. **Batch operations** - Group related calls when possible
3. **Cache results** - Store frequently accessed data locally
4. **Pagination** - Use `--limit` and `--offset` for large datasets

### Optimize SQL Queries

1. **Use LIMIT** - Always add LIMIT clause to prevent massive result sets
2. **Select specific columns** - Avoid `SELECT *` when possible
3. **Filter early** - Apply WHERE clauses to reduce data transfer
4. **Use schema discovery** - Prevent query failures and retries

---

## Testing Recommendations

### Before Production Use

1. **Test with --count** - Verify endpoint works and check data size
2. **Test with --summary** - Review data structure
3. **Test with filters** - Ensure parameters work correctly
4. **Test error cases** - Handle missing parameters, invalid IDs
5. **Monitor tokens** - Track actual token usage

### SQL Query Testing

1. **Test schema discovery** - Verify all scripts work for connector type
2. **Test with LIMIT 1** - Validate query structure before full execution
3. **Test error handling** - Try invalid queries and verify fix-sql.ts works
4. **Test natural language** - Verify generate-sql.ts produces correct queries

---

## Common Mistakes to Avoid

### Mistake 1: Skipping Token Efficiency Options

❌ **Bad:**

```bash
bun run scripts/api-call.ts GET /api/connector
# Returns 434 connectors, uses 200,000+ tokens!
```

✅ **Good:**

```bash
bun run scripts/api-call.ts GET /api/connector --count
# Returns count only, uses ~50 tokens
```

### Mistake 2: Guessing Schema Names

❌ **Bad:**

```bash
bun run scripts/execute-sql.ts 123 "SELECT * FROM users"
# Error: Table 'users' does not exist
```

✅ **Good:**

```bash
# First discover the schema
bun run scripts/list-schemas.ts 123
bun run scripts/list-tables.ts 123 public
# Then use correct name
bun run scripts/execute-sql.ts 123 "SELECT * FROM public.user_accounts LIMIT 10"
```

### Mistake 3: Missing Required Parameters

❌ **Bad:**

```bash
bun run scripts/api-call.ts GET /api/automations
# Returns null - missing internalID parameter
```

✅ **Good:**

```bash
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --count
```

### Mistake 4: Not Using Schema Context for SQL Generation

❌ **Bad:**

```bash
bun run scripts/generate-sql.ts 456 "Get top customers"
# May generate incorrect table/column names
```

✅ **Good:**

```bash
# First get schema context
bun run scripts/get-schema-context.ts 456 --output=schema.json
# Then generate with context
bun run scripts/generate-sql.ts 456 "Get top customers" --schema-file=schema.json
```

---

**Last Updated:** 2025-11-21
**Related Guides:**

- [Getting Started](./getting-started.md)
- [Token Efficiency](./token-efficiency.md)
- [Error Handling](./error-handling.md)
- [Security](./security.md)
- [Schema Discovery](./schema-discovery.md)
- [SQL Assistant](./sql-assistant.md)
