# Get Current User Information

Retrieve information about the currently authenticated Databasin user.

**Task:** Use the `databasin-api` skill to call the `/api/my/account` endpoint and display user profile information.

**Steps:**

1. Read the endpoint documentation from `.claude/skills/databasin-api/references/working-endpoints.md` for `/api/my/account`
2. Use the `databasin-api` skill to execute: `GET /api/my/account`
3. Format the response to show:
   - User ID
   - Email
   - Full name
   - Account status
   - Permissions/roles
   - Organization memberships

**Expected output format:**

```
👤 Current User Profile:

Name: John Doe
Email: john.doe@company.com
User ID: 12345

Account Status: Active
Created: 2023-06-15

Organizations:
- TechCorp (ID: 101) - Role: Admin
- DataTeam (ID: 202) - Role: Member

Permissions:
- Can create projects
- Can manage pipelines
- Can execute SQL queries
```

**API call:**

```bash
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/my/account
```
