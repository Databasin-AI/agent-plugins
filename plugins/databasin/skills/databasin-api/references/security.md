# Security Best Practices

**Protecting JWT tokens and credentials**

---

## JWT Token Security

### Token Storage

**Location:** `.token` file in current working directory

**Protection:**

- File is git-ignored automatically
- Contains only the JWT token string (no JSON, no extra data)
- Should have restrictive file permissions

---

### Token Lifecycle

**Expiration:**

- JWT tokens typically expire after **1 hour**
- Expired tokens return **401 Unauthorized**
- Obtain new token when expired

---

### Token Protection Best Practices

#### ✅ DO

- Keep `.token` file in git-ignored directory
- Use restrictive file permissions (e.g., `chmod 600 .token`)
- Obtain fresh token when needed
- Sign out and get new token if compromised
- Use separate tokens for different environments

---

#### ❌ DON'T

- Commit `.token` file to version control
- Share tokens with others
- Use production tokens in development
- Log tokens in application output
- Include tokens in error messages
- Store tokens in publicly accessible locations

---

### Checking Token Validity

```bash
# Test if token is valid
bun run scripts/api-call.ts GET /api/ping

# If successful, token is valid
# If 401 error, token is expired or invalid
```

---

## File Permissions

### Recommended Permissions

```bash
# Make .token file readable only by owner
chmod 600 .token

# Verify permissions
ls -la .token
# Should show: -rw------- (600)
```

---

### Directory Permissions

```bash
# Ensure project directory isn't world-readable
chmod 750 .

# Check permissions
ls -ld .
```

---

## Git Ignore

### Verify .gitignore

Ensure `.token` file is git-ignored:

```bash
# Check if .token is in .gitignore
grep "\.token" .gitignore

# If not present, add it
echo ".token" >> .gitignore
```

---

### Common Git-Ignored Files

These credential files should NEVER be committed:

- `.token` - JWT token file
- `.env` - Environment variables
- `.cache/` - Cache directory
- `node_modules/` - Dependencies

---

## Token Compromise Response

### If Token is Compromised

**Immediate actions:**

1. **Sign out of Databasin application**
   - This invalidates the current JWT token

2. **Delete `.token` file**

   ```bash
   rm .token
   ```

3. **Sign in again to get new token**
   - New token will have different signature

4. **Review recent API activity**
   - Check for unauthorized access
   - Report suspicious activity

5. **Change password if needed**
   - If you suspect account compromise

---

## Environment Separation

### Development vs Production

**Never use production tokens in development:**

```bash
# Development
# .token contains dev environment JWT

# Production
# Use separate .token file or environment variables
```

---

### Using Environment Variables (Alternative)

Instead of `.token` file, you can use environment variables:

```bash
# Set JWT in environment
export DATABASIN_JWT="your-jwt-token-here"

# Modify api-call.ts to read from env if .token not found
```

---

## API Security Best Practices

### Principle of Least Privilege

**Only request what you need:**

```bash
# ✅ Request only necessary fields
bun run scripts/api-call.ts GET /api/my/account --fields=id,email

# ❌ Don't fetch all data unnecessarily
bun run scripts/api-call.ts GET /api/connector
```

---

### Avoid Logging Sensitive Data

**Don't log:**

- JWT tokens
- Passwords
- API keys
- Connection strings with credentials

**Example - Safe logging:**

```bash
# ✅ Log count only
echo "Found $(bun run scripts/api-call.ts GET /api/my/projects --count) projects"

# ❌ Don't log full response with sensitive data
bun run scripts/api-call.ts GET /api/connector > all-connectors.log
```

---

## Network Security

### Use HTTPS

**Always use HTTPS endpoints:**

```bash
# ✅ HTTPS (secure)
baseUrl: "https://api.databasin.com"

# ❌ HTTP (insecure)
baseUrl: "http://api.databasin.com"
```

---

### Localhost Development

For local development, HTTP is acceptable:

```bash
# OK for localhost only
baseUrl: "http://localhost:9000"
```

**Never** use HTTP for production or remote APIs.

---

## Credential Management

### Password Security

If using automated authentication (not recommended for this skill):

- Use strong, unique passwords
- Store passwords in secure credential managers
- Never commit passwords to version control
- Rotate passwords regularly
- Use MFA when available

---

### Token Rotation

**Best practice:** Rotate tokens regularly

```bash
# Sign out and get new token daily/weekly
# For automated systems, implement token refresh logic
```

---

## Production Deployment

### Using Secrets Managers

For production deployments, use secrets managers:

- **Azure Key Vault**
- **AWS Secrets Manager**
- **HashiCorp Vault**
- **Docker Secrets**
- **Kubernetes Secrets**

---

### Environment Variables in CI/CD

```bash
# GitHub Actions example
- name: Call Databasin API
  env:
    DATABASIN_JWT: ${{ secrets.DATABASIN_JWT }}
  run: |
    echo "$DATABASIN_JWT" > .token
    bun run scripts/api-call.ts GET /api/my/projects
    rm .token
```

---

## Audit and Monitoring

### Track API Usage

**Monitor for:**

- Unusual access patterns
- High volume of requests
- Failed authentication attempts
- Access from unexpected IPs

---

### Review Logs Regularly

```bash
# Check application logs for security events
# Look for 401 errors (auth failures)
# Monitor for suspicious activity
```

---

## Security Checklist

### Before Committing Code

- [ ] `.token` file is in `.gitignore`
- [ ] No tokens in source code
- [ ] No passwords in configuration files
- [ ] Sensitive files are git-ignored
- [ ] Code doesn't log sensitive data

---

### Regular Maintenance

- [ ] Rotate JWT tokens regularly
- [ ] Review `.gitignore` coverage
- [ ] Check file permissions
- [ ] Update dependencies
- [ ] Review API access logs

---

### When Sharing Code

- [ ] Remove all `.token` files
- [ ] Remove all credential files
- [ ] Provide `.example` config templates
- [ ] Document credential requirements
- [ ] Don't include actual credentials in examples

---

## Common Security Mistakes

### ❌ Mistake 1: Committing Tokens

```bash
# Never do this
git add .token
git commit -m "Added config"
```

**Prevention:**

```bash
# Use .gitignore
echo ".token" >> .gitignore
```

---

### ❌ Mistake 2: Sharing Tokens in Logs

```bash
# Don't log full API responses with credentials
bun run scripts/api-call.ts GET /api/connector > output.log
git add output.log
```

**Prevention:**

```bash
# Log counts or summaries only
bun run scripts/api-call.ts GET /api/connector --count
```

---

### ❌ Mistake 3: Using Production in Development

```bash
# Don't mix environments
# .token should be for dev environment only
```

**Prevention:**

- Use separate tokens per environment
- Label token files clearly (`.token.dev`, `.token.prod`)
- Never commit production tokens

---

### ❌ Mistake 4: Weak File Permissions

```bash
# Don't allow world-readable tokens
chmod 777 .token  # ❌ Bad!
```

**Prevention:**

```bash
# Restrict to owner only
chmod 600 .token  # ✅ Good!
```

---

## See Also

- **[getting-started.md](./getting-started.md)** - Setup guide
- **[error-handling.md](./error-handling.md)** - 401 authentication errors
- **[programmatic-usage.md](./programmatic-usage.md)** - Using in code safely

---

**Last Updated:** 2025-11-17
