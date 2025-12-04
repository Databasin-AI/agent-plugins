# Pipeline Creation Automation Guide

This document outlines the complete pipeline creation process for Databasin, designed to help you build CLI scripts or automated tools that create pipelines programmatically.

## Pipeline Creation Process Outline

### Step 0: Prerequisites & Initialization

**What you need:**

- User credentials (institutionID, ownerID, internalID/projectId)
- Available connectors for the project (fetch from `/connector` endpoint)
- Connector configurations (loaded from `static/config/connectors/`)
- Pipeline configuration settings

**API Call:**

```
GET /connector?institutionID={id}&internalID={projectId}
```

---

### Step 1: Initial Configuration (Screen 0)

**Information Required:**

- **pipelineName** - String, max 27 chars
- **sourceConnectorID** - Integer (must have `egressTargetSupport: true`)
- **targetConnectorID** - Integer (must have `ingressTargetSupport: true`)
- **ingestionPattern** - "datalake" OR "data warehouse"
- **targetCatalogName** - String (required if data warehouse mode)
- **targetSchemaName** - String (required if datalake mode)
- **createCatalogs** - Boolean (auto-create catalogs)
- **sourceNamingConvention** - Boolean (true = short names, false = long names)

**Validation:**

- Pipeline name must be non-empty
- Source and target connectors must be selected
- If data warehouse: targetCatalogName required
- If datalake: targetSchemaName required

**Note:** When you select the source connector, fetch its wizard config:

```javascript
const wizardConfig = await configClient.getPipelineWizardConfiguration(
	sourceConnector.connectorSubType
);
// This tells you which screens (1-10) you need to complete
const requiredScreens = wizardConfig.sourceConnector.pipelineRequiredScreens;
```

---

### Step 2: Navigate Dynamic Screens (Varies by Connector)

The **requiredScreens** array determines which screens you hit. Common patterns:

#### **For Database Connectors (e.g., MySQL, PostgreSQL)**

**Typical flow:** `[1, 2, 3, 4, 5]` (Catalogs → Artifacts → Columns → Ingest → Final)

**Screen 1 - Catalogs:**

```
GET /connector/catalogs/{connectorID}
```

- Select a catalog from the list
- Store as `selectedCatalog`

**Screen 2 - Artifacts (Tables):**

```
GET /v2/connector/tables/{connectorID}?schema={selectedSchema}&catalog={selectedCatalog}
```

- Select one or more tables/artifacts
- Store as array: `selectedArtifacts`

**Screen 3 - Columns:**

```
POST /connector/columns
Body: { connectorID, objects: [selectedArtifacts], chosenDatabaseSchema: selectedSchema }
```

- For each artifact, select which columns to ingest
- Store as: `selectedColumns[tableName] = [column1, column2, ...]`

**Screen 4 - Ingestion Options:**

```
POST /connector/ingestiontype
Body: { connectorID, objects: [selectedArtifacts], chosenDatabaseSchema: selectedSchema }
```

- For each artifact, configure:
  - ingestionType (full, delta, snapshot)
  - watermarkColumnName (for delta)
  - mergeColumns (for delta)
  - backloadNumDays
  - snapshotRetentionPeriod
  - detectDeletes (for delta with merge)
  - autoExplode (for nested data)

---

#### **For File Connectors (e.g., S3, Azure Blob)**

**Typical flow:** `[2, 4, 5]` (Artifacts → Ingest → Final)

**Screen 2 - Artifacts (Files):**

- Can enter wildcard patterns (e.g., `*.csv`, `data_*.json`)
- Or select individual files from connector
- Store as: `selectedArtifacts`

**Screen 4 - Ingestion Options:**

- Per file configuration:
  - sourceFileName (the file path/pattern)
  - sourceFileFormat (csv, json, parquet, xml, etc.)
  - containsHeader (for CSV)
  - columnHeaderLineNumber (for CSV)
  - sourceFileDelimiter (for CSV/TXT)
  - autoExplode (for JSON/nested formats)
  - rowTag (for XML)
  - xsdPath (for XML)

---

#### **For API Connectors**

**Typical flow:** `[8, 9, 10, 4, 5]` or `[10, 4, 5]` (API Config → Auth → Generic → Ingest → Final)

**Screen 8 - API Configuration:** Legacy API config screen
**Screen 9 - API Authentication:** OAuth/token setup
**Screen 10 - Generic API Configuration:** Modern API config

Configuration includes:

- API endpoint URL
- Authentication method
- Request payload
- Response format

---

### Step 3: Final Configuration (Screen 5)

**Job Details Required:**

- **tags** - String array (optional)
- **jobClusterSize** - "S" | "M" | "L" | "XL"
- **emailNotifications** - Email array
- **jobRunSchedule** - Cron string (e.g., "0 10 \* \* \*")
- **jobRunTimeZone** - Timezone string (e.g., "UTC")
- **jobTimeout** - Integer (seconds, default 43200)

**Validation:**

- Schedule, timeout, and cluster size must all be set

---

### Step 4: Build Final Payload & Create

**Assemble the complete payload:**

