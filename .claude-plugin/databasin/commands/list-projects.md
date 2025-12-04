# List Databasin Projects

Retrieve all projects accessible to the current user from the Databasin API.

**Task:** Use the `databasin-api` skill to call the `/api/my/projects` endpoint and display the results in a user-friendly format.

**Steps:**

1. Read the endpoint documentation from `.claude/skills/databasin-api/references/working-endpoints.md` for `/api/my/projects`
2. Use the `databasin-api` skill to execute: `GET /api/my/projects`
3. Format the response to show:
   - Project ID
   - Project name
   - Organization ID
   - Creation date
   - Status

**Expected output format:**

```
📊 Your Databasin Projects:

1. ProjectName (ID: ABC123)
   - Organization: OrgName (ID: 456)
   - Created: 2024-01-15
   - Status: Active

2. AnotherProject (ID: DEF789)
   ...
```

**Token efficiency tip:** If there are many projects, use `--limit=10 --fields=projectID,projectName,organizationID` to reduce token usage.
