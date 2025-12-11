# Databasin Data Discovery & Query Assistant

A specialized Claude Code skill that transforms natural language questions into SQL queries using the Databasin CLI, with **structured JSON responses** containing both natural language answers and executable queries.

## What This Skill Does

This skill specializes in:

1. **Data Discovery** - Systematically explore what data is available in connectors
2. **Natural Language to SQL** - Convert questions like "how many sales last quarter" into proper SQL
3. **Complex Analytics** - Time series, comparisons, aggregations, rankings
4. **Structured Output** - ALWAYS returns JSON with `answer` and `query` properties

## Key Feature: Structured JSON Responses

**Every response follows this format:**

```json
{
  "answer": "Natural language answer to your question",
  "query": "The exact SQL query used to get this answer"
}
```

This means you get:
- ✅ Human-readable answers
- ✅ Copy-paste ready SQL queries
- ✅ Consistent, parseable output
- ✅ Easy integration with other tools

## Usage Examples

### Example 1: Simple Query

**You ask:**
> "How many orders did we have last month?"

**Claude responds:**
```json
{
  "answer": "You had 2,847 orders in November 2024, totaling $456,789 in revenue. This is 12.3% higher than October (2,536 orders).",
  "query": "SELECT COUNT(*) as order_count, SUM(amount) as total_revenue FROM orders WHERE created_at >= '2024-11-01' AND created_at < '2024-12-01'"
}
```

### Example 2: Complex Comparison

**You ask:**
> "How many sales of Product A did we have each quarter last year, and how does that compare to the year before?"

**Claude discovers the data structure, then responds:**
```json
{
  "answer": "Product A quarterly sales comparison:\n\n2023: Q1: 1,234 units (+14.9% vs 2022), Q2: 1,567 units (+21.8%), Q3: 1,890 units (-5.2%), Q4: 2,103 units (+31.6%)\n\nOverall 2023: 6,794 units vs 2022: 5,952 units (+14.1% YoY)",
  "query": "WITH quarterly_sales AS (SELECT EXTRACT(YEAR FROM o.created_at) as year, EXTRACT(QUARTER FROM o.created_at) as quarter, SUM(oi.quantity) as total_quantity FROM orders o INNER JOIN order_items oi ON o.id = oi.order_id WHERE oi.product_id = 5 AND o.created_at >= '2022-01-01' GROUP BY EXTRACT(YEAR FROM o.created_at), EXTRACT(QUARTER FROM o.created_at)) SELECT curr.quarter, curr.total_quantity as y2023_sales, prev.total_quantity as y2022_sales, ROUND(100.0 * (curr.total_quantity - prev.total_quantity) / prev.total_quantity, 2) as pct_change FROM quarterly_sales curr LEFT JOIN quarterly_sales prev ON curr.quarter = prev.quarter AND prev.year = 2022 WHERE curr.year = 2023"
}
```

### Example 3: Data Discovery

**You ask:**
> "What data is available in our production database?"

**Claude explores and responds:**
```json
{
  "answer": "Your production database has 6 schemas:\n\nSales: orders (2.3M rows), order_items (8.9M rows), invoices (2.1M rows)\nCustomers: customers (450K rows), addresses (680K rows)\nProducts: products (12K rows), categories (45 rows), inventory (12K rows)\n\nData spans from 2018 to present.",
  "query": "databasin sql schemas conn-prod-db --catalog production; databasin sql tables conn-prod-db --catalog production --schema sales",
  "discovered": {
    "catalogs": ["production"],
    "schemas": ["sales", "customers", "products", "analytics", "reporting", "admin"],
    "tables": ["orders", "order_items", "customers", "products", "...]
  }
}
```

### Example 4: Healthcare Analytics

**You ask:**
> "Tell me the average number of patients that were admitted to the ER department last week"

