# Databasin Connector Fields Reference

Complete reference of all connector configuration fields.

## Required Fields (connectorRequiredFields)

Fields that must be provided when creating a connector of a specific type.

| reqID | Field Name                    | API Name                        | Type   | Description                                                 |
| ----- | ----------------------------- | ------------------------------- | ------ | ----------------------------------------------------------- |
| 1     | Name                          | `connectorName`                 | String | Unique name for the connector                               |
| 2     | Host                          | `connectorHost`                 | String | Full URL of the server                                      |
| 3     | Port                          | `connectorPort`                 | String | Port number the server is running on                        |
| 4     | Database Name                 | `connectorDatabaseName`         | String | Database name to connect to                                 |
| 5     | ADLS Storage Account Name     | `connectorStorageAccountName`   | String | Azure storage account name                                  |
| 6     | ADLS Container Name           | `connectorContainerName`        | String | Azure container name within storage account                 |
| 7     | Remote Folder Path            | `fileFolderName`                | String | Full path (URL) of folder containing files                  |
| 8     | SFTP Home Directory           | `fileFolderName`                | String | Folder containing needed files                              |
| 9     | SFTP Key File Location        | `sftpKeyFileLocation`           | String | Folder location containing SFTP key file                    |
| 10    | S3 Bucket Name                | `connectorStorageAccountName`   | String | Name of S3 storage bucket                                   |
| 11    | Redcap Report ID              | `connectorUsername`             | String | ID of the Report from Redcap                                |
| 12    | Redcap URL                    | `connectorHost`                 | String | The Redcap URL                                              |
| 13    | Account Endpoint              | `connectorHost`                 | String | Cosmos Account Endpoint URL                                 |
| 14    | Account ID                    | `connectorHost`                 | String | The Account ID                                              |
| 15    | External Storage Connector ID | `storageCredentialsConnectorID` | Int    | Connector ID configured in Databricks as External Connector |
| 16    | HTTP Path                     | `httpPath`                      | String | HTTP Path from Databricks SQL Warehouse                     |
| 17    | Box Folder URL                | `fileFolderName`                | String | Full URL of parent box folder                               |
| 18    | Warehouse Name                | `warehouse`                     | String | Full name of Snowflake Warehouse                            |
| 19    | Share Name                    | `connectorDatabaseName`         | String | Name of SMB share to connect to                             |
| 20    | File Path                     | `connectorDatabaseName`         | String | Path to the file                                            |
| 21    | Base Name                     | `connectorDatabaseName`         | String | Schema name (Base name in Airtable)                         |
| 22    | Sharepoint Site URL           | `connectorHost`                 | String | Full URL to Sharepoint site                                 |
| 23    | Sharepoint Library Name       | `connectorDatabaseName`         | String | Name of library containing files                            |
| 24    | Azure Tenant ID               | `connectorAdditionalDetails`    | String | ID of Azure Tenant connecting to                            |
| 25    | URL                           | `connectorHost`                 | String | URL of server connecting to                                 |
| 26    | Organization URL              | `connectorHost`                 | String | URL of server connecting to                                 |
| 27    | Catalog Name                  | `connectorCatalogName`          | String | Default catalog name (default: hive_metastore)              |
| 28    | Stage Database Name           | `connectorCatalogName`          | String | Existing database for staging data                          |
| 29    | Login URL                     | `connectorHost`                 | String | Full URL of Salesforce server                               |
| 30    | Security Token                | `securityToken`                 | String | Salesforce security token                                   |
| 31    | Base URL                      | `connectorHost`                 | String | Base URL of web API endpoint                                |
| 32    | Tenant                        | `connectorAdditionalDetails`    | String | Tenant name associated with organization                    |
| 33    | Shop URL                      | `connectorHost`                 | String | Full URL of Shopify shop                                    |
| 34    | Company Domain URL            | `connectorHost`                 | String | Company domain for Pipedrive account                        |
| 35    | Owner Login                   | `connectorUsername`             | String | Username for individual/organization account                |
| 36    | Livy Session Job Endpoint     | `connectorHost`                 | String | Session Job connection string from Azure Fabric             |
| 37    | Fabric Lakehouse Name         | `connectorDatabaseName`         | String | Name of Fabric Data Lakehouse                               |
| 38    | Fabric Environment ID         | `warehouse`                     | String | ID of environment for Livy batch jobs                       |
| 39    | External Storage Connector    | `storageCredentialsConnectorID` | ADLS   | Connector for ADLS storage location                         |
| 40    | Authentication Database Name  | `connectorAdditionalDetails`    | String | MongoDB database for authentication                         |
| 41    | CompanyID                     | `connectorDatabaseName`         | String | Unique identifier of company for authentication             |
| 42    | Connection Type               | `connectorDatabaseName`         | Enum   | Method to connect to Workday (SOAP/Reports)                 |
| 43    | Azure OpenAI Endpoint         | `connectorHost`                 | String | Azure OpenAI service endpoint URL                           |
| 44    | API Version                   | `connectorAdditionalDetails`    | String | API version to use (e.g., 2024-02-15-preview)               |
| 45    | Deployment Name               | `connectorDatabaseName`         | String | Name of deployed model in Azure OpenAI                      |

