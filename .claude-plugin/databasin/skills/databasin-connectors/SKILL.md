---
name: databasin-connectors
description: Expert skill for creating, managing, and troubleshooting Databasin data connectors through natural language interaction. Use this skill when users need to create new connectors (MySQL, S3, ADLS, etc.), modify existing connector settings, test connections, or troubleshoot connection issues.
---

# Databasin Connectors Skill

Expert skill for creating, managing, and troubleshooting Databasin data connectors through natural language interaction.

## When to Use This Skill

Use this skill when the user requests help with:

- **Creating new connectors** - "Create a MySQL connector for our production database"
- **Modifying existing connectors** - "Update the credentials for connector 123"
- **Testing connector connections** - "Test if the S3 connector is working"
- **Deleting connectors** - "Remove the old Salesforce connector"
- **Understanding connector types** - "What connector types are available?"
- **Troubleshooting connection issues** - "Why can't my ADLS connector connect?"
- **Exploring connector configurations** - "Show me what fields I need for a Snowflake connector"

## Core Capabilities

This skill provides:

1. **Connector Creation** - Create any of 434+ supported connector types with proper validation
2. **Connector Management** - Update settings, credentials, and configuration
3. **Connection Testing** - Verify connectors are properly configured
4. **Connector Discovery** - List and explore available connector types
5. **Configuration Validation** - Automatic validation during creation
6. **OAuth Management** - Guide users through OAuth flows for cloud providers

## Available Resources

### CLI Commands

All connector operations use the `databasin connectors` command suite:

**Core Commands:**

```bash
databasin connectors list -p <project> [--full] [--fields <fields>] [--json]
databasin connectors get <id> [--json] [--fields <fields>]
databasin connectors create <file> -p <project>
databasin connectors update <id> <file>
databasin connectors delete <id> [--yes]
databasin connectors test <id>
```

**Output Formats:**

- **Table** (default) - Human-readable formatted tables
- **JSON** - Use `--json` flag for JSON output
- **CSV** - Use `--csv` flag for CSV output
- **Field Filtering** - Use `--fields` to show specific fields only

**Token Efficiency:**

- `list` defaults to **count mode** (returns only count, not full objects)
- Use `--full` flag to fetch complete connector objects
- Use `--fields` to limit returned data
- Use `--limit` to restrict number of results

### Reference Documentation (in `references/`)

- `connector-types-guide.md` - Complete guide to all 9 connector categories
- `field-reference.md` - All 45 required and 17 optional fields
- `authentication-guide.md` - All 22 authentication types with examples
- `api-endpoints.md` - Databasin connector API reference
- `examples.md` - Real-world connector configurations

### Asset Templates (in `assets/`)

Ready-to-use JSON templates:

- `mysql-template.json`
- `postgresql-template.json`
- `s3-template.json`
- `adls-template.json`
- `sftp-template.json`
- `snowflake-template.json`
- `salesforce-template.json`
- `generic-api-template.json`

## Typical Workflows

### A. Creating a New Connector

**User Request:** "I need to create a MySQL connector for our production database"

**Steps:**

1. **Gather Requirements**

   ```
   Ask user for:
   - Connector type (MySQL confirmed)
   - Host and port
   - Database name
   - Username and password
   - Organization ID (institutionID)
   - Project ID (internalID)
   - Owner ID (ownerID)
   ```

2. **Check Template**

   ```bash
   # Show user the MySQL template
   Read assets/mysql-template.json
   ```