**Claude responds:**
```json
{
  "answer": "Last week (Dec 2-8, 2024), the ER department had 342 total admissions, averaging 48.9 patients per day. Peak day was Saturday with 67 admissions, lowest was Monday with 38.",
  "query": "SELECT COUNT(*) as total_admissions, COUNT(*) / 7.0 as avg_per_day, MIN(admitted_at) as week_start, MAX(admitted_at) as week_end FROM hospital.admissions WHERE department = 'ER' AND admitted_at >= DATE_TRUNC('week', CURRENT_DATE - INTERVAL '1 week') AND admitted_at < DATE_TRUNC('week', CURRENT_DATE)"
}
```

## How It Works

### 1. Discovery Phase
Claude systematically explores your data:

```
Connectors → Catalogs → Schemas → Tables → Sample Data
```

This ensures Claude understands:
- What tables exist
- Column names and data types
- Date formats
- Relationships between tables
- Available filters

### 2. Query Construction
Claude translates natural language into SQL:

- **Time references**: "last month", "each quarter", "year-over-year"
- **Comparisons**: "compare to", "vs", "how does X differ from Y"
- **Aggregations**: "total", "average", "count", "sum"
- **Filters**: "Product A", "California customers", "ER department"
- **Rankings**: "top 10", "highest", "best performing"

### 3. Execution & Response
Claude runs the query and formats results:

- Natural language summary of findings
- Specific numbers and percentages
- Key insights and trends
- The exact SQL query for reuse

## Supported Query Types

### Time-Based Analysis
- Daily, weekly, monthly, quarterly, yearly aggregations
- Time period comparisons (MoM, QoQ, YoY)
- Moving averages and trends
- Date range filters

### Aggregations
- Counts, sums, averages, min/max
- Group by categories, time periods, dimensions
- Percentages and ratios
- Statistical calculations

### Comparisons
- Period over period (this month vs last month)
- Year over year (2024 vs 2023)
- Category comparisons (Product A vs Product B)
- Benchmark comparisons (actual vs target)

### Rankings
- Top N by metric (top 10 customers by revenue)
- Bottom performers
- Percentile rankings
- Growth rankings

### Multi-Table Joins
- Customer + Orders
- Orders + Products
- Patients + Admissions + Departments
- Any complex relationships

### Data Quality
- NULL counts
- Duplicate detection
- Completeness checks
- Outlier identification

## Installation

```bash
# Copy to Claude Code skills directory
cp -r databasin-query-assistant ~/.claude/skills/user/databasin-query

# Or extract from archive
tar -xzf databasin-query-assistant.tar.gz
mv databasin-query-assistant ~/.claude/skills/user/databasin-query
```

## Prerequisites

1. **Databasin CLI installed:**
   ```bash
   curl -fsSL https://raw.githubusercontent.com/Databasin-AI/databasin-cli/main/install.sh | bash
   ```

2. **Authenticated:**
   ```bash
   databasin auth login
   ```

3. **Connectors configured:**
   ```bash
   databasin connectors list
   ```

## Best Practices for Users

### Be Specific About Time Periods
❌ "Show me recent sales"
✅ "Show me sales from last week"
✅ "Show me daily sales for the past 30 days"

### Mention the Data You Want
❌ "Give me a report"
✅ "How many orders did we have by category last month?"
✅ "Show me customer acquisition by channel in Q3"

### Specify Comparisons Clearly
❌ "How are we doing?"
✅ "How does this month's revenue compare to last month?"
✅ "What's our year-over-year growth in user signups?"

### Ask Follow-Up Questions
```
You: "Show me our top customers"
Claude: [returns top 10]
You: "Now show me their purchase frequency"
Claude: [analyzes purchase patterns]
You: "What percentage of revenue do they represent?"
Claude: [calculates revenue concentration]
```

## What Makes This Skill Special

### 1. Structured Output
Unlike generic responses, this skill ALWAYS returns JSON with:
- `answer`: What you need to know
- `query`: How to get it again

### 2. Discovery-First Approach
Doesn't assume data structure - explores and understands before querying.

### 3. Complex Analytics
Handles sophisticated queries:
- Multi-table joins
- Time series comparisons
- Window functions
- CTEs (Common Table Expressions)
- Aggregations with grouping

