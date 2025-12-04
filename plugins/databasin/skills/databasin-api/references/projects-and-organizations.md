# Projects and Organizations Guide

**Working with user context, projects, and organizations**

---

## Overview

The proper way to get user context in Databasin is through these two primary endpoints:

1. **`/api/my/organizations`** - All organizations the current user belongs to
2. **`/api/my/projects`** - All projects the current user has access to

These endpoints provide complete user context including roles, permissions, and associations.

---

## Get User's Organizations

### Basic Usage

```bash
# Get count of organizations
bun run scripts/api-call.ts GET /api/my/organizations --count

# Get all organizations
bun run scripts/api-call.ts GET /api/my/organizations

# Get summary view
bun run scripts/api-call.ts GET /api/my/organizations --summary
```

---

### Response Fields

Organizations return these key fields:

- **`id`** - Organization ID
- **`name`** - Organization name
- **`shortName`** - Short name/code
- **`enabled`** - Whether organization is active (1 = yes, 0 = no)
- **`deleted`** - Deletion status (1 = deleted, 0 = active)
- **`createdAt`** - Creation timestamp
- **`updatedAt`** - Last update timestamp

---

### Example Response

```json
[
	{
		"id": 1,
		"name": "Acme Corporation",
		"shortName": "ACME",
		"enabled": 1,
		"deleted": 0,
		"createdAt": "2024-01-15T10:30:00Z",
		"updatedAt": "2024-11-01T14:22:00Z"
	}
]
```

---

## Get User's Projects

### Basic Usage

```bash
# Get count of projects
bun run scripts/api-call.ts GET /api/my/projects --count

# Get all projects
bun run scripts/api-call.ts GET /api/my/projects

# Get summary view
bun run scripts/api-call.ts GET /api/my/projects --summary

# Get just essential fields
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalId,institutionId
```

---

### Response Fields

Projects return these key fields:

- **`id`** - Project ID
- **`name`** - Project name
- **`description`** - Project description
- **`institutionId`** - Organization ID (links to organization)
- **`administratorId`** - User ID of project admin
- **`internalId`** - Internal ID used for connector/pipeline associations
- **`enabled`** - Whether project is active
- **`deleted`** - Deletion status
- **`isVisible`** - Visibility setting
- **`canRequestAccess`** - Whether users can request access

---

### Example Response

```json
[
	{
		"id": 42,
		"name": "Sales Analytics",
		"description": "Sales data integration and reporting",
		"institutionId": 1,
		"administratorId": 5,
		"internalId": "N1r8Do",
		"enabled": 1,
		"deleted": 0,
		"isVisible": 1,
		"canRequestAccess": 1,
		"createdAt": "2024-03-10T09:15:00Z",
		"updatedAt": "2024-11-15T16:45:00Z"
	}
]
```

---

### Determining User Role

**Check if you're the project administrator:**

```bash
# Get your user ID from account endpoint
bun run scripts/api-call.ts GET /api/my/account --fields=id

# Get project details
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,administratorId

# If administratorId matches your user ID, you're the admin
```

---

## Understanding internalId

The **`internalId`** field is crucial - it links projects to connectors, pipelines, and other resources.

**Usage:**

```bash
# Get connectors for a project
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do"

# Get pipelines for a project
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do"

# Get automations for a project
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do"
```

---

## Complete User Context Workflow

### Step 1: Get Organizations

```bash
bun run scripts/api-call.ts GET /api/my/organizations
```

This tells you:

- Which organizations you belong to
- Organization IDs for filtering

---

### Step 2: Get Projects

```bash
bun run scripts/api-call.ts GET /api/my/projects
```

This tells you:

- All projects you can access
- Which organization each project belongs to (via `institutionId`)
- Your role (via `administratorId`)
- Project internal IDs for resource queries

---

### Step 3: Get Project Resources

```bash
# Extract internalId from project (e.g., "N1r8Do")
# Then query resources for that project

# Connectors
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --count

# Pipelines
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do" --count

# Automations
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --count
```

