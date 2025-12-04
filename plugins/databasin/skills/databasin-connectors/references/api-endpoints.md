# Databasin Connector API Endpoints

Quick reference for all connector-related API endpoints.

## Base URL

All endpoints are relative to the API base URL:

- **Local Development:** `http://localhost:9000`
- **Production:** Set via `PUBLIC_API_URI` environment variable

## Authentication

All API requests require JWT authentication via Bearer token:

```
Authorization: Bearer <jwt_token>
```

Store your JWT token in a `.token` file in the current working directory.

---

## Connector Endpoints

### List All Connectors

**GET** `/api/connector`

Retrieves all connectors, optionally filtered by organization and project.

**Query Parameters:**

- `institutionID` (optional) - Filter by organization ID
- `internalID` (optional) - Filter by project ID

**Response:**

```json
[
	{
		"connectorID": 123,
		"connectorName": "Production MySQL",
		"connectorType": "RDBMS",
		"connectorHost": "mysql.example.com",
		"connectorPort": "3306",
		"connectorDatabaseName": "analytics",
		"institutionID": 1,
		"internalID": "proj-001",
		"ownerID": 456,
		"active": true,
		"createdDate": "2025-01-15T10:30:00Z",
		"lastModifiedDate": "2025-01-20T14:45:00Z"
	}
]
```

**Note:** Fetching all connectors can return 434+ records consuming significant tokens. Always filter by project when possible.

**CLI Example:**

```bash
bun -e "
import { DatabasinAPIClient } from './scripts/api_client.ts';
const client = new DatabasinAPIClient();
const connectors = await client.listConnectors(1, 'proj-001');
console.log(JSON.stringify(connectors, null, 2));
"
```

---

### Get Single Connector

**GET** `/api/connector/{connectorID}`

Retrieves details for a specific connector.

**Path Parameters:**

- `connectorID` - Connector ID

**Response:**

```json
{
	"connectorID": 123,
	"connectorName": "Production MySQL",
	"connectorType": "RDBMS",
	"connectorHost": "mysql.example.com",
	"connectorPort": "3306",
	"connectorDatabaseName": "analytics",
	"connectorUsername": "databasin_user",
	"connectorAuthType": 2,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456,
	"active": true,
	"connectorMaxConnections": 8,
	"createdDate": "2025-01-15T10:30:00Z",
	"lastModifiedDate": "2025-01-20T14:45:00Z"
}
```

**Note:** Password/secret fields are never returned in responses for security.

**CLI Example:**

```bash
bun scripts/api_client.ts get-connector 123
```

---

### Create Connector

**POST** `/api/connector`

Creates a new connector.

**Request Body:**

```json
{
	"connectorName": "Production MySQL",
	"connectorType": "RDBMS",
	"connectorHost": "mysql.example.com",
	"connectorPort": "3306",
	"connectorDatabaseName": "analytics",
	"connectorUsername": "databasin_user",
	"connectorPassword": "secure_password",
	"connectorAuthType": 2,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

**Response:**

```json
{
	"connectorID": 789,
	"message": "Connector created successfully",
	"status": "success"
}
```

**CLI Example:**

```bash
bun create_connector.ts mysql_config.json
```

---

### Update Connector

**PUT** `/api/connector/{connectorID}`

Updates an existing connector's configuration.

**Path Parameters:**

- `connectorID` - Connector ID to update

**Request Body:**

```json
{
	"connectorName": "Production MySQL - Updated",
	"connectorPassword": "new_secure_password",
	"connectorMaxConnections": 16
}
```

**Note:** Only include fields you want to update. Other fields remain unchanged.

**Response:**

```json
{
	"connectorID": 123,
	"message": "Connector updated successfully",
	"status": "success"
}
```

**CLI Example:**

```bash
bun modify_connector.ts credentials 123 new_user new_password
bun modify_connector.ts name 123 "New Connector Name"
```

---

### Delete Connector

**DELETE** `/api/connector/{connectorID}`

Deletes a connector.

**Path Parameters:**

- `connectorID` - Connector ID to delete

**Response:**

```json
{
	"message": "Connector deleted successfully",
	"status": "success"
}
```

**Note:** This is a destructive operation. Any pipelines using this connector will fail.

**CLI Example:**

```bash
bun delete_connector.ts 123 --force
```

---

### Test Connector

**POST** `/api/connector/{connectorID}/test`

Tests a connector's connection.

**Path Parameters:**

- `connectorID` - Connector ID to test

**Request Body:**

```json
{}
```

**Response (Success):**

```json
{
	"success": true,
	"status": "success",
	"message": "Connection test successful",
	"details": {
		"connectorType": "RDBMS",
		"testDuration": "1.2s"
	}
}
```

**Response (Failure):**

```json
{
	"success": false,
	"status": "error",
	"message": "Connection failed: Access denied for user 'databasin_user'@'10.0.0.5'",
	"error": "Authentication failure"
}
```

**Note:** Not all connectors support testing. Check `testConnectorSupport` flag in connector configuration.

**CLI Example:**

```bash
bun test_connector.ts 123
bun test_connector.ts 456 --details
```

---

### Refresh Connector Metadata

**POST** `/api/connector/{connectorID}/refresh`

Refreshes cached metadata for a connector (catalogs, schemas, tables).

**Path Parameters:**

- `connectorID` - Connector ID

**Request Body:**

```json
{}
```

**Response:**

```json
{
  "message": "Metadata refresh initiated",
  "status": "success",
  "catalogCount": 5,
  "schemaCount": 42,
  "tableCount": 1,234
}
```

**Note:** Metadata refresh can take several seconds to minutes for large databases.

**CLI Example:**

```bash
curl -X POST \
  -H "Authorization: Bearer $(cat .token)" \
  http://localhost:9000/api/connector/123/refresh