3. **Create Configuration File**

   ```bash
   # Create mysql_prod.json with user's values
   Write mysql_prod.json
   ```

   Example configuration:

   ```json
   {
   	"connectorName": "MySQL Production",
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

4. **Create Connector** (validation automatic)

   ```bash
   databasin connectors create mysql_prod.json -p proj-001
   ```

5. **Test Connection**

   ```bash
   databasin connectors test <connector_id>
   ```

6. **Confirm Success**
   ```
   Inform user:
   - Connector ID
   - Connection test result
   - Next steps (use in pipeline, etc.)
   ```

### B. Modifying Connector Credentials

**User Request:** "Update the password for connector 123"

**Steps:**

1. **Get Current Connector**

   ```bash
   databasin connectors get 123
   ```

2. **Show Current Config** (without password)

   ```
   Display to user:
   - Connector name
   - Type
   - Host
   - Database
   ```

3. **Create Update File**

   ```bash
   # Create credentials update file
   echo '{
     "connectorUsername": "new_user",
     "connectorPassword": "new_password"
   }' > /tmp/creds_update.json
   ```

4. **Update Credentials**

   ```bash
   databasin connectors update 123 /tmp/creds_update.json
   ```

5. **Test Updated Connection**

   ```bash
   databasin connectors test 123
   ```

6. **Clean Up**
   ```bash
   rm /tmp/creds_update.json
   ```

### C. Exploring Connector Types

**User Request:** "What File & API connectors are available?"

**Steps:**

1. **Reference Documentation**

   ```bash
   # Show user the connector types guide
   Read references/connector-types-guide.md
   ```

2. **Explain Available Connectors**

   ```
   File & API Category includes:
   - Amazon S3 (S3 Access Key authentication)
   - Azure Data Lake Storage (Access Key or Service Principal)
   - SFTP (Password authentication)
   - Box, Google Drive (OAuth required)
   - Generic REST API (API Key, Bearer Token, or None)

   Reference: assets/ directory contains templates for:
   - s3-template.json
   - adls-template.json
   - sftp-template.json
   - generic-api-template.json
   ```

3. **Provide Template** (if user wants to create one)
   ```bash
   # Show relevant template
   Read assets/s3-template.json
   # or
   Read assets/adls-template.json
   ```

### D. Troubleshooting Connection Issues

**User Request:** "My S3 connector isn't working"

**Steps:**

1. **Test Connector**

   ```bash
   databasin connectors test <connector_id>
   ```

2. **Get Connector Details**

   ```bash
   databasin connectors get <connector_id> --json
   ```

3. **Analyze Error**

   ```
   Common S3 issues:
   - Invalid access keys (403 Forbidden)
   - Incorrect bucket name (404 Not Found)
   - Permission/policy issues (403 Access Denied)
   - Region mismatch (301 Moved Permanently)
   - Network connectivity (Connection timeout)
   ```

4. **Check Configuration**

   ```
   Reference: references/authentication-guide.md
   - Verify authType is 7 (S3 Access Key And Secret)
   - Check connectorUsername is AWS Access Key ID
   - Confirm connectorPassword is AWS Secret Access Key
   - Verify connectorStorageAccountName is bucket name
   - Ensure region is in connectorAdditionalDetails if needed
   ```

5. **Create Fix**

   ```bash
   # Create update with corrected values
   echo '{
     "connectorUsername": "AKIAIOSFODNN7EXAMPLE",
     "connectorPassword": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
     "connectorAdditionalDetails": "region=us-west-2"
   }' > /tmp/s3_fix.json

   databasin connectors update <connector_id> /tmp/s3_fix.json
   ```

6. **Test Again**
   ```bash
   databasin connectors test <connector_id>
   ```

### E. Deleting a Connector

**User Request:** "Delete connector 789"

**Steps:**

1. **Get Connector Details**

   ```bash
   databasin connectors get 789
   ```

2. **Warn About Dependencies**

   ```
   ⚠ IMPORTANT: Check if connector is used by pipelines!

   To check pipeline usage:
   databasin pipelines list -p <project> --full --json | grep "789"

   Deleting will break any pipelines using this connector.
   ```

3. **Confirm with User**

   ```
   Show connector details and ask:
   "Are you sure you want to delete [Connector Name] (ID: 789)?"
   ```

4. **Delete Connector**

   ```bash
   # With confirmation prompt
   databasin connectors delete 789

   # Skip confirmation (if user is certain)
   databasin connectors delete 789 --yes
   ```

5. **Confirm Deletion**
   ```
   Verify deletion was successful and inform user.
   ```

### F. Listing Connectors

**User Request:** "Show me all connectors in project proj-001"

**Steps:**

1. **Get Count First** (token efficient)

   ```bash
   databasin connectors list -p proj-001
   ```

   Output:

   ```
   ✔ Total connectors: 23

   ⚠ Use --full to fetch full connector objects
   ℹ Filtered by project: proj-001
   ```

2. **If Full List Needed**

   ```bash
   # Get all connectors with key fields only
   databasin connectors list -p proj-001 --full --fields connectorID,connectorName,connectorType,status
   ```

3. **For JSON Export**

   ```bash
   # Export to JSON for processing
   databasin connectors list -p proj-001 --full --json > connectors.json
   ```

4. **For CSV Export**
   ```bash
   # Export to CSV for spreadsheet
   databasin connectors list -p proj-001 --full --csv > connectors.csv
   ```

### G. OAuth Connector Setup

**User Request:** "I need to connect to Salesforce using OAuth"

OAuth connectors require special handling for authorization flows, token acquisition, and automatic token refresh. This workflow covers the complete OAuth setup process for cloud-based services.

#### OAuth Overview

**What are OAuth Connectors?**

OAuth (Open Authorization) connectors use the OAuth 2.0 protocol to securely access third-party services without storing passwords. Instead of credentials, these connectors:

- Use temporary access tokens
- Support automatic token refresh
- Require one-time user authorization
- Store refresh tokens for long-term access

**When to Use OAuth vs Basic Auth:**

| Use OAuth When:                            | Use Basic Auth When:               |
| ------------------------------------------ | ---------------------------------- |
| Service requires OAuth (Google, Microsoft) | Service supports username/password |
| Need delegated access to user resources    | Using service account credentials  |
| Want automatic token refresh               | Direct database/API key access     |
| Connecting to SaaS platforms               | Internal systems or legacy APIs    |

**Common OAuth Connectors:**

- **CRM & ERP:** Salesforce, Microsoft Dynamics 365, HubSpot
- **Cloud Storage:** Google Drive, Box, OneDrive
- **Collaboration:** Slack, Microsoft Teams, Zoom
- **Productivity:** Google Sheets, Microsoft 365, Asana
- **Marketing:** Mailchimp, Facebook Ads, LinkedIn Ads

#### OAuth Flow Overview

**Authorization Flow Steps:**

```
1. User Request → Databasin generates authorization URL
                     ↓
2. User clicks URL → Redirects to provider (e.g., Salesforce)
                     ↓
3. User grants permission → Provider redirects back with auth code
                     ↓
4. Databasin exchanges code → Receives access token + refresh token
                     ↓
5. Tokens stored securely → Connector ready to use
                     ↓