---

## Optional Fields (connectorOptionalFields)

Fields that can be optionally provided for additional configuration.

| optID | Field Name                       | API Name                           | Type     | Default | Description                                        |
| ----- | -------------------------------- | ---------------------------------- | -------- | ------- | -------------------------------------------------- |
| 1     | Additional Connection Parameters | `connectorAdditionalDetails`       | String   | -       | Additional properties (e.g., queryTimeout)         |
| 2     | Connector Max Connections        | `connectorMaxConnections`          | Int      | 8       | Maximum concurrent connections per pipeline        |
| 3     | Database Name                    | `connectorDatabaseName`            | String   | -       | Database name to connect to                        |
| 4     | Directory Name                   | `fileFolderName`                   | String   | -       | Folder name or hierarchy containing files          |
| 5     | Additional Box URL Filter        | `connectorAdditionalDetails`       | String   | -       | Additional Box URLs (comma-separated)              |
| 6     | Domain Name                      | `connectorAdditionalDetails`       | String   | -       | Optional domain name for connection                |
| 7     | Organization Name                | `connectorDatabaseName`            | String   | -       | Optional organization name                         |
| 8     | Edition                          | `connectorDatabaseName`            | Enum     | -       | Edition type (CustomerService, FieldService, etc.) |
| 9     | Create All Tables As External    | `storageCredentialsExternalTables` | Boolean  | false   | Create tables as external tables                   |
| 10    | External Storage Connector ID    | `storageCredentialsConnectorID`    | Int      | -       | Databricks External Connector ID                   |
| 11    | Access DB Username               | `connectorUsername`                | String   | -       | Optional database username                         |
| 12    | Access DB Password               | `securityToken`                    | Password | -       | Optional database password                         |
| 13    | API Version                      | `connectorAdditionalDetails`       | String   | -       | Salesforce API version override (default: 62.0)    |
| 14    | CompanyID                        | `connectorDatabaseName`            | String   | -       | Optional Company ID (uses first if not specified)  |
| 15    | Azure Tenant ID                  | `connectorAdditionalDetails`       | String   | -       | Azure Tenant ID (for multi-tenant users)           |
| 16    | External Storage Connector       | `storageCredentialsConnectorID`    | ADLS     | -       | Connector for ADLS storage location                |
| 17    | Databricks Account ID            | `connectorAdditionalDetails`       | String   | -       | Required for governance module                     |

---

## Common API Field Mappings

### Basic Connection Fields

- `connectorName` - Display name of the connector
- `connectorType` - Category type (RDBMS, File & API, etc.)
- `connectorHost` - Server hostname or URL
- `connectorPort` - Server port number
- `connectorDatabaseName` - Database/schema/bucket name

