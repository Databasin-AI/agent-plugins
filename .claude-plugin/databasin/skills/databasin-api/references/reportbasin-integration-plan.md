# ReportBasin Integration Plan for Claude Code

## Executive Summary

This plan outlines the integration of Databasin's ReportBasin module capabilities into Claude Code, enabling users to build Apache ECharts-powered reports through natural conversation. The integration leverages existing schema discovery and SQL generation scripts while adding new conversational workflows specifically for report building.

---

## Current State Analysis

### Existing Infrastructure (✅ Available)

**databasin-api Skill Scripts:**

- `list-schemas.ts` - Discover available database schemas
- `list-tables.ts` - List tables in a schema
- `describe-table.ts` - Get column definitions for a table
- `get-schema-context.ts` - Build comprehensive schema context
- `generate-sql.ts` - Generate SQL from natural language
- `execute-sql.ts` - Execute SQL queries via connector
- `fix-sql.ts` - Auto-fix failed SQL queries

**ReportBasin Web Module:**

- Context establishment system (9 critical rules for LLM)
- SQL extraction patterns (multiple formats)
- Auto-retry mechanism for failed queries
- ECharts integration with 31+ chart types
- ExtendedChartMapper for intelligent chart selection
- Template-based dashboards (Executive, Creative, Analytical, Standard)

### Gap Analysis

**Missing Components for Claude Code:**

1. ❌ Interactive report requirements gathering
2. ❌ Multi-query report building workflow
3. ❌ Chart generation and configuration
4. ❌ Report artifact generation (HTML export)
5. ❌ Conversational refinement capabilities
6. ❌ Specialized report-building agent

---

## Integration Architecture

### Phase 1: Enhanced Script Layer

#### New Scripts to Add

**1. `build-report-context.ts`**

- **Purpose**: Establish report-specific context with LLM
- **Inputs**:
  - connectorID (warehouse connector)
  - llmConnectorID (LLM connector)
  - schema context (from get-schema-context.ts)
- **Process**:
  1. Load schema context
  2. Format the 9 critical rules for SQL generation
  3. Send context message to LLM
  4. Verify acknowledgment
  5. Return context ID/session marker
- **Output**: Context establishment confirmation + session context

**2. `generate-report-queries.ts`**

- **Purpose**: Generate multiple SQL queries for a report dashboard
- **Inputs**:
  - llmConnectorID
  - report requirements (natural language)
  - established context
  - template style (executive, creative, analytical, standard)
- **Process**:
  1. Use established context
  2. Request SQL queries based on requirements
  3. Extract SQL queries from response
  4. Parse query titles, suggestions, metadata
  5. Return structured query definitions
- **Output**: Array of query definitions with SQL, titles, suggestions

**3. `execute-report-queries.ts`**

- **Purpose**: Execute all report queries with retry logic
- **Inputs**:
  - connectorID (warehouse)
  - llmConnectorID (for fixes)
  - query definitions array
  - context (for retry fixes)
- **Process**:
  1. Execute each query sequentially
  2. On failure, use fix-sql.ts to attempt repair
  3. Track success/failure/auto-fixed status
  4. Return results with metadata
- **Output**: Query results with execution metadata

**4. `suggest-chart-types.ts`**

- **Purpose**: Analyze query results and suggest optimal chart types
- **Inputs**:
  - query results (columns + sample data)
  - template style preference
- **Process**:
  1. Analyze data patterns (time series, hierarchical, KPI, etc.)
  2. Apply template-specific chart preferences
  3. Generate chart type recommendations
  4. Provide chart configuration suggestions
- **Output**: Chart type + configuration for each query

**5. `generate-report-artifact.ts`**

- **Purpose**: Create standalone HTML report with embedded ECharts
- **Inputs**:
  - report title/description
  - query results
  - chart configurations
  - template style
- **Process**:
  1. Generate HTML structure
  2. Embed ECharts library
  3. Generate chart initialization code
  4. Apply template styling
  5. Create self-contained HTML file
- **Output**: HTML file path

**6. `refine-report.ts`**

- **Purpose**: Modify existing report based on user feedback
- **Inputs**:
  - current report definition
  - refinement request (natural language)
  - llmConnectorID
  - context
- **Process**:
  1. Analyze refinement request
  2. Determine modifications needed (template change, query changes, chart type changes)
  3. Generate modified SQL if needed
  4. Return updated report definition
- **Output**: Updated report definition

---

### Phase 2: Conversational Agent

#### New Agent: `reportbasin-builder`

**Agent Configuration:**

