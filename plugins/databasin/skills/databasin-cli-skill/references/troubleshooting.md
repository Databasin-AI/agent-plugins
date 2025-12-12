# Databasin CLI Troubleshooting Guide

Comprehensive guide for diagnosing and resolving common issues when using the Databasin CLI.

## General Troubleshooting Workflow

When encountering any issue, follow this systematic approach:

```bash
# 1. Enable debug mode
export DATABASIN_DEBUG=true

# 2. Verify authentication
databasin auth whoami
databasin auth verify

# 3. Check the specific resource
databasin <resource-type> get <resource-id>

# 4. Review logs
databasin <resource-type> logs <resource-id>

# 5. Test connectivity (for connectors)
databasin sql exec <connector-id> "SELECT 1"
```

## Authentication Issues

### Error: "Token expired" or "Unauthorized"

**Symptoms:**
- CLI returns 401 Unauthorized errors
- Commands fail with authentication errors
- `databasin auth verify` returns false

**Diagnosis:**
```bash
databasin auth verify
```

**Solution:**
```bash
# Re-authenticate via browser
databasin auth login

# Verify successful login
databasin auth whoami

# If issues persist, check token file
cat ~/.databasin/.token
```

**Prevention:**
- Tokens typically expire after a period of inactivity
- Set up automatic re-authentication in scripts
- Use long-lived tokens for automated workflows

### Error: "Cannot connect to API"

**Symptoms:**
- Network connection errors
- Timeouts
- "Cannot reach server" messages

**Diagnosis:**
```bash
# Check API endpoint
echo $DATABASIN_API_URL

# Test connectivity
curl -I ${DATABASIN_API_URL:-http://localhost:9000}/health
```

**Solution:**
```bash
# Verify correct API URL
export DATABASIN_API_URL="https://api.databasin.com"

# Check network/firewall settings
# Verify VPN connection if required
```

## Connector Issues

### Error: "Connector not found"

**Symptoms:**
- Commands return 404 Not Found
- Connector ID doesn't exist

**Diagnosis:**
```bash
# List all available connectors
databasin connectors list

# Search by name
databasin connectors list --json | jq '.[] | select(.name | contains("production"))'
```

**Solution:**
```bash
# Use correct connector ID from the list
databasin connectors get <correct-id>

# If connector doesn't exist, create it
databasin connectors create connector-config.json
```

### Error: "Connection failed" or "Cannot connect to database"

**Symptoms:**
- SQL execution fails
- Connector status shows "failed"
- Connection timeout errors

**Diagnosis:**
```bash
# Get connector details
databasin connectors get <connector-id>

# Test basic connectivity
databasin sql exec <connector-id> "SELECT 1"

# Enable debug mode
DATABASIN_DEBUG=true databasin sql exec <connector-id> "SELECT 1"
```

**Common Causes & Solutions:**

#### 1. Wrong Credentials
```json
{
  "name": "My Database",
  "type": "postgres",
  "config": {
    "host": "db.example.com",
    "port": 5432,
    "database": "production",
    "username": "correct_username",  // ← Check this
    "password": "correct_password",  // ← And this
    "ssl": true
  }
}
```

Solution:
```bash
# Update connector with correct credentials
databasin connectors update <connector-id> updated-config.json
```

#### 2. Network/Firewall Issues
- Verify host is reachable: `ping db.example.com`
- Check port is open: `telnet db.example.com 5432`
- Verify firewall rules allow Databasin IP addresses
- Check VPN requirements

#### 3. SSL/TLS Issues
```json
{
  "config": {
    "ssl": true,
    "sslmode": "require",  // Try "verify-full" or "prefer"
    "sslrootcert": "/path/to/ca-cert.pem"  // If needed
  }
}
```

#### 4. Wrong Database/Schema
```bash
# Verify database exists
databasin sql exec <connector-id> "SELECT current_database()"

# List available catalogs
databasin sql catalogs <connector-id>
```

### Error: "Permission denied" on SQL Execution

**Symptoms:**
- Can connect but cannot query tables
- "Access denied" errors
- "Insufficient privileges" messages

**Diagnosis:**
```bash
# Test basic SELECT permission
databasin sql exec <connector-id> "SELECT 1"

# Check current user
databasin sql exec <connector-id> "SELECT current_user"

# List accessible schemas
databasin sql schemas <connector-id>
```

**Solution:**
```sql
-- Grant necessary permissions on the database side
GRANT SELECT ON ALL TABLES IN SCHEMA public TO databasin_user;
GRANT USAGE ON SCHEMA public TO databasin_user;

-- For specific table
GRANT SELECT ON TABLE users TO databasin_user;
```

## Pipeline Issues

### Error: "Pipeline execution failed"