### Authentication Fields

- `connectorUsername` - Username for authentication
- `connectorPassword` - Password/token/secret
- `connectorAuthType` - Authentication method ID (see auth types)
- `securityToken` - Additional security token (Salesforce, etc.)

### Azure-Specific Fields

- `connectorStorageAccountName` - Azure storage account name
- `connectorContainerName` - Azure container name
- `connectorAdditionalDetails` - Tenant ID or other Azure details

### File/Storage Fields

- `fileFolderName` - Remote folder path or directory
- `sftpKeyFileLocation` - SSH key file location
- `storageCredentialsConnectorID` - External storage connector reference

### Advanced Configuration

- `connectorMaxConnections` - Connection pool size
- `connectorAdditionalDetails` - Miscellaneous configuration
- `httpPath` - HTTP path for SQL warehouses
- `warehouse` - Warehouse name for Snowflake/Databricks

### Organizational Fields

- `institutionID` - Organization/institution identifier
- `internalID` - Project identifier
- `ownerID` - User ID of connector owner

---

## Field Type Definitions

### String

Plain text value. Can be empty string unless marked as required.

### Int

Integer number. Must be valid integer value.

### Boolean

True/false value. Usually defaults to false if not specified.

### Enum

Must be one of specific allowed values. Check field definition for `allowedValues`.

**Example:** Connection Type (reqID 42)

- Allowed: `["SOAP", "Reports"]`

### Password

Sensitive string value. Will be encrypted in storage and never returned in API responses.

### ADLS

Special type referencing an Azure Data Lake Storage connector.

---

## Validation Rules

### Required Field Validation

- All fields with reqID in `connectorRequiredFields` array must be present
- Cannot be null or undefined
- String fields cannot be empty unless explicitly allowed

### Type Validation

- Strings must be valid UTF-8
- Integers must be valid numbers
- Ports must be 1-65535
- URLs must be valid format (http:// or https://)

### Length Limits

- Connector name: 3-255 characters
- Host/URL fields: max 2000 characters
- Username: max 255 characters
- Database names: max 255 characters

### Business Rules

- `connectorMaxConnections` should be 1-100 (warning if >100)
- Port numbers must be valid TCP ports
- URLs should use HTTPS when available
- Tenant IDs should match Azure GUID format

---

## Field Selection Strategy

When creating a connector:

1. **Identify connector type** from categories
2. **Check required fields** for that specific connector name
3. **Add authentication fields** based on auth type
4. **Consider optional fields** for advanced configuration
5. **Validate before submission** using validate_connector_config.ts

---

## Examples

### MySQL Connector (Minimal)

```json
{
	"connectorName": "Production MySQL",
	"connectorType": "RDBMS",
	"connectorHost": "mysql.example.com",
	"connectorPort": "3306",
	"connectorDatabaseName": "analytics",
	"connectorUsername": "databasin_user",
	"connectorPassword": "secure_password",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 123
}
```

### S3 Connector (With Optional Fields)

```json
{
	"connectorName": "S3 Data Lake",
	"connectorType": "File & API",
	"connectorStorageAccountName": "my-data-bucket",
	"connectorUsername": "AKIAIOSFODNN7EXAMPLE",
	"connectorPassword": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
	"fileFolderName": "/raw-data/",
	"connectorAdditionalDetails": "region=us-east-1",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 123
}
```

### Azure Data Lake (Service Principal Auth)

```json
{
	"connectorName": "ADLS Gen2 Production",
	"connectorType": "File & API",
	"connectorStorageAccountName": "mycompanystorage",
	"connectorContainerName": "data-warehouse",
	"fileFolderName": "/ingestion/",
	"connectorUsername": "app-client-id",
	"connectorPassword": "client-secret",
	"connectorAdditionalDetails": "tenant-id-guid",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 123
}
```