---

## Helper Script: get-user-context.ts

Use the helper script to fetch and cache your context:

```bash
# Fetch and cache user context
bun run scripts/get-user-context.ts

# Force refresh cached data
bun run scripts/get-user-context.ts --refresh
```

This script caches results to avoid repeated API calls.

---

## Common Scenarios

### Scenario 1: List All My Projects

```bash
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,description
```

---

### Scenario 2: Find Projects in Specific Organization

```bash
# Get all projects
bun run scripts/api-call.ts GET /api/my/projects

# Filter by institutionId (client-side)
# Or use jq if available:
bun run scripts/api-call.ts GET /api/my/projects | jq '.[] | select(.institutionId == 1)'
```

---

### Scenario 3: Get Complete Context for One Project

```bash
# Get project details
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalId,institutionId

# Extract internalId (e.g., "N1r8Do")
INTERNAL_ID="N1r8Do"

# Get connectors
bun run scripts/api-call.ts GET "/api/connector?internalID=$INTERNAL_ID" --summary

# Get pipelines
bun run scripts/api-call.ts GET "/api/pipeline?internalID=$INTERNAL_ID" --summary

# Get automations
bun run scripts/api-call.ts GET "/api/automations?internalID=$INTERNAL_ID" --count
```

---

### Scenario 4: Check Admin Status

```bash
# Get your user ID
MY_ID=$(bun run scripts/api-call.ts GET /api/my/account --fields=id | jq -r '.id')

# Get projects where you're admin
bun run scripts/api-call.ts GET /api/my/projects | jq --arg id "$MY_ID" '.[] | select(.administratorId == ($id | tonumber))'
```

---

## Deprecated Endpoints

### ⚠️ DO NOT USE: /api/projects?orgId={orgID}

**Problem:** Has backend serialization bug with LocalDateTime fields

**Solution:** Use `/api/my/projects` instead and filter client-side

```bash
# ❌ DON'T USE
bun run scripts/api-call.ts GET "/api/projects?orgId=1"

# ✅ USE THIS INSTEAD
bun run scripts/api-call.ts GET /api/my/projects
# Then filter by institutionId client-side
```

See **[deprecated-endpoints.md](./deprecated-endpoints.md)** for details.

---

## Token Efficiency Tips

### For Small Number of Projects (<20)

```bash
# Fetch all - token usage is reasonable
bun run scripts/api-call.ts GET /api/my/projects
```

---

### For Large Number of Projects (>20)

```bash
# Count first
bun run scripts/api-call.ts GET /api/my/projects --count

# Get summary
bun run scripts/api-call.ts GET /api/my/projects --summary

# Fetch specific fields only
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalId
```

---

### For Organizations

```bash
# Usually <10 organizations, safe to fetch all
bun run scripts/api-call.ts GET /api/my/organizations
```

---

## Related Endpoints

### User Account

```bash
# Get current user details
bun run scripts/api-call.ts GET /api/my/account --fields=id,firstName,lastName,email
```

---

### Accessible Connections

```bash
# Get connections accessible to current user
bun run scripts/api-call.ts GET /api/connections/accessible
```

---

### User Notifications

```bash
# Get notifications for current user
bun run scripts/api-call.ts GET /api/notifications
```

---

### User Metrics

```bash
# All accessible metrics
bun run scripts/api-call.ts GET /api/metrics

# Only metrics owned by user
bun run scripts/api-call.ts GET /api/metrics/owned
```

---

### Data Exchanges

```bash
# Get data exchanges accessible by current user
bun run scripts/api-call.ts GET /api/exchanges
```

---

## See Also

- **[getting-started.md](./getting-started.md)** - Quick start guide
- **[connectors.md](./connectors.md)** - Working with connectors
- **[pipelines.md](./pipelines.md)** - Working with pipelines
- **[working-endpoints.md](./working-endpoints.md)** - Complete endpoint reference
- **[token-efficiency.md](./token-efficiency.md)** - Optimize API usage

---

**Last Updated:** 2025-11-17
