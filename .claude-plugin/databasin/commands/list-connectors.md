# List Databasin Connectors

Retrieve available data source connectors from the Databasin API.

**⚠️ CRITICAL TOKEN WARNING:** The `/api/connector` endpoint can return a large number of connectors. ALWAYS use token-efficient options.

**Task:** Use the `databasin-api` skill to call the `/api/connector` endpoint with appropriate filtering.

**Steps:**

1. Read the endpoint documentation from `.claude/skills/databasin-api/references/working-endpoints.md` for `/api/connector`
2. Ask the user what they're looking for:
   - Just a count? Use `--count`
   - Specific fields? Use `--fields=connectorID,connectorName,category`
   - Limited results? Use `--limit=20`
3. Execute the API call with appropriate options
4. Format the response clearly

**Common usage patterns:**

**Pattern 1: Get count only**

```bash
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/connector --count
```

**Pattern 2: List first 20 connectors with key fields**

```bash
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/connector \
  --fields=connectorID,connectorName,category,iconUrl \
  --limit=20
```

**Pattern 3: Get summary**

```bash
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/connector --summary
```

**Expected output format:**

```
🔌 Databasin Connectors:

Total available: 434

Showing first 20:
1. PostgreSQL (ID: 1)
   - Category: Database

2. MySQL (ID: 2)
   - Category: Database

...
```
