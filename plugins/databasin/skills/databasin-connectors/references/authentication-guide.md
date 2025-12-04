# Databasin Connector Authentication Guide

Complete guide to connector authentication types and how to configure them.

## Overview

Databasin supports 22 different authentication methods across various connector types. Each connector specifies which authentication types it supports via the `connectorAuthTypes` array.

---

## Authentication Types

### 1. OAuth (authID: 1)

**Description:** Sign in to your account for access (browser-based flow)

**Connectors:** Box, Dropbox, Google Drive, Google Cloud Storage, OneDrive, Sharepoint, and many SaaS platforms

**API Fields:**

- `connectorPassword` - Stores the OAuth token after authentication

**Flow:**

1. User initiates OAuth flow via `oAuthURL` from connector configuration
2. User authenticates in browser
3. Access token returned and stored in `connectorPassword`
4. Refresh token managed automatically by Databasin

**Example Configuration:**

```json
{
	"connectorName": "Box Production",
	"connectorAuthType": 1,
	"connectorPassword": "oauth_token_here"
}
```

**Notes:**

- Some connectors provide `oAuthURL` in configuration
- Token refresh handled automatically
- May support global OAuth (organization-wide) if `globalOAuthSupport: true`

---

### 2. Basic (authID: 2)

**Description:** Use a username and password for access

**Connectors:** SMB, many database systems

**API Fields:**

- `connectorUsername` - Username for authentication
- `connectorPassword` - Password for authentication

**Example Configuration:**

```json
{
	"connectorName": "SMB File Share",
	"connectorAuthType": 2,
	"connectorUsername": "domain\\user",
	"connectorPassword": "secure_password"
}
```

---

### 3. Azure Access Key (authID: 3)

**Description:** Use an Azure storage key for access

**Connectors:** Azure Data Lake Storage (ADLS), Azure Databricks Volumes

**API Fields:**

- `connectorPassword` - Azure storage access key

**Example Configuration:**

```json
{
	"connectorName": "ADLS Production",
	"connectorAuthType": 3,
	"connectorStorageAccountName": "mycompanystorage",
	"connectorPassword": "azure_access_key_here=="
}
```

**How to Get Azure Access Key:**

1. Navigate to Azure Portal → Storage Account
2. Select "Access keys" from left menu
3. Copy key1 or key2

---

### 4. Azure SAS Token (authID: 4)

**Description:** Use an Azure SAS token for access

**Connectors:** Azure Data Lake Storage (ADLS), Azure Databricks Volumes

**API Fields:**

- `connectorPassword` - Azure SAS token

**Example Configuration:**

```json
{
	"connectorName": "ADLS with SAS",
	"connectorAuthType": 4,
	"connectorPassword": "?sv=2021-06-08&ss=bfqt&srt=sco&sp=rwdlacupiytfx..."
}
```

**How to Generate SAS Token:**

1. Navigate to Azure Portal → Storage Account
2. Select "Shared access signature" from left menu
3. Configure permissions and expiration
4. Click "Generate SAS and connection string"

---

### 5. Azure Service Principal (authID: 5)

**Description:** Use an Azure Service Principal and Secret for access

**Connectors:** Many Azure services

**API Fields:**

- `connectorUsername` - Service Principal Client ID
- `connectorPassword` - Service Principal Secret

**Example Configuration:**

```json
{
	"connectorName": "ADLS with Service Principal",
	"connectorAuthType": 5,
	"connectorUsername": "app-client-id-guid",
	"connectorPassword": "client-secret-value"
}
```

**Setup Steps:**

1. Create App Registration in Azure AD
2. Create client secret for the app
3. Grant app access to storage account (Storage Blob Data Contributor role)
4. Use Client ID as username and Secret as password

---

### 6. Personal Access Token (authID: 6)

**Description:** Use a personal access token (PAT) for access

**Connectors:** Azure DevOps, GitHub, GitLab, Generic API

**API Fields:**

- `connectorPassword` - Personal Access Token

**Example Configuration:**

