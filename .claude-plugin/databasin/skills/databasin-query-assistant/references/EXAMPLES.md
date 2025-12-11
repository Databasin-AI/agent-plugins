# JSON Response Examples

Complete examples of how this skill responds to various types of questions, always in structured JSON format.

## Basic Queries

### Simple Count

**Question:** "How many customers do we have?"

**Response:**
```json
{
  "answer": "You have 45,678 customers in the database. 42,301 (92.6%) are active, 3,377 (7.4%) are inactive.",
  "query": "SELECT COUNT(*) as total, COUNT(*) FILTER (WHERE status = 'active') as active, COUNT(*) FILTER (WHERE status = 'inactive') as inactive FROM customers"
}
```

### Simple Filter

**Question:** "Show me orders from California"

**Response:**
```json
{
  "answer": "Found 1,234 orders from California customers, totaling $456,789 in revenue. Average order value: $370.12.",
  "query": "SELECT COUNT(*) as order_count, SUM(amount) as total_revenue, AVG(amount) as avg_order_value FROM orders o INNER JOIN customers c ON o.customer_id = c.id WHERE c.state = 'CA'"
}
```

### Date Range

**Question:** "How many sales did we have last week?"

**Response:**
```json
{
  "answer": "Last week (Dec 2-8, 2024) you had 892 sales totaling $67,345. That's 234 (35.6%) more sales than the previous week.",
  "query": "SELECT COUNT(*) as sales_count, SUM(amount) as revenue, MIN(created_at) as week_start, MAX(created_at) as week_end FROM orders WHERE created_at >= DATE_TRUNC('week', CURRENT_DATE - INTERVAL '1 week') AND created_at < DATE_TRUNC('week', CURRENT_DATE)"
}
```

## Time Series Analysis

### Daily Breakdown

**Question:** "Show me daily revenue for the past 2 weeks"

**Response:**
```json
{
  "answer": "Daily revenue for the past 2 weeks:\n\nWeek of Nov 25: $18.2K Mon, $22.4K Tue, $19.8K Wed, $24.1K Thu, $28.9K Fri (peak), $21.3K Sat, $16.7K Sun\nWeek of Dec 2: $19.5K Mon, $23.7K Tue, $21.2K Wed, $25.8K Thu, $30.2K Fri (peak), $22.9K Sat, $18.1K Sun\n\nAverage: $22.4K/day. Trend: +8.3% week-over-week.",
  "query": "SELECT DATE(created_at) as date, TO_CHAR(created_at, 'Dy') as day_of_week, SUM(amount) as revenue FROM orders WHERE created_at >= CURRENT_DATE - INTERVAL '14 days' GROUP BY DATE(created_at), TO_CHAR(created_at, 'Dy') ORDER BY date"
}
```

### Monthly Trend

**Question:** "Show me monthly order counts for this year"

**Response:**
```json
{
  "answer": "2024 monthly order counts:\nJan: 2,345 | Feb: 2,567 | Mar: 3,123 | Apr: 3,456 | May: 3,890 | Jun: 4,234 | Jul: 4,567 | Aug: 4,890 | Sep: 5,123 | Oct: 5,456 | Nov: 5,789 | Dec: 4,234 (partial)\n\nTotal: 49,674 orders. Average: 4,556/month. Growth: +147% from Jan to Nov peak.",
  "query": "SELECT TO_CHAR(created_at, 'Mon') as month, EXTRACT(MONTH FROM created_at) as month_num, COUNT(*) as order_count FROM orders WHERE EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE) GROUP BY TO_CHAR(created_at, 'Mon'), EXTRACT(MONTH FROM created_at) ORDER BY month_num"
}
```

### Quarterly Comparison

**Question:** "Compare Q3 and Q4 revenue"

**Response:**
```json
{
  "answer": "Q3 2024 revenue: $1,234,567 (12,345 orders, $100.03 avg)\nQ4 2024 revenue: $1,456,789 (13,567 orders, $107.38 avg)\n\nQ4 vs Q3: +$222,222 revenue (+18.0%), +1,222 orders (+9.9%), +$7.35 avg order value (+7.3%)",
  "query": "WITH quarterly_data AS (SELECT EXTRACT(QUARTER FROM created_at) as quarter, COUNT(*) as orders, SUM(amount) as revenue, AVG(amount) as avg_order FROM orders WHERE created_at >= '2024-07-01' GROUP BY EXTRACT(QUARTER FROM created_at)) SELECT q3.revenue as q3_revenue, q4.revenue as q4_revenue, q4.revenue - q3.revenue as difference, ROUND(100.0 * (q4.revenue - q3.revenue) / q3.revenue, 2) as pct_change FROM (SELECT * FROM quarterly_data WHERE quarter = 3) q3, (SELECT * FROM quarterly_data WHERE quarter = 4) q4"
}
```