```yaml
name: reportbasin-builder
description: Interactive agent for building Apache ECharts reports from Databasin warehouse data. Guides users through report creation with natural conversation.
tools: All tools (especially databasin-api skill scripts)
```

**Conversational Flow:**

```
1. GATHER REQUIREMENTS
   ├─ Identify warehouse connector
   ├─ Discover available schemas/tables
   ├─ Understand report purpose
   └─ Determine template style preference

2. BUILD CONTEXT
   ├─ Call build-report-context.ts
   ├─ Establish schema understanding with LLM
   └─ Confirm context acknowledgment

3. GENERATE QUERIES
   ├─ Collect report requirements (KPIs, trends, breakdowns)
   ├─ Call generate-report-queries.ts
   ├─ Show user the proposed queries
   └─ Allow refinement

4. EXECUTE & VISUALIZE
   ├─ Call execute-report-queries.ts
   ├─ Handle auto-retry for failures
   ├─ Call suggest-chart-types.ts
   ├─ Show preview of data + chart types
   └─ Allow chart type overrides

5. GENERATE ARTIFACT
   ├─ Call generate-report-artifact.ts
   ├─ Create HTML report file
   ├─ Show file location
   └─ Offer to open in browser

6. REFINE (Optional Loop)
   ├─ Accept refinement requests
   ├─ Call refine-report.ts
   └─ Jump back to step 4
```

**Example Conversation:**

```
User: Help me build a report on our sales data

Agent: I'll help you build a sales report. Let me start by discovering your available data.

[Calls list-schemas.ts, list-tables.ts]

Agent: I found these tables in your warehouse:
- main.customers (id, name, region, signup_date)
- main.orders (id, customer_id, order_date, total)
- main.products (id, name, category, price)

What would you like to analyze? For example:
- Revenue trends over time
- Top customers by sales
- Product performance by category

User: I want to see revenue trends and top customers

Agent: Great! I'll create a report with:
1. Revenue trend over time
2. Top 10 customers by total sales

What style would you prefer?
- Executive (clean, professional, KPI-focused)
- Creative (unique visualizations)
- Analytical (data-focused charts)
- Standard (balanced approach)

User: Executive style

Agent: Perfect. Let me build the report...

[Calls build-report-context.ts]
[Calls generate-report-queries.ts with executive template]

Agent: I've generated these queries:
1. "Monthly Revenue Trend" - Line chart showing revenue over last 12 months
2. "Top 10 Customers" - Bar chart of highest-value customers

Executing queries...

[Calls execute-report-queries.ts]

Agent: ✅ All queries executed successfully!
- Query 1: 12 rows (Jan-Dec revenue)
- Query 2: 10 rows (top customers)

[Calls suggest-chart-types.ts]

Agent: Generating chart configurations...
- Monthly Revenue: Line chart with gradient fill
- Top Customers: Horizontal bar chart

[Calls generate-report-artifact.ts]

Agent: ✅ Report generated!
📄 File: /home/user/reports/sales-executive-report-2025-11-20.html

The report includes:
- Executive-style dashboard
- 2 interactive ECharts visualizations
- Standalone HTML (no dependencies)

Would you like me to:
- Open the report in your browser
- Make any changes to the report
- Add more charts
```

---

### Phase 3: LLM Integration Patterns

#### Critical Rules System

**Context Message Template:**

```
During this conversation, we will be discussing the following tables and columns:

[TABLE LIST WITH COLUMNS]

IMPORTANT RULES:
1. You may only use the exact table names and column names provided above
2. All queries must be valid Apache Trino SQL (or Databricks if specified)
3. Never make up or assume table names or column names
4. When asked for dashboards or reports, respond with only the SQL queries needed
5. Each query should be preceded by a comment line: -- Query Title
6. Do not return JSON structures, chart types, or visualization recommendations
7. Do not use time slices like CURRENT_DATE - INTERVAL '7' DAY
8. Return multiple queries when building dashboards
9. Each query should serve a specific analytical purpose

Please confirm your understanding by responding: "I understand and agree"
```

#### SQL Extraction Patterns

The system supports multiple SQL formats from LLM:

**Pattern 1: Markdown code blocks**

```sql
SELECT * FROM table
```

**Pattern 2: SQL comments with titles**

```sql
-- Monthly Revenue Trend
-- X-SUGGESTION: month, Y-SUGGESTION: revenue
SELECT
  DATE_TRUNC('month', order_date) as month,
  SUM(total) as revenue
FROM main.orders
GROUP BY 1
ORDER BY 1;
```

**Pattern 3: JSON format** (legacy support)

