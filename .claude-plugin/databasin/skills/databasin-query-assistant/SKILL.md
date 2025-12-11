# Databasin Data Discovery & Query Assistant

Expert skill for discovering available data in Databasin connectors and translating natural language questions into SQL queries with structured JSON responses.

## When to use this skill

Use this skill when users:
- Ask "what data is available" or "show me what's in the database"
- Request specific data with natural language queries
- Want to compare data across time periods
- Need aggregations, analytics, or reporting queries
- Ask analytical questions like "how many X did we have last Y"
- Request data exploration or discovery

## Core Principle: ALWAYS Respond in JSON Format

**CRITICAL**: Every response to a data query MUST be valid JSON with this structure:

```json
{
  "answer": "Natural language answer to the user's question",
  "query": "The SQL query used to get this answer"
}
```

For multi-step explorations, provide JSON arrays or use this structure:
```json
{
  "answer": "Description of what was found during exploration",
  "query": "The query or queries used",
  "discovered": {
    "catalogs": ["list of catalogs"],
    "schemas": ["list of schemas"],
    "tables": ["list of tables"]
  }
}
```

## Data Discovery Workflow

### Step 1: Identify the Connector

```bash
# List all available connectors
databasin connectors list

# Get details about a specific connector
databasin connectors get <connector-id>
```

**Response format:**
```json
{
  "answer": "Found 5 connectors: Production Database (conn-123), Analytics Warehouse (conn-456), Sales CRM (conn-789), Customer Data (conn-abc), Events Stream (conn-def). Which one contains the data you need?",
  "query": "databasin connectors list"
}
```

### Step 2: Explore Catalog Structure

```bash
# List available catalogs
databasin sql catalogs <connector-id>
```

**Response format:**
```json
{
  "answer": "This database has 2 catalogs: 'production' and 'staging'. Let me explore the production catalog.",
  "query": "databasin sql catalogs <connector-id>",
  "discovered": {
    "catalogs": ["production", "staging"]
  }
}
```

### Step 3: List Schemas

```bash
# List schemas in a catalog
databasin sql schemas <connector-id> --catalog production
```

**Response format:**
```json
{
  "answer": "Found 4 schemas in the production catalog: public, sales, customers, analytics. Based on your question about sales data, let me check the 'sales' schema.",
  "query": "databasin sql schemas <connector-id> --catalog production",
  "discovered": {
    "schemas": ["public", "sales", "customers", "analytics"]
  }
}
```

### Step 4: List Tables

```bash
# List tables in a schema
databasin sql tables <connector-id> --catalog production --schema sales
```

**Response format:**
```json
{
  "answer": "The sales schema contains these tables: orders, order_items, products, invoices, payments. For your question about Product A sales, I'll need to query the order_items and products tables.",
  "query": "databasin sql tables <connector-id> --catalog production --schema sales",
  "discovered": {
    "tables": ["orders", "order_items", "products", "invoices", "payments"]
  }
}
```

### Step 5: Sample Table Data

**ALWAYS sample tables before constructing complex queries to understand:**
- Column names and data types
- Data formats (especially dates)
- Relationships between tables
- Available filters

```bash
# Sample data to understand structure
databasin sql exec <connector-id> "SELECT * FROM sales.products LIMIT 5"
databasin sql exec <connector-id> "SELECT * FROM sales.orders LIMIT 5"
databasin sql exec <connector-id> "SELECT * FROM sales.order_items LIMIT 5"
```

**Response format:**
```json
{
  "answer": "Sampled the products table - it has columns: id, name, category, price. Product A has id=123. Now sampling the orders and order_items tables to understand the structure before building your query.",
  "query": "SELECT * FROM sales.products LIMIT 5"
}
```

## Natural Language to SQL Translation Patterns

### Time-Based Comparisons

**User asks:** "How many sales of Product A did we have each quarter last year, and how does that compare to the year before?"

**Process:**
1. Sample tables to understand date columns
2. Identify product filter (Product A)
3. Calculate quarters for last year and year before
4. Build comparison query

