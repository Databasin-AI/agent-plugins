# Common SQL Query Patterns for Databasin CLI

This reference provides SQL query patterns for common data exploration and analysis tasks when using the Databasin CLI.

## Data Exploration

### Sample Data from a Table
```sql
-- Basic sample
SELECT * FROM table_name LIMIT 10;

-- Sample with specific columns
SELECT id, name, email, created_at 
FROM users 
LIMIT 5;

-- Random sample (PostgreSQL)
SELECT * 
FROM table_name 
ORDER BY RANDOM() 
LIMIT 100;
```

### Table Schema Information
```sql
-- PostgreSQL: Table structure
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND table_name = 'users'
ORDER BY ordinal_position;

-- MySQL: Table structure
DESCRIBE table_name;

-- SQL Server: Table structure
EXEC sp_columns table_name;
```

### Record Counts
```sql
-- Simple count
SELECT COUNT(*) as total_records 
FROM table_name;

-- Count with conditions
SELECT COUNT(*) as active_users 
FROM users 
WHERE status = 'active';

-- Count by group
SELECT 
    status,
    COUNT(*) as count
FROM users
GROUP BY status
ORDER BY count DESC;
```

## Data Quality Checks

### Find NULL Values
```sql
-- Count nulls in specific column
SELECT COUNT(*) - COUNT(email) as null_emails
FROM users;

-- Comprehensive null check
SELECT 
    COUNT(*) as total_records,
    COUNT(email) as non_null_emails,
    COUNT(*) - COUNT(email) as null_emails,
    ROUND(100.0 * (COUNT(*) - COUNT(email)) / COUNT(*), 2) as null_percentage
FROM users;

-- Find rows with null values
SELECT *
FROM users
WHERE email IS NULL
LIMIT 10;
```

### Find Duplicates
```sql
-- Find duplicate emails
SELECT 
    email,
    COUNT(*) as count
FROM users
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY count DESC;

-- Show duplicate records
WITH duplicates AS (
    SELECT email, COUNT(*) as count
    FROM users
    GROUP BY email
    HAVING COUNT(*) > 1
)
SELECT u.*
FROM users u
INNER JOIN duplicates d ON u.email = d.email
ORDER BY u.email, u.created_at;
```

### Data Range Analysis
```sql
-- Find min/max dates
SELECT 
    MIN(created_at) as earliest_record,
    MAX(created_at) as latest_record,
    DATEDIFF(day, MIN(created_at), MAX(created_at)) as days_span
FROM orders;

-- Find min/max values
SELECT 
    MIN(amount) as min_amount,
    MAX(amount) as max_amount,
    AVG(amount) as avg_amount,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) as median_amount
FROM orders;
```

### Outlier Detection
```sql
-- Find outliers using standard deviation
WITH stats AS (
    SELECT 
        AVG(amount) as mean,
        STDDEV(amount) as std_dev
    FROM orders
)
SELECT *
FROM orders, stats
WHERE ABS(amount - mean) > 3 * std_dev;

-- Find top/bottom values
SELECT * 
FROM orders 
ORDER BY amount DESC 
LIMIT 10;  -- Top 10

SELECT * 
FROM orders 
ORDER BY amount ASC 
LIMIT 10;  -- Bottom 10
```

## Time-Based Queries

### Filter by Date Ranges
```sql
-- Last 30 days
SELECT *
FROM orders
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days';

-- Specific date range
SELECT *
FROM orders
WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';

-- Current month
SELECT *
FROM orders
WHERE DATE_TRUNC('month', created_at) = DATE_TRUNC('month', CURRENT_DATE);

-- Last quarter
SELECT *
FROM orders
WHERE created_at >= DATE_TRUNC('quarter', CURRENT_DATE - INTERVAL '3 months')
  AND created_at < DATE_TRUNC('quarter', CURRENT_DATE);
```

### Time-Based Aggregations
```sql
-- Daily counts
SELECT 
    DATE(created_at) as date,
    COUNT(*) as orders_count,
    SUM(amount) as total_revenue
FROM orders
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Monthly aggregation
SELECT 
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as order_count,
    SUM(amount) as revenue,
    AVG(amount) as avg_order_value
FROM orders
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC;

-- Hour of day analysis
SELECT 
    EXTRACT(HOUR FROM created_at) as hour,
    COUNT(*) as event_count
FROM events
GROUP BY EXTRACT(HOUR FROM created_at)
ORDER BY hour;
```