```json
{
  "queries": [
    {
      "title": "Revenue Trend",
      "sql": "SELECT ...",
      "chartTypes": {...},
      "dataPattern": "time-series"
    }
  ]
}
```

#### Auto-Retry Mechanism

**Fix Request Format:**

```
The following SQL query failed with an error. Please fix it and return only the corrected SQL query:

Failed SQL:
[ORIGINAL SQL]

Error:
[ERROR MESSAGE]

Please provide only the fixed SQL query.
```

**Success Indicators:**

- `wasAutoFixed: true` flag
- Console logs: "✅ Fixed query succeeded! Rows: X"
- Error details preserved for debugging

---

### Phase 4: Chart Generation System

#### Chart Type Intelligence

**Data Pattern Detection:**

```typescript
interface DataPatterns {
	isTimeSeries: boolean; // Date/time columns present
	isHierarchical: boolean; // Parent-child relationships
	isFlow: boolean; // Source-target columns
	isKPI: boolean; // Single numeric value
	isGeographic: boolean; // Location columns
	isCategorical: boolean; // Category columns
	isNumerical: boolean; // Numeric measures
	rowCount: number;
	columnCount: number;
}
```

**Template-Based Selection:**

- **Executive**: Clean gauges, simple bars, donut charts, KPI cards
- **Creative**: Sankey, themeRiver, liquidfill, treemap, sunburst
- **Analytical**: Scatter, heatmap, parallel, box plot, bar/line
- **Standard**: Bar, line, pie, area (safe defaults)

**Chart Type Catalog (31+ types):**

- Basic: bar, line, area, pie, scatter
- Advanced: sankey, treemap, sunburst, radar, heatmap
- Specialized: liquidfill, gauge, funnel, rose, pictorialBar
- Time-based: candlestick, themeRiver
- Statistical: boxplot, parallel

#### ECharts Configuration Generation

**Base Configuration Template:**

```javascript
{
  title: { show: false },  // Titles in card headers
  tooltip: { trigger: 'axis' },
  legend: { bottom: 0 },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '10%',
    containLabel: true
  },
  xAxis: { type: 'category', data: [...] },
  yAxis: { type: 'value' },
  series: [{
    type: 'bar',
    data: [...],
    itemStyle: { ... }
  }]
}
```

**Template-Specific Styling:**

- Executive: Professional blues/grays, subtle gradients
- Creative: Bold colors, unique shapes, animations
- Analytical: Neutral colors, grid emphasis, data labels
- Standard: Default ECharts palette

---

### Phase 5: Report Artifact Generation

#### HTML Export Structure

```html
<!DOCTYPE html>
<html>
	<head>
		<title>Report Title</title>
		<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
		<style>
			/* Template-specific CSS */
			/* Grid layout for charts */
			/* Responsive design */
		</style>
	</head>
	<body>
		<div class="report-container">
			<header>
				<h1>Report Title</h1>
				<p>Report Description</p>
				<p class="metadata">Generated: 2025-11-20 | Source: Databasin</p>
			</header>

			<!-- KPI Cards Section -->
			<div class="kpi-grid">
				<div
					class="kpi-card"
					id="kpi-1"></div>
				<!-- More KPIs -->
			</div>

			<!-- Charts Section -->
			<div class="charts-grid">
				<div class="chart-card">
					<h3>Chart Title</h3>
					<div
						id="chart-1"
						style="height: 400px;"></div>
				</div>
				<!-- More charts -->
			</div>
		</div>

		<script>
			// Chart initialization code
			const chart1 = echarts.init(document.getElementById('chart-1'));
			chart1.setOption({...});

			// Responsive handling
			window.addEventListener('resize', () => {
			  chart1.resize();
			});
		</script>
	</body>
</html>
```

**Key Features:**

- Self-contained (no external dependencies except ECharts CDN)
- Responsive grid layout
- Template-specific styling
- Interactive charts (zoom, pan, tooltip)
- Print-friendly CSS

---

## Implementation Roadmap

### Week 1: Foundation Scripts

- ✅ Audit existing scripts
- 🔨 Create `build-report-context.ts`
- 🔨 Create `generate-report-queries.ts`
- 🔨 Test context establishment flow

### Week 2: Execution & Visualization

- 🔨 Create `execute-report-queries.ts`
- 🔨 Integrate auto-retry mechanism
- 🔨 Create `suggest-chart-types.ts`
- 🔨 Implement pattern detection logic

### Week 3: Artifact Generation

- 🔨 Create `generate-report-artifact.ts`
- 🔨 Build HTML templates for each style
- 🔨 Implement ECharts configuration generation
- 🔨 Test HTML exports