## Year-Over-Year Comparisons

### Simple YoY

**Question:** "How does this month compare to the same month last year?"

**Response:**
```json
{
  "answer": "December 2024: $456,789 revenue, 4,234 orders\nDecember 2023: $389,012 revenue, 3,890 orders\n\nYear-over-year growth: +$67,777 (+17.4% revenue), +344 orders (+8.8%)\nAverage order value increased from $100.00 to $107.90 (+7.9%)",
  "query": "WITH monthly_data AS (SELECT DATE_TRUNC('month', created_at) as month, EXTRACT(YEAR FROM created_at) as year, COUNT(*) as orders, SUM(amount) as revenue, AVG(amount) as avg_order FROM orders WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 year') GROUP BY DATE_TRUNC('month', created_at), EXTRACT(YEAR FROM created_at)) SELECT curr.revenue as current_revenue, prev.revenue as last_year_revenue, curr.revenue - prev.revenue as difference, ROUND(100.0 * (curr.revenue - prev.revenue) / prev.revenue, 2) as pct_change FROM monthly_data curr LEFT JOIN monthly_data prev ON EXTRACT(MONTH FROM curr.month) = EXTRACT(MONTH FROM prev.month) AND prev.year = curr.year - 1 WHERE curr.year = EXTRACT(YEAR FROM CURRENT_DATE)"
}
```

### Multi-Period YoY

**Question:** "How many sales of Product A did we have each quarter last year, and how does that compare to the year before?"

**Response:**
```json
{
  "answer": "Product A quarterly sales comparison:\n\n2023:\nQ1: 1,234 units (2022: 1,074 units, +14.9%)\nQ2: 1,567 units (2022: 1,287 units, +21.8%)\nQ3: 1,890 units (2022: 1,993 units, -5.2%)\nQ4: 2,103 units (2022: 1,598 units, +31.6%)\n\nFull Year:\n2023: 6,794 units\n2022: 5,952 units\nGrowth: +842 units (+14.1%)\n\nBest quarter: Q4 2023 with 31.6% YoY growth\nOnly decline: Q3 2023 down 5.2%",
  "query": "WITH quarterly_sales AS (SELECT EXTRACT(YEAR FROM o.created_at) as year, EXTRACT(QUARTER FROM o.created_at) as quarter, SUM(oi.quantity) as total_quantity FROM orders o INNER JOIN order_items oi ON o.id = oi.order_id INNER JOIN products p ON oi.product_id = p.id WHERE p.name = 'Product A' AND o.created_at >= '2022-01-01' AND o.created_at < '2024-01-01' GROUP BY EXTRACT(YEAR FROM o.created_at), EXTRACT(QUARTER FROM o.created_at)) SELECT curr.year, curr.quarter, curr.total_quantity as current_year, prev.total_quantity as previous_year, curr.total_quantity - prev.total_quantity as difference, ROUND(100.0 * (curr.total_quantity - prev.total_quantity) / prev.total_quantity, 2) as pct_change FROM quarterly_sales curr LEFT JOIN quarterly_sales prev ON curr.quarter = prev.quarter AND prev.year = curr.year - 1 WHERE curr.year = 2023 ORDER BY curr.quarter"
}
```

## Ranking Queries

### Top N

**Question:** "Who are our top 10 customers by revenue?"