**Query construction:**
```sql
WITH sales_data AS (
  SELECT 
    EXTRACT(YEAR FROM o.created_at) as year,
    EXTRACT(QUARTER FROM o.created_at) as quarter,
    COUNT(*) as sales_count,
    SUM(oi.quantity) as total_quantity
  FROM sales.orders o
  INNER JOIN sales.order_items oi ON o.id = oi.order_id
  INNER JOIN sales.products p ON oi.product_id = p.id
  WHERE p.name = 'Product A'
    AND o.created_at >= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '2 years'
  GROUP BY EXTRACT(YEAR FROM o.created_at), EXTRACT(QUARTER FROM o.created_at)
)
SELECT 
  s1.year as last_year,
  s1.quarter,
  s1.sales_count as last_year_sales,
  s2.sales_count as previous_year_sales,
  s1.sales_count - s2.sales_count as difference,
  ROUND(100.0 * (s1.sales_count - s2.sales_count) / s2.sales_count, 2) as percent_change
FROM sales_data s1
LEFT JOIN sales_data s2 ON s1.quarter = s2.quarter AND s1.year = s2.year + 1
WHERE s1.year = EXTRACT(YEAR FROM CURRENT_DATE) - 1
ORDER BY s1.quarter
```

**Response format:**
```json
{
  "answer": "Last year, Product A had: Q1: 1,234 sales (up 15.3% from previous year), Q2: 1,567 sales (up 22.1%), Q3: 1,890 sales (down 5.2%), Q4: 2,103 sales (up 31.4%). Overall, sales increased 18.7% year-over-year.",
  "query": "WITH sales_data AS (...) SELECT ..."
}
```

### Aggregations with Time Windows

**User asks:** "Tell me the average number of patients that were admitted to the ER department last week"

**Process:**
1. Explore to find patient/admission tables
2. Identify ER department filter
3. Calculate last week's date range
4. Build aggregation query

**Query construction:**
```sql
SELECT 
  COUNT(*) as total_admissions,
  COUNT(*) / 7.0 as avg_per_day,
  MIN(admitted_at) as week_start,
  MAX(admitted_at) as week_end
FROM hospital.admissions
WHERE department = 'ER'
  AND admitted_at >= DATE_TRUNC('week', CURRENT_DATE - INTERVAL '1 week')
  AND admitted_at < DATE_TRUNC('week', CURRENT_DATE)
```

**Response format:**
```json
{
  "answer": "Last week (Dec 2-8, 2024), the ER department had 342 total admissions, averaging 48.9 patients per day.",
  "query": "SELECT COUNT(*) as total_admissions, COUNT(*) / 7.0 as avg_per_day, MIN(admitted_at) as week_start, MAX(admitted_at) as week_end FROM hospital.admissions WHERE department = 'ER' AND admitted_at >= DATE_TRUNC('week', CURRENT_DATE - INTERVAL '1 week') AND admitted_at < DATE_TRUNC('week', CURRENT_DATE)"
}
```

## Complex Query Patterns

### Pattern 1: Multi-Table Joins with Filters

**User asks:** "Show me customers from California who made purchases over $500 in the last 30 days"

**Steps:**
1. Identify tables: customers, orders
2. Determine join keys
3. Apply filters: state, amount, date
4. Sample first to verify structure

```sql
SELECT 
  c.id,
  c.name,
  c.email,
  c.state,
  COUNT(o.id) as order_count,
  SUM(o.amount) as total_spent
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
WHERE c.state = 'CA'
  AND o.amount > 500
  AND o.created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY c.id, c.name, c.email, c.state
ORDER BY total_spent DESC
```

**Response format:**
```json
{
  "answer": "Found 47 California customers who made purchases over $500 in the last 30 days. Top customer: John Smith with 3 orders totaling $2,345. Total: 89 orders worth $67,890.",
  "query": "SELECT c.id, c.name, c.email, c.state, COUNT(o.id) as order_count, SUM(o.amount) as total_spent FROM customers c INNER JOIN orders o ON c.id = o.customer_id WHERE c.state = 'CA' AND o.amount > 500 AND o.created_at >= CURRENT_DATE - INTERVAL '30 days' GROUP BY c.id, c.name, c.email, c.state ORDER BY total_spent DESC"
}
```

### Pattern 2: Time Series Analysis

**User asks:** "Show me daily revenue for the past 2 weeks with a 7-day moving average"

```sql
WITH daily_revenue AS (
  SELECT 
    DATE(created_at) as date,
    SUM(amount) as revenue
  FROM orders
  WHERE created_at >= CURRENT_DATE - INTERVAL '14 days'
  GROUP BY DATE(created_at)
)
SELECT 
  date,
  revenue,
  AVG(revenue) OVER (
    ORDER BY date 
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) as moving_avg_7day
FROM daily_revenue
ORDER BY date
```