### Week 4: Refinement & Agent

- 🔨 Create `refine-report.ts`
- 🔨 Build `reportbasin-builder` agent
- 🔨 Design conversational flow
- 🔨 Test full workflow end-to-end

### Week 5: Polish & Documentation

- 🔨 Error handling improvements
- 🔨 User-friendly error messages
- 🔨 Agent documentation
- 🔨 Usage examples
- 🔨 Video walkthrough

---

## Technical Considerations

### Performance

- Stream query execution progress to user
- Limit concurrent SQL executions (1 at a time for stability)
- Cache schema context to avoid repeated discovery
- Optimize HTML export file size

### Error Handling

- Clear error messages with actionable suggestions
- Graceful degradation (skip failed charts, continue with successes)
- Schema validation before SQL generation
- Timeout handling for long-running queries

### Security

- JWT token management (reuse existing .token pattern)
- SQL injection prevention (parameterized queries where possible)
- File path validation for HTML export
- Sandboxed HTML execution

### User Experience

- Show progress indicators during execution
- Provide clear status updates ("Executing query 2 of 5...")
- Allow skipping failed queries
- Offer undo/redo for refinements
- Save report definitions for reuse

---

## Integration with Existing Infrastructure

### Reuse Patterns

**From Web Module:**

- SQL extraction logic (ReportbasinApiClient.extractSQLQueries)
- Context establishment pattern (9 critical rules)
- Auto-retry mechanism (fix-sql workflow)
- Chart type mapping logic (ExtendedChartMapper)
- Template definitions (executive, creative, analytical, standard)

**From databasin-api Skill:**

- Schema discovery workflow
- SQL generation pattern
- Execute-with-retry pattern
- Token efficiency flags (--count, --summary, --fields)

**New for Claude Code:**

- Conversational requirements gathering
- Multi-query report coordination
- HTML artifact generation
- Interactive refinement loop

---

## Success Metrics

### Phase 1 Success Criteria

- ✅ Context establishment works reliably (>95% acknowledgment rate)
- ✅ SQL generation produces valid queries (>90% success rate)
- ✅ Auto-retry fixes >70% of failed queries

### Phase 2 Success Criteria

- ✅ End-to-end report generation completes without manual intervention
- ✅ Chart type suggestions are appropriate (user satisfaction >80%)
- ✅ HTML exports are fully functional and standalone

### Phase 3 Success Criteria

- ✅ Agent successfully guides users through report building
- ✅ Refinement loop works for common modifications
- ✅ Users can generate reports in <5 minutes on average

---

## Example Use Cases

### Use Case 1: Sales Executive Dashboard

**User Intent**: Monthly sales performance review

**Flow:**

1. User: "Build me a sales dashboard"
2. Agent discovers sales-related tables
3. Agent suggests KPIs (total revenue, avg order value, customer count)
4. Agent suggests trends (revenue by month, orders by region)
5. Generates 5 SQL queries
6. Executes with auto-retry
7. Creates executive-style dashboard with gauges and line charts
8. Exports to HTML

**Output**: Professional dashboard with 2 KPIs, 3 charts, ~2 minute generation time

### Use Case 2: Product Analytics (Creative Style)

**User Intent**: Understand product category performance

**Flow:**

1. User: "Show me product insights with creative visualizations"
2. Agent discovers product/category tables
3. Suggests sankey flow (category → product → sales)
4. Suggests treemap (category hierarchy by revenue)
5. Suggests themeRiver (category trends over time)
6. Generates 3 advanced SQL queries
7. Creates creative-style dashboard with unique charts

**Output**: Visually striking dashboard with flow diagrams and hierarchical views

### Use Case 3: Customer Behavior Analysis (Analytical)

**User Intent**: Deep dive into customer segments

**Flow:**

1. User: "Analyze customer behavior patterns"
2. Agent discovers customer/order tables
3. Suggests scatter plot (order frequency vs avg order value)
4. Suggests heatmap (day of week vs hour of day orders)
5. Suggests parallel coordinates (customer attributes)
6. Generates analytical queries with statistical functions
7. Creates analytical dashboard with data-dense visualizations

**Output**: Data-focused dashboard with correlation and distribution analysis

---

## Migration Notes

### From Web Module to Claude Code

**What Stays the Same:**

- SQL generation prompts (9 critical rules)
- SQL extraction patterns
- Auto-retry mechanism
- Chart type selection logic
- Template definitions

**What Changes:**

- Delivery mechanism (scripts + agent vs Svelte components)
- User interaction (conversation vs UI forms)
- State management (file-based vs reactive stores)
- Output format (HTML file vs live dashboard)