**Symptoms:**
- Pipeline runs but completes with errors
- Data not transferred
- Partial data transfer

**Diagnosis:**
```bash
# Get pipeline details
databasin pipelines get <pipeline-id>

# Review logs - MOST IMPORTANT STEP
databasin pipelines logs <pipeline-id>

# Check recent error logs only
databasin pipelines logs <pipeline-id> --level error

# Get source connector status
databasin connectors get <source-connector-id>

# Get target connector status
databasin connectors get <target-connector-id>
```

**Common Causes & Solutions:**

#### 1. Source Data Issues
```bash
# Check if source table exists
databasin sql tables <source-connector-id> --catalog <cat> --schema <schema>

# Sample source data
databasin sql exec <source-connector-id> "SELECT * FROM source_table LIMIT 5"

# Check for NULL values that might cause issues
databasin sql exec <source-connector-id> "
  SELECT 
    COUNT(*) as total,
    COUNT(*) - COUNT(required_column) as nulls
  FROM source_table
"
```

#### 2. Transformation Errors
```json
{
  "transformations": [
    {
      "type": "map",
      "fields": {
        "target_col": "CAST(source_col AS INTEGER)"  // ← May fail if data isn't numeric
      }
    }
  ]
}
```

Solution: Add data validation
```json
{
  "transformations": [
    {
      "type": "filter",
      "condition": "source_col IS NOT NULL AND source_col ~ '^[0-9]+$'"
    },
    {
      "type": "map",
      "fields": {
        "target_col": "CAST(source_col AS INTEGER)"
      }
    }
  ]
}
```

#### 3. Schema Mismatch
```bash
# Compare schemas
databasin sql exec <source-connector-id> "
  SELECT column_name, data_type 
  FROM information_schema.columns 
  WHERE table_name = 'source_table'
" --csv > source_schema.csv

databasin sql exec <target-connector-id> "
  SELECT column_name, data_type 
  FROM information_schema.columns 
  WHERE table_name = 'target_table'
" --csv > target_schema.csv

diff source_schema.csv target_schema.csv
```

Solution: Update pipeline to map columns correctly
```json
{
  "transformations": [
    {
      "type": "map",
      "fields": {
        "target_id": "source_user_id",
        "target_name": "CONCAT(source_first_name, ' ', source_last_name)",
        "target_email": "source_email_address"
      }
    }
  ]
}
```

#### 4. Target Constraints
```bash
# Check for constraint violations in logs
databasin pipelines logs <pipeline-id> | grep -i "constraint\|unique\|foreign key"

# Test with small batch first
# Modify pipeline to process fewer records initially
```

### Error: "Pipeline not running on schedule"

**Symptoms:**
- Pipeline should run automatically but doesn't
- Schedule appears correct but no executions
- Manual runs work fine

**Diagnosis:**
```bash
# Get pipeline configuration
databasin pipelines get <pipeline-id> --json | jq '.schedule'

# Check pipeline status
databasin pipelines get <pipeline-id> --json | jq '.status'

# Review recent runs
databasin pipelines list --project <project-id> --json | \
  jq '.[] | select(.id=="<pipeline-id>") | .lastRun'
```

**Solution:**
```bash
# Verify schedule is enabled
# Check if pipeline is in "active" status
# Review system time zone settings

# Update schedule if needed
cat > updated-pipeline.json << 'EOF'
{
  "schedule": "0 6 * * *",  // 6 AM daily
  "enabled": true
}
EOF

databasin pipelines update <pipeline-id> updated-pipeline.json
```

## Project & Permission Issues

### Error: "Project not found"

**Symptoms:**
- Cannot access project
- Project ID returns 404

**Diagnosis:**
```bash
# List all accessible projects
databasin projects list

# Check if using correct project ID
databasin projects list --json | jq '.[] | {id, name}'
```

**Solution:**
```bash
# Use correct project ID from list
PROJECT_ID=$(databasin projects list --json | jq -r '.[] | select(.name=="My Project") | .id')
databasin pipelines list --project $PROJECT_ID
```

### Error: "Insufficient permissions"

**Symptoms:**
- Cannot create/update/delete resources
- "Access denied" on certain operations
- Can view but cannot modify

**Diagnosis:**
```bash
# Check your permissions in the project
databasin projects users <project-id>

# Verify your user
databasin auth whoami
```

**Solution:**
- Contact project administrator to grant appropriate permissions
- Verify you're using the correct account
- Check if you need to be added to the project team

## SQL Query Issues

### Error: "Syntax error in SQL"

**Symptoms:**
- SQL execution fails
- Parser errors
- Invalid query messages