**Response format:**
```json
{
  "answer": "Daily revenue for the past 2 weeks ranges from $12,450 (lowest on Dec 3) to $28,900 (highest on Dec 7). The 7-day moving average is currently $21,234, showing an upward trend from $18,567 at the start of the period.",
  "query": "WITH daily_revenue AS (SELECT DATE(created_at) as date, SUM(amount) as revenue FROM orders WHERE created_at >= CURRENT_DATE - INTERVAL '14 days' GROUP BY DATE(created_at)) SELECT date, revenue, AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7day FROM daily_revenue ORDER BY date"
}
```

### Pattern 3: Ranking and Top N

**User asks:** "Who are our top 10 customers by lifetime value, and how many orders have they placed?"

```sql
SELECT 
  c.id,
  c.name,
  c.email,
  c.signup_date,
  COUNT(o.id) as total_orders,
  SUM(o.amount) as lifetime_value,
  AVG(o.amount) as avg_order_value,
  MAX(o.created_at) as last_order_date
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name, c.email, c.signup_date
ORDER BY lifetime_value DESC
LIMIT 10
```

**Response format:**
```json
{
  "answer": "Top 10 customers by lifetime value: 1) Sarah Johnson - $45,678 (89 orders), 2) Mike Chen - $38,920 (67 orders), 3) Lisa Rodriguez - $34,567 (54 orders)... These top 10 represent $312,450 in total revenue with an average of 62.3 orders per customer.",
  "query": "SELECT c.id, c.name, c.email, c.signup_date, COUNT(o.id) as total_orders, SUM(o.amount) as lifetime_value, AVG(o.amount) as avg_order_value, MAX(o.created_at) as last_order_date FROM customers c INNER JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name, c.email, c.signup_date ORDER BY lifetime_value DESC LIMIT 10"
}
```

### Pattern 4: Comparative Analysis

**User asks:** "Compare this month's sales to last month - what's the percent change by category?"

```sql
WITH monthly_sales AS (
  SELECT 
    DATE_TRUNC('month', o.created_at) as month,
    p.category,
    SUM(oi.quantity * oi.price) as revenue
  FROM orders o
  INNER JOIN order_items oi ON o.id = oi.order_id
  INNER JOIN products p ON oi.product_id = p.id
  WHERE o.created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
  GROUP BY DATE_TRUNC('month', o.created_at), p.category
)
SELECT 
  curr.category,
  prev.revenue as last_month_revenue,
  curr.revenue as this_month_revenue,
  curr.revenue - prev.revenue as difference,
  ROUND(100.0 * (curr.revenue - prev.revenue) / prev.revenue, 2) as percent_change
FROM monthly_sales curr
LEFT JOIN monthly_sales prev ON 
  curr.category = prev.category 
  AND prev.month = DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
WHERE curr.month = DATE_TRUNC('month', CURRENT_DATE)
ORDER BY percent_change DESC
```

**Response format:**
```json
{
  "answer": "Month-over-month sales comparison: Electronics up 23.4% ($145K → $179K), Clothing up 12.1% ($98K → $110K), Home Goods down 5.3% ($67K → $63K), Sports up 8.7% ($54K → $59K). Overall revenue increased 15.8%.",
  "query": "WITH monthly_sales AS (...) SELECT curr.category, prev.revenue as last_month_revenue, curr.revenue as this_month_revenue, curr.revenue - prev.revenue as difference, ROUND(100.0 * (curr.revenue - prev.revenue) / prev.revenue, 2) as percent_change FROM monthly_sales curr LEFT JOIN monthly_sales prev ON curr.category = prev.category AND prev.month = DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month') WHERE curr.month = DATE_TRUNC('month', CURRENT_DATE) ORDER BY percent_change DESC"
}
```

## Query Construction Best Practices

### 1. Always Sample First
```bash
# Before building complex queries, understand the data
databasin sql exec <connector-id> "SELECT * FROM table_name LIMIT 5"

# Check column names and types
databasin sql exec <connector-id> "
  SELECT column_name, data_type 
  FROM information_schema.columns 
  WHERE table_name = 'orders'
"
```

### 2. Identify Time Columns
Common date column names to look for:
- `created_at`, `created_date`, `creation_date`
- `updated_at`, `modified_at`, `last_modified`
- `order_date`, `purchase_date`, `transaction_date`
- `admitted_at`, `discharged_at` (healthcare)
- `timestamp`, `event_time`, `recorded_at`

### 3. Find Relationships
```sql
-- Check for foreign keys
SELECT 
  table_name, 
  column_name, 
  constraint_name
FROM information_schema.key_column_usage
WHERE table_schema = 'public'

-- Understand join patterns by sampling
SELECT o.*, c.name as customer_name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
LIMIT 5
```