## Joins and Relationships

### Simple Inner Join
```sql
SELECT 
    o.id as order_id,
    o.created_at,
    o.amount,
    c.name as customer_name,
    c.email as customer_email
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.created_at >= '2024-01-01'
ORDER BY o.created_at DESC;
```

### Left Join (Include All Records from Left Table)
```sql
-- Find customers with no orders
SELECT 
    c.id,
    c.name,
    c.email,
    COUNT(o.id) as order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name, c.email
HAVING COUNT(o.id) = 0;
```

### Multiple Joins
```sql
SELECT 
    o.id as order_id,
    c.name as customer_name,
    p.name as product_name,
    oi.quantity,
    oi.price
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE o.created_at >= CURRENT_DATE - INTERVAL '7 days';
```

## Aggregations and Analytics

### Top N Analysis
```sql
-- Top 10 customers by revenue
SELECT 
    c.name,
    c.email,
    COUNT(o.id) as order_count,
    SUM(o.amount) as total_revenue
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name, c.email
ORDER BY total_revenue DESC
LIMIT 10;

-- Top products by quantity sold
SELECT 
    p.name,
    SUM(oi.quantity) as total_quantity,
    SUM(oi.quantity * oi.price) as total_revenue
FROM products p
INNER JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id, p.name
ORDER BY total_quantity DESC
LIMIT 20;
```

### Running Totals
```sql
-- Running total of revenue
SELECT 
    DATE(created_at) as date,
    SUM(amount) as daily_revenue,
    SUM(SUM(amount)) OVER (ORDER BY DATE(created_at)) as running_total
FROM orders
GROUP BY DATE(created_at)
ORDER BY date;
```

### Window Functions
```sql
-- Rank customers by revenue
SELECT 
    name,
    total_revenue,
    RANK() OVER (ORDER BY total_revenue DESC) as revenue_rank
FROM (
    SELECT 
        c.id,
        c.name,
        SUM(o.amount) as total_revenue
    FROM customers c
    INNER JOIN orders o ON c.id = o.customer_id
    GROUP BY c.id, c.name
) customer_revenue;

-- Calculate moving average
SELECT 
    DATE(created_at) as date,
    SUM(amount) as daily_revenue,
    AVG(SUM(amount)) OVER (
        ORDER BY DATE(created_at) 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as seven_day_avg
FROM orders
GROUP BY DATE(created_at)
ORDER BY date;
```

## Text Search and Pattern Matching

### Basic Text Filters
```sql
-- Starts with
SELECT * FROM users 
WHERE email LIKE 'john%';

-- Contains
SELECT * FROM products 
WHERE name LIKE '%laptop%';

-- Ends with
SELECT * FROM users 
WHERE email LIKE '%@gmail.com';

-- Case-insensitive search (PostgreSQL)
SELECT * FROM products 
WHERE name ILIKE '%MacBook%';
```

### Regular Expression Search
```sql
-- PostgreSQL: Find emails with specific pattern
SELECT * FROM users 
WHERE email ~ '^[a-z]+\.[a-z]+@company\.com$';

-- Find phone numbers
SELECT * FROM customers 
WHERE phone ~ '^\d{3}-\d{3}-\d{4}$';
```

## Conditional Logic

### CASE Statements
```sql
-- Categorize customers
SELECT 
    id,
    name,
    total_orders,
    CASE 
        WHEN total_orders >= 100 THEN 'VIP'
        WHEN total_orders >= 50 THEN 'Premium'
        WHEN total_orders >= 10 THEN 'Regular'
        ELSE 'New'
    END as customer_tier
FROM (
    SELECT 
        c.id,
        c.name,
        COUNT(o.id) as total_orders
    FROM customers c
    LEFT JOIN orders o ON c.id = o.customer_id
    GROUP BY c.id, c.name
) customer_orders;

-- Conditional aggregation
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_orders,
    COUNT(CASE WHEN amount > 100 THEN 1 END) as high_value_orders,
    COUNT(CASE WHEN amount <= 100 THEN 1 END) as low_value_orders
FROM orders
GROUP BY DATE(created_at);
```

## Subqueries

### Subquery in WHERE Clause
```sql
-- Find customers who ordered above average amount
SELECT *
FROM customers
WHERE id IN (
    SELECT customer_id
    FROM orders
    WHERE amount > (SELECT AVG(amount) FROM orders)
);
```