```

---

## Related Endpoints

### Get Connector Catalogs

**GET** `/api/connector/{connectorID}/catalogs`

Returns list of catalogs (databases) for a connector.

**Response:**

```json
[
	{
		"catalogName": "analytics_prod",
		"description": "Production analytics database"
	},
	{
		"catalogName": "sales_data",
		"description": "Sales database"
	}
]
```

---

### Get Connector Schemas

**GET** `/api/connector/{connectorID}/schemas?catalog={catalogName}`

Returns list of schemas for a connector and catalog.

**Query Parameters:**

- `catalog` - Catalog name (required for some connectors)

**Response:**

```json
[
	{
		"schemaName": "public",
		"description": "Public schema"
	},
	{
		"schemaName": "reporting",
		"description": "Reporting schema"
	}
]
```

---

### Get Connector Tables

**GET** `/api/connector/{connectorID}/tables?catalog={catalogName}&schema={schemaName}`

Returns list of tables/artifacts for a connector.

**Query Parameters:**

- `catalog` - Catalog name (optional, depends on connector type)
- `schema` - Schema name (optional, depends on connector type)

**Response:**

```json
[
	{
		"tableName": "customers",
		"tableType": "TABLE",
		"rowCount": 125000,
		"sizeInBytes": 52428800
	},
	{
		"tableName": "orders",
		"tableType": "TABLE",
		"rowCount": 456789,
		"sizeInBytes": 209715200
	}
]
```

---

### Get Connector Columns

**GET** `/api/connector/{connectorID}/columns?catalog={catalogName}&schema={schemaName}&table={tableName}`

Returns list of columns for a specific table.

**Query Parameters:**

- `catalog` - Catalog name (optional)
- `schema` - Schema name (optional)
- `table` - Table name (required)

**Response:**

```json
[
	{
		"columnName": "customer_id",
		"dataType": "INT",
		"isNullable": false,
		"isPrimaryKey": true
	},
	{
		"columnName": "email",
		"dataType": "VARCHAR(255)",
		"isNullable": false,
		"isPrimaryKey": false
	}
]
```

---

## Error Responses

All endpoints may return standard HTTP error responses:

### 400 Bad Request

```json
{
	"error": "Bad Request",
	"message": "Missing required field: connectorName",
	"status": 400
}
```

### 401 Unauthorized

```json
{
	"error": "Unauthorized",
	"message": "Invalid or expired authentication token",
	"status": 401
}
```

### 404 Not Found

```json
{
	"error": "Not Found",
	"message": "Connector with ID 999 not found",
	"status": 404
}
```

### 500 Internal Server Error

```json
{
	"error": "Internal Server Error",
	"message": "An unexpected error occurred",
	"status": 500
}
```

---

## Rate Limiting

API requests may be rate limited. Check response headers:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

If rate limited, you'll receive a 429 Too Many Requests response.

---

## Best Practices

### Token Efficiency

- Filter by `institutionID` and `internalID` when listing connectors
- Avoid fetching all connectors without filters
- Cache connector lists when possible

### Error Handling

- Always check for error responses before processing data
- Implement retry logic for 5xx errors
- Handle 401 errors by refreshing authentication token

### Testing

- Test connections after creation/modification
- Use connector test endpoint before creating pipelines
- Verify metadata refresh completed before querying catalogs/schemas

### Security

- Store JWT tokens securely (never in code)
- Rotate authentication tokens regularly
- Use HTTPS in production
- Never log sensitive fields (passwords, secrets)