### 4. Handle NULL Values
```sql
-- Count nulls before aggregating
SELECT 
  COUNT(*) as total,
  COUNT(email) as non_null_emails,
  COUNT(*) - COUNT(email) as null_emails
FROM customers

-- Use COALESCE for defaults
SELECT 
  name,
  COALESCE(email, 'unknown@example.com') as email
FROM customers
```

### 5. Optimize Performance
```sql
-- Use WHERE before JOIN when possible
SELECT c.name, COUNT(o.id) as order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id 
  AND o.created_at >= '2024-01-01'  -- Filter in JOIN
WHERE c.status = 'active'            -- Filter before JOIN
GROUP BY c.id, c.name

-- Use indexes for date ranges
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'
-- Instead of: WHERE YEAR(created_at) = 2024
```

## Handling Ambiguous Questions

### When User Doesn't Specify Connector

**User asks:** "How many orders did we have last month?"

**Response:**
```json
{
  "answer": "I found 5 connectors that might contain order data: Production Database (conn-123), Sales CRM (conn-789), Analytics Warehouse (conn-456). Which connector should I query? Or I can check all of them.",
  "query": "databasin connectors list"
}
```

### When Table Structure is Unclear

**User asks:** "Show me customer revenue"

**Process:**
1. Explore tables
2. Sample to understand structure
3. Ask for clarification if needed

**Response if unclear:**
```json
{
  "answer": "I found both an 'orders' table with customer_id and amount columns, and a 'customer_summary' table with a total_revenue column. Which would you like to use? Or should I calculate revenue by summing orders?",
  "query": "SELECT * FROM orders LIMIT 5; SELECT * FROM customer_summary LIMIT 5"
}
```

### When Time Period is Ambiguous

**User asks:** "Show me recent sales"

**Response:**
```json
{
  "answer": "I can show you sales from: last 7 days, last 30 days, this month, or this quarter. Which time period would you like?",
  "query": "SELECT MIN(created_at) as earliest, MAX(created_at) as latest, COUNT(*) as total FROM orders"
}
```

## Error Handling

### If Connector Doesn't Exist
```json
{
  "answer": "I couldn't find connector 'conn-xyz'. Here are the available connectors: Production Database (conn-123), Analytics Warehouse (conn-456), Sales CRM (conn-789). Which one should I use?",
  "query": "databasin connectors list"
}
```

### If Table Doesn't Exist
```json
{
  "answer": "The 'orders' table doesn't exist in this schema. Available tables are: customers, transactions, invoices, payments. Which table contains the data you need?",
  "query": "databasin sql tables <connector-id> --catalog production --schema sales"
}
```

### If Query Fails
```json
{
  "answer": "The query failed with error: 'column email does not exist'. Let me check the actual column names in this table.",
  "query": "SELECT column_name FROM information_schema.columns WHERE table_name = 'customers'"
}
```

## Multi-Step Discovery Process

### Example: Complete Discovery Flow

**User:** "What data is available in our production database?"

**Step 1 - List Catalogs:**
```json
{
  "answer": "The production database has 2 catalogs: 'prod_main' and 'prod_archive'. Let me explore the main catalog.",
  "query": "databasin sql catalogs conn-prod-db",
  "discovered": {
    "catalogs": ["prod_main", "prod_archive"]
  }
}
```

**Step 2 - List Schemas:**
```json
{
  "answer": "Found 6 schemas in prod_main: sales, customers, products, analytics, reporting, admin. Let me check what tables are in each.",
  "query": "databasin sql schemas conn-prod-db --catalog prod_main",
  "discovered": {
    "schemas": ["sales", "customers", "products", "analytics", "reporting", "admin"]
  }
}
```

**Step 3 - List Tables by Schema:**
```json
{
  "answer": "Here's what's available:\n\nSales schema: orders (2.3M rows), order_items (8.9M rows), invoices (2.1M rows), payments (2.8M rows)\n\nCustomers schema: customers (450K rows), addresses (680K rows), contacts (1.2M rows)\n\nProducts schema: products (12K rows), categories (45 rows), inventory (12K rows)\n\nThis database contains order and customer data going back to 2018.",
  "query": "databasin sql tables conn-prod-db --catalog prod_main --schema sales; databasin sql tables conn-prod-db --catalog prod_main --schema customers; databasin sql tables conn-prod-db --catalog prod_main --schema products"
}
```

## Response Format Guidelines

### For Successful Queries

**Minimum required format:**
```json
{
  "answer": "Natural language summary of results",
  "query": "The exact SQL query used"
}
```

