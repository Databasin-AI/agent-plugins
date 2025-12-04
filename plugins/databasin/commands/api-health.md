# Check Databasin API Health

Verify that the Databasin API is running and accessible.

**Task:** Use the `databasin-api` skill to call the `/api/ping` health check endpoint.

**Steps:**

1. Read the endpoint documentation from `.claude/skills/databasin-api/references/working-endpoints.md` for `/api/ping`
2. Use the `databasin-api` skill to execute: `GET /api/ping`
3. Report the status clearly

**Expected output format:**

```
🏥 Databasin API Health Check:

Status: ✅ HEALTHY
Response: pong
Response Time: 45ms
API Base URL: http://localhost:9000

Authentication: ✅ Token valid
Token Status: Active (expires: never)
```

**API call:**

```bash
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/ping
```

**Note:** This endpoint does NOT require authentication, making it perfect for verifying:

- API server is running
- Network connectivity
- Base URL configuration is correct

**If health check fails:**

1. Verify the API server is running (check `http://localhost:9000` in browser)
2. Check `.claude/skills/databasin-api/.local.config.json` has correct `baseUrl`
3. Verify no firewall or network issues
