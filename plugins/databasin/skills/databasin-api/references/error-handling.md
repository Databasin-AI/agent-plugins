# Error Handling and Troubleshooting Guide

**Common errors, null responses, and how to fix them**

---

## HTTP Status Codes

### Success Codes

- **200** - OK (successful GET)
- **201** - Created (successful POST)
- **204** - No Content (successful DELETE)

---

### Client Error Codes

#### 400 - Bad Request

**Cause:** Malformed payload or missing required parameters

**Solutions:**

1. Check payload JSON syntax
2. Verify required fields are present
3. Consult **[working-endpoints.md](./working-endpoints.md)** for required parameters
4. Check **[deprecated-endpoints.md](./deprecated-endpoints.md)** for known issues

**Example:**

```bash
# ❌ Missing required parameter
bun run scripts/api-call.ts GET /api/automations
# Returns 400 or null

# ✅ Include required parameter
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do"
```

---

#### 401 - Unauthorized

**Cause:** Invalid or expired JWT token

**Solutions:**

1. Check `.token` file exists and contains valid JWT
2. Verify JWT hasn't expired (tokens expire after ~1 hour)
3. Ensure token is properly formatted (no extra whitespace)

**Example:**

```bash
# Check token file
cat .token

# Verify no extra whitespace
cat .token | wc -c

# Test with simple endpoint
bun run scripts/api-call.ts GET /api/ping
```

---

#### 404 - Not Found

**Cause:** Invalid endpoint path or resource doesn't exist

**Solutions:**

1. Verify endpoint path is correct
2. Check resource ID exists
3. Consult **[working-endpoints.md](./working-endpoints.md)** for valid endpoints

**Example:**

```bash
# ❌ Wrong endpoint path
bun run scripts/api-call.ts GET /api/project/123

# ✅ Correct path
bun run scripts/api-call.ts GET /api/my/projects
```

---

### Server Error Codes

#### 500 - Internal Server Error

**Cause:** Backend error (bug, database issue, etc.)

**Solutions:**

1. Check API logs (if you have access)
2. Try endpoint with minimal parameters
3. Report to backend team if persistent
4. Check **[deprecated-endpoints.md](./deprecated-endpoints.md)** for known backend bugs

**Example:**

```bash
# Some endpoints have serialization bugs
# See deprecated-endpoints.md for alternatives
```

---

## Null Responses

### Understanding Null Responses

Some Databasin endpoints return `null` instead of errors when:

- Required parameters are missing
- No data matches the query
- The endpoint expects specific filters

---

### --count with Null Responses

The `--count` option handles null responses correctly:

- **`null` or `undefined`** → Returns `{"count": 0}`
- **Array responses** → Returns `{"count": <array.length>}`
- **Object responses** → Returns `{"count": 1}`

**Example:**

```bash
# Without required parameter - returns null
bun run scripts/api-call.ts GET /api/automations --count
# Output: {"count": 0}

# With required parameter - returns data
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --count
# Output: {"count": 17}
```

---

### Troubleshooting Null Responses

**Step 1: Check if count returns 0**

```bash
bun run scripts/api-call.ts GET /api/automations --count
# {"count": 0} ← Null response or no data
```

**Step 2: Consult endpoint documentation**

```bash
# Check for required parameters
grep -A 20 "automations" references/working-endpoints.md
```

**Step 3: Add required parameters**

```bash
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --count
# {"count": 17} ← Data found!
```

---

## Endpoints Known to Require Parameters

### /api/automations

**Requires:** `internalID`

```bash
# ❌ Returns null
bun run scripts/api-call.ts GET /api/automations

# ✅ Returns data
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do"
```

---

### /api/pipeline

**Recommended:** `internalID` and/or `institutionID`

```bash
# ⚠️ May return incomplete data
bun run scripts/api-call.ts GET /api/pipeline

# ✅ Returns filtered data
bun run scripts/api-call.ts GET "/api/pipeline?internalID=N1r8Do"
```

---

### /api/connector

**Optional filters, but recommended for token efficiency**

```bash
# ⚠️ Returns 434 items = 200,000+ tokens
bun run scripts/api-call.ts GET /api/connector

# ✅ Filtered and efficient
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --count
```

