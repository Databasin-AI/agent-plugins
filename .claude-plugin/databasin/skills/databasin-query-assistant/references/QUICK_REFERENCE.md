# Quick Reference Guide

## JSON Response Format

**Every response must follow this structure:**

```json
{
  "answer": "Natural language answer",
  "query": "SQL query or CLI command"
}
```

## Question Pattern Recognition

| User Says | Interpret As | SQL Pattern |
|-----------|--------------|-------------|
| "How many..." | COUNT | `SELECT COUNT(*) FROM table` |
| "Show me total..." | SUM | `SELECT SUM(column) FROM table` |
| "Average..." | AVG | `SELECT AVG(column) FROM table` |
| "Last week/month" | Date filter | `WHERE created_at >= DATE_TRUNC(...)` |
| "This vs last..." | Comparison | Use CTE with LEFT JOIN |
| "Year-over-year" | YoY comparison | Filter by year, compare periods |
| "Top 10..." | Ranking | `ORDER BY ... DESC LIMIT 10` |
| "By category" | Grouping | `GROUP BY category` |
| "Daily/monthly breakdown" | Time series | `GROUP BY DATE_TRUNC('day', ...)` |
| "Compared to..." | Side-by-side | Join on matching dimension |

## Time Period Translation

| Natural Language | SQL |
|-----------------|-----|
| "last week" | `>= DATE_TRUNC('week', CURRENT_DATE - INTERVAL '1 week')` |
| "this month" | `>= DATE_TRUNC('month', CURRENT_DATE)` |
| "last 30 days" | `>= CURRENT_DATE - INTERVAL '30 days'` |
| "last quarter" | `>= DATE_TRUNC('quarter', CURRENT_DATE - INTERVAL '3 months')` |
| "this year" | `WHERE EXTRACT(YEAR FROM date) = EXTRACT(YEAR FROM CURRENT_DATE)` |
| "last year" | `WHERE EXTRACT(YEAR FROM date) = EXTRACT(YEAR FROM CURRENT_DATE) - 1` |

## Discovery Workflow

```
Step 1: List Connectors
  databasin connectors list
  
Step 2: Explore Catalogs
  databasin sql catalogs <connector-id>
  
Step 3: List Schemas
  databasin sql schemas <connector-id> --catalog <catalog>
  
Step 4: List Tables
  databasin sql tables <connector-id> --catalog <cat> --schema <sch>
  
Step 5: Sample Data
  databasin sql exec <connector-id> "SELECT * FROM table LIMIT 5"
  
Step 6: Build Query
  Based on discovered structure
  
Step 7: Execute & Format
  Return JSON with answer and query
```

## Common Query Patterns

### Simple Count
```sql
SELECT COUNT(*) as count FROM table_name
WHERE condition
```

### Aggregation with Grouping
```sql
SELECT 
  category,
  COUNT(*) as count,
  SUM(amount) as total
FROM table_name
GROUP BY category
ORDER BY total DESC
```

### Time-Based Aggregation
```sql
SELECT 
  DATE_TRUNC('month', created_at) as month,
  COUNT(*) as count,
  SUM(amount) as total
FROM table_name
WHERE created_at >= '2024-01-01'
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month
```

### Period Comparison
```sql
WITH period_data AS (
  SELECT 
    DATE_TRUNC('month', created_at) as month,
    SUM(amount) as revenue
  FROM orders
  GROUP BY DATE_TRUNC('month', created_at)
)
SELECT 
  curr.month,
  curr.revenue as current_revenue,
  prev.revenue as previous_revenue,
  curr.revenue - prev.revenue as difference
FROM period_data curr
LEFT JOIN period_data prev 
  ON prev.month = curr.month - INTERVAL '1 month'
ORDER BY curr.month DESC
```

### Top N
```sql
SELECT 
  name,
  COUNT(*) as count,
  SUM(amount) as total
FROM table_name
GROUP BY name
ORDER BY total DESC
LIMIT 10
```

### Moving Average
```sql
WITH daily_data AS (
  SELECT 
    DATE(created_at) as date,
    SUM(amount) as value
  FROM table_name
  GROUP BY DATE(created_at)
)
SELECT 
  date,
  value,
  AVG(value) OVER (
    ORDER BY date 
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) as moving_avg_7day
FROM daily_data
```

## Response Templates

### Successful Query
```json
{
  "answer": "Found [NUMBER] [ENTITY]. [KEY_METRICS]. [INSIGHTS].",
  "query": "SELECT ... FROM ... WHERE ..."
}
```

### Discovery Response
```json
{
  "answer": "The [DATABASE] contains [NUMBER] schemas: [LIST]. [SUMMARY].",
  "query": "databasin sql schemas ...",
  "discovered": {
    "schemas": ["schema1", "schema2"]
  }
}
```