6. Access token expires → Automatic refresh using refresh token
```

**Token Lifecycle:**

- **Access Token:** Short-lived (1-2 hours), used for API requests
- **Refresh Token:** Long-lived (months/years), used to get new access tokens
- **Automatic Refresh:** Databasin handles token refresh transparently

#### Complete OAuth Connector Example: Salesforce

**Steps:**

1. **Gather OAuth Requirements**

   ```
   Ask user for:
   - Salesforce instance URL (e.g., https://yourcompany.salesforce.com)
   - OAuth client ID (from Salesforce Connected App)
   - OAuth client secret (from Salesforce Connected App)
   - Organization ID (institutionID)
   - Project ID (internalID)
   - Owner ID (ownerID)
   ```

2. **Check OAuth Template**

   ```bash
   # Show user the Salesforce OAuth template
   Read assets/salesforce-template.json
   ```

3. **Create Salesforce OAuth Configuration**

   ```bash
   # Create salesforce_oauth.json
   Write salesforce_oauth.json
   ```

   **Complete OAuth Configuration:**

   ```json
   {
   	"connectorName": "Salesforce Production CRM",
   	"connectorType": "CRM & ERP",
   	"connectorHost": "yourcompany.salesforce.com",
   	"connectorPort": "443",
   	"connectorAuthType": 14,
   	"oauthClientId": "3MVG9..._your_client_id_here",
   	"oauthClientSecret": "1234567890ABCDEF",
   	"oauthRedirectUri": "https://databasin.yourcompany.com/oauth/callback",
   	"oauthScopes": "api refresh_token offline_access",
   	"oauthAuthorizationUrl": "https://yourcompany.salesforce.com/services/oauth2/authorize",
   	"oauthTokenUrl": "https://yourcompany.salesforce.com/services/oauth2/token",
   	"oauthAutoRefresh": true,
   	"connectorAdditionalDetails": "apiVersion=v58.0",
   	"institutionID": 1,
   	"internalID": "proj-001",
   	"ownerID": 456
   }
   ```

   **OAuth-Specific Fields Explained:**
   - `connectorAuthType: 14` - OAuth 2.0 Authorization Code Flow
   - `oauthClientId` - From Connected App in Salesforce Setup
   - `oauthClientSecret` - From Connected App in Salesforce Setup
   - `oauthRedirectUri` - Must match Connected App callback URL exactly
   - `oauthScopes` - Permissions requested (space-separated)
   - `oauthAuthorizationUrl` - Provider's authorization endpoint
   - `oauthTokenUrl` - Provider's token exchange endpoint
   - `oauthAutoRefresh: true` - Enable automatic token refresh

4. **Create Connector** (generates authorization URL)

   ```bash
   databasin connectors create salesforce_oauth.json -p proj-001
   ```

   Output:

   ```
   ✔ Connector created successfully
   ✔ Connector ID: 789

   ⚠ OAuth Authorization Required

   To complete setup, visit this URL to authorize:
   https://yourcompany.salesforce.com/services/oauth2/authorize?
     client_id=3MVG9..._your_client_id_here&
     redirect_uri=https://databasin.yourcompany.com/oauth/callback&
     response_type=code&
     scope=api%20refresh_token%20offline_access&
     state=connector_789

   After authorization, tokens will be stored automatically.
   ```

5. **User Completes Authorization**

   ```
   User clicks the authorization URL:
   1. Redirected to Salesforce login
   2. Logs in with Salesforce credentials
   3. Approves requested permissions
   4. Redirected back to Databasin
   5. Tokens automatically stored in connector
   ```

6. **Verify OAuth Setup**

   ```bash
   # Test connection (uses stored tokens)
   databasin connectors test 789
   ```

   Success output:

   ```
   ✔ Connection test successful
   ✔ OAuth tokens valid
   ℹ Access token expires in: 1h 45m
   ℹ Refresh token valid
   ```

7. **Confirm Success**
   ```
   Inform user:
   - Connector ID: 789
   - OAuth authorization complete
   - Tokens stored securely
   - Automatic refresh enabled
   - Ready to use in pipelines
   ```

#### Token Refresh Handling

**Automatic Refresh Configuration:**

```json
{
	"oauthAutoRefresh": true,
	"oauthRefreshTokenExpiryDays": 90
}
```

**How Automatic Refresh Works:**

```
API Request → Access token expired?
                     ↓
              Yes: Use refresh token → Get new access token
                     ↓
              Store new tokens → Retry API request
                     ↓
              Success: Return data
```

**Manual Token Refresh:**

If automatic refresh fails or you need to force refresh:

```bash
# Trigger manual token refresh
databasin connectors refresh-token 789
```

**Refresh Token Expiration:**

When refresh tokens expire (typically 90-180 days):

```bash
# Test will show expired refresh token
databasin connectors test 789
```

Output:

```
✘ Connection test failed
✘ Refresh token expired

⚠ Re-authorization Required

Visit this URL to re-authorize:
https://yourcompany.salesforce.com/services/oauth2/authorize?...
```

**Re-authorization Steps:**

1. User clicks new authorization URL
2. Logs in again (if needed)
3. Approves permissions
4. New tokens stored automatically

**Best Practices:**

- Set `oauthAutoRefresh: true` always
- Monitor token expiry in production
- Alert users 7 days before refresh token expiry
- Keep authorization URLs accessible for re-auth

#### Common OAuth Connectors Configuration

**1. Salesforce**

```json
{
	"connectorName": "Salesforce Production",
	"connectorType": "CRM & ERP",
	"connectorHost": "yourcompany.salesforce.com",
	"connectorPort": "443",
	"connectorAuthType": 14,
	"oauthClientId": "3MVG9...",
	"oauthClientSecret": "ABC123...",
	"oauthRedirectUri": "https://databasin.yourcompany.com/oauth/callback",
	"oauthScopes": "api refresh_token offline_access",
	"oauthAuthorizationUrl": "https://yourcompany.salesforce.com/services/oauth2/authorize",
	"oauthTokenUrl": "https://yourcompany.salesforce.com/services/oauth2/token",
	"oauthAutoRefresh": true,
	"connectorAdditionalDetails": "apiVersion=v58.0",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

**Required Scopes:** `api refresh_token offline_access`

**Setup Notes:**

- Create Connected App in Salesforce Setup
- Enable OAuth Settings in Connected App
- Add callback URL to Allowed Redirect URIs
- Copy Consumer Key (client ID) and Consumer Secret

**2. Google Sheets/Drive**

```json
{
	"connectorName": "Google Drive Data Files",
	"connectorType": "File & API",
	"connectorHost": "www.googleapis.com",
	"connectorPort": "443",
	"connectorAuthType": 14,
	"oauthClientId": "123456789-abcdefg.apps.googleusercontent.com",
	"oauthClientSecret": "GOCSPX-...",
	"oauthRedirectUri": "https://databasin.yourcompany.com/oauth/callback",
	"oauthScopes": "https://www.googleapis.com/auth/drive.readonly https://www.googleapis.com/auth/spreadsheets.readonly",
	"oauthAuthorizationUrl": "https://accounts.google.com/o/oauth2/v2/auth",
	"oauthTokenUrl": "https://oauth2.googleapis.com/token",
	"oauthAutoRefresh": true,
	"connectorAdditionalDetails": "access_type=offline&prompt=consent",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

**Required Scopes:**

- Drive: `https://www.googleapis.com/auth/drive.readonly`
- Sheets: `https://www.googleapis.com/auth/spreadsheets.readonly`
- Full access: Replace `.readonly` with nothing

**Setup Notes:**

- Create project in Google Cloud Console
- Enable Google Drive API and/or Google Sheets API
- Create OAuth 2.0 Client ID (Web application)
- Add authorized redirect URI
- Important: `access_type=offline` required for refresh tokens

**3. Microsoft 365 (OneDrive/SharePoint)**

```json
{
	"connectorName": "Microsoft 365 Files",
	"connectorType": "File & API",
	"connectorHost": "graph.microsoft.com",
	"connectorPort": "443",
	"connectorAuthType": 14,
	"oauthClientId": "12345678-1234-1234-1234-123456789012",
	"oauthClientSecret": "ABC~123...",
	"oauthRedirectUri": "https://databasin.yourcompany.com/oauth/callback",
	"oauthScopes": "Files.Read.All Sites.Read.All offline_access",
	"oauthAuthorizationUrl": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
	"oauthTokenUrl": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
	"oauthAutoRefresh": true,
	"connectorAdditionalDetails": "tenant=common",
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

**Required Scopes:**

- OneDrive: `Files.Read.All offline_access`
- SharePoint: `Sites.Read.All offline_access`
- Note: `offline_access` required for refresh tokens

**Setup Notes:**

- Register app in Azure Portal (App registrations)
- Add platform: Web with redirect URI
- Create client secret in Certificates & secrets
- Add API permissions for Microsoft Graph
- Replace `/common/` with `/YOUR_TENANT_ID/` for single-tenant apps

**4. Slack**

```json
{
	"connectorName": "Slack Workspace",
	"connectorType": "Collaboration",
	"connectorHost": "slack.com",
	"connectorPort": "443",
	"connectorAuthType": 14,
	"oauthClientId": "123456789012.123456789012",
	"oauthClientSecret": "abc123def456...",
	"oauthRedirectUri": "https://databasin.yourcompany.com/oauth/callback",
	"oauthScopes": "channels:read channels:history files:read",
	"oauthAuthorizationUrl": "https://slack.com/oauth/v2/authorize",
	"oauthTokenUrl": "https://slack.com/api/oauth.v2.access",
	"oauthAutoRefresh": true,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

**Required Scopes:**

- Read channels: `channels:read channels:history`
- Read files: `files:read`
- Read users: `users:read`
- Note: Slack tokens don't expire by default (no refresh needed)

**Setup Notes:**

- Create app at api.slack.com/apps
- Add OAuth & Permissions → Redirect URLs
- Add Bot Token Scopes (not User Token Scopes)
- Install app to workspace

**5. HubSpot**

```json
{
	"connectorName": "HubSpot CRM",
	"connectorType": "CRM & ERP",
	"connectorHost": "api.hubapi.com",
	"connectorPort": "443",
	"connectorAuthType": 14,
	"oauthClientId": "12345678-1234-1234-1234-123456789012",
	"oauthClientSecret": "abc123-def456-ghi789",
	"oauthRedirectUri": "https://databasin.yourcompany.com/oauth/callback",
	"oauthScopes": "crm.objects.contacts.read crm.objects.companies.read crm.objects.deals.read",
	"oauthAuthorizationUrl": "https://app.hubspot.com/oauth/authorize",
	"oauthTokenUrl": "https://api.hubapi.com/oauth/v1/token",
	"oauthAutoRefresh": true,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

**Required Scopes:**

- Contacts: `crm.objects.contacts.read`
- Companies: `crm.objects.companies.read`
- Deals: `crm.objects.deals.read`
- Custom objects: `crm.objects.custom.read`

**Setup Notes:**

- Create app in HubSpot Developer Account
- Configure OAuth settings in app
- Add redirect URI
- Copy Client ID and Client Secret
- Tokens expire after 6 hours (auto-refresh required)

#### OAuth Troubleshooting

**1. "Invalid Client" Error**

```
✘ OAuth authorization failed
✘ Error: invalid_client
```

**Causes:**

- Wrong client ID or client secret
- Client ID/secret from wrong environment (dev vs prod)
- Spaces or newlines in credentials

**Fix:**

```bash
# Update with correct credentials
echo '{
  "oauthClientId": "correct_client_id",
  "oauthClientSecret": "correct_client_secret"
}' > /tmp/oauth_fix.json

databasin connectors update 789 /tmp/oauth_fix.json
rm /tmp/oauth_fix.json
```

**2. "Invalid Grant" Error**

```
✘ Connection test failed
✘ Error: invalid_grant
```

**Causes:**

- Authorization code expired (used after 10 minutes)
- Refresh token revoked by user
- Refresh token expired
- Provider changed security settings

**Fix:**

- User must re-authorize the connector
- Click the new authorization URL provided
- Complete OAuth flow again

**3. "Redirect URI Mismatch" Error**

```
✘ OAuth authorization failed
✘ Error: redirect_uri_mismatch
```

**Causes:**

- Redirect URI in connector doesn't match provider config
- Protocol mismatch (http vs https)
- Trailing slash difference
- Port number missing

**Fix:**

```bash
# Update redirect URI to match provider exactly
echo '{
  "oauthRedirectUri": "https://databasin.yourcompany.com/oauth/callback"
}' > /tmp/redirect_fix.json

databasin connectors update 789 /tmp/redirect_fix.json
rm /tmp/redirect_fix.json
```

**Also verify in provider:**

- Salesforce: Connected App → Callback URL
- Google: OAuth Client → Authorized redirect URIs
- Microsoft: App Registration → Redirect URIs

**4. "Insufficient Scope" Error**

```
✘ API request failed
✘ Error: insufficient_scope
```

**Causes:**

- Connector missing required OAuth scopes
- User didn't approve all scopes during authorization
- Provider added new required scopes

**Fix:**

```bash
# Update scopes and re-authorize
echo '{
  "oauthScopes": "api refresh_token offline_access full_scope_here"
}' > /tmp/scope_fix.json

