# Token Efficiency Guide

**Critical best practices to avoid API rate limits and massive token usage**

---

## Why Token Efficiency Matters

**Without token-efficient options:**

- `/api/connector` returns 434 connectors = **200,000+ tokens**
- `/api/config` returns full config = **50,000+ tokens**
- `/api/my/projects` (18 projects) = **20,000+ tokens**

**With token-efficient options:**

- Same queries can use **50-500 tokens** instead

---

## Token-Efficient Options

### --count (Most Efficient)

Returns only the count of items. **Uses ~50 tokens.**

```bash
# How many projects?
bun run scripts/api-call.ts GET /api/my/projects --count
# Output: {"count": 18}  ✅ ~50 tokens

# How many connectors?
bun run scripts/api-call.ts GET /api/connector --count
# Output: {"count": 434}  ✅ ~50 tokens
```

**Use when:** You only need to know "how many"

---

### --summary (Balanced)

Returns total count + first 3 items as sample. **Uses ~500-2,000 tokens.**

```bash
# Get overview of projects
bun run scripts/api-call.ts GET /api/my/projects --summary
# Output: {"total": 18, "sample": [first 3 projects]}  ✅ ~500 tokens

# See what connectors exist
bun run scripts/api-call.ts GET /api/connector --summary
# Output: {"total": 434, "sample": [first 3 connectors]}  ✅ ~2,000 tokens
```

**Use when:** Exploring what's available, need to see structure

---

### --fields=field1,field2 (Selective)

Returns only specified fields. **Saves 50-80% tokens.**

```bash
# Get just project names and IDs
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalId
# ✅ Uses 30-50% less tokens than full response

# Get connector names only
bun run scripts/api-call.ts GET /api/connector --fields=connectorID,connectorName --limit=20
# ✅ Uses ~1,000 tokens instead of 20,000+
```

**Use when:** You know exactly which fields you need

---

### --limit=N (Controlled)

Limits results to N items.

```bash
# Get first 10 connectors
bun run scripts/api-call.ts GET /api/connector --limit=10
# ✅ Manageable token usage

# Get 5 most recent projects
bun run scripts/api-call.ts GET /api/my/projects --limit=5
```

**Use when:** Working with large datasets

---

### --offset=N (Pagination)

Skip first N items. Combine with `--limit` for pagination.

```bash
# Get items 11-20
bun run scripts/api-call.ts GET /api/connector --offset=10 --limit=10

# Get items 21-30
bun run scripts/api-call.ts GET /api/connector --offset=20 --limit=10
```

**Use when:** Implementing pagination

---

### --compact (Formatting)

Removes JSON pretty-printing. **Saves ~30% tokens.**

```bash
# Compact output for programmatic use
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name --compact
```

**Use when:** Consuming output programmatically

---

## Combining Options for Maximum Efficiency

**Best practice: Stack options together**

```bash
# Count first to understand scope
bun run scripts/api-call.ts GET /api/connector --count
# {"count": 434}

# Then get just what you need
bun run scripts/api-call.ts GET /api/connector \
  --fields=connectorID,connectorName,connectorType \
  --limit=50 \
  --compact
# ✅ Minimal token usage with maximum information
```

---

## Recommended Workflow

### Step 1: Count First

Always start with `--count` to understand data volume:

```bash
bun run scripts/api-call.ts GET /api/my/projects --count
# {"count": 18}  ← Small dataset, can fetch all

bun run scripts/api-call.ts GET /api/connector --count
# {"count": 434}  ← Large dataset, use filters!
```

---

### Step 2: Use Summary for Exploration

If count is large, use `--summary` to see structure:

```bash
bun run scripts/api-call.ts GET /api/connector --summary
# Shows first 3 connectors to understand fields available
```

---

### Step 3: Fetch What You Need

Use `--fields` and `--limit` for targeted queries:

```bash
# Get specific fields, limited results
bun run scripts/api-call.ts GET /api/connector \
  --fields=connectorID,connectorName,connectorType \
  --limit=20
```

---

### Step 4: Paginate Large Datasets

For very large datasets, paginate:

```bash
# First page
bun run scripts/api-call.ts GET /api/connector --fields=id,name --limit=50

# Second page
bun run scripts/api-call.ts GET /api/connector --fields=id,name --limit=50 --offset=50
```

---

## Token Usage Comparison