---

### /api/lakebasin/connections

**Requires:** `projectId`

```bash
# ❌ Returns error
bun run scripts/api-call.ts GET /api/lakebasin/connections

# ✅ Returns data
bun run scripts/api-call.ts GET "/api/lakebasin/connections?projectId=42"
```

---

## Common Error Scenarios

### Scenario 1: "I get null for everything"

**Diagnosis:**

```bash
# Test with simple endpoint
bun run scripts/api-call.ts GET /api/ping

# If ping fails, check authentication
bun run scripts/api-call.ts GET /api/my/account
```

**Solutions:**

1. Check JWT token is valid
2. Verify `.token` file exists
3. Try with endpoint that requires no parameters

---

### Scenario 2: "Count returns 0 but I know data exists"

**Diagnosis:**

```bash
# Get your projects to find correct internalID
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalId
```

**Solutions:**

1. Verify you're using correct `internalID`
2. Check endpoint requires specific parameters
3. Consult **[working-endpoints.md](./working-endpoints.md)**

---

### Scenario 3: "Endpoint returns HTML error page"

**Cause:** Endpoint doesn't exist or has backend routing issue

**Solutions:**

1. Verify endpoint path in **[working-endpoints.md](./working-endpoints.md)**
2. Check **[deprecated-endpoints.md](./deprecated-endpoints.md)** for known broken endpoints
3. Try alternative endpoint if available

---

### Scenario 4: "Token usage is massive"

**Diagnosis:**

```bash
# Check how many items returned
bun run scripts/api-call.ts GET /api/connector --count
# {"count": 434} ← Very large!
```

**Solutions:**

1. Always use `--count` first
2. Apply filters (`internalID`, `institutionID`)
3. Use `--fields` and `--limit`
4. See **[token-efficiency.md](./token-efficiency.md)**

---

## Recommended Workflow for New Endpoints

### Step 1: Test with --count

```bash
bun run scripts/api-call.ts GET /api/new-endpoint --count
```

**If returns `{"count": 0}` → Missing required parameters**

---

### Step 2: Check Documentation

```bash
grep -A 20 "new-endpoint" references/working-endpoints.md
grep -A 20 "new-endpoint" references/deprecated-endpoints.md
```

---

### Step 3: Add Required Parameters

```bash
# Example: adding internalID
bun run scripts/api-call.ts GET "/api/new-endpoint?internalID=N1r8Do" --count
```

---

### Step 4: Get Summary

```bash
bun run scripts/api-call.ts GET "/api/new-endpoint?internalID=N1r8Do" --summary
```

---

### Step 5: Fetch What You Need

```bash
bun run scripts/api-call.ts GET "/api/new-endpoint?internalID=N1r8Do" \
  --fields=field1,field2 \
  --limit=25
```

---

## Debugging Tools

### Check API Connectivity

```bash
# Simplest endpoint
bun run scripts/api-call.ts GET /api/ping
```

---

### Verify Authentication

```bash
# Get your account details
bun run scripts/api-call.ts GET /api/my/account --fields=id,email
```

---

### Test Parameter Requirements

```bash
# Try without parameters
bun run scripts/api-call.ts GET /api/automations --count

# Try with parameters
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do" --count

# Compare results
```

---

### Validate internalID

```bash
# Get all valid internalIDs
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalId

# Use one to test
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --count
```

---

## Error Messages and Meanings

### "JWT token missing or invalid"

**Solution:** Check `.token` file contains valid JWT

---

### "Bad Request"

**Solution:** Check payload syntax and required parameters

---

### "Resource not found"

**Solution:** Verify resource ID and endpoint path

---

### "Forbidden"

**Solution:** Check permissions for resource access

---

## See Also

- **[working-endpoints.md](./working-endpoints.md)** - Valid endpoints with examples
- **[deprecated-endpoints.md](./deprecated-endpoints.md)** - Broken endpoints to avoid
- **[getting-started.md](./getting-started.md)** - Setup and first calls
- **[token-efficiency.md](./token-efficiency.md)** - Optimize API usage

---

**Last Updated:** 2025-11-17
