# Connectors Guide

**Working with Databasin data source connectors**

---

## Overview

Connectors represent data source connections in Databasin (databases, APIs, files, etc.). The system supports 50+ connector types with standardized configuration patterns.

**Base endpoint:** `/api/connector`

---

## List Connectors

### ⚠️ CRITICAL: Token Efficiency Warning

**Without filters, `/api/connector` returns 434+ connectors = 200,000+ tokens!**

**ALWAYS use token-efficient options:**

```bash
# Count first
bun run scripts/api-call.ts GET /api/connector --count

# Get summary
bun run scripts/api-call.ts GET /api/connector --summary

# Fetch specific fields with limit
bun run scripts/api-call.ts GET /api/connector --fields=connectorID,connectorName,connectorType --limit=20
```

---

### Get Connectors for Specific Project

```bash
# Count connectors in project
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --count

# Get summary
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --summary

# Get specific fields
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" \
  --fields=connectorID,connectorName,connectorType,connectorSubType
```

---

### Filter by Institution

```bash
# Get connectors for organization
bun run scripts/api-call.ts GET "/api/connector?institutionID=1" --count

# Combine filters
bun run scripts/api-call.ts GET "/api/connector?institutionID=1&internalID=N1r8Do" --summary
```

---

## Connector Fields

### Essential Fields

- **`connectorID`** - Unique connector ID
- **`connectorName`** - Display name
- **`connectorType`** - Connector category (database, api, file, etc.)
- **`connectorSubType`** - Specific type (postgres, mysql, salesforce, etc.)
- **`institutionID`** - Organization ID
- **`internalID`** - Project internal ID
- **`ownerID`** - User ID of connector owner
- **`isPrivate`** - Privacy setting (0 = shared, 1 = private)

---

### Connection Details

- **`connectorHost`** - Hostname or URL
- **`connectorPort`** - Port number
- **`connectorDatabase`** - Database name
- **`connectorSchema`** - Schema name
- **`connectorUsername`** - Username for authentication

**Note:** Passwords are not returned by API for security

---

### Status Fields

- **`isActive`** - Whether connector is active
- **`isDeleted`** - Deletion status
- **`createdAt`** - Creation timestamp
- **`updatedAt`** - Last update timestamp

---

## Get Specific Connector

```bash
# By connector ID
bun run scripts/api-call.ts GET /api/connector/58

# Get specific fields only
bun run scripts/api-call.ts GET /api/connector/58 --fields=connectorID,connectorName,connectorType,isActive
```

---

## Create Connector

### Basic Example

```bash
bun run scripts/api-call.ts POST /api/connector '{
  "connectorName": "Production DB",
  "connectorType": "database",
  "connectorSubType": "postgres",
  "connectorHost": "db.example.com",
  "connectorPort": "5432",
  "connectorDatabase": "production",
  "connectorUsername": "dbuser",
  "connectorPassword": "secure-password",
  "institutionID": 1,
  "internalID": "N1r8Do",
  "ownerID": 5,
  "isPrivate": 0
}'
```

---

### Required Fields

When creating a connector, these fields are typically required:

- **`connectorName`** - Must be unique within project
- **`connectorType`** - Valid type (database, api, file, etc.)
- **`connectorSubType`** - Specific connector type
- **`institutionID`** - Organization ID
- **`internalID`** - Project internal ID
- **`ownerID`** - Your user ID

**Connection-specific fields vary by connector type.**

---

## Update Connector

```bash
bun run scripts/api-call.ts PUT /api/connector '{
  "connectorID": 58,
  "connectorName": "Updated Name",
  "isActive": 1
}'
```

**Note:** Include connectorID and any fields to update

---

## Delete Connector

```bash
bun run scripts/api-call.ts DELETE /api/connector '{"connectorID": 58}'
```

**Warning:** This soft-deletes the connector (sets isDeleted=1)

---

## Common Connector Types

### Database Connectors

- **postgres** - PostgreSQL
- **mysql** - MySQL/MariaDB
- **sqlserver** - Microsoft SQL Server
- **oracle** - Oracle Database
- **snowflake** - Snowflake
- **redshift** - Amazon Redshift
- **bigquery** - Google BigQuery

---

### API Connectors

- **salesforce** - Salesforce CRM
- **hubspot** - HubSpot
- **stripe** - Stripe payments
- **shopify** - Shopify e-commerce
- **rest** - Generic REST API
- **graphql** - GraphQL API