databasin connectors update 789 /tmp/scope_fix.json
rm /tmp/scope_fix.json

# User must re-authorize to grant new scopes
databasin connectors test 789  # Will provide new auth URL
```

**5. "Token Expired" Error**

```
✘ Connection test failed
✘ Access token expired
✘ Refresh token failed
```

**Causes:**

- Refresh token expired
- Auto-refresh disabled
- Provider revoked tokens
- User revoked app access

**Fix:**

```bash
# Check auto-refresh is enabled
databasin connectors get 789 --json --fields oauthAutoRefresh

# If disabled, enable it
echo '{
  "oauthAutoRefresh": true
}' > /tmp/refresh_fix.json

databasin connectors update 789 /tmp/refresh_fix.json
rm /tmp/refresh_fix.json

# If refresh token expired, re-authorize
databasin connectors test 789  # Will provide auth URL
```

**6. "Access Denied" Error**

```
✘ OAuth authorization failed
✘ Error: access_denied
```

**Causes:**

- User clicked "Deny" during authorization
- User lacks permission to grant scopes
- Admin restrictions on OAuth apps

**Fix:**

- User must click authorization URL again and approve
- For enterprise apps: Contact admin to allow OAuth app
- Check user has permission to grant requested scopes

#### CLI Commands for OAuth

**Create OAuth Connector:**

```bash
# Create connector with OAuth config
databasin connectors create salesforce_oauth.json -p proj-001