### 4. Natural Language Understanding
Interprets business language:
- "last quarter" → proper date math
- "year-over-year" → comparison logic
- "top performers" → ranking query
- "average per day" → aggregation + division

### 5. Error Handling
If something fails:
- Explains what went wrong
- Suggests how to fix it
- Offers alternatives
- Still returns valid JSON

## Example Workflows

### Workflow 1: Exploring New Database
```
1. You: "What's in the sales database?"
   → Claude lists catalogs, schemas, tables

2. You: "Show me sample data from the orders table"
   → Claude shows structure and sample rows

3. You: "How many orders do we have?"
   → Claude counts total orders

4. You: "Break that down by month for the last 6 months"
   → Claude creates monthly aggregation
```

### Workflow 2: Business Question
```
1. You: "Which products are selling best this quarter?"
   → Claude ranks products by sales

2. You: "How does that compare to last quarter?"
   → Claude adds comparison

3. You: "Show me the trend over the last 4 quarters"
   → Claude creates quarterly trend analysis

4. You: "Export that to CSV"
   → Claude provides the query to run with --csv flag
```

### Workflow 3: Dashboard Metrics
```
1. You: "I need metrics for a sales dashboard"
   → Claude asks what metrics

2. You: "Revenue, order count, average order value, top products"
   → Claude builds each query

3. You: "All for this month vs last month"
   → Claude adds comparison logic

4. You: "Format as JSON for my API"
   → Claude already does this automatically!
```

## Common Question Patterns

The skill recognizes and translates:

### Counting
- "How many X..."
- "Count of..."
- "Number of..."
- "Total X..."

### Aggregating
- "Total revenue..."
- "Average order value..."
- "Sum of..."
- "Maximum/Minimum..."

### Time-Based
- "Last week/month/quarter/year"
- "This vs last..."
- "Year-over-year..."
- "Daily/Weekly/Monthly breakdown"

### Filtering
- "Customers from California..."
- "Products in Electronics category..."
- "Orders over $500..."
- "Active users..."

### Ranking
- "Top 10..."
- "Best performing..."
- "Highest/Lowest..."
- "Bottom performers..."

### Comparing
- "How does X compare to Y..."
- "Difference between..."
- "Growth rate..."
- "Percentage change..."

## Parsing the JSON Response

Since responses are always JSON, you can easily:

### In JavaScript
```javascript
const response = JSON.parse(claudeResponse);
console.log(response.answer);  // Human-readable
console.log(response.query);   // SQL to reuse
```

### In Python
```python
import json
response = json.loads(claude_response)
print(response['answer'])
print(response['query'])
```

### In Shell
```bash
echo $CLAUDE_RESPONSE | jq '.query' | databasin sql exec conn-123
```

### In Your App
```javascript
fetch('/api/claude', {
  method: 'POST',
  body: JSON.stringify({ question: userQuestion })
})
.then(r => r.json())
.then(data => {
  showAnswer(data.answer);
  saveQuery(data.query);
});
```

## Limitations

### What This Skill Does NOT Do
- ❌ Modify data (INSERT, UPDATE, DELETE)
- ❌ Create or alter tables
- ❌ Manage permissions
- ❌ Pipeline creation (use the general Databasin CLI skill for that)

### What This Skill DOES Do
- ✅ Read and analyze data
- ✅ Discover data structures
- ✅ Execute SELECT queries
- ✅ Provide insights and analytics
- ✅ Return structured JSON responses

## Tips for Best Results

1. **Start with discovery** if working with unfamiliar data
2. **Be specific** about time periods and filters
3. **Ask follow-up questions** to refine queries
4. **Request clarification** if the answer isn't quite right
5. **Use the queries** - they're designed to be copied and reused

## Support

- **Databasin CLI**: https://github.com/Databasin-AI/databasin-cli
- **Platform**: https://databasin.ai

## License

CC-BY-4.0 (same as Databasin CLI)

---

**Transform your natural language questions into insights - with structured JSON output every time!**