**Response:**
```json
{
  "answer": "Top 10 customers by lifetime revenue:\n\n1. Acme Corp - $145,678 (89 orders, customer since 2019)\n2. TechCo Inc - $128,934 (67 orders, customer since 2020)\n3. Global Solutions - $112,456 (54 orders, customer since 2018)\n4. Enterprise Systems - $98,765 (78 orders, customer since 2021)\n5. Innovation Labs - $87,654 (45 orders, customer since 2022)\n6. Digital Dynamics - $76,543 (62 orders, customer since 2020)\n7. Smart Solutions - $68,432 (51 orders, customer since 2021)\n8. Future Tech - $59,321 (43 orders, customer since 2022)\n9. Next Gen Corp - $54,210 (38 orders, customer since 2023)\n10. Prime Industries - $49,876 (41 orders, customer since 2022)\n\nThese top 10 represent $881,869 (23.4% of total revenue)",
  "query": "SELECT c.name, c.customer_since, COUNT(o.id) as order_count, SUM(o.amount) as lifetime_revenue FROM customers c INNER JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name, c.customer_since ORDER BY lifetime_revenue DESC LIMIT 10"
}
```

### Top by Category

**Question:** "What are our best-selling products by category?"

**Response:**
```json
{
  "answer": "Best-selling products by category:\n\nElectronics: MacBook Pro - 1,234 units ($1.9M)\nClothing: Classic T-Shirt - 8,765 units ($263K)\nHome: Coffee Maker - 3,456 units ($345K)\nSports: Running Shoes - 2,890 units ($289K)\nBooks: Data Science Guide - 5,432 units ($271K)\n\nTotal across top products: $3.07M (representing 42% of total revenue)",
  "query": "WITH ranked_products AS (SELECT p.category, p.name, SUM(oi.quantity) as units_sold, SUM(oi.quantity * oi.price) as revenue, ROW_NUMBER() OVER (PARTITION BY p.category ORDER BY SUM(oi.quantity * oi.price) DESC) as rank FROM products p INNER JOIN order_items oi ON p.id = oi.product_id GROUP BY p.category, p.name) SELECT category, name, units_sold, revenue FROM ranked_products WHERE rank = 1 ORDER BY revenue DESC"
}
```

## Multi-Table Joins

### Customer Orders Analysis

**Question:** "Show me customers from New York who made purchases over $500 in the last 30 days"

**Response:**
```json
{
  "answer": "Found 47 New York customers with $500+ purchases in the last 30 days:\n\nTotal orders: 89\nTotal revenue: $67,890\nAverage order value: $763.03\n\nTop customers:\n1. Sarah Johnson (Manhattan) - 3 orders, $2,345\n2. Mike Chen (Brooklyn) - 2 orders, $1,987\n3. Lisa Rodriguez (Queens) - 4 orders, $3,210\n\nAll 47 customers combined represent 12.3% of this month's revenue.",
  "query": "SELECT c.id, c.name, c.city, c.state, COUNT(o.id) as order_count, SUM(o.amount) as total_spent FROM customers c INNER JOIN orders o ON c.id = o.customer_id WHERE c.state = 'NY' AND o.amount > 500 AND o.created_at >= CURRENT_DATE - INTERVAL '30 days' GROUP BY c.id, c.name, c.city, c.state ORDER BY total_spent DESC"
}
```

### Product Performance

**Question:** "Which products have the highest return rate?"

**Response:**
```json
{
  "answer": "Products with highest return rates (min 50 orders):\n\n1. Budget Headphones - 18.5% return rate (234/1,265 orders)\n2. Cheap Keyboard - 15.2% return rate (89/585 orders)\n3. Generic Mouse - 12.8% return rate (156/1,219 orders)\n4. Low-End Monitor - 11.3% return rate (67/593 orders)\n5. Basic Webcam - 9.7% return rate (78/804 orders)\n\nOverall return rate: 5.2%\nRecommendation: Investigate quality issues with Budget Headphones (3.5x average rate)",
  "query": "WITH product_stats AS (SELECT p.name, COUNT(DISTINCT o.id) as total_orders, COUNT(DISTINCT CASE WHEN o.status = 'returned' THEN o.id END) as returned_orders FROM products p INNER JOIN order_items oi ON p.id = oi.product_id INNER JOIN orders o ON oi.order_id = o.id GROUP BY p.id, p.name HAVING COUNT(DISTINCT o.id) >= 50) SELECT name, returned_orders, total_orders, ROUND(100.0 * returned_orders / total_orders, 2) as return_rate FROM product_stats ORDER BY return_rate DESC LIMIT 5"
}
```

## Healthcare Examples

### Patient Admissions

**Question:** "Tell me the average number of patients that were admitted to the ER department last week"