**Diagnosis:**
```bash
# Test simple query first
databasin sql exec <connector-id> "SELECT 1"

# Test table access
databasin sql exec <connector-id> "SELECT * FROM table_name LIMIT 1"

# Enable debug mode
DATABASIN_DEBUG=true databasin sql exec <connector-id> "<query>"
```

**Common Mistakes:**

#### 1. Wrong SQL Dialect
```sql
-- PostgreSQL-specific (won't work on MySQL)
SELECT * FROM users WHERE email ILIKE '%example%';

-- Use LIKE for MySQL
SELECT * FROM users WHERE LOWER(email) LIKE '%example%';
```

#### 2. Unescaped Quotes
```bash
# Wrong - shell interprets quotes
databasin sql exec conn-123 "SELECT * FROM users WHERE name = 'John'"

# Right - escape quotes
databasin sql exec conn-123 "SELECT * FROM users WHERE name = 'John'"
# Or use different quotes
databasin sql exec conn-123 'SELECT * FROM users WHERE name = "John"'
```

#### 3. Missing Schema Qualification
```sql
-- May fail if table isn't in default schema
SELECT * FROM users;

-- Better - specify schema
SELECT * FROM public.users;
```

### Error: "Table or view does not exist"

**Diagnosis:**
```bash
# List available catalogs
databasin sql catalogs <connector-id>

# List schemas
databasin sql schemas <connector-id> --catalog <catalog>

# List tables
databasin sql tables <connector-id> --catalog <catalog> --schema <schema>
```

**Solution:**
```sql
-- Use fully qualified name
SELECT * FROM catalog.schema.table_name;

-- Or set default schema in connector config
```

### Error: "Query timeout"

**Symptoms:**
- Long-running queries fail
- Connection drops during execution
- "Execution time exceeded" errors

**Diagnosis:**
```bash
# Check query execution plan
databasin sql exec <connector-id> "EXPLAIN <your_query>"

# Test with LIMIT
databasin sql exec <connector-id> "<your_query> LIMIT 10"
```

**Solutions:**

1. **Add proper indexes:**
```sql
-- Identify slow operations in EXPLAIN output
EXPLAIN ANALYZE SELECT * FROM large_table WHERE column = 'value';

-- Add index on frequently filtered columns
CREATE INDEX idx_column ON large_table(column);
```

2. **Optimize query:**
```sql
-- Bad - Full table scan
SELECT * FROM orders WHERE DATE(created_at) = '2024-01-01';

-- Good - Use indexed column directly
SELECT * FROM orders 
WHERE created_at >= '2024-01-01' 
  AND created_at < '2024-01-02';
```

3. **Break into smaller batches:**
```sql
-- Instead of one huge query
SELECT * FROM large_table;

-- Process in batches
SELECT * FROM large_table WHERE id BETWEEN 1 AND 10000;
SELECT * FROM large_table WHERE id BETWEEN 10001 AND 20000;
-- etc.
```

## Automation Issues

### Error: "Automation failed to execute"

**Diagnosis:**
```bash
# Get automation details
databasin automations get <automation-id>

# Review logs
databasin automations logs <automation-id>

# Check related resources (pipelines, connectors)
```

**Common Causes:**
- Dependent pipeline failed
- External API unavailable
- Condition not met for execution
- Configuration error

**Solution:**
```bash
# Test manually first
databasin automations run <automation-id>

# Review logs for specific error
databasin automations logs <automation-id> --level error

# Update configuration if needed
databasin automations update <automation-id> updated-config.json
```

## Performance Issues

### Slow Pipeline Execution

**Diagnosis:**
```bash
# Check pipeline logs for timing information
databasin pipelines logs <pipeline-id>

# Monitor individual steps
# Look for "execution_time" in logs
```

**Solutions:**

1. **Optimize source queries:**
```json
{
  "sourceQuery": "SELECT * FROM large_table WHERE status = 'active'",  // ← Add WHERE clause
  "batchSize": 1000  // ← Adjust batch size
}
```

2. **Add indexes:**
```sql
-- On source table
CREATE INDEX idx_status ON large_table(status);

-- On join columns
CREATE INDEX idx_foreign_key ON orders(customer_id);
```

3. **Use incremental loading:**
```json
{
  "sourceQuery": "SELECT * FROM orders WHERE created_at > :last_run_time",
  "incrementalField": "created_at"
}
```

4. **Parallel processing:**
```json
{
  "parallelism": 4,  // Process in parallel
  "batchSize": 5000   // Larger batches
}
```

### High Memory Usage

**Symptoms:**
- Pipeline fails with out-of-memory errors
- System becomes unresponsive
- Crashes during execution

**Solutions:**

1. **Reduce batch size:**
```json
{
  "batchSize": 500  // Smaller batches, more iterations
}
```

