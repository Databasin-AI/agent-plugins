# Databasin Pipeline API Endpoints

This document lists all API endpoints used for pipeline operations.

## Authentication

All requests require a JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## Pipeline Endpoints

### Get Pipelines

```
GET /pipeline?institutionID={id}&internalID={projectId}&ownerID={ownerId}
```

Returns a list of all pipelines for a project.

### Get Pipeline Details

```
GET /pipeline/v2/{pipelineID}
```

Returns detailed configuration for a specific pipeline.

### Create Pipeline

```
POST /pipeline
Content-Type: application/json

{
  "institutionID": Number,
  "internalID": String,
  "ownerID": Number,
  "pipelineName": String,
  "isPrivate": 0 | 1,
  "connectorTechnology": [String],
  "targetCatalogName": String,
  "targetSchemaName": String,
  "ingestionPattern": "data warehouse" | "datalake",
  "createCatalogs": Boolean,
  "sourceNamingConvention": Boolean,
  "jobDetails": { ... },
  "items": [ ... ]
}
```

### Update Pipeline

```
PUT /pipeline
Content-Type: application/json

{
  "pipelineID": Number,
  "institutionID": Number,
  "internalID": String,
  "ownerID": Number,
  "isPrivate": 0 | 1,
  "items": [],
  "jobDetails": { ... },
  "sourceNamingConvention": Boolean
}
```

### Delete Pipeline

```
DELETE /pipeline
Content-Type: application/json

{
  "pipelineID": Number
}
```

## Connector Endpoints

### Get Connectors

```
GET /connector?institutionID={id}&internalID={projectId}
```

Returns available connectors for a project.

### Get Catalogs

```
GET /connector/catalogs/{connectorID}
GET /v2/connector/catalogs/{connectorID}
```

First endpoint includes schemas, second is catalogs only.

### Get Schemas

```
GET /v2/connector/schemas/{connectorID}?catalog={catalogName}
```

Returns schemas for a connector (optionally filtered by catalog).

### Get Artifacts (Tables/Files)

```
GET /v2/connector/tables/{connectorID}?schema={schema}&catalog={catalog}
```

Returns available artifacts for a connector/schema combination.

### Get Columns

```
POST /connector/columns
Content-Type: application/json

{
  "connectorID": Number,
  "objects": [String],
  "chosenDatabaseSchema": String
}
```

Returns column information for selected artifacts.

### Get Ingestion Options

```
POST /connector/ingestiontype
Content-Type: application/json

{
  "connectorID": Number,
  "objects": [String],
  "chosenDatabaseSchema": String
}
```

Returns recommended ingestion configuration for selected artifacts.

## Artifact Endpoints

### Add Pipeline Artifacts

```
POST /pipeline/artifacts
Content-Type: application/json

{
  "pipelineID": Number,
  "targetConnectionID": Number,
  "connectorSubType": String,
  "artifacts": [Object],
  "institutionID": Number,
  "ownerID": Number,
  "internalID": String,
  "jobDetails": {}
}
```

### Update Artifact

```
PUT /artifacts
Content-Type: application/json

{
  "artifactID": Number,
  "sourceConnectionID": Number,
  "targetConnectionID": Number,
  "artifactType": Number,
  ... (artifact configuration fields)
}
```

### Delete Artifact

```
DELETE /artifacts
Content-Type: application/json

{
  "artifactID": Number
}
```

### Toggle Artifact Status

```
PUT /artifacts
Content-Type: application/json

{
  "artifactID": Number,
  "isActive": 0 | 1
}
```

## Pipeline Control Endpoints

### Start Pipeline

```
POST /pipeline/run
Content-Type: application/json

{
  "pipelineID": Number,
  "institutionID": Number,
  "internalID": String,
  "ownerID": Number,
  "jobName": String,
  "runType": String
}
```

### Stop Pipeline

```
POST /pipeline/stop
Content-Type: application/json

{
  "pipelineID": Number,
  "jobName": String
}
```

## Response Format

Most endpoints return responses in the format:

```json
{
  "data": <response_data>,
  "error": <error_message_or_null>
}
```

Error responses:

```json
{
	"data": null,
	"error": "Error message description"
}
```
