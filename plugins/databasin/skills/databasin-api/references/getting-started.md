# Getting Started with Databasin API

**Quick setup guide for making your first API calls**

---

## Authentication

The API client reads the JWT token from a `.token` file in the current working directory. This file should contain only the JWT token string.

**Token file location:** `.token` (in project root)

---

## Your First API Call

```bash
# Check API connection
bun run scripts/api-call.ts GET /api/ping

# Get your organizations (count only - very efficient)
bun run scripts/api-call.ts GET /api/my/organizations --count

# Get your projects (summary view)
bun run scripts/api-call.ts GET /api/my/projects --summary
```

---

## Essential Commands

### Check What's Available

```bash
# How many projects do I have?
bun run scripts/api-call.ts GET /api/my/projects --count

# How many connectors?
bun run scripts/api-call.ts GET /api/connector --count

# Get a sample of what's available
bun run scripts/api-call.ts GET /api/my/projects --summary
```

### Get Specific Data

```bash
# Get project names and IDs only
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalId

# Get first 10 connectors with specific fields
bun run scripts/api-call.ts GET /api/connector --fields=connectorID,connectorName,connectorType --limit=10
```

---

## Token-Efficient Options

**ALWAYS use these to avoid massive token usage:**

- `--count` - Get just the count (uses ~50 tokens)
- `--summary` - Get count + first 3 samples (uses ~500-2000 tokens)
- `--fields=field1,field2` - Return only specific fields (saves 50-80%)
- `--limit=N` - Limit results to N items
- `--compact` - Remove JSON formatting (saves ~30%)

**Example:**

```bash
# BAD: Returns all 434 connectors (200,000+ tokens!)
bun run scripts/api-call.ts GET /api/connector

# GOOD: Count first, then get what you need
bun run scripts/api-call.ts GET /api/connector --count
bun run scripts/api-call.ts GET /api/connector --fields=connectorID,connectorName --limit=10
```

See **[token-efficiency.md](./token-efficiency.md)** for complete guide.

---

## Essential Reading

**BEFORE calling any endpoint, consult:**

- **[working-endpoints.md](./working-endpoints.md)** - 15+ tested endpoints with examples
- **[deprecated-endpoints.md](./deprecated-endpoints.md)** - Broken endpoints to avoid

**Why this matters:**

1. Avoid endpoints that return errors or null
2. Learn required parameters
3. Optimize token usage
4. See tested examples

---

## Common First Tasks

### Get Your User Context

```bash
# Get all organizations you belong to
bun run scripts/api-call.ts GET /api/my/organizations

# Get all projects you have access to
bun run scripts/api-call.ts GET /api/my/projects
```

See **[projects-and-organizations.md](./projects-and-organizations.md)** for details.

### Work with Connectors

```bash
# Get connectors for a specific project
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --count
```

See **[connectors.md](./connectors.md)** for details.

### Work with Pipelines

```bash
# Get pipelines for a project
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do" --count
```

See **[pipelines.md](./pipelines.md)** for details.

---

## Error Handling

**HTTP Status Codes:**

- **200-299** - Success
- **400** - Bad Request (check payload or required parameters)
- **401** - Unauthorized (check JWT token)
- **404** - Not Found (check endpoint path)
- **500** - Server Error (check API logs)

**If you get errors:**

1. Check **[deprecated-endpoints.md](./deprecated-endpoints.md)** for known issues
2. Verify required parameters in **[working-endpoints.md](./working-endpoints.md)**
3. See **[error-handling.md](./error-handling.md)** for troubleshooting

---

## Next Steps

**For specific tasks, see:**

- **[projects-and-organizations.md](./projects-and-organizations.md)** - User context, projects, organizations
- **[connectors.md](./connectors.md)** - Data source management
- **[pipelines.md](./pipelines.md)** - Pipeline operations
- **[token-efficiency.md](./token-efficiency.md)** - Optimize API usage
- **[programmatic-usage.md](./programmatic-usage.md)** - Use in your code
- **[security.md](./security.md)** - Token security best practices

---

**Last Updated:** 2025-11-17