**Response:**
```json
{
  "answer": "ER Admissions for last week (Dec 2-8, 2024):\n\nTotal: 342 patients\nAverage per day: 48.9 patients\n\nDaily breakdown:\nMon: 38 patients (lowest)\nTue: 45 patients\nWed: 42 patients\nThu: 51 patients\nFri: 55 patients\nSat: 67 patients (highest - weekend peak)\nSun: 44 patients\n\nPeak hours: 6pm-10pm averaged 8.2 patients/hour\nCompared to previous week: +5.1% increase",
  "query": "SELECT COUNT(*) as total_admissions, COUNT(*) / 7.0 as avg_per_day, MIN(admitted_at) as week_start, MAX(admitted_at) as week_end, EXTRACT(DOW FROM admitted_at) as day_of_week, COUNT(*) as day_count FROM hospital.admissions WHERE department = 'ER' AND admitted_at >= DATE_TRUNC('week', CURRENT_DATE - INTERVAL '1 week') AND admitted_at < DATE_TRUNC('week', CURRENT_DATE) GROUP BY EXTRACT(DOW FROM admitted_at)"
}
```

### Length of Stay Analysis

**Question:** "What's the average length of stay by department?"

**Response:**
```json
{
  "answer": "Average length of stay by department (last 90 days):\n\nICU: 4.2 days (longest)\nSurgery: 3.8 days\nER: 0.3 days (same-day discharge for most)\nPediatrics: 2.1 days\nMaternity: 2.5 days\nGeneral Medicine: 3.2 days\n\nOverall hospital average: 2.8 days\nTotal patient days: 12,450\nOccupancy rate: 87.3%",
  "query": "SELECT department, COUNT(*) as patient_count, AVG(EXTRACT(EPOCH FROM (discharged_at - admitted_at))/86400) as avg_length_of_stay, SUM(EXTRACT(EPOCH FROM (discharged_at - admitted_at))/86400) as total_patient_days FROM hospital.admissions WHERE admitted_at >= CURRENT_DATE - INTERVAL '90 days' AND discharged_at IS NOT NULL GROUP BY department ORDER BY avg_length_of_stay DESC"
}
```

## Data Discovery Responses

### List Available Data

**Question:** "What data is available in our production database?"

**Response:**
```json
{
  "answer": "Your production database contains:\n\nSales Schema:\n- orders: 2.3M rows (2018-present)\n- order_items: 8.9M rows\n- invoices: 2.1M rows\n- payments: 2.8M rows\n\nCustomers Schema:\n- customers: 450K rows\n- addresses: 680K rows\n- contacts: 1.2M rows\n- preferences: 420K rows\n\nProducts Schema:\n- products: 12K active products\n- categories: 45 categories\n- inventory: 12K SKUs\n- prices: 24K price records\n\nThe database spans 6+ years of operational data.",
  "query": "databasin sql schemas conn-prod --catalog production; databasin sql tables conn-prod --catalog production --schema sales",
  "discovered": {
    "catalogs": ["production", "staging"],
    "schemas": ["sales", "customers", "products", "analytics", "reporting", "admin"],
    "tables": ["orders", "order_items", "customers", "products", "inventory", "..."]
  }
}
```

### Sample Table Structure

**Question:** "Show me what's in the customers table"

**Response:**
```json
{
  "answer": "The customers table has 450,123 rows with these columns:\n\nIdentifiers:\n- id (integer, primary key)\n- external_id (varchar, unique)\n\nPersonal Info:\n- name (varchar)\n- email (varchar, unique)\n- phone (varchar)\n\nLocation:\n- city (varchar)\n- state (varchar, 2-letter code)\n- zip_code (varchar)\n\nMetadata:\n- status (varchar: active/inactive/suspended)\n- customer_since (timestamp)\n- last_order_at (timestamp, nullable)\n- total_orders (integer)\n- lifetime_value (decimal)\n\nSample data shows customers from 2015 to present, mostly 'active' status (92.6%)",
  "query": "SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'customers' ORDER BY ordinal_position; SELECT * FROM customers LIMIT 5"
}
```

## Error Responses

### Table Not Found

**Question:** "Show me data from the sales_summary table"

**Response:**
```json
{
  "answer": "The table 'sales_summary' doesn't exist in this database. Available tables in the sales schema are: orders, order_items, products, invoices, payments. Did you mean one of these?",
  "query": "databasin sql tables conn-prod --catalog production --schema sales",
  "error": "Table 'sales_summary' not found",
  "suggestion": "Check available tables: orders, order_items, products, invoices, payments"
}
```

