# Programmatic Usage Guide

**Using the Databasin API client in your TypeScript/JavaScript code**

---

## Overview

Instead of calling the CLI script, you can import and use the API client directly in your code. This is useful for:

- Building automation scripts
- Integrating with other tools
- Creating custom workflows
- Testing and validation

---

## Basic Usage

### Import the Client

```typescript
import { callApi } from './scripts/api-call.ts';
```

---

### Read JWT Token

```typescript
// Read JWT from .token file
const tokenFile = Bun.file('.token');
const jwt = (await tokenFile.text()).trim();
```

---

### Make API Call

```typescript
// Configure API call
const config = {
	jwt: jwt,
	baseUrl: 'http://localhost:9000'
};

// Make GET request
const result = await callApi('GET', '/api/my/projects', config);

if (result.ok) {
	const data = await result.json();
	console.log('Projects:', data);
} else {
	console.error('Error:', result.status, await result.text());
}
```

---

## Complete Example

### Simple Script

```typescript
#!/usr/bin/env bun

// Read JWT token
const tokenFile = Bun.file('.token');
const jwt = (await tokenFile.text()).trim();

const config = {
	jwt: jwt,
	baseUrl: 'http://localhost:9000'
};

// Get projects
const projectsResponse = await callApi('GET', '/api/my/projects', config);

if (projectsResponse.ok) {
	const projects = await projectsResponse.json();
	console.log(`Found ${projects.length} projects`);

	for (const project of projects) {
		console.log(`- ${project.name} (${project.internalId})`);
	}
} else {
	console.error('Failed to get projects:', await projectsResponse.text());
	process.exit(1);
}
```

---

## Advanced Examples

### Example 1: Get Project Resources

```typescript
#!/usr/bin/env bun

const tokenFile = Bun.file('.token');
const jwt = (await tokenFile.text()).trim();

const config = {
	jwt: jwt,
	baseUrl: 'http://localhost:9000'
};

// Get projects
const projectsResponse = await callApi('GET', '/api/my/projects', config);
const projects = await projectsResponse.json();

// For each project, get connectors and pipelines
for (const project of projects) {
	console.log(`\n=== ${project.name} ===`);

	// Get connectors
	const connectorsResponse = await callApi(
		'GET',
		`/api/connector?internalID=${project.internalId}`,
		config
	);

	if (connectorsResponse.ok) {
		const connectors = await connectorsResponse.json();
		console.log(`Connectors: ${connectors.length}`);
	}

	// Get pipelines
	const pipelinesResponse = await callApi(
		'GET',
		`/api/pipeline?internalID=${project.internalId}`,
		config
	);

	if (pipelinesResponse.ok) {
		const pipelines = await pipelinesResponse.json();
		console.log(`Pipelines: ${pipelines.length}`);
	}
}
```

---

### Example 2: Create and Run Pipeline

```typescript
#!/usr/bin/env bun

const tokenFile = Bun.file('.token');
const jwt = (await tokenFile.text()).trim();

const config = {
	jwt: jwt,
	baseUrl: 'http://localhost:9000'
};

// Get user ID
const accountResponse = await callApi('GET', '/api/my/account', config);
const account = await accountResponse.json();

// Create pipeline
const pipelineData = {
	pipelineName: 'Auto-generated Pipeline',
	sourceConnectorID: 58,
	targetConnectorID: 62,
	institutionID: 1,
	internalID: 'N1r8Do',
	ownerID: account.id,
	isActive: 1
};

const createResponse = await callApi('POST', '/api/pipeline', config, JSON.stringify(pipelineData));

if (createResponse.ok) {
	const pipeline = await createResponse.json();
	console.log(`Created pipeline: ${pipeline.pipelineID}`);

	// Run the pipeline
	const runData = { pipelineID: pipeline.pipelineID };
	const runResponse = await callApi('POST', '/api/pipeline/run', config, JSON.stringify(runData));

	if (runResponse.ok) {
		console.log('Pipeline started successfully');
	} else {
		console.error('Failed to run pipeline:', await runResponse.text());
	}
} else {
	console.error('Failed to create pipeline:', await createResponse.text());
}
```