# Output includes authorization URL
# User must visit URL to complete setup
```

**Check OAuth Status:**

```bash
# View OAuth token status
databasin connectors get 789 --json --fields oauthAccessToken,oauthRefreshToken,oauthTokenExpiry

# Test connection (triggers refresh if needed)
databasin connectors test 789
```

**Manual Token Refresh:**

```bash
# Force token refresh
databasin connectors refresh-token 789

# Output:
# ✔ Token refreshed successfully
# ℹ New access token expires in: 2h 0m
```

**Handle Re-authorization:**

```bash
# When refresh token expires
databasin connectors test 789

# Output includes new auth URL:
# ⚠ Re-authorization Required
# Visit: https://provider.com/oauth/authorize?...

# After user authorizes, test again
databasin connectors test 789

# ✔ Connection test successful
# ✔ New tokens stored
```

**Update OAuth Configuration:**

```bash
# Update client credentials
echo '{
  "oauthClientId": "new_client_id",
  "oauthClientSecret": "new_client_secret"
}' > /tmp/oauth_update.json

databasin connectors update 789 /tmp/oauth_update.json
rm /tmp/oauth_update.json

# User must re-authorize after credential change
databasin connectors test 789
```

**Enable/Disable Auto-Refresh:**

```bash
# Enable automatic token refresh
echo '{"oauthAutoRefresh": true}' > /tmp/enable_refresh.json
databasin connectors update 789 /tmp/enable_refresh.json
rm /tmp/enable_refresh.json

# Disable automatic token refresh
echo '{"oauthAutoRefresh": false}' > /tmp/disable_refresh.json
databasin connectors update 789 /tmp/disable_refresh.json
rm /tmp/disable_refresh.json
```

#### OAuth Best Practices

**1. Always Enable Auto-Refresh**

```json
{
	"oauthAutoRefresh": true
}
```

**2. Request Minimal Scopes**

```
Only request scopes you actually need:
✓ Good: "api refresh_token"
✗ Bad: "api refresh_token full_access admin"
```

**3. Store Client Secrets Securely**

```bash
# Use environment variables
export SALESFORCE_CLIENT_SECRET="abc123..."

# Reference in connector creation
echo "{
  \"oauthClientId\": \"3MVG9...\",
  \"oauthClientSecret\": \"$SALESFORCE_CLIENT_SECRET\"
}" > salesforce_oauth.json
```

**4. Monitor Token Expiry**

```bash
# Check token expiry regularly
databasin connectors get 789 --json --fields oauthTokenExpiry