### Error Response
```json
{
  "answer": "[ERROR_EXPLANATION]. Available options are: [LIST]. [SUGGESTION].",
  "query": "The command that failed",
  "error": "Error message",
  "suggestion": "What to try next"
}
```

### Clarification Needed
```json
{
  "answer": "I need more information: [WHAT'S_MISSING]. Options: [CHOICES].",
  "query": null,
  "clarification_needed": "Specific question"
}
```

## CLI Commands Reference

```bash
# List connectors
databasin connectors list

# Get connector details
databasin connectors get <connector-id>

# List catalogs
databasin sql catalogs <connector-id>

# List schemas
databasin sql schemas <connector-id> --catalog <catalog>

# List tables
databasin sql tables <connector-id> --catalog <cat> --schema <sch>

# Execute query
databasin sql exec <connector-id> "SELECT ... FROM ..."

# Output formats
--json    # JSON output
--csv     # CSV output
```

## Critical Rules

1. ✅ **ALWAYS return JSON** with `answer` and `query` properties
2. ✅ **Sample tables first** before building complex queries
3. ✅ **Use specific numbers** in answers, not just "many" or "some"
4. ✅ **Include context** - explain what the numbers mean
5. ✅ **Show the query** - users want to reuse it
6. ✅ **Handle errors gracefully** - explain and suggest alternatives
7. ✅ **Ask when unclear** - don't guess at ambiguous requests
8. ✅ **Optimize queries** - use proper indexes and JOINs
9. ✅ **Format dates correctly** - check sample data first
10. ✅ **Provide insights** - don't just report raw numbers

## Common Mistakes to Avoid

❌ **Don't:**
- Return plain text without JSON structure
- Query without sampling data first
- Assume table structures
- Give vague answers like "there are some orders"
- Guess at column names
- Use inefficient queries
- Ignore date formats

✅ **Do:**
- Always return valid JSON
- Explore data structure first
- Sample before querying
- Provide specific numbers and percentages
- Check actual column names
- Use optimized SQL patterns
- Adapt to discovered date formats

## Example Interaction Flow

```
User: "How many sales last quarter?"

Step 1: Identify connector
→ Check databasin connectors list

Step 2: Explore structure
→ Sample orders table to find date column

Step 3: Determine quarter dates
→ Calculate Q4 2024: Oct 1 - Dec 31

Step 4: Build query
→ SELECT COUNT(*) FROM orders WHERE ...

Step 5: Execute
→ Run query, get result

Step 6: Format response
→ Return JSON:
{
  "answer": "Q4 2024 had 5,432 sales totaling $678,901...",
  "query": "SELECT COUNT(*) as count, SUM(amount)..."
}
```

## Testing Your Responses

Before sending, verify:
- [ ] Response is valid JSON
- [ ] Has "answer" property with specific numbers
- [ ] Has "query" property with the actual SQL
- [ ] Answer includes insights, not just raw data
- [ ] Query is executable and optimized
- [ ] Handles edge cases (no data, errors, etc.)

## Date/Time Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `DATE_TRUNC('day', col)` | Round to day | `2024-12-09 14:23:45` → `2024-12-09 00:00:00` |
| `DATE_TRUNC('month', col)` | Round to month | `2024-12-09` → `2024-12-01` |
| `EXTRACT(QUARTER FROM col)` | Get quarter | `2024-12-09` → `4` |
| `EXTRACT(YEAR FROM col)` | Get year | `2024-12-09` → `2024` |
| `CURRENT_DATE` | Today's date | `2024-12-09` |
| `CURRENT_DATE - INTERVAL '7 days'` | 7 days ago | `2024-12-02` |
| `AGE(date1, date2)` | Difference | `'3 months 7 days'` |

## Aggregation Functions

| Function | Purpose |
|----------|---------|
| `COUNT(*)` | Count all rows |
| `COUNT(col)` | Count non-null values |
| `COUNT(DISTINCT col)` | Count unique values |
| `SUM(col)` | Total of numeric column |
| `AVG(col)` | Average of numeric column |
| `MIN(col)` | Minimum value |
| `MAX(col)` | Maximum value |
| `STDDEV(col)` | Standard deviation |

## Window Functions

| Function | Purpose |
|----------|---------|
| `ROW_NUMBER() OVER (...)` | Sequential numbering |
| `RANK() OVER (...)` | Ranking with gaps |
| `AVG(col) OVER (...)` | Moving average |
| `SUM(col) OVER (...)` | Running total |
| `LAG(col) OVER (...)` | Previous row value |
| `LEAD(col) OVER (...)` | Next row value |

## Quick Checklist

Before every response:
1. ✓ Is this valid JSON?
2. ✓ Does it have "answer" and "query"?
3. ✓ Are numbers specific (not vague)?
4. ✓ Does answer provide insight?
5. ✓ Is query optimized?
6. ✓ Will query work as written?
7. ✓ Did I sample data first?
8. ✓ Is date math correct?
