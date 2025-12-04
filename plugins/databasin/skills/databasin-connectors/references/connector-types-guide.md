# Databasin Connector Types Guide

This guide provides an overview of all available connector types in Databasin and their characteristics.

## Connector Categories

Databasin organizes connectors into 9 main categories:

### 1. RDBMS (ID: 1)

Relational Database Management Systems

**Common Connectors:**

- Microsoft SQL Server
- MySQL
- PostgreSQL
- Oracle
- Microsoft Access
- Amazon RDS
- Azure SQL

**Characteristics:**

- Support for catalogs, schemas, tables, and columns
- Full ingress and egress support
- Standard SQL query capabilities
- Connection testing available
- Typical authentication: Username/Password, Azure AD

**Required Screens:**

- Screen 7: Connector selection
- Screen 2: Catalog selection
- Screen 3: Schema selection
- Screen 4: Table/artifact selection
- Screen 5: Column selection

---

### 2. Big Data & NoSQL (ID: 2)

Large-scale and NoSQL database systems

**Common Connectors:**

- MongoDB
- Cassandra
- DynamoDB
- Cosmos DB
- HBase
- Couchbase

**Characteristics:**

- Schema-less or flexible schema support
- Horizontal scalability
- Various data models (document, key-value, column-family)
- May not support all SQL operations
- Typical authentication: API keys, Account keys, Username/Password

---

### 3. File & API (ID: 3)

File storage systems and REST API endpoints

**Common Connectors:**

- Amazon S3
- Azure Data Lake Storage (ADLS)
- Box
- Dropbox
- Google Drive
- SFTP
- Generic API
- Sharepoint

**Characteristics:**

- File-based data ingestion
- Support for CSV, JSON, XML, Parquet, Excel formats
- Wildcard file selection in some connectors
- OAuth support for cloud providers
- Both ingress and egress for most connectors

**Required Screens:**

- Screen 2: File/folder selection
- Screen 4: File format configuration
- Screen 5: Column mapping (for structured files)

**File Drop Target:**
Some connectors (S3, ADLS, Box, Google Drive) support direct file drop functionality.

---

### 4. Marketing (ID: 4)

Marketing automation and analytics platforms

**Common Connectors:**

- Google Analytics
- Adobe Analytics
- Mailchimp
- HubSpot Marketing
- Marketo

**Characteristics:**

- Read-only access (egress only)
- OAuth authentication common
- Pre-defined schemas based on platform APIs
- Rate limiting considerations
- Time-based data extraction

---

### 5. CRM & ERP (ID: 5)

Customer Relationship Management and Enterprise Resource Planning systems

**Common Connectors:**

- Salesforce
- Microsoft Dynamics 365
- Microsoft Dataverse
- SAP
- Oracle ERP
- Workday

**Characteristics:**

- Complex object relationships
- Custom field support
- OAuth or service principal authentication
- API version management
- Both ingress and egress for some connectors

---

### 6. E-Commerce (ID: 6)

Online retail and e-commerce platforms

**Common Connectors:**

- Shopify
- WooCommerce
- Magento
- BigCommerce

**Characteristics:**

- Product, order, customer data access
- OAuth authentication typical
- Webhook support for real-time updates
- Rate limiting
- Egress-only for most connectors

---

### 7. Accounting (ID: 7)

Financial and accounting software

**Common Connectors:**

- QuickBooks
- Xero
- Sage
- NetSuite

**Characteristics:**

- Financial data access
- OAuth authentication required
- Strict data validation rules
- Audit trail requirements
- Egress-only for most connectors

---

### 8. Collaboration (ID: 8)

Team collaboration and productivity tools

**Common Connectors:**

- Microsoft Teams
- Slack
- Jira
- Confluence
- Asana

**Characteristics:**

- User and activity data
- OAuth or API token authentication
- Message and file access
- Egress-only typically
- Rate limiting considerations

---

### 9. AI & LLM (ID: 9)

Artificial Intelligence and Large Language Model platforms

**Common Connectors:**

- Azure OpenAI
- OpenAI API
- Anthropic Claude
- Google Vertex AI

**Characteristics:**

- API-based integration
- Token/key authentication
- Request/response pattern
- Cost per API call considerations
- Rate limits and quotas

---

## Connector Support Flags

Each connector has several boolean flags that indicate capabilities:

### ingressTargetSupport

**True:** Connector can be used as a data source (read from)
**False:** Connector cannot be used as a source

### egressTargetSupport

**True:** Connector can be used as a data destination (write to)
**False:** Connector cannot be used as a destination

### testConnectorSupport

**True:** Connection can be tested before use
**False:** No test functionality available

### databasinFileDropTarget

**True:** Supports direct file upload/drop functionality
**False:** No file drop support

### globalOAuthSupport

**True:** Supports organization-wide OAuth configuration
**False:** OAuth must be configured per connector instance

### active

**True:** Connector is active and available for use
**False:** Connector is disabled or deprecated

---

## Screen Flow Patterns

Different connector types require different wizard screen sequences:

### RDBMS Pattern (Full Hierarchy)

1. Screen 7: Connector selection
2. Screen 2: Catalog selection
3. Screen 3: Schema selection
4. Screen 4: Table selection
5. Screen 5: Column selection

### File & API Pattern (File-Based)

1. Screen 2: File/folder selection
2. Screen 4: File format configuration
3. Screen 5: Column mapping

### API Pattern (Generic API)

1. Screen 10: API endpoint configuration
2. Screen 5: Response mapping

### Simplified Pattern (Some NoSQL, Marketing, etc.)

1. Screen 2: Container/collection selection
2. Screen 4: Artifact selection
3. Screen 5: Field mapping

---

## Authentication Considerations

### OAuth Connectors

Require browser-based authentication flow. Some provide `oAuthURL` in configuration.

**Examples:** Box, Google Drive, Salesforce, Shopify

### Service Principal / App Registration

Azure-based connectors often use service principal authentication.

**Examples:** Azure Data Lake Storage, Microsoft Dataverse, Azure OpenAI

### API Key / Token

Simple token-based authentication for APIs.

**Examples:** Generic API, Redcap, Many AI/LLM connectors

### Username/Password

Traditional authentication for databases and file systems.

**Examples:** MySQL, PostgreSQL, SFTP, SMB

---

## Choosing the Right Connector Type

**For structured database sources:**
→ Use RDBMS category

**For cloud file storage:**
→ Use File & API category (S3, ADLS, Google Drive, etc.)

**For SaaS application data:**
→ Use appropriate category (Marketing, CRM & ERP, E-Commerce, etc.)

**For custom REST APIs:**
→ Use Generic API connector in File & API category

**For NoSQL databases:**
→ Use Big Data & NoSQL category

**For AI/ML integration:**
→ Use AI & LLM category