```json
{
	"connectorName": "GitHub API",
	"connectorAuthType": 6,
	"connectorPassword": "ghp_1234567890abcdefghijklmnop"
}
```

---

### 7. S3 Access Key And Secret (authID: 7)

**Description:** Access key and secret for access

**Connectors:** Amazon S3

**API Fields:**

- `connectorUsername` - AWS Access Key ID
- `connectorPassword` - AWS Secret Access Key

**Example Configuration:**

```json
{
	"connectorName": "S3 Production Bucket",
	"connectorAuthType": 7,
	"connectorUsername": "AKIAIOSFODNN7EXAMPLE",
	"connectorPassword": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}
```

**How to Get AWS Credentials:**

1. AWS Console → IAM → Users → Security credentials
2. Create access key
3. Save Access Key ID and Secret Access Key

---

### 8. API Key (authID: 8)

**Description:** Use a generated API Key for access

**Connectors:** Redcap, Generic API, many SaaS APIs

**API Fields:**

- `connectorPassword` - API Key

**Example Configuration:**

```json
{
	"connectorName": "Redcap API",
	"connectorAuthType": 8,
	"connectorPassword": "1234567890ABCDEF1234567890ABCDEF"
}
```

---

### 9-13. NTLM, AzureAD, Account Key, Password, Server (authID: 9-13)

**Description:** Variations of username/password authentication

**API Fields:**

- `connectorUsername` - Username
- `connectorPassword` - Password

**Usage:** Similar to Basic auth but with specific authentication protocol requirements.

---

### 14. Azure Service Principal (Extended) (authID: 14)

**Description:** Use Azure EntraID Credentials with Tenant

**Connectors:** Microsoft Dataverse, Azure services requiring tenant specification

**API Fields:**

- `connectorUsername` - Client ID
- `connectorPassword` - Client Secret
- `connectorAdditionalDetails` - Azure Tenant ID

**Example Configuration:**

```json
{
	"connectorName": "Dataverse Connection",
	"connectorAuthType": 14,
	"connectorUsername": "app-client-id",
	"connectorPassword": "client-secret",
	"connectorAdditionalDetails": "tenant-id-guid"
}
```

---

### 15. Azure Datalake Storage Gen2 SSL (authID: 15)

**Description:** Use Account Key to access ADLS bucket

**API Fields:**

- `connectorStorageAccountName` - Storage Account Name
- `connectorPassword` - Access Key

**Example Configuration:**

```json
{
	"connectorName": "ADLS Gen2",
	"connectorAuthType": 15,
	"connectorStorageAccountName": "mycompanystorage",
	"connectorPassword": "access_key_here=="
}
```

---

### 16. User Token (authID: 16)

**Description:** User Token authentication

**API Fields:**

- `connectorPassword` - User Token

---

### 17. OAuth (Box Specific) (authID: 17)

**Description:** Box-specific OAuth authentication

**Connectors:** Box (when OAuth is supported)

**API Fields:**

- `connectorPassword` - OAuth token

---

### 18. API Token (authID: 18)

**Description:** Supply username (email) and API token

**Connectors:** Generic API, Jira, Confluence

**API Fields:**

- `connectorUsername` - Username (typically email)
- `connectorPassword` - API Token

**Example Configuration:**

```json
{
	"connectorName": "Jira API",
	"connectorAuthType": 18,
	"connectorUsername": "user@example.com",
	"connectorPassword": "api-token-here"
}
```

---

### 19. Fabric Workspace Identity (authID: 19)

**Description:** Use Azure Fabric Workspace Identity

**API Fields:**

- `connectorUsername` - Client ID
- `connectorPassword` - Client Secret
- `connectorAdditionalDetails` - Azure Tenant ID

---

### 20. Bearer Token (authID: 20)

**Description:** User-generated Bearer Token

**Connectors:** Generic API, REST APIs

**API Fields:**

- `connectorPassword` - Bearer Token

**Example Configuration:**

