# Refresh Databasin JWT Token

Obtain a fresh JWT authentication token using the automated browser-based login flow.

**Task:** Use the `refresh-databasin-jwt` skill to authenticate and save a fresh JWT token to the `.token` file.

**Steps:**

1. Ensure `.auth-config.json` exists in the project root with valid credentials:
   ```json
   {
   	"username": "your-email@company.com",
   	"password": "your-password",
   	"loginUrl": "http://localhost:3000"
   }
   ```
2. Run the refresh-jwt script:
   ```bash
   bun run .claude/skills/refresh-databasin-jwt/refresh-jwt.ts
   ```
3. Verify the token was saved to `.token` in the project root
4. Confirm the token works by testing a simple API call

**When to use this:**

- When you get 401 Unauthorized errors from the API
- When the current token has expired
- When setting up a new development environment
- Before starting a work session

**Expected output:**

```
🌐 Launching browser...
📝 Using auth config: /path/to/project/.auth-config.json
🔐 Navigating to login page...
✅ Successfully authenticated
📦 Extracted JWT token from localStorage
💾 Saving token to /path/to/project/.token...
✅ Token saved successfully
✅ Token refresh complete
```

**Troubleshooting:**

- If `.auth-config.json` is missing, create it from `.auth-config.example.json`
- If login fails, verify credentials in `.auth-config.json`
- If browser launch fails, ensure Playwright is installed: `bun add -d playwright && bunx playwright install chromium`
