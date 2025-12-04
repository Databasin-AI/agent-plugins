# Databasin API References

**Created:** 2025-11-16
**Purpose:** Quick reference documentation for Databasin API endpoints

---

## 📁 Available Documentation

### [working-endpoints.md](./working-endpoints.md)

**Complete endpoint reference guide**

Contains detailed documentation for 15+ verified working endpoints including:

- Projects & Organizations
- Connectors
- Pipelines
- Users
- System endpoints
- Automations
- Metadata
- Reports

Each endpoint includes:

- Description and purpose
- Token usage estimates
- Authentication requirements
- Common use case scenarios
- Code examples with token-efficient options
- Response field documentation

**Use this when:** You need to call a Databasin API endpoint and want to know the correct usage

---

### [deprecated-endpoints.md](./deprecated-endpoints.md)

**Broken and problematic endpoints**

Documents endpoints that should NOT be used:

- Deprecated endpoints with backend bugs
- Endpoints with broken serialization
- Endpoints returning HTML errors
- Token-heavy endpoints requiring caution
- Required parameter documentation

**Use this when:** An endpoint isn't working as expected or you get unexpected errors

---

## 🚀 Quick Start

### Most Common Endpoints

```bash
# Get user's projects (use this often!)
bun run scripts/api-call.ts GET /api/my/projects --count
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalID --limit=10

# Get current user info
bun run scripts/api-call.ts GET /api/my/account --fields=id,firstName,lastName,email

# Get organizations
bun run scripts/api-call.ts GET /api/my/organizations --count

# Get connectors for a project
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --count

# Get pipelines for a project
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do" --count

# Get automations for a project
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --count

# Health check
bun run scripts/api-call.ts GET /api/ping
```

---

## ⚠️ Critical Warnings

### 1. Token-Heavy Endpoints

**NEVER call these without filters:**

- `/api/connector` - 434 connectors = ~200,000 tokens!
- `/api/config` - Full config = ~50,000 tokens

**Always use:** `--count`, `--summary`, `--fields`, or `--limit`

### 2. Required Parameters

**These endpoints REQUIRE parameters or they fail:**

- `/api/pipeline` → needs `internalID`
- `/api/lakebasin/connections` → needs `projectId`
- `/api/automations` → recommended `internalID`

### 3. Deprecated Endpoints

**DO NOT USE:**

- `/api/projects?orgId={id}` → Use `/api/my/projects` instead

---

## 💡 Token Efficiency Best Practices

### Always Start with Count

```bash
# Step 1: Check how much data exists
bun run scripts/api-call.ts GET /api/my/projects --count

# Step 2: If count is large, use fields + limit
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name --limit=10

# Step 3: Only get full data if absolutely needed
```

### Use Summary for Large Datasets

```bash
# Get total count + first 3 samples
bun run scripts/api-call.ts GET /api/connector --summary
```

### Combine Options for Maximum Efficiency

```bash
# Fields + limit + compact = minimal tokens
bun run scripts/api-call.ts GET /api/connector --fields=connectorID,connectorName --limit=5 --compact
```

---

## 📊 Token Usage Reference

| Endpoint                    | Full Data | With --count | With --fields --limit=10 |
| --------------------------- | --------- | ------------ | ------------------------ |
| `/api/connector`            | ~200,000  | ~50          | ~1,000                   |
| `/api/my/projects` (18)     | ~20,000   | ~50          | ~2,000                   |
| `/api/config`               | ~50,000   | ~50          | ~5,000                   |
| `/api/my/organizations` (7) | ~5,000    | ~50          | ~500                     |
| `/api/my/account`           | ~2,000    | N/A          | ~500                     |

---

## 🔍 How to Use These References

### Scenario 1: "I need to get projects"

1. Open [working-endpoints.md](./working-endpoints.md)
2. Search for "projects"
3. Find `/api/my/projects` section
4. Copy example command
5. Modify for your needs

### Scenario 2: "This endpoint is broken"

1. Open [deprecated-endpoints.md](./deprecated-endpoints.md)
2. Check if endpoint is listed
3. Find recommended alternative
4. Check "Lessons Learned" section

### Scenario 3: "Token usage is too high"

1. Check if endpoint is in "Token-Heavy Endpoints" section
2. Use `--count` first
3. Apply `--fields` and `--limit` filters
4. Refer to token usage reference table

---

## 📝 Documentation Maintenance

### Adding New Endpoints

When documenting a new endpoint, include:

1. Endpoint path and HTTP method
2. Description and purpose
3. Token usage estimate
4. Auth requirements
5. Required/optional parameters
6. Common scenarios (3-5 use cases)
7. Code examples
8. Response field documentation

### Reporting Issues

If you find:

- Incorrect documentation
- New broken endpoints
- Better usage patterns

Update the relevant document and note the discovery date.

---

## 📚 Topic-Specific Guides

For detailed guidance on specific topics:

- **[getting-started.md](./getting-started.md)** - Setup, authentication, first API calls
- **[token-efficiency.md](./token-efficiency.md)** - Optimize API usage, reduce token consumption
- **[projects-and-organizations.md](./projects-and-organizations.md)** - User context, projects, organizations
- **[connectors.md](./connectors.md)** - Data source management
- **[pipelines.md](./pipelines.md)** - Pipeline operations and monitoring
- **[automations.md](./automations.md)** - Scheduling, cron expressions, automation triggers
- **[error-handling.md](./error-handling.md)** - Troubleshooting errors and null responses
- **[security.md](./security.md)** - JWT token security and credential management
- **[programmatic-usage.md](./programmatic-usage.md)** - Using API client in your code

---

## 🛠️ Related Files

- `../scripts/api-call.ts` - Main API client script
- `../.token` - JWT token file (git-ignored)
- `../SKILL.md` - Full skill documentation

---

**Last Updated:** 2025-11-17
**Status:** ✅ Active and maintained
**Endpoints Tested:** 15+
**Topic Guides:** 9
**Coverage:** Core functionality across all modules