```json
{
	"connectorName": "Custom API",
	"connectorAuthType": 20,
	"connectorPassword": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 21. Access Token (authID: 21)

**Description:** Use an access token for access

**API Fields:**

- `connectorPassword` - Access Token

---

### 22. None (authID: 22)

**Description:** No authentication required

**Connectors:** Public APIs, Generic API without auth

**API Fields:** None required

**Example Configuration:**

```json
{
	"connectorName": "Public Data API",
	"connectorAuthType": 22
}
```

---

## Choosing the Right Authentication Type

### For Azure Services

- **ADLS/Blob Storage:** Azure Access Key (3), Azure SAS Token (4), or Azure Service Principal (5)
- **Dataverse/Dynamics:** Azure Service Principal Extended (14)
- **Fabric:** Fabric Workspace Identity (19)

### For AWS Services

- **S3:** S3 Access Key And Secret (7)

### For SaaS Applications

- **OAuth-enabled:** OAuth (1)
- **API Key based:** API Key (8)
- **Token based:** API Token (18) or Bearer Token (20)

### For Databases

- **SQL Databases:** Basic (2), Password (12), or Server (13)
- **Cloud Databases:** Depends on provider (usually username/password or key-based)

### For File Systems

- **SFTP:** Password (12)
- **SMB:** Basic (2) with domain\\username format

### For Public APIs

- **No auth required:** None (22)

---

## Security Best Practices

### Password/Secret Management

- Never commit credentials to version control
- Use environment variables or secure vaults
- Rotate credentials regularly
- Use minimal required permissions

### OAuth

- Review permissions requested during OAuth flow
- Revoke unused OAuth tokens
- Monitor OAuth token usage
- Enable MFA on OAuth provider accounts

### Service Principals

- Use separate service principals per environment
- Grant least-privilege access
- Set expiration on client secrets
- Monitor service principal activity

### API Keys/Tokens

- Generate unique keys per connector
- Set expiration when supported
- Rotate keys periodically
- Monitor for unauthorized usage

---

## Testing Authentication

After configuring authentication, test the connector:

```bash
bun test_connector.ts <connector_id>
```

This will verify:

- Credentials are valid
- Network connectivity works
- Permissions are sufficient
- Connection parameters are correct

---

## Troubleshooting

### OAuth Failures

- Check `oAuthURL` is correct
- Verify user has permissions
- Check for expired tokens
- Confirm redirect URIs match

### Access Key Failures

- Verify key is not expired
- Check key permissions/scopes
- Confirm storage account name is correct
- Verify network/firewall rules

### Username/Password Failures

- Check for special characters in password
- Verify username format (especially for domain accounts)
- Confirm account is not locked
- Check password has not expired

### API Key/Token Failures

- Verify token has not expired
- Check token permissions/scopes
- Confirm API endpoint allows token auth
- Verify token format is correct

---

## Examples by Connector Type

### MySQL with Basic Auth

```json
{
	"connectorName": "MySQL Production",
	"connectorType": "RDBMS",
	"connectorHost": "mysql.example.com",
	"connectorPort": "3306",
	"connectorDatabaseName": "analytics",
	"connectorAuthType": 2,
	"connectorUsername": "databasin_user",
	"connectorPassword": "secure_password"
}
```

### S3 with Access Key

```json
{
	"connectorName": "S3 Data Lake",
	"connectorType": "File & API",
	"connectorStorageAccountName": "my-data-bucket",
	"connectorAuthType": 7,
	"connectorUsername": "AKIAIOSFODNN7EXAMPLE",
	"connectorPassword": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}
```

### ADLS with Service Principal

```json
{
	"connectorName": "ADLS Production",
	"connectorType": "File & API",
	"connectorStorageAccountName": "mycompanystorage",
	"connectorContainerName": "data-warehouse",
	"connectorAuthType": 5,
	"connectorUsername": "app-client-id-guid",
	"connectorPassword": "client-secret-value"
}
```

### Generic API with Bearer Token

```json
{
	"connectorName": "Custom REST API",
	"connectorType": "File & API",
	"connectorHost": "https://api.example.com",
	"connectorAuthType": 20,
	"connectorPassword": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