| Query                                             | Tokens Used | Best For                         |
| ------------------------------------------------- | ----------- | -------------------------------- |
| `GET /api/connector`                              | ~200,000    | ❌ **NEVER** use without options |
| `GET /api/connector --count`                      | ~50         | ✅ Counting                      |
| `GET /api/connector --summary`                    | ~2,000      | ✅ Exploring data                |
| `GET /api/connector --fields=id,name --limit=10`  | ~500        | ✅ Specific needs                |
| `GET /api/my/projects`                            | ~20,000     | ⚠️ OK for small datasets         |
| `GET /api/my/projects --summary`                  | ~500        | ✅ Quick overview                |
| `GET /api/my/projects --fields=id,name --compact` | ~800        | ✅ List of names                 |

---

## When to Use Each Option

### Use --count when:

- ✅ You only need to know "how many"
- ✅ Checking if data exists before fetching
- ✅ Validating query parameters work
- ✅ Quick data volume assessment

### Use --summary when:

- ✅ Exploring unfamiliar endpoints
- ✅ Understanding response structure
- ✅ Seeing what fields are available
- ✅ Getting a quick overview

### Use --fields when:

- ✅ You know exactly which fields you need
- ✅ Reducing token usage on known queries
- ✅ Building focused data reports
- ✅ Extracting specific information

### Use --limit when:

- ✅ Working with large datasets
- ✅ Implementing pagination
- ✅ Getting "top N" results
- ✅ Sampling data

### Use --compact when:

- ✅ Programmatic consumption
- ✅ Piping to other tools
- ✅ Saving output to files
- ✅ Every token counts

---

## Common Mistakes to Avoid

### ❌ DON'T: Fetch all connectors without limits

```bash
bun run scripts/api-call.ts GET /api/connector
# Uses 200,000+ tokens!
```

### ✅ DO: Count first, then fetch what you need

```bash
bun run scripts/api-call.ts GET /api/connector --count
bun run scripts/api-call.ts GET /api/connector --fields=connectorID,connectorName --limit=20
```

---

### ❌ DON'T: Return all fields when you only need a few

```bash
bun run scripts/api-call.ts GET /api/my/projects
# Returns 15+ fields per project
```

### ✅ DO: Specify only the fields you need

```bash
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalId
```

---

### ❌ DON'T: Fetch large datasets without pagination

```bash
bun run scripts/api-call.ts GET /api/connector --fields=id,name
# Still returns all 434 connectors
```

### ✅ DO: Use limit for large datasets

```bash
bun run scripts/api-call.ts GET /api/connector --fields=id,name --limit=50
```

---

## Endpoint-Specific Token Usage

See **[working-endpoints.md](./working-endpoints.md)** for detailed token usage by endpoint.

**High-volume endpoints requiring filters:**

- `/api/connector` - 434 items without filters
- `/api/pipeline` - Varies by project, use `internalID` filter
- `/api/config` - Single large object, use `--fields`

**Safe endpoints (small responses):**

- `/api/my/account` - Single user object
- `/api/my/organizations` - Usually <10 organizations
- `/api/ping` - Health check only

---

## Examples

### Efficient Project Query

```bash
# Step 1: Check count
bun run scripts/api-call.ts GET /api/my/projects --count
# {"count": 18}

# Step 2: Get just what you need
bun run scripts/api-call.ts GET /api/my/projects --fields=id,name,internalId
# ✅ Minimal token usage
```

---

### Efficient Connector Search

```bash
# Step 1: Count connectors for project
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --count
# {"count": 23}

# Step 2: Get summary to see structure
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" --summary

# Step 3: Fetch specific fields
bun run scripts/api-call.ts GET "/api/connector?internalID=N1r8Do" \
  --fields=connectorID,connectorName,connectorType \
  --limit=25
```

---

### Large Dataset Pagination

```bash
# Count total
bun run scripts/api-call.ts GET /api/connector --count
# {"count": 434}

# Fetch in pages of 50
bun run scripts/api-call.ts GET /api/connector --fields=id,name --limit=50 --offset=0
bun run scripts/api-call.ts GET /api/connector --fields=id,name --limit=50 --offset=50
bun run scripts/api-call.ts GET /api/connector --fields=id,name --limit=50 --offset=100
```

---

## See Also

- **[working-endpoints.md](./working-endpoints.md)** - Endpoint-specific token usage examples
- **[getting-started.md](./getting-started.md)** - Quick start guide
- **[README.md](./README.md)** - Overview and quick reference

---

**Last Updated:** 2025-11-17