### Correlated Subquery
```sql
-- Find each customer's most recent order
SELECT 
    c.id,
    c.name,
    o.created_at as last_order_date
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
WHERE o.created_at = (
    SELECT MAX(created_at)
    FROM orders o2
    WHERE o2.customer_id = c.id
);
```

### Common Table Expressions (CTEs)
```sql
-- Multiple CTEs for complex analysis
WITH monthly_revenue AS (
    SELECT 
        DATE_TRUNC('month', created_at) as month,
        SUM(amount) as revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', created_at)
),
monthly_customers AS (
    SELECT 
        DATE_TRUNC('month', created_at) as month,
        COUNT(DISTINCT customer_id) as customer_count
    FROM orders
    GROUP BY DATE_TRUNC('month', created_at)
)
SELECT 
    r.month,
    r.revenue,
    c.customer_count,
    r.revenue / c.customer_count as revenue_per_customer
FROM monthly_revenue r
INNER JOIN monthly_customers c ON r.month = c.month
ORDER BY r.month DESC;
```

## Data Transformation

### String Manipulation
```sql
-- Concatenate columns
SELECT 
    CONCAT(first_name, ' ', last_name) as full_name,
    email
FROM users;

-- Extract parts of strings
SELECT 
    email,
    SPLIT_PART(email, '@', 1) as username,
    SPLIT_PART(email, '@', 2) as domain
FROM users;

-- Change case
SELECT 
    UPPER(name) as name_upper,
    LOWER(email) as email_lower
FROM users;
```

### Date Manipulation
```sql
-- Extract date parts
SELECT 
    created_at,
    EXTRACT(YEAR FROM created_at) as year,
    EXTRACT(MONTH FROM created_at) as month,
    EXTRACT(DAY FROM created_at) as day,
    EXTRACT(DOW FROM created_at) as day_of_week
FROM orders;

-- Date arithmetic
SELECT 
    created_at,
    created_at + INTERVAL '7 days' as week_later,
    created_at - INTERVAL '1 month' as month_ago
FROM orders;

-- Format dates
SELECT 
    TO_CHAR(created_at, 'YYYY-MM-DD') as date_string,
    TO_CHAR(created_at, 'Month DD, YYYY') as formatted_date
FROM orders;
```

## Performance Optimization

### Using EXPLAIN
```sql
-- Analyze query execution plan
EXPLAIN ANALYZE
SELECT *
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.created_at >= '2024-01-01';
```

### Index Usage Hints
```sql
-- Ensure proper indexing for common queries
-- Index on foreign keys
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- Index on frequently filtered columns
CREATE INDEX idx_orders_created_at ON orders(created_at);

-- Composite index for multiple columns
CREATE INDEX idx_orders_customer_date ON orders(customer_id, created_at);
```

## Exporting Data

### CSV Export with Headers
```bash
# Using databasin CLI
databasin sql exec conn-123 "
SELECT 
    id,
    name,
    email,
    created_at
FROM users
WHERE status = 'active'
ORDER BY created_at DESC
" --csv > active_users.csv
```

### JSON Export
```bash
# Export as JSON array
databasin sql exec conn-123 "
SELECT 
    json_agg(json_build_object(
        'id', id,
        'name', name,
        'email', email
    )) as users
FROM users
" --json > users.json
```

## Tips for Effective Queries

1. **Always use LIMIT when exploring:** Prevents accidentally pulling millions of rows
2. **Filter early:** Use WHERE clauses to reduce data before JOINs
3. **Use appropriate indexes:** Check execution plans with EXPLAIN
4. **Aggregate wisely:** Use GROUP BY efficiently
5. **Test incrementally:** Build complex queries step by step
6. **Comment your queries:** Use `-- comment` for clarity
7. **Format for readability:** Use proper indentation and line breaks

## Common Mistakes to Avoid

❌ **Don't:**
```sql
-- Select everything without LIMIT
SELECT * FROM large_table;

-- Use SELECT DISTINCT when not needed
SELECT DISTINCT * FROM users WHERE id = 123;

-- Use subqueries when JOIN would be faster
SELECT * FROM orders WHERE customer_id IN (SELECT id FROM customers);
```

✅ **Do:**
```sql
-- Always use LIMIT when exploring
SELECT * FROM large_table LIMIT 10;

-- Only use DISTINCT when necessary
SELECT * FROM users WHERE id = 123;

-- Use JOINs for better performance
SELECT o.* FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;
```