---

### File Connectors

- **s3** - Amazon S3
- **azure-blob** - Azure Blob Storage
- **gcs** - Google Cloud Storage
- **ftp** - FTP/SFTP
- **local** - Local filesystem

---

## Common Scenarios

### Scenario 1: List Connectors in a Project

```bash
# Get internalId from projects endpoint
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalId

# Count connectors in project
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --count

# Get connector details
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" \
  --fields=connectorID,connectorName,connectorType,connectorSubType
```

---

### Scenario 2: Find Specific Connector Type

```bash
# Get all Salesforce connectors
bun run scripts/api-call.ts GET /api/connector \
  --fields=connectorID,connectorName,connectorSubType \
  | grep -i salesforce

# Or filter client-side with jq
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" | \
  jq '.[] | select(.connectorSubType == "salesforce")'
```

---

### Scenario 3: Create Database Connector

```bash
# Get your project's internalId and institutionId
bun run scripts/api-call.ts GET /api/my/projects --fields=id,internalId,institutionId

# Get your user ID
bun run scripts/api-call.ts GET /api/my/account --fields=id

# Create connector
bun run scripts/api-call.ts POST /api/connector '{
  "connectorName": "Analytics DB",
  "connectorType": "database",
  "connectorSubType": "postgres",
  "connectorHost": "analytics.db.local",
  "connectorPort": "5432",
  "connectorDatabase": "analytics",
  "connectorUsername": "readonly",
  "connectorPassword": "password123",
  "institutionID": 1,
  "internalID": "N1r8Do",
  "ownerID": 5,
  "isPrivate": 0
}'
```

---

### Scenario 4: Update Connector Status

```bash
# Deactivate connector
bun run scripts/api-call.ts PUT /api/connector '{
  "connectorID": 58,
  "isActive": 0
}'

# Reactivate connector
bun run scripts/api-call.ts PUT /api/connector '{
  "connectorID": 58,
  "isActive": 1
}'
```

---

### Scenario 5: Get Connector Configuration

```bash
# Get full connector details
bun run scripts/api-call.ts GET /api/connector/58

# Get just connection info
bun run scripts/api-call.ts GET /api/connector/58 \
  --fields=connectorHost,connectorPort,connectorDatabase,connectorUsername
```

---

## Token Efficiency Examples

### Inefficient (200,000+ tokens)

```bash
# ❌ Returns ALL connectors
bun run scripts/api-call.ts GET /api/connector
```

---

### Efficient (<100 tokens)

```bash
# ✅ Count only
bun run scripts/api-call.ts GET /api/connector --count
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --count
```

---

### Efficient (~2,000 tokens)

```bash
# ✅ Summary view
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --summary
```

---

### Efficient (~500-1,000 tokens)

```bash
# ✅ Specific fields with limit
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" \
  --fields=connectorID,connectorName,connectorType \
  --limit=25
```

---

## Related Endpoints

### Connector Config

```bash
# Get connector configuration metadata
bun run scripts/api-call.ts GET /api/config
```

**Warning:** Large response (~50,000 tokens), use `--fields` or `--count`

---

### Connector Testing

```bash
# Test connector connection (if endpoint exists)
bun run scripts/api-call.ts POST /api/connector/test '{
  "connectorID": 58
}'
```

---

## Troubleshooting

### Problem: Getting null response

**Solution:** Connector endpoint requires `internalID` or `institutionID` filter

```bash
# ❌ May return incomplete data
bun run scripts/api-call.ts GET /api/connector

# ✅ Use project filter
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do"
```

---

### Problem: Too many tokens

**Solution:** Use token-efficient options

```bash
# Count first
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --count

# Then fetch with fields/limit
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" \
  --fields=connectorID,connectorName --limit=50
```

---

### Problem: Can't find connector type

**Solution:** Check available connector types in config

```bash
# Get connector type definitions
bun run scripts/api-call.ts GET /api/config \
  --fields=connectorTypes
```

---

## See Also

- **[projects-and-organizations.md](./projects-and-organizations.md)** - Get project internalId
- **[pipelines.md](./pipelines.md)** - Using connectors in pipelines
- **[token-efficiency.md](./token-efficiency.md)** - Optimize API usage
- **[working-endpoints.md](./working-endpoints.md)** - Complete endpoint reference

---

**Last Updated:** 2025-11-17
