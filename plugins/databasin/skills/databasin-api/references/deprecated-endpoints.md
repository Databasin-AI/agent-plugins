# Databasin API - Deprecated & Broken Endpoints

**Last Updated:** 2025-11-16
**Purpose:** Track endpoints that should not be used and why

---

## Deprecated Endpoints

### GET `/api/projects?orgId={orgID}`

**Status:** ⚠️ DEPRECATED - Use `/api/my/projects` instead
**Issue:** Backend serialization bug with LocalDateTime
**Error:** Returns 500 Internal Server Error
**Alternative:** Use `/api/my/projects` and filter by `organizationId` field
**Discovered:** Previous conversation testing

**Why it's broken:**

- Java LocalDateTime objects aren't properly serialized to JSON
- Backend error: "No serializer found for class java.time.LocalDateTime"

**Migration path:**

```bash
# OLD (broken):
bun run scripts/api-call.ts GET "/api/projects?orgId=17"

# NEW (working):
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,organizationId,organizationName

# Then filter on client side for organizationId === 17
```

---

## Endpoints That Return Null Without Required Parameters

### GET `/api/automations` (without internalID)

**Status:** ⚠️ Returns `null` when internalID is missing
**Issue:** Endpoint requires `internalID` parameter but returns null instead of error
**Discovered:** 2025-11-16 during automation count testing
**Fixed:** Updated `--count` logic to handle null responses correctly

**Behavior:**

```bash
# Without internalID - returns null
bun run scripts/api-call.ts GET /api/automations
# Response: null
# --count returns: {"count": 0}

# With internalID - returns array
bun run scripts/api-call.ts GET "/api/automations?internalID=N1r8Do"
# Response: [array of 17 automation objects]
# --count returns: {"count": 17}
```

**Why this matters:**

- The endpoint silently returns null instead of 400 Bad Request
- Original `--count` logic incorrectly returned `{"count": 1}` for null
- Now correctly returns `{"count": 0}` for null responses
- This pattern may exist in other endpoints requiring parameters

**Correct usage:**

```bash
# Always include internalID for automations
bun run scripts/api-call.ts GET "/api/automations?internalID={projectInternalID}" --count
```

**Lesson learned:**

- Always test endpoints with and without required parameters
- Use `--count` to quickly verify if parameters are missing
- Check `references/working-endpoints.md` for required parameters before calling endpoints
- If `--count` returns 0, you may be missing required parameters

---

## Endpoints Requiring Authentication Errors

### GET `/api/lakebasin/connections?projectId={id}`

**Status:** ⚠️ Returns HTML error page
**Issue:** Endpoint returns HTML error instead of JSON
**Error Type:** Likely authentication or routing issue
**Tested:** 2025-11-16

**Symptoms:**

- Returns HTML error page instead of JSON
- May be related to missing authentication header or incorrect route

**Investigation needed:**

- Check if endpoint exists in backend routes
- Verify authentication requirements
- Check if endpoint URL changed

---

### GET `/api/governance/connectors`

**Status:** ⚠️ Returns HTML error page
**Issue:** Endpoint returns HTML error instead of JSON
**Error Type:** Likely authentication or routing issue
**Tested:** 2025-11-16

**Symptoms:**

- Returns HTML error page instead of JSON
- May require special governance permissions

**Investigation needed:**

- Check if endpoint exists in backend routes
- Verify permission requirements
- Check API client implementation

---

### GET `/api/notifications/{userId}`

**Status:** ⚠️ Returns HTML error page
**Issue:** Endpoint returns HTML error instead of JSON
**Error Type:** Likely routing issue
**Tested:** 2025-11-16

**Symptoms:**

- Returns HTML error page instead of JSON
- Endpoint structure may have changed

**Suggested alternatives:**

- Check NotificationsApiClient.js for correct endpoint
- May need different route format

---

## Important Endpoint Requirements

### Endpoints Requiring Parameters

**These endpoints will FAIL with 400 Bad Request if required parameters are missing:**

#### `/api/pipeline`

- **Requires:** `internalID` parameter (project internal ID)
- **Error without:** 400 Bad Request
- **Correct usage:** `/api/pipeline?internalID=N1r8Do`

#### `/api/lakebasin/connections`

- **Requires:** `projectId` parameter
- **Error without:** HTML error page
- **Correct usage:** `/api/lakebasin/connections?projectId=12`

---

## Token-Heavy Endpoints

**These endpoints can consume 50,000+ tokens if used incorrectly:**

### `/api/connector`

- **Without filters:** Returns 434 connectors (~200,000 tokens!)
- **Always use:** `--count`, `--fields`, `--limit`, or `internalID` filter
- **Safe usage:**
  ```bash
  bun run scripts/api-call.ts GET /api/connector --count
  bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --limit=10
  ```

### `/api/config`

- **Full data:** ~50,000 tokens (includes all connector configurations)
- **Always use:** `--summary` or `--fields` filter
- **Safe usage:**
  ```bash
  bun run scripts/api-call.ts GET /api/config --summary
  ```

---

## Lessons Learned

### 1. Always Check Required Parameters

- Many endpoints require context parameters (projectId, internalID, etc.)
- Missing parameters cause 400 Bad Request errors
- Check API client implementations for required params

### 2. Token Management is Critical

- Large result sets can consume 100,000+ tokens
- Always use `--count` first to check data size
- Use `--fields` and `--limit` to reduce token usage
- Prefer `--summary` over full data for large datasets

### 3. HTML Errors Indicate Routing Problems

- HTML error pages mean:
  - Endpoint doesn't exist
  - Authentication failed
  - Missing required middleware
- Check backend routes file and API client implementations

### 4. Authentication vs Authorization

- Some endpoints require specific roles (admin, project member, etc.)
- 401 = Not authenticated (no token or expired token)
- 403 = Not authorized (valid token but insufficient permissions)
- HTML error = Routing/middleware issue

---

**Testing Completed:** 2025-11-16
**Issues Documented:** 6 problematic endpoints
**Status:** ✅ Verified and documented