2. **Process incrementally:**
```json
{
  "incrementalField": "id",
  "incrementalValue": "last_processed_id"
}
```

3. **Stream instead of batch:**
```json
{
  "mode": "streaming",  // Process records as they come
  "bufferSize": 100
}
```

## Data Quality Issues

### Duplicate Records in Target

**Diagnosis:**
```bash
# Check for duplicates
databasin sql exec <target-connector-id> "
  SELECT 
    email, 
    COUNT(*) as count
  FROM users
  GROUP BY email
  HAVING COUNT(*) > 1
"
```

**Solutions:**

1. **Add unique constraint:**
```sql
ALTER TABLE users ADD CONSTRAINT unique_email UNIQUE (email);
```

2. **Use UPSERT in pipeline:**
```json
{
  "loadStrategy": "upsert",
  "upsertKey": ["email"]
}
```

3. **Deduplicate before load:**
```json
{
  "transformations": [
    {
      "type": "deduplicate",
      "keys": ["email"],
      "keepFirst": true
    }
  ]
}
```

### NULL Values Where Not Expected

**Diagnosis:**
```bash
# Find nulls
databasin sql exec <connector-id> "
  SELECT COUNT(*) - COUNT(email) as null_count
  FROM users
"
```

**Solutions:**

1. **Add filter:**
```json
{
  "transformations": [
    {
      "type": "filter",
      "condition": "email IS NOT NULL"
    }
  ]
}
```

2. **Provide defaults:**
```json
{
  "transformations": [
    {
      "type": "map",
      "fields": {
        "email": "COALESCE(email, 'unknown@example.com')"
      }
    }
  ]
}
```

## Emergency Procedures

### Pipeline Stuck in "Running" State

```bash
# Get pipeline status
databasin pipelines get <pipeline-id>

# Try to cancel (if supported)
databasin pipelines cancel <pipeline-id>

# If that doesn't work, contact support with:
# - Pipeline ID
# - Last known logs
# - Timeline of events
```

### Mass Connector Failure

```bash
# Check all connectors
for id in $(databasin connectors list --json | jq -r '.[].id'); do
  echo "Testing $id..."
  databasin sql exec $id "SELECT 1" 2>&1 | grep -q "success" && echo "✓ OK" || echo "✗ FAILED"
done

# Review error patterns
# Check for common causes (network outage, credentials rotated, etc.)
```

### Data Loss Concern

```bash
# Immediately:
# 1. Stop all pipelines
# 2. Document what happened
# 3. Check target database for records
databasin sql exec <target-connector-id> "
  SELECT COUNT(*) FROM target_table
  WHERE created_at >= '<time_of_concern>'
"

# 4. Review logs for the time period
databasin pipelines logs <pipeline-id> --since "<timestamp>"

# 5. Contact support if data actually lost
```

## Preventive Measures

### Regular Health Checks

```bash
#!/bin/bash
# health-check.sh

# Check authentication
databasin auth verify || { echo "Auth failed!"; exit 1; }

# Test all connectors
for id in $(databasin connectors list --json | jq -r '.[].id'); do
  databasin sql exec $id "SELECT 1" || echo "Connector $id failed"
done

# Check recent pipeline runs
databasin pipelines list --json | jq '.[] | select(.status=="failed")'
```

### Monitoring Script

```bash
#!/bin/bash
# monitor.sh

# Get failed pipelines from last 24 hours
FAILED=$(databasin pipelines list --json | \
  jq -r '.[] | select(.status=="failed" and .lastRun > (now - 86400)) | .id')

if [ -n "$FAILED" ]; then
  echo "Failed pipelines: $FAILED"
  # Send alert
fi
```

### Backup Critical Configurations

```bash
# Export all connector configs
mkdir -p backups
for id in $(databasin connectors list --json | jq -r '.[].id'); do
  databasin connectors get $id --json > "backups/connector-$id.json"
done

# Export all pipeline configs
for id in $(databasin pipelines list --json | jq -r '.[].id'); do
  databasin pipelines get $id --json > "backups/pipeline-$id.json"
done
```

## Getting Help

When all else fails:

1. **Gather diagnostic information:**
   ```bash
   databasin --version
   databasin auth whoami
   databasin <resource> get <id> --json
   databasin <resource> logs <id>
   ```

2. **Enable debug mode:**
   ```bash
   DATABASIN_DEBUG=true databasin <command>
   ```

3. **Document the issue:**
   - What were you trying to do?
   - What command did you run?
   - What error did you see?
   - What have you tried?

4. **Check documentation:**
   - GitHub repository: https://github.com/Databasin-AI/databasin-cli
   - Databasin platform docs

5. **Contact support:**
   - Provide all diagnostic information
   - Include relevant log excerpts
   - Describe business impact