---

### Example 3: Monitor Pipeline Status

```typescript
#!/usr/bin/env bun

const tokenFile = Bun.file('.token');
const jwt = (await tokenFile.text()).trim();

const config = {
	jwt: jwt,
	baseUrl: 'http://localhost:9000'
};

const pipelineID = 123;

// Poll for status
async function checkStatus() {
	const response = await callApi('GET', `/api/pipeline/${pipelineID}`, config);

	if (response.ok) {
		const pipeline = await response.json();
		console.log(`Status: ${pipeline.lastRunStatus}`);
		console.log(`Last run: ${pipeline.lastRunDate}`);

		return pipeline.lastRunStatus;
	}

	return null;
}

// Check every 30 seconds
const interval = setInterval(async () => {
	const status = await checkStatus();

	if (status === 'success' || status === 'failed') {
		clearInterval(interval);
		console.log(`Pipeline finished with status: ${status}`);

		if (status === 'failed') {
			// Get logs
			const logsResponse = await callApi(
				'GET',
				`/api/pipeline/logs?pipelineID=${pipelineID}`,
				config
			);

			if (logsResponse.ok) {
				const logs = await logsResponse.json();
				console.log('Error logs:', logs);
			}
		}
	}
}, 30000);
```

---

### Example 4: Batch Create Connectors

```typescript
#!/usr/bin/env bun

const tokenFile = Bun.file('.token');
const jwt = (await tokenFile.text()).trim();

const config = {
	jwt: jwt,
	baseUrl: 'http://localhost:9000'
};

// Get user context
const accountResponse = await callApi('GET', '/api/my/account', config);
const account = await accountResponse.json();

const projectsResponse = await callApi('GET', '/api/my/projects', config);
const projects = await projectsResponse.json();

const project = projects[0]; // Use first project

// Define connectors to create
const connectorConfigs = [
	{
		connectorName: 'Prod Database',
		connectorType: 'database',
		connectorSubType: 'postgres',
		connectorHost: 'prod-db.example.com',
		connectorPort: '5432'
	},
	{
		connectorName: 'Staging Database',
		connectorType: 'database',
		connectorSubType: 'postgres',
		connectorHost: 'staging-db.example.com',
		connectorPort: '5432'
	}
];

// Create connectors
for (const connectorConfig of connectorConfigs) {
	const payload = {
		...connectorConfig,
		institutionID: project.institutionId,
		internalID: project.internalId,
		ownerID: account.id,
		isPrivate: 0
	};

	const response = await callApi('POST', '/api/connector', config, JSON.stringify(payload));

	if (response.ok) {
		const connector = await response.json();
		console.log(`✓ Created: ${connector.connectorName} (ID: ${connector.connectorID})`);
	} else {
		console.error(`✗ Failed to create ${connectorConfig.connectorName}:`, await response.text());
	}
}
```

---

## Error Handling

### Basic Error Handling

```typescript
const response = await callApi('GET', '/api/my/projects', config);

if (!response.ok) {
	console.error(`HTTP ${response.status}:`, await response.text());
	process.exit(1);
}

const data = await response.json();
```

---

### Try-Catch Error Handling

```typescript
try {
	const response = await callApi('GET', '/api/my/projects', config);

	if (!response.ok) {
		throw new Error(`HTTP ${response.status}: ${await response.text()}`);
	}

	const data = await response.json();
	// Process data
} catch (error) {
	console.error('API call failed:', error.message);
	process.exit(1);
}
```

---

### Retry Logic

```typescript
async function callApiWithRetry(method, endpoint, config, body = null, maxRetries = 3) {
	for (let i = 0; i < maxRetries; i++) {
		try {
			const response = await callApi(method, endpoint, config, body);

			if (response.ok) {
				return response;
			}

			// Don't retry client errors (4xx)
			if (response.status >= 400 && response.status < 500) {
				return response;
			}

			// Retry server errors (5xx)
			console.log(`Retry ${i + 1}/${maxRetries} after ${response.status} error`);
			await new Promise((resolve) => setTimeout(resolve, 1000 * (i + 1)));
		} catch (error) {
			if (i === maxRetries - 1) throw error;
			console.log(`Retry ${i + 1}/${maxRetries} after error:`, error.message);
			await new Promise((resolve) => setTimeout(resolve, 1000 * (i + 1)));
		}
	}
}
```

