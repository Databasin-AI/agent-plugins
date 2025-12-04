# Databasin Connector Asset Templates

This directory contains JSON templates for creating common connector types.

## Available Templates

### Database Connectors

- **`mysql-template.json`** - MySQL database connector
- **`postgresql-template.json`** - PostgreSQL database connector
- **`snowflake-template.json`** - Snowflake data warehouse connector

### Cloud Storage Connectors

- **`s3-template.json`** - Amazon S3 bucket connector
- **`adls-template.json`** - Azure Data Lake Storage Gen2 connector (multiple auth methods)

### File Transfer Connectors

- **`sftp-template.json`** - SFTP server connector

### SaaS Application Connectors

- **`salesforce-template.json`** - Salesforce CRM connector (production and sandbox)

### API Connectors

- **`generic-api-template.json`** - Generic REST API connector (multiple auth methods)

## How to Use Templates

### 1. Copy the Template

```bash
cp assets/mysql-template.json my-connector.json
```

### 2. Edit the Configuration

Replace placeholder values with your actual configuration:

- `institutionID` - Your organization ID
- `internalID` - Your project ID
- `ownerID` - Your user ID
- Authentication credentials
- Connection details (host, port, database, etc.)

### 3. Validate the Configuration

Validation happens automatically during connector creation. You can create the connector directly.

### 4. Create the Connector

```bash
databasin connectors create -p <projectId> -f my-connector.json
```

## Template Structure

All templates include:

- `_comment` field - Explains the template and required changes (remove before submission)
- Required fields for the connector type
- Recommended optional fields
- Example values showing proper format
- Placeholder text indicating what to replace

### Multi-Option Templates

Some templates (ADLS, Salesforce, Generic API) include multiple configuration options:

- Each option is prefixed with `_authMethod` or `_production`/`_sandbox`
- Extract the option you need and remove others
- Remove the prefix before using

**Example - ADLS Template:**

```json
{
  "_authMethod1_accessKey": { ... },
  "_authMethod2_sasToken": { ... },
  "_authMethod3_servicePrincipal": { ... }
}
```

To use Service Principal auth, extract that section:

```json
{
  "connectorName": "ADLS with Service Principal",
  "connectorType": "File & API",
  "connectorStorageAccountName": "your_storage_account_name",
  ...
}
```

## Required Fields

All connector templates require these organizational fields:

- `institutionID` - Organization/institution identifier
- `internalID` - Project identifier
- `ownerID` - User ID of connector owner

Get these values from:

- Databasin UI project settings
- API response from `/api/projects`
- Your Databasin administrator

## Authentication Types Reference

| authID | Name                               | Usage                                        |
| ------ | ---------------------------------- | -------------------------------------------- |
| 1      | OAuth                              | Cloud providers (Box, Google Drive, etc.)    |
| 2      | Basic                              | Username/password for databases and services |
| 3      | Azure Access Key                   | Azure storage with access key                |
| 4      | Azure SAS Token                    | Azure storage with SAS token                 |
| 5      | Azure Service Principal            | Azure services with app registration         |
| 6      | Personal Access Token              | PAT-based APIs                               |
| 7      | S3 Access Key And Secret           | AWS S3 with access keys                      |
| 8      | API Key                            | API key in header or query param             |
| 12     | Password                           | SFTP and similar services                    |
| 14     | Azure Service Principal (Extended) | Azure with tenant ID                         |
| 20     | Bearer Token                       | JWT or bearer token APIs                     |
| 22     | None                               | Public APIs without authentication           |

See `references/authentication-guide.md` for complete authentication documentation.

## Validation

Validation happens automatically when creating a connector with the CLI:

```bash
databasin connectors create -p <projectId> -f my-connector.json
```

The validator checks:

- Required fields for the connector type
- Field data types and formats
- Authentication configuration
- Business rules (connection limits, port ranges, etc.)

## Best Practices

1. **Use descriptive connector names**
   - Include environment (Production, Staging, Dev)
   - Include system name
   - Example: "MySQL Production Analytics"

2. **Set appropriate connection limits**
   - Default: 8 connections
   - High-volume: 16-20 connections
   - Low-volume: 4-8 connections

3. **Use additional connection parameters**
   - SSL/TLS settings
   - Timeout values
   - Compression settings
   - Example: `"connectorAdditionalDetails": "ssl=true&connectTimeout=30000"`

4. **Test after creation**

   ```bash
   databasin connectors test <connectorId>
   ```

5. **Document custom configurations**
   - Add comments to your configuration files
   - Track connection parameters and settings
   - Maintain separate configs for each environment

## Environment-Specific Configurations

Create separate connector files for each environment:

```
connectors/
├── mysql-production.json
├── mysql-staging.json
├── mysql-development.json
├── s3-production.json
└── s3-development.json
```

This allows you to:

- Version control configurations
- Deploy to different environments
- Maintain separate credentials
- Track changes over time

## Security Notes

**Never commit credentials to version control!**

Use placeholder values in templates:

```json
{
	"connectorPassword": "REPLACE_WITH_ACTUAL_PASSWORD",
	"connectorUsername": "REPLACE_WITH_ACTUAL_USERNAME"
}
```

Replace before deployment:

- Use environment variables
- Use secret management systems
- Use secure configuration management

## Troubleshooting

### Template Validation Fails

1. Check all required fields are present
2. Verify `institutionID`, `internalID`, `ownerID` are numbers/strings as required
3. Ensure `connectorType` matches exactly (case-sensitive)
4. Validate authentication type is supported for the connector

### Connector Creation Fails

1. Validate configuration first
2. Check JWT token is valid (`.token` file)
3. Verify network connectivity to API
4. Test connection after creation

### Connection Test Fails

1. Verify credentials are correct
2. Check host and port are accessible
3. Confirm firewall rules allow connection
4. Validate authentication method is correct

For more help, see:

- `references/field-reference.md` - Complete field documentation
- `references/authentication-guide.md` - Authentication methods
- `references/api-endpoints.md` - API endpoint reference
- `references/examples.md` - Real-world examples