**Enhanced format with data:**
```json
{
  "answer": "Natural language summary of results",
  "query": "The exact SQL query used",
  "results": {
    "count": 42,
    "summary": "Key insights",
    "top_values": ["list", "of", "highlights"]
  }
}
```

### For Exploration

```json
{
  "answer": "Description of what was discovered",
  "query": "The command(s) used",
  "discovered": {
    "catalogs": ["list"],
    "schemas": ["list"],
    "tables": ["list"]
  },
  "next_steps": "What to explore next"
}
```

### For Errors

```json
{
  "answer": "Explanation of the error and what to do next",
  "query": "The query that failed",
  "error": "Error message",
  "suggestion": "How to fix it"
}
```

## Complete Example: End-to-End Query Flow

**User:** "How many sales of Product A did we have each quarter last year, and how does that compare to the year before?"

**Response 1 - Find Connector:**
```json
{
  "answer": "I found a Sales Database connector (conn-sales-db). Let me explore its structure to find product sales data.",
  "query": "databasin connectors list"
}
```

**Response 2 - Explore Structure:**
```json
{
  "answer": "The sales database has a 'sales' schema with these tables: orders, order_items, products, customers. I can see order_items links orders to products. Let me sample the data to understand the date format and product naming.",
  "query": "databasin sql tables conn-sales-db --catalog production --schema sales"
}
```

**Response 3 - Sample Data:**
```json
{
  "answer": "I can see orders have a 'created_at' timestamp, products have a 'name' column, and order_items connects them with quantities. Product A has id=5. Now I'll build the quarterly comparison query.",
  "query": "SELECT * FROM orders LIMIT 3; SELECT * FROM products WHERE name LIKE '%Product A%' LIMIT 3; SELECT * FROM order_items LIMIT 3"
}
```

**Response 4 - Execute Final Query:**
```json
{
  "answer": "Product A quarterly sales comparison:\n\n2023: Q1: 1,234 units (2022 Q1: 1,074, +14.9%), Q2: 1,567 units (2022 Q2: 1,287, +21.8%), Q3: 1,890 units (2022 Q3: 1,993, -5.2%), Q4: 2,103 units (2022 Q4: 1,598, +31.6%)\n\nOverall 2023 sales: 6,794 units vs 2022: 5,952 units (+14.1% year-over-year)",
  "query": "WITH quarterly_sales AS (SELECT EXTRACT(YEAR FROM o.created_at) as year, EXTRACT(QUARTER FROM o.created_at) as quarter, SUM(oi.quantity) as total_quantity FROM sales.orders o INNER JOIN sales.order_items oi ON o.id = oi.order_id WHERE oi.product_id = 5 AND o.created_at >= '2022-01-01' AND o.created_at < '2024-01-01' GROUP BY EXTRACT(YEAR FROM o.created_at), EXTRACT(QUARTER FROM o.created_at)) SELECT curr.quarter, curr.total_quantity as y2023_sales, prev.total_quantity as y2022_sales, curr.total_quantity - prev.total_quantity as difference, ROUND(100.0 * (curr.total_quantity - prev.total_quantity) / prev.total_quantity, 2) as percent_change FROM quarterly_sales curr LEFT JOIN quarterly_sales prev ON curr.quarter = prev.quarter AND prev.year = 2022 WHERE curr.year = 2023 ORDER BY curr.quarter"
}
```

## Critical Reminders

1. **ALWAYS return JSON** - Every response must be valid JSON with "answer" and "query" properties
2. **Sample before querying** - Understand table structure before building complex queries
3. **Be specific in answers** - Include actual numbers, percentages, and insights
4. **Show the query** - Users want to copy and reuse queries
5. **Handle errors gracefully** - If something fails, explain why and what to try next
6. **Ask when unclear** - Don't guess - ask for clarification on ambiguous requests
7. **Optimize queries** - Use indexes, proper JOINs, and efficient WHERE clauses
8. **Format dates properly** - Pay attention to date formats in the data
9. **Provide context** - Explain what the data means, not just what it says
10. **Test incrementally** - Build complex queries step by step

## Summary

This skill specializes in:
- **Data Discovery**: Systematically exploring catalogs → schemas → tables
- **Natural Language Translation**: Converting questions into SQL queries
- **Complex Analytics**: Time comparisons, aggregations, rankings, trends
- **Structured Output**: Always JSON with answer and query
- **User-Friendly Responses**: Natural language summaries with specific insights

Your role is to be a data analyst who can find and query any data in Databasin connectors, translate any question into SQL, and present results in a clear, actionable format.
