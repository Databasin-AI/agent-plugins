# Databasin Connector Configuration Examples

Real-world connector configuration examples for different use cases.

## MySQL Database Connector

### Basic MySQL Connection

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

### MySQL with Connection Pooling

```json
{
	"connectorName": "High Volume MySQL",
	"connectorType": "RDBMS",
	"connectorHost": "mysql-pool.example.com",
	"connectorPort": "3306",
	"connectorDatabaseName": "sales",
	"connectorUsername": "etl_user",
	"connectorPassword": "etl_password",
	"connectorAuthType": 2,
	"connectorMaxConnections": 16,
	"connectorAdditionalDetails": "connectTimeout=30000&queryTimeout=60000",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## PostgreSQL Database Connector

### Standard PostgreSQL

```json
{
	"connectorName": "PostgreSQL Analytics",
	"connectorType": "RDBMS",
	"connectorHost": "postgres.example.com",
	"connectorPort": "5432",
	"connectorDatabaseName": "warehouse",
	"connectorUsername": "databasin_ro",
	"connectorPassword": "readonly_password",
	"connectorAuthType": 2,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

### PostgreSQL on AWS RDS

```json
{
	"connectorName": "RDS PostgreSQL",
	"connectorType": "RDBMS",
	"connectorHost": "mydb.c9akciq32.us-east-1.rds.amazonaws.com",
	"connectorPort": "5432",
	"connectorDatabaseName": "production",
	"connectorUsername": "admin",
	"connectorPassword": "rds_password",
	"connectorAuthType": 2,
	"connectorAdditionalDetails": "ssl=true&sslmode=require",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## Microsoft SQL Server Connector

### SQL Server with Windows Auth

```json
{
	"connectorName": "SQL Server Production",
	"connectorType": "RDBMS",
	"connectorHost": "sqlserver.corp.local",
	"connectorPort": "1433",
	"connectorDatabaseName": "SalesDB",
	"connectorUsername": "DOMAIN\\serviceaccount",
	"connectorPassword": "service_password",
	"connectorAuthType": 2,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

### Azure SQL Database

```json
{
	"connectorName": "Azure SQL DB",
	"connectorType": "RDBMS",
	"connectorHost": "myserver.database.windows.net",
	"connectorPort": "1433",
	"connectorDatabaseName": "CustomerData",
	"connectorUsername": "azureuser@myserver",
	"connectorPassword": "azure_password",
	"connectorAuthType": 10,
	"connectorAdditionalDetails": "encrypt=true&trustServerCertificate=false",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## Amazon S3 Connector

### S3 with Access Keys

```json
{
	"connectorName": "S3 Data Lake",
	"connectorType": "File & API",
	"connectorStorageAccountName": "my-data-lake-bucket",
	"fileFolderName": "/raw-data/sales/",
	"connectorUsername": "AKIAIOSFODNN7EXAMPLE",
	"connectorPassword": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
	"connectorAuthType": 7,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

### S3 with Regional Configuration

```json
{
	"connectorName": "S3 West Region",
	"connectorType": "File & API",
	"connectorStorageAccountName": "west-region-data",
	"fileFolderName": "/incoming/",
	"connectorUsername": "AKIAIOSFODNN7EXAMPLE",
	"connectorPassword": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
	"connectorAuthType": 7,
	"connectorAdditionalDetails": "region=us-west-2&serverSideEncryption=true",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## Azure Data Lake Storage (ADLS) Connector

### ADLS with Access Key

```json
{
	"connectorName": "ADLS Gen2 Production",
	"connectorType": "File & API",
	"connectorStorageAccountName": "mycompanydatalake",
	"connectorContainerName": "raw-data",
	"fileFolderName": "/ingestion/",
	"connectorPassword": "azure_access_key_base64==",
	"connectorAuthType": 3,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

### ADLS with Service Principal

```json
{
	"connectorName": "ADLS with Service Principal",
	"connectorType": "File & API",
	"connectorStorageAccountName": "productionstorage",
	"connectorContainerName": "datawarehouse",
	"fileFolderName": "/",
	"connectorUsername": "12345678-1234-1234-1234-123456789abc",
	"connectorPassword": "client-secret-value",
	"connectorAuthType": 5,
	"connectorAdditionalDetails": "tenant-id-guid",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

### ADLS with SAS Token

```json
{
	"connectorName": "ADLS SAS Token",
	"connectorType": "File & API",
	"connectorStorageAccountName": "tempstorage",
	"connectorContainerName": "exports",
	"fileFolderName": "/monthly/",
	"connectorPassword": "?sv=2021-06-08&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2025-12-31T23:59:59Z&st=2025-01-01T00:00:00Z&spr=https&sig=signature_here",
	"connectorAuthType": 4,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## SFTP Connector

### SFTP with Password

```json
{
	"connectorName": "SFTP File Server",
	"connectorType": "File & API",
	"connectorHost": "sftp.example.com",
	"connectorPort": "22",
	"fileFolderName": "/data/exports/",
	"connectorUsername": "sftpuser",
	"connectorPassword": "sftp_password",
	"connectorAuthType": 12,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

### SFTP with Key File

```json
{
	"connectorName": "SFTP with SSH Key",
	"connectorType": "File & API",
	"connectorHost": "secure-sftp.example.com",
	"connectorPort": "22",
	"fileFolderName": "/incoming/",
	"sftpKeyFileLocation": "/path/to/keyfile/id_rsa",
	"connectorUsername": "keyuser",
	"connectorAuthType": 12,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## Snowflake Connector

### Snowflake Data Warehouse

```json
{
	"connectorName": "Snowflake Production",
	"connectorType": "RDBMS",
	"connectorHost": "mycompany.snowflakecomputing.com",
	"connectorDatabaseName": "ANALYTICS_DB",
	"warehouse": "COMPUTE_WH",
	"connectorUsername": "DATABASIN_USER",
	"connectorPassword": "snowflake_password",
	"connectorAuthType": 2,
	"connectorAdditionalDetails": "schema=PUBLIC&role=DATABASIN_ROLE",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## Databricks Connector

### Databricks SQL Warehouse

```json
{
	"connectorName": "Databricks Analytics",
	"connectorType": "Big Data & NoSQL",
	"connectorHost": "adb-1234567890123456.7.azuredatabricks.net",
	"httpPath": "/sql/1.0/warehouses/abc123def456",
	"connectorCatalogName": "main",
	"connectorUsername": "token",
	"connectorPassword": "dapi1234567890abcdef1234567890ab",
	"connectorAuthType": 6,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

### Databricks with External Storage

```json
{
	"connectorName": "Databricks with Unity Catalog",
	"connectorType": "Big Data & NoSQL",
	"connectorHost": "adb-1234567890123456.7.azuredatabricks.net",
	"httpPath": "/sql/1.0/warehouses/abc123def456",
	"connectorCatalogName": "unity_catalog",
	"storageCredentialsConnectorID": 789,
	"storageCredentialsExternalTables": true,
	"connectorUsername": "token",
	"connectorPassword": "dapi1234567890abcdef1234567890ab",
	"connectorAuthType": 6,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## Salesforce Connector

### Salesforce Production

```json
{
	"connectorName": "Salesforce CRM",
	"connectorType": "CRM & ERP",
	"connectorHost": "https://login.salesforce.com",
	"connectorUsername": "api.user@company.com",
	"connectorPassword": "salesforce_password",
	"securityToken": "ABC123DEF456GHI789",
	"connectorAuthType": 2,
	"connectorAdditionalDetails": "v=62.0",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

### Salesforce Sandbox

```json
{
	"connectorName": "Salesforce Sandbox",
	"connectorType": "CRM & ERP",
	"connectorHost": "https://test.salesforce.com",
	"connectorUsername": "test.user@company.com.sandbox",
	"connectorPassword": "test_password",
	"securityToken": "SANDBOX_TOKEN_123",
	"connectorAuthType": 2,
	"institutionID": 1,
	"internalID": "proj-dev",
	"ownerID": 456
}
```

---

## Microsoft Dataverse Connector

### Dataverse with Service Principal

```json
{
	"connectorName": "Dynamics Dataverse",
	"connectorType": "File & API",
	"connectorHost": "https://org.crm.dynamics.com",
	"connectorUsername": "app-client-id-guid",
	"connectorPassword": "client-secret-value",
	"connectorAdditionalDetails": "tenant-id-guid",
	"connectorAuthType": 14,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## MongoDB Connector

### MongoDB Atlas

```json
{
	"connectorName": "MongoDB Atlas Cluster",
	"connectorType": "Big Data & NoSQL",
	"connectorHost": "cluster0.abc123.mongodb.net",
	"connectorPort": "27017",
	"connectorDatabaseName": "production",
	"connectorUsername": "databasin_user",
	"connectorPassword": "mongo_password",
	"connectorAuthType": 2,
	"connectorAdditionalDetails": "authSource=admin&ssl=true",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

### MongoDB with Authentication Database

```json
{
	"connectorName": "MongoDB with Auth DB",
	"connectorType": "Big Data & NoSQL",
	"connectorHost": "mongodb.example.com",
	"connectorPort": "27017",
	"connectorDatabaseName": "analytics",
	"connectorUsername": "admin_user",
	"connectorPassword": "admin_password",
	"connectorAuthType": 2,
	"connectorAdditionalDetails": "authenticationDatabase=admin",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## Generic API Connector

### REST API with Bearer Token

```json
{
	"connectorName": "Custom REST API",
	"connectorType": "File & API",
	"connectorHost": "https://api.example.com/v1",
	"connectorPassword": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
	"connectorAuthType": 20,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

### API with API Key Header

```json
{
	"connectorName": "Third-Party API",
	"connectorType": "File & API",
	"connectorHost": "https://data.thirdparty.com/api",
	"connectorPassword": "api-key-1234567890abcdef",
	"connectorAuthType": 8,
	"connectorAdditionalDetails": "headerName=X-API-Key",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

### Public API (No Auth)

```json
{
	"connectorName": "Public Data API",
	"connectorType": "File & API",
	"connectorHost": "https://api.publicdata.gov/v1",
	"connectorAuthType": 22,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## Box Connector (OAuth)

### Box with OAuth

```json
{
	"connectorName": "Box Cloud Storage",
	"connectorType": "File & API",
	"fileFolderName": "https://app.box.com/folder/123456789",
	"connectorPassword": "oauth_token_from_auth_flow",
	"connectorAuthType": 1,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

**Note:** OAuth token obtained through browser authentication flow using `oAuthURL` from connector configuration.

---

## Google Drive Connector

### Google Drive with OAuth

```json
{
	"connectorName": "Google Drive Files",
	"connectorType": "File & API",
	"fileFolderName": "/My Drive/Data Exports",
	"connectorPassword": "google_oauth_token",
	"connectorAuthType": 1,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## Sharepoint Connector

### Sharepoint Online

```json
{
	"connectorName": "Sharepoint Document Library",
	"connectorType": "File & API",
	"connectorHost": "https://company.sharepoint.com/sites/DataTeam",
	"connectorDatabaseName": "Shared Documents",
	"fileFolderName": "/Reports/Monthly/",
	"connectorPassword": "oauth_token_from_auth_flow",
	"connectorAuthType": 1,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## SMB File Share Connector

### Windows File Share

```json
{
	"connectorName": "Network File Share",
	"connectorType": "File & API",
	"connectorHost": "fileserver.corp.local",
	"connectorDatabaseName": "DataShare",
	"fileFolderName": "/Exports/Daily/",
	"connectorUsername": "DOMAIN\\serviceaccount",
	"connectorPassword": "share_password",
	"connectorAuthType": 2,
	"connectorAdditionalDetails": "domain=CORP",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## Azure OpenAI Connector

### Azure OpenAI Service

```json
{
	"connectorName": "Azure OpenAI GPT-4",
	"connectorType": "AI & LLM",
	"connectorHost": "https://mycompany.openai.azure.com/",
	"connectorDatabaseName": "gpt-4-deployment",
	"connectorPassword": "azure_openai_api_key",
	"connectorAdditionalDetails": "2024-02-15-preview",
	"connectorAuthType": 8,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

---

## Usage Patterns

### Minimal Configuration

Use only required fields for the connector type:

```json
{
	"connectorName": "Simple MySQL",
	"connectorType": "RDBMS",
	"connectorHost": "mysql.local",
	"connectorPort": "3306",
	"connectorDatabaseName": "test",
	"connectorUsername": "user",
	"connectorPassword": "pass",
	"connectorAuthType": 2,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

### Full Configuration

Include optional fields for advanced scenarios:

```json
{
	"connectorName": "Advanced MySQL",
	"connectorType": "RDBMS",
	"connectorHost": "mysql-primary.cluster.local",
	"connectorPort": "3306",
	"connectorDatabaseName": "production",
	"connectorUsername": "etl_user",
	"connectorPassword": "complex_password",
	"connectorAuthType": 2,
	"connectorMaxConnections": 20,
	"connectorAdditionalDetails": "useSSL=true&requireSSL=true&connectTimeout=30000&socketTimeout=60000&useCompression=true",
	"institutionID": 1,
	"internalID": "proj-prod",
	"ownerID": 456
}
```