---

## Token Efficiency in Code

### Use Count First

```typescript
// Check count before fetching
const countResponse = await callApi(
	'GET',
	'/api/connector?internalID=N1r8Do',
	config,
	null,
	{ count: true } // If your client supports options
);

const { count } = await countResponse.json();
console.log(`Found ${count} connectors`);

if (count > 100) {
	// Use pagination or fields filter
	console.log('Large dataset - using pagination');
}
```

---

### Fetch Only Needed Fields

```typescript
// Instead of full response
const response = await callApi('GET', '/api/my/projects?fields=id,name,internalId', config);
```

---

### Pagination

```typescript
async function getAllConnectors(internalID, batchSize = 50) {
	const allConnectors = [];
	let offset = 0;

	while (true) {
		const response = await callApi(
			'GET',
			`/api/connector?internalID=${internalID}&limit=${batchSize}&offset=${offset}`,
			config
		);

		if (!response.ok) break;

		const batch = await response.json();
		if (batch.length === 0) break;

		allConnectors.push(...batch);
		offset += batchSize;
	}

	return allConnectors;
}
```

---

## Best Practices

### 1. Reuse Configuration

```typescript
// Create config once
const config = {
	jwt: (await Bun.file('.token').text()).trim(),
	baseUrl: 'http://localhost:9000'
};

// Reuse for all calls
const projects = await callApi('GET', '/api/my/projects', config);
const connectors = await callApi('GET', '/api/connector', config);
```

---

### 2. Validate Responses

```typescript
const response = await callApi('GET', '/api/my/projects', config);

if (!response.ok) {
	throw new Error(`API error: ${response.status}`);
}

const data = await response.json();

// Validate data structure
if (!Array.isArray(data)) {
	throw new Error('Expected array response');
}
```

---

### 3. Log Appropriately

```typescript
// ✅ Log summary info
console.log(`Processing ${projects.length} projects`);

// ❌ Don't log full API responses (may contain tokens/credentials)
// console.log('All data:', projects);
```

---

### 4. Handle Authentication Errors

```typescript
const response = await callApi('GET', '/api/my/projects', config);

if (response.status === 401) {
	console.error('Authentication failed - JWT token may be expired');
	console.error('Please refresh your .token file');
	process.exit(1);
}
```

---

## Testing

### Mock API Responses

```typescript
// For testing, mock the callApi function
const mockCallApi = async (method, endpoint, config, body = null) => {
	// Return mock data
	return {
		ok: true,
		status: 200,
		json: async () => [{ id: 1, name: 'Test Project', internalId: 'TEST123' }]
	};
};

// Use mock in tests
const response = await mockCallApi('GET', '/api/my/projects', config);
```

---

## Deployment Considerations

### Environment Variables

```typescript
// Read config from environment
const config = {
	jwt: process.env.DATABASIN_JWT || (await Bun.file('.token').text()).trim(),
	baseUrl: process.env.DATABASIN_API_URL || 'http://localhost:9000'
};
```

---

### Docker

```dockerfile
FROM oven/bun:1

WORKDIR /app

COPY . .

# Install dependencies
RUN bun install

# JWT token provided via environment or volume mount
CMD ["bun", "run", "my-script.ts"]
```

---

### CI/CD

```yaml
# GitHub Actions example
- name: Run API Script
  env:
    DATABASIN_JWT: ${{ secrets.DATABASIN_JWT }}
  run: |
    echo "$DATABASIN_JWT" > .token
    bun run my-script.ts
    rm .token
```

---

## See Also

- **[getting-started.md](./getting-started.md)** - Basic usage guide
- **[error-handling.md](./error-handling.md)** - Error handling strategies
- **[security.md](./security.md)** - Token security best practices
- **[token-efficiency.md](./token-efficiency.md)** - Optimize API usage

---

**Last Updated:** 2025-11-17