# Alert users 7 days before refresh token expires
```

**5. Use Separate Connectors per Environment**

```
Salesforce Production (OAuth)  → prod.salesforce.com
Salesforce Sandbox (OAuth)     → test.salesforce.com
Salesforce Dev (OAuth)         → dev.salesforce.com
```

**6. Keep Authorization URLs Accessible**

```
After creating OAuth connector:
- Save authorization URL
- Share with authorized users
- Include in onboarding docs
- Keep for re-authorization needs
```

**7. Handle Re-authorization Gracefully**

```
Monitor for refresh token expiry:
- Set up alerts
- Notify users in advance
- Provide self-service re-auth link
- Document re-auth process
```

#### OAuth Security Considerations

**1. Redirect URI Validation**

- Always use HTTPS (not HTTP)
- Match provider configuration exactly
- Don't use wildcards
- Validate in both connector and provider

**2. Client Secret Protection**

- Never commit to version control
- Use environment variables
- Rotate secrets periodically
- Don't log or display secrets

**3. Token Storage**

- Databasin stores tokens encrypted
- Tokens never shown in CLI output
- Access tokens auto-refreshed
- Refresh tokens protected

**4. Scope Limitations**

- Request minimal required scopes
- Document why each scope is needed
- Review scopes periodically
- Remove unused scopes

**5. Token Expiry Monitoring**

- Track access token expiry
- Alert on refresh token expiry
- Implement re-auth notifications
- Log token refresh events

## Integration Workflows

### End-to-End: MySQL to Snowflake Daily Sync

This workflow demonstrates how connectors integrate with pipelines and automations to create a complete ETL solution. The connectors skill handles Parts 1-3 (connector creation and testing). Parts 4-6 are covered by the **databasin-pipelines** and **databasin-automations** skills.

**Complete Workflow Reference:** See `CROSS-SKILL-WORKFLOW-EXAMPLE.md` for the full end-to-end example including pipeline and automation setup.

**Workflow Overview:**

```
MySQL Connector → Pipeline (Extract/Transform/Load) → Snowflake Connector → Automation (Schedule/Monitor)
```

**This Section Covers:** Creating and testing source and target connectors (connector-specific tasks only).

---

#### Part 1: Create Source Connector (MySQL)

**Step 1: Create MySQL Connector Configuration**

Create file: `mysql-source-connector.json`

```json
{
	"connectorName": "MySQL Orders Source",
	"connectorType": "RDBMS",
	"connectorHost": "mysql.example.com",
	"connectorPort": "3306",
	"connectorDatabaseName": "ecommerce_prod",
	"connectorUsername": "databasin_reader",
	"connectorPassword": "your_secure_password",
	"connectorAuthType": 2,
	"connectorAdditionalDetails": "useSSL=true&sslMode=REQUIRED&connectTimeout=30",
	"connectorMaxConnections": 10,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

**Important Fields:**

- `connectorType`: "RDBMS" for MySQL databases
- `connectorAuthType`: 2 (Basic authentication)
- `connectorAdditionalDetails`: SSL settings and timeouts
- `connectorMaxConnections`: Connection pool size (10 recommended for source connectors)

**Step 2: Create the MySQL Connector**

```bash
databasin connectors create mysql-source-connector.json -p proj-001
```

**Expected Output:**

```
✔ Connector created successfully
✔ Connector ID: 123

┌─────────────────────┬──────────────────────────┐
│ Field               │ Value                    │
├─────────────────────┼──────────────────────────┤
│ connectorID         │ 123                      │
│ connectorName       │ MySQL Orders Source      │
│ connectorType       │ RDBMS                    │
│ connectorHost       │ mysql.example.com        │
│ connectorPort       │ 3306                     │
│ status              │ active                   │
└─────────────────────┴──────────────────────────┘
```

**Important:** Save the connector ID (123) - you'll need it when creating the pipeline.

---

#### Part 2: Create Target Connector (Snowflake)

**Step 1: Create Snowflake Connector Configuration**

Create file: `snowflake-target-connector.json`

```json
{
	"connectorName": "Snowflake Analytics Warehouse",
	"connectorType": "Big Data & NoSQL",
	"connectorHost": "xy12345.us-east-1.snowflakecomputing.com",
	"connectorPort": "443",
	"connectorDatabaseName": "ANALYTICS_DB",
	"connectorUsername": "DATABASIN_LOADER",
	"connectorPassword": "your_snowflake_password",
	"connectorAuthType": 2,
	"connectorAdditionalDetails": "warehouse=COMPUTE_WH&schema=ORDERS&role=DATA_LOADER_ROLE&authenticator=snowflake",
	"connectorMaxConnections": 8,
	"institutionID": 1,
	"internalID": "proj-001",
	"ownerID": 456
}
```

**Important Fields:**

- `connectorType`: "Big Data & NoSQL" for Snowflake
- `connectorHost`: Full Snowflake account URL
- `connectorAdditionalDetails`: Warehouse, schema, role, and authenticator settings
- `connectorMaxConnections`: 8 recommended for target connectors (lower than source to avoid overload)

**Snowflake-Specific Notes:**

- `warehouse`: Virtual warehouse to use for loading (must be running)
- `schema`: Target schema for tables
- `role`: Role with INSERT/CREATE permissions
- `authenticator`: "snowflake" for username/password auth

**Step 2: Create the Snowflake Connector**

```bash
databasin connectors create snowflake-target-connector.json -p proj-001
```

**Expected Output:**

```
✔ Connector created successfully
✔ Connector ID: 456

┌─────────────────────┬──────────────────────────────────────────┐
│ Field               │ Value                                    │
├─────────────────────┼──────────────────────────────────────────┤
│ connectorID         │ 456                                      │
│ connectorName       │ Snowflake Analytics Warehouse            │
│ connectorType       │ Big Data & NoSQL                         │
│ connectorHost       │ xy12345.us-east-1.snowflakecomputing.com │
│ connectorPort       │ 443                                      │
│ status              │ active                                   │
└─────────────────────┴──────────────────────────────────────────┘
```

**Important:** Save the connector ID (456) - you'll need it when creating the pipeline.

---

#### Part 3: Test Both Connectors

**Step 1: Test MySQL Source Connector**

```bash
databasin connectors test 123
```

**Expected Output (~5-10 seconds):**

```
✔ Connection test successful
✔ Database: ecommerce_prod
✔ Tables discovered: 12
✔ Sample query: Successfully retrieved rows
ℹ Connection pool: 10 connections available
```

**Troubleshooting MySQL:**

- ❌ "Connection refused" → Check firewall rules and `connectorHost:connectorPort`
- ❌ "Authentication failed" → Verify `connectorUsername` and `connectorPassword`
- ❌ "Database not found" → Check `connectorDatabaseName` spelling
- ❌ "SSL error" → Adjust SSL settings in `connectorAdditionalDetails`

**Step 2: Test Snowflake Target Connector**

```bash
databasin connectors test 456
```

**Expected Output (~10-15 seconds):**

```
✔ Connection test successful
✔ Warehouse: COMPUTE_WH (running)
✔ Database/Schema: ANALYTICS_DB.ORDERS
✔ Write permissions: Verified
✔ Sample write test: Successfully wrote and deleted test row
ℹ Connection pool: 8 connections available
```

**Troubleshooting Snowflake:**

- ❌ "Invalid account identifier" → Check `connectorHost` format
- ❌ "Warehouse not found" → Verify warehouse name in `connectorAdditionalDetails` and ensure it's running
- ❌ "Insufficient privileges" → Check role has USAGE on warehouse and CREATE TABLE on schema
- ❌ "Network error" → Check Snowflake network policy allows your IP

**Success Criteria:**
Both connectors should show:

- ✔ Connection test successful
- ✔ Database/warehouse accessible
- ✔ Appropriate permissions verified

---

#### Next Steps: Pipeline and Automation Setup

**Connectors are now ready to use in pipelines!**

The next steps involve creating a pipeline that uses these connectors:

1. **Create Pipeline** - Define extract/transform/load logic using connector IDs 123 (source) and 456 (target)
2. **Add Pipeline Artifacts** - Configure source table (MySQL orders) and target table (Snowflake orders)
3. **Test Pipeline** - Run manual test to verify data flow
4. **Create Automation** - Schedule daily runs with notifications

**Reference the following skills for next steps:**

- **databasin-pipelines skill** - Create pipeline with these connector IDs
- **databasin-automations skill** - Schedule automated daily runs

**Complete Workflow Example:**
See `CROSS-SKILL-WORKFLOW-EXAMPLE.md` for the full end-to-end implementation including:

- Pipeline configuration with transformations
- Column mappings and data quality rules
- Automation scheduling with cron expressions
- Monitoring and error handling

**Quick Preview - Pipeline Creation (next step):**

```bash
# After creating connectors 123 and 456, create a pipeline:
databasin pipelines create pipeline-config.json

# Pipeline config references connector IDs:
{
  "sourceConnectorId": "123",   # MySQL connector from Part 1
  "targetConnectorId": "456",   # Snowflake connector from Part 2
  "syncMode": "incremental",
  ...
}
```

## Authentication

### CLI Authentication

All operations require authentication via the Databasin CLI.

**Initial Setup:**

```bash
# One-time login
databasin login

# Enter credentials when prompted
# JWT token stored in ~/.databasin/auth.json
```

**Token Management:**

- CLI automatically refreshes expired tokens
- No manual token file management required
- Authentication persists across sessions

**Troubleshooting:**

If you get authentication errors:

```bash
# Re-authenticate
databasin login

# Verify authentication
databasin connectors list -p <project>
```

### Databasin API Skill Integration

This skill works seamlessly with the `databasin-api` skill for deeper API understanding.

**When to reference databasin-api skill:**

- Understanding endpoint payloads
- Learning about new API features
- Troubleshooting complex API errors
- Checking token efficiency warnings

## Configuration Defaults

### Required Organizational Fields

Always require from user:

- `institutionID` - Organization identifier (number)
- `internalID` - Project identifier (string)
- `ownerID` - User identifier (number)

**How to get these:**

```bash
# List projects to find IDs
databasin projects list --full --json

# Output shows:
# - institutionID
# - internalID (project ID)
# - ownerID
```

### Connector Type Selection

**Guide users to correct type:**

| User Needs          | Connector Type           |
| ------------------- | ------------------------ |
| SQL Database        | RDBMS                    |
| Cloud file storage  | File & API               |
| REST API            | File & API (Generic API) |
| NoSQL database      | Big Data & NoSQL         |
| CRM/ERP system      | CRM & ERP                |
| Marketing platform  | Marketing                |
| E-commerce platform | E-Commerce               |
| Accounting software | Accounting               |
| Collaboration tool  | Collaboration            |
| AI/LLM service      | AI & LLM                 |

**Reference:** `references/connector-types-guide.md`

### Authentication Type Selection

**Common patterns:**

| Connector                     | Auth Type                   |
| ----------------------------- | --------------------------- |
| MySQL, PostgreSQL, SQL Server | 2 (Basic)                   |
| Amazon S3                     | 7 (S3 Access Key)           |
| ADLS (Access Key)             | 3 (Azure Access Key)        |
| ADLS (Service Principal)      | 5 (Azure Service Principal) |
| SFTP                          | 12 (Password)               |
| Salesforce                    | 2 (Basic) + securityToken   |
| Generic API (Key)             | 8 (API Key)                 |
| Generic API (Bearer)          | 20 (Bearer Token)           |
| Public API                    | 22 (None)                   |

**Reference:** `references/authentication-guide.md`

## Validation and Error Handling

### Automatic Validation

**The CLI validates automatically during creation:**

```bash
# Validation happens automatically
databasin connectors create config.json -p proj-001

# If validation fails, you'll see:
✘ Failed to create connector
✘ Invalid connector configuration
  Error: Missing required field: connectorHost
  Suggestion: Check the connector configuration schema
```

**Common Validation Errors:**

1. **Missing Required Fields**

   ```
   Error: Missing required field: connectorHost
   Fix: Add connectorHost to configuration
   ```

2. **Invalid Connector Type**

   ```
   Error: Invalid connector type
   Fix: Use exact type from categories (case-sensitive)
   ```

3. **Invalid Port Number**

   ```
   Error: connectorPort must be 1-65535
   Fix: Provide valid port number
   ```

4. **Missing Authentication**
   ```
   Warning: This connector requires authentication
   Fix: Add connectorUsername and connectorPassword
   ```

### Connection Testing

**Always test after creation:**

```bash
databasin connectors test <connector_id>
```

**Common Connection Errors:**

1. **Authentication Failed**

   ```
   ✘ Connection test failed
   ✘ Authentication failed: Invalid credentials

   Fix: Update credentials
   echo '{"connectorUsername":"correct_user","connectorPassword":"correct_pass"}' > fix.json
   databasin connectors update <id> fix.json
   ```

2. **Host Unreachable**

   ```
   ✘ Connection test failed
   ✘ Connection timeout: Unable to reach host

   Cause: Network/firewall issue or wrong host
   Fix: Verify host and check network connectivity
   ```

3. **Database Not Found**

   ```
   ✘ Connection test failed
   ✘ Database not found: Unknown database 'analytics'

   Cause: Wrong database name
   Fix: Update database name
   echo '{"connectorDatabaseName":"correct_db"}' > fix.json
   databasin connectors update <id> fix.json
   ```

### CLI Error Messages

The CLI provides context-aware error messages:

**404 Not Found:**

```
✘ Connector not found (404)
  Connector ID: 123
  Suggestion: Run 'databasin connectors list --full' to see available connectors
```

**403 Access Denied:**

```
✘ Access denied (403)
  Connector ID: 456
  Suggestion: You don't have permission to access this connector
```

**Network Errors:**

```
✘ Error testing connector
✘ Network error: Unable to connect to API
  Suggestion: Check your internet connection and try again
```

## Best Practices

### 1. Security

- **Never log credentials** - CLI automatically redacts passwords in output
- **Use environment variables** - Store sensitive values outside config files
- **Rotate credentials regularly** - Update passwords periodically
- **Use service accounts** - Don't use personal credentials

**Secure credential updates:**

```bash
# Use environment variables
echo "{
  \"connectorUsername\": \"$DB_USER\",
  \"connectorPassword\": \"$DB_PASS\"
}" > /tmp/secure_creds.json

databasin connectors update 123 /tmp/secure_creds.json

# Immediately remove temp file
rm /tmp/secure_creds.json
```

### 2. Naming Conventions

**Recommend:**

```
[System] [Environment] [Purpose]

Examples:
- "MySQL Production Analytics"
- "S3 Staging Data Lake"
- "Snowflake Dev Warehouse"
- "Salesforce Production CRM"
```

### 3. Connection Pooling

**Default:** 8 connections

**Adjust based on usage:**

- Low volume: 4-8 connections
- Medium volume: 8-16 connections
- High volume: 16-20 connections
- Don't exceed 100 (performance issues)

**Configuration:**

```json
{
	"connectorMaxConnections": 16
}
```

### 4. Additional Parameters

**Common use cases:**

```json
{
	"connectorAdditionalDetails": "ssl=true&connectTimeout=30000"
}
```

**Examples:**

- SSL/TLS: `ssl=true&sslmode=require`
- Timeouts: `connectTimeout=30000&queryTimeout=60000`
- Compression: `useCompression=true`
- Region (S3): `region=us-west-2`

### 5. Environment Management

**Separate connectors per environment:**

```
MySQL Production (ID: 123)
MySQL Staging (ID: 456)
MySQL Development (ID: 789)
```

**Benefits:**

- Isolated credentials
- Different connection limits
- Environment-specific settings
- Safer testing

## Token Efficiency

### CLI Optimization Features

The CLI includes built-in token efficiency:

**1. Count Mode (Default)**

```bash
# Only returns count, not full objects
databasin connectors list -p proj-001

# Output: Total connectors: 23
# Tokens used: ~100 (vs ~50,000 for full objects)
```

**2. Field Filtering**

```bash
# Return only specific fields
databasin connectors list -p proj-001 --full --fields connectorID,connectorName,connectorType

# Reduces token usage by 80%+
```

**3. Result Limiting**

```bash
# Limit number of results
databasin connectors list -p proj-001 --full --limit 10

# Only fetch what you need
```

**4. Automatic Warnings**

```
⚠ Token Usage Warning
  Response size: 125,432 characters
  Exceeds threshold: 100,000 characters

  Optimization suggestions:
  - Use count mode (default) to get count only
  - Use --fields to limit displayed fields
  - Use --limit to reduce number of results
  - Use --project to filter by project
```

### Best Practices for Token Efficiency

1. **Always use count mode first**

   ```bash
   # Check count before fetching full objects
   databasin connectors list -p proj-001
   ```

2. **Use field filtering**

   ```bash
   # Only fetch fields you need
   databasin connectors list -p proj-001 --full --fields connectorID,connectorName,status
   ```

3. **Filter by project**

   ```bash
   # Always specify project ID
   databasin connectors list -p proj-001
   ```

4. **Use pagination**
   ```bash
   # Fetch in batches
   databasin connectors list -p proj-001 --full --limit 20
   ```

## Output Formats

### Table Format (Default)

**List output:**

```
✔ Total connectors: 23

⚠ Use --full to fetch full connector objects
ℹ Filtered by project: proj-001
```

**Get output:**

```
✔ Connector retrieved

┌─────────────────────┬──────────────────────────┐
│ Field               │ Value                    │
├─────────────────────┼──────────────────────────┤
│ connectorID         │ 123                      │
│ connectorName       │ MySQL Production         │
│ connectorType       │ RDBMS                    │
│ connectorHost       │ mysql.example.com        │
│ connectorPort       │ 3306                     │
│ status              │ active                   │
└─────────────────────┴──────────────────────────┘
```

### JSON Format

```bash
databasin connectors get 123 --json
```

Output:

```json
{
	"connectorID": 123,
	"connectorName": "MySQL Production",
	"connectorType": "RDBMS",
	"connectorHost": "mysql.example.com",
	"connectorPort": "3306",
	"connectorDatabaseName": "analytics",
	"status": "active"
}
```

### CSV Format

```bash
databasin connectors list -p proj-001 --full --csv
```

Output:

```csv
connectorID,connectorName,connectorType,status
123,MySQL Production,RDBMS,active
456,S3 Data Lake,File & API,active
789,Snowflake Warehouse,Big Data & NoSQL,active
```

<!--
## CLI Configuration (PLANNED - NOT YET IMPLEMENTED)

⚠️ NOTE: The `databasin config ...` commands documented below are planned functionality
but have NOT been implemented in the current CLI version. Do not attempt to use these
commands as they will fail. This section is preserved for future reference.

### Global Configuration File

Location: `~/.databasin/config.json`

**Example:**
```json
{
  "output": {
    "format": "table",
    "colors": true
  },
  "tokenEfficiency": {
    "warnThreshold": 100000
  },
  "defaults": {
    "project": "proj-001"
  }
}
```

**Set defaults:**
```bash
# Set default project
databasin config set defaults.project proj-001

# Set default output format
databasin config set output.format json

# Disable colors
databasin config set output.colors false
```
-->

## Troubleshooting

### Common Issues

**1. Authentication Errors**

```
✘ Error: Unauthorized (401)

Solution:
databasin login
```

**2. Connector Not Found**

```
✘ Connector not found (404)

Solutions:
- Verify connector ID
- Check if you have access to the project
- Run: databasin connectors list -p <project> --full
```

**3. Validation Errors**

```
✘ Invalid connector configuration

Solutions:
- Check required fields in references/field-reference.md
- Verify connector type matches template
- Ensure authentication fields are correct
```

**4. Connection Test Failures**

```
✘ Connection test failed

Solutions:
- Verify credentials are correct
- Check network connectivity
- Confirm firewall allows connections
- Validate host and port
- Check database/bucket name
```

**5. Large Response Warnings**

```
⚠ Token Usage Warning

Solutions:
- Use count mode: databasin connectors list -p <project>
- Use field filtering: --fields connectorID,connectorName
- Use result limiting: --limit 20
- Filter by project: -p <project>
```

## When to Use Other Skills

**Use `databasin-api` skill when:**

- Need API endpoint details
- Understanding token efficiency
- Troubleshooting API errors
- Learning about API capabilities

**Use `databasin-pipelines` skill when:**

- Creating pipelines with connectors
- Managing pipeline artifacts
- Pipeline scheduling
- Connector usage in pipelines

**Use `echart-report-builder` skill when:**

- Creating reports from connector data
- Building dashboards
- Analyzing connector datasets
- Visualizing connection metrics

## Summary

This skill enables complete connector lifecycle management through natural language:

1. **Create** - Guide users through connector creation with automatic validation
2. **Modify** - Update settings and credentials via JSON files
3. **Test** - Verify connections work properly with detailed error reporting
4. **Delete** - Safely remove connectors with confirmation and dependency warnings
5. **Explore** - Discover available connector types via reference documentation
6. **Troubleshoot** - Diagnose and fix connection issues with context-aware guidance

Always:

- Use CLI commands for all operations
- Leverage automatic validation on creation
- Test connections after creation or updates
- Provide clear, actionable error messages
- Reference documentation for connector types and auth methods
- Optimize for token efficiency (count mode, field filtering, project filtering)
- Guide users to appropriate output formats (--json, --csv, table)
- Prioritize security (never log credentials, use temp files, clean up)

The goal is to make connector management simple, safe, and efficient through conversational interaction powered by the Databasin CLI.