```javascript
{
  institutionID: Number,
  internalID: String,
  ownerID: Number,
  pipelineName: String,
  isPrivate: 0 | 1,
  connectorTechnology: [sourceConnectorSubType],
  targetCatalogName: String,
  targetSchemaName: String,
  ingestionPattern: "data warehouse" | "datalake",
  createCatalogs: Boolean,
  sourceNamingConvention: Boolean,
  jobDetails: {
    tags: [],
    jobClusterSize: String,
    emailNotifications: [],
    jobRunSchedule: String,
    jobRunTimeZone: String,
    jobTimeout: String
  },
  items: [
    {
      sourceConnectionID: Number,
      targetConnectionID: Number,
      artifactType: Number, // derived from connector type
      sourceDatabaseName: String,
      sourceSchemaName: String,
      sourceTableName: String,
      sourceColumnNames: [String] | null, // null = all columns
      targetDatabaseName: String,
      targetSchemaName: String,
      targetTableName: String,
      ingestionType: String,
      watermarkColumnName: [],
      mergeColumns: [],
      backloadNumDays: Number,
      snapshotRetentionPeriod: Number,
      detectDeletes: Boolean,
      autoExplode: Boolean,
      // File-specific fields
      sourceFileName: String,
      sourceFileFormat: String,
      sourceFileDelimiter: String,
      containsHeader: Boolean,
      columnHeaderLineNumber: Number,
      // API-specific fields
      apiRoute: String,
      apiCallType: String,
      apiPayload: String,
      apiResponseFormat: String
    }
    // ... one item per selected artifact
  ]
}
```

**Submit:**

```
POST /pipeline
Body: JSON.stringify(payload)
```

---

## Key Gotchas for CLI Implementation

### 1. Connector Type Mapping

Need to map connector subType (e.g., "mysql") to artifactType ID (1=RDBMS, 3=File, etc.)

- Reference: `src/lib/pipelines/PipelinesApiClient.js:88`

### 2. Data Type Conversions

Backend is picky about types:

- `isPrivate`: Boolean → 0|1
- `jobTimeout`: Number → String
- Boolean fields like `containsHeader`, `detectDeletes` need careful handling

### 3. Dynamic Screens

Each connector config defines which screens to show via `pipelineRequiredScreens`

- Don't assume all connectors follow the same path

### 4. Column Selection

- `null` = all columns
- Array = specific columns only
- Track which tables were "modified" to know when to send the array

### 5. File Format Detection

Auto-detect from extension (`.csv`, `.json`, etc.) and set appropriate defaults

- Reference: `src/lib/pipelines/ArtifactWizardViewModelBase.svelte.js:656`

### 6. Validation Per Screen

Each screen has its own validation logic:

- **Initial**: name + connectors + target config
- **Artifacts**: at least 1 selected
- **Columns**: at least 1 column across all tables
- **Ingest**: all items must be valid
- **Final**: schedule + cluster + timeout set

---

## Implementation Strategy

### Option 1: Interactive CLI

Prompt user for each piece of information in sequence:

1. List available connectors, ask user to select source and target
2. Fetch wizard config to determine required screens
3. Walk through each screen, prompting for necessary data
4. Build final payload and submit

### Option 2: Configuration File

Accept a JSON/YAML config file with all required information:

```yaml
pipeline:
  name: 'My Pipeline'
  sourceConnector: 'mysql-connector-1'
  targetConnector: 'snowflake-connector-1'
  ingestionPattern: 'data warehouse'
  targetCatalog: 'analytics'

artifacts:
  - table: 'users'
    columns: ['id', 'email', 'created_at']
    ingestionType: 'delta'
    watermark: 'updated_at'
  - table: 'orders'
    columns: null # all columns
    ingestionType: 'full'

schedule:
  cron: '0 10 * * *'
  timezone: 'UTC'
  clusterSize: 'M'
```

### Option 3: Programmatic API

Create a library that exposes methods for each step:

```javascript
const pipelineBuilder = new PipelineBuilder(credentials);
await pipelineBuilder.setConnectors(sourceId, targetId);
await pipelineBuilder.selectArtifacts(['table1', 'table2']);
await pipelineBuilder.configureIngestion({ ... });
await pipelineBuilder.setSchedule({ ... });
const result = await pipelineBuilder.create();
```

---

## Screen Flow Reference

### Screen ID Mapping

- **0**: Initial configuration (always required)
- **1**: Catalogs selection
- **2**: Artifacts/Tables selection
- **3**: Columns selection
- **4**: Ingestion options
- **5**: Final configuration (always required)
- **6**: Databases selection (alternative to catalogs)
- **7**: Schemas selection
- **8**: API Configuration (legacy)
- **9**: API Authentication
- **10**: Generic API Configuration (modern)

### Common Screen Flows by Connector Type

**RDBMS (MySQL, PostgreSQL, SQL Server):**

```
[0, 1, 2, 3, 4, 5]
Initial → Catalogs → Artifacts → Columns → Ingest → Final
```

**File Storage (S3, Azure Blob):**

```
[0, 2, 4, 5]
Initial → Artifacts → Ingest → Final
```

**Cloud Warehouse (Snowflake, Databricks):**

```
[0, 6, 7, 2, 3, 4, 5]
Initial → Databases → Schemas → Artifacts → Columns → Ingest → Final
```

**API Connectors:**

```
[0, 10, 4, 5]
Initial → API Config → Ingest → Final
```

---

## File References

- **Wizard ViewModel**: `src/lib/pipelines/PipelineCreationWizardViewModel.svelte.js`
- **Base ViewModel**: `src/lib/pipelines/ArtifactWizardViewModelBase.svelte.js`
- **API Client**: `src/lib/pipelines/PipelinesApiClient.js`
- **Initial Screen**: `src/lib/pipelines/screens/InitialScreen.svelte`
- **Artifacts Screen**: `src/lib/pipelines/screens/ArtifactsScreen.svelte`
- **Columns Screen**: `src/lib/pipelines/screens/ColumnsScreen.svelte`
- **Final Screen**: `src/lib/pipelines/screens/FinalConfigurationScreen.svelte`