**Benefits of Claude Code Implementation:**

- No UI development needed
- Faster iteration on prompts and logic
- Direct file system access for reports
- Can integrate with git for report versioning
- Terminal-native workflow for data analysts

---

## Appendix

### A. Script Signatures

```typescript
// build-report-context.ts
interface BuildContextParams {
	connectorID: number;
	llmConnectorID: number;
	schemaContext?: SchemaContext;
}
interface BuildContextResult {
	success: boolean;
	contextID: string;
	acknowledged: boolean;
	message?: string;
}

// generate-report-queries.ts
interface GenerateQueriesParams {
	llmConnectorID: number;
	requirements: string;
	contextID: string;
	templateStyle: 'executive' | 'creative' | 'analytical' | 'standard';
}
interface GenerateQueriesResult {
	queries: QueryDefinition[];
	totalQueries: number;
}

// execute-report-queries.ts
interface ExecuteQueriesParams {
	connectorID: number;
	llmConnectorID: number;
	queries: QueryDefinition[];
	contextID: string;
}
interface ExecuteQueriesResult {
	results: QueryResult[];
	successCount: number;
	failureCount: number;
	autoFixedCount: number;
}

// suggest-chart-types.ts
interface SuggestChartsParams {
	results: QueryResult[];
	templateStyle: string;
}
interface SuggestChartsResult {
	chartConfigs: ChartConfiguration[];
}

// generate-report-artifact.ts
interface GenerateArtifactParams {
	title: string;
	description: string;
	results: QueryResult[];
	chartConfigs: ChartConfiguration[];
	templateStyle: string;
	outputPath?: string;
}
interface GenerateArtifactResult {
	success: boolean;
	filePath: string;
	fileSize: number;
}
```

### B. LLM Prompt Templates

**Context Establishment:**

```
[See "Critical Rules System" section above]
```

**Query Generation:**

```
Based on the schema context we established, generate SQL queries for:
{requirements}

Return multiple SQL queries, each with:
- A comment line starting with -- describing the query
- Optional axis suggestions: -- X-SUGGESTION: col, Y-SUGGESTION: col
- The SQL query itself

Style: {templateStyle}
- Executive: Focus on KPIs and clean trends
- Creative: Unique analytical perspectives
- Analytical: Deep statistical analysis
- Standard: Balanced coverage

Generate 3-5 queries that together provide comprehensive insights.
```

**Query Refinement:**

```
The current dashboard has these queries:
{currentQueries}

The user requests: {refinementRequest}

Modify the queries as needed. Return:
- Keep: Queries that don't need changes
- Modify: Updated SQL for changed queries
- Add: New queries if requested
- Remove: Query titles to remove if requested

Return only the SQL queries in the same format as before.
```

### C. Chart Type Decision Tree

```
1. Check row count
   └─ 1 row → KPI/Gauge

2. Check for date/time columns
   └─ Yes → Time series
      ├─ Single metric → Line chart
      ├─ Multiple metrics → Multi-line or area chart
      └─ Categories over time → Stacked area or themeRiver

3. Check for hierarchical patterns
   └─ Parent-child → Treemap or Sunburst

4. Check for flow patterns (source-target)
   └─ Yes → Sankey diagram

5. Check for geographic columns
   └─ Yes → Map or geo chart

6. Check column types
   ├─ 1 category + 1 numeric → Bar chart
   ├─ 2+ numerics → Scatter plot
   ├─ Category distribution → Pie/Donut
   └─ Multiple dimensions → Parallel coordinates

7. Apply template preferences
   ├─ Executive → Simplify (bar/line/gauge)
   ├─ Creative → Unique (sankey/treemap/liquidfill)
   ├─ Analytical → Data-rich (scatter/heatmap/parallel)
   └─ Standard → Safe defaults (bar/line/pie)
```

---

## Conclusion

This integration plan provides a comprehensive roadmap for bringing ReportBasin's powerful report-building capabilities to Claude Code. By reusing proven patterns from the web module and adapting them to a conversational interface, we can deliver a seamless, AI-powered report generation experience that feels natural in the terminal environment.

The phased approach ensures steady progress with testable milestones, while the detailed technical specifications provide clear implementation guidance.

**Next Steps:**

1. Review and approve this plan
2. Set up project tracking for 5-week timeline
3. Begin Week 1 implementation
4. Schedule weekly demos and iterations

---

**Document Version**: 1.0
**Last Updated**: 2025-11-20
**Status**: 📋 Planning Phase
**Owner**: Databasin Development Team