### Ambiguous Request

**Question:** "Show me the numbers"

**Response:**
```json
{
  "answer": "I need more information to help you. What specific numbers would you like to see? For example:\n\n- Order counts by time period?\n- Revenue totals?\n- Customer counts?\n- Product sales?\n- Inventory levels?\n\nOr if you'd like to explore what's available, I can show you all tables and their data.",
  "query": null,
  "clarification_needed": "Please specify which metrics or data you'd like to analyze"
}
```

### No Connector Specified

**Question:** "How many orders do we have?"

**Response:**
```json
{
  "answer": "I found 5 connectors that might contain order data:\n\n1. Production Database (conn-prod-db) - Primary sales data\n2. Analytics Warehouse (conn-analytics) - Aggregated data\n3. Sales CRM (conn-crm) - CRM order history\n4. Archive Database (conn-archive) - Historical data\n5. Staging Database (conn-staging) - Test environment\n\nWhich database should I query? Or I can check all of them and combine the results.",
  "query": "databasin connectors list",
  "connectors_found": [
    {"id": "conn-prod-db", "name": "Production Database"},
    {"id": "conn-analytics", "name": "Analytics Warehouse"},
    {"id": "conn-crm", "name": "Sales CRM"},
    {"id": "conn-archive", "name": "Archive Database"},
    {"id": "conn-staging", "name": "Staging Database"}
  ]
}
```

## Complex Analytics

### Cohort Analysis

**Question:** "Show me customer retention by signup cohort"

**Response:**
```json
{
  "answer": "Customer retention by signup cohort (monthly):\n\n2024 Cohorts:\nJan 2024: 234 customers, 89% active (month 11)\nFeb 2024: 267 customers, 91% active (month 10)\nMar 2024: 312 customers, 93% active (month 9)\n...\nNov 2024: 456 customers, 98% active (month 1)\n\nTrends:\n- 6-month retention averages 82%\n- 12-month retention averages 76%\n- Best cohort: March 2024 (93% active at 9 months)\n- Recent cohorts show improved retention (+5% vs 2023)",
  "query": "WITH cohorts AS (SELECT DATE_TRUNC('month', customer_since) as cohort_month, COUNT(*) as cohort_size, COUNT(*) FILTER (WHERE status = 'active') as active_count FROM customers WHERE customer_since >= '2024-01-01' GROUP BY DATE_TRUNC('month', customer_since)) SELECT cohort_month, cohort_size, active_count, ROUND(100.0 * active_count / cohort_size, 2) as retention_rate, DATE_PART('month', AGE(CURRENT_DATE, cohort_month)) as months_since_signup FROM cohorts ORDER BY cohort_month"
}
```

### Moving Averages

**Question:** "Show me 7-day moving average of daily sales"

**Response:**
```json
{
  "answer": "Daily sales with 7-day moving average (last 30 days):\n\nCurrent trend: $23,456/day (7-day MA)\n30 days ago: $19,234/day (7-day MA)\nGrowth: +22.0% over the period\n\nPeak day: Dec 7 with $31,234 (33% above MA)\nLowest day: Dec 3 with $15,678 (33% below MA)\n\nWeekday pattern: Fridays average $28K (highest), Sundays $18K (lowest)\n\nThe moving average shows steady upward trend, suggesting strong momentum going into year-end.",
  "query": "WITH daily_sales AS (SELECT DATE(created_at) as date, SUM(amount) as revenue FROM orders WHERE created_at >= CURRENT_DATE - INTERVAL '30 days' GROUP BY DATE(created_at)) SELECT date, revenue, AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7day FROM daily_sales ORDER BY date"
}
```

## Pattern Summary

Every response follows this structure:

```json
{
  "answer": "Human-readable summary with specific numbers and insights",
  "query": "The exact SQL query or command used",
  
  // Optional fields based on context:
  "discovered": {
    "catalogs": [],
    "schemas": [],
    "tables": []
  },
  "error": "Error message if applicable",
  "suggestion": "What to try next",
  "clarification_needed": "What information is missing"
}
```

This ensures:
- ✅ Consistent, parseable output
- ✅ Human-readable answers
- ✅ Reusable queries
- ✅ Clear error handling
- ✅ Easy integration with other tools
