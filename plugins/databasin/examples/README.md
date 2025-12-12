# Databasin CLI Examples

This directory contains comprehensive, real-world examples for using the Databasin CLI effectively.

## Available Examples

### [PostgreSQL to Snowflake Pipeline](./postgres-to-snowflake-pipeline.md)
**Complete end-to-end workflow** for extracting data from PostgreSQL and loading into Snowflake.

**What you'll learn:**
- Authentication and project identification
- Creating and testing connectors
- Exploring source data structure
- Building pipeline configurations
- Validating before deployment
- Monitoring execution
- Troubleshooting common issues

**Key topics:**
- ✅ Using project internal IDs correctly
- ✅ Testing connectors before building pipelines
- ✅ Validating configurations with `databasin pipelines validate`
- ✅ Monitoring with logs and history commands
- ✅ Cloning pipelines for different environments

---

### [Troubleshooting Failed Pipelines](./troubleshooting-failed-pipeline.md)
**Systematic approach** to diagnosing and fixing pipeline failures.

**What you'll learn:**
- Reading and interpreting pipeline logs
- Identifying root causes of failures
- Common failure scenarios and solutions
- Testing fixes before deployment
- Preventive monitoring strategies

**Covered scenarios:**
- ✅ Schema changes breaking pipelines
- ✅ Connection timeouts
- ✅ Permission errors
- ✅ Data type mismatches
- ✅ Schedule configuration issues
- ✅ Debug mode for detailed diagnostics

---

### [Connector Inspection and Pipeline Cloning](./connector-inspection-and-cloning.md)
**Advanced techniques** for connector analysis and rapid pipeline deployment.

**What you'll learn:**
- Using `databasin connectors inspect` for comprehensive analysis
- Understanding database structure before building pipelines
- Cloning pipelines for environment promotion
- Testing different configurations safely
- Creating pipeline backups

**Key workflows:**
- ✅ Comprehensive connector inspection
- ✅ Troubleshooting with inspect output
- ✅ Environment promotion (dev → staging → prod)
- ✅ Testing schedule variations
- ✅ Bulk cloning operations
- ✅ Pipeline backup strategies

---

## Critical Concepts

### Always Use Project Internal IDs

**IMPORTANT:** When using Databasin CLI commands that require a `--project` argument, always use the project's **internal ID** (string like "N1r8Do"), not the project name.

**How to find your project ID:**
```bash
databasin auth whoami

# Example output:
# User: john.doe@company.com
# Organizations:
#   - Acme Corp (ID: 123)
# Projects:
#   - Production Data Warehouse (ID: N1r8Do)  ← Use this ID
#   - Development Environment (ID: K9mPx2)    ← Or this ID
```

**Correct usage:**
```bash
# ✅ CORRECT - using internal ID
databasin connectors list --project N1r8Do
databasin pipelines create config.json --project N1r8Do
databasin pipelines clone 8901 --project N1r8Do
```

**Incorrect usage:**
```bash
# ❌ WRONG - using project name (will fail)
databasin connectors list --project "Production Data Warehouse"
```

### Essential Commands Reference

**Authentication:**
```bash
databasin auth login          # Login via browser
databasin auth whoami         # View user and project IDs
databasin auth verify         # Verify token validity
```

**Connectors:**
```bash
databasin connectors list --project <id>           # Count connectors
databasin connectors list --full --project <id>    # List all details
databasin connectors inspect <id-or-name>          # Comprehensive analysis
databasin connectors test <id>                     # Test connection
```

**Pipelines:**
```bash
databasin pipelines list --project <id>            # List pipelines
databasin pipelines create <file> --project <id>   # Create pipeline
databasin pipelines clone <id> --project <id>      # Clone pipeline
databasin pipelines run <id>                       # Execute pipeline
databasin pipelines logs <id>                      # View logs (critical!)
databasin pipelines validate <file>                # Validate config
```

**SQL Queries:**
```bash
databasin sql discover <connector-id>              # Full structure
databasin sql tables <connector-id>                # List tables
databasin sql exec <connector-id> "<query>"        # Execute query
```

## Getting Started

1. **Start with Authentication:**
   - Run `databasin auth login`
   - Note your project ID from `databasin auth whoami`

2. **Explore Your First Example:**
   - New users: Start with [PostgreSQL to Snowflake Pipeline](./postgres-to-snowflake-pipeline.md)
   - Troubleshooting: See [Troubleshooting Failed Pipelines](./troubleshooting-failed-pipeline.md)
   - Advanced users: Jump to [Connector Inspection and Cloning](./connector-inspection-and-cloning.md)

3. **Practice with Your Own Data:**
   - Modify the examples to use your actual connectors
   - Always use `--dry-run` when testing
   - Validate configurations before creating pipelines

## Common Patterns

### Pipeline Creation Pattern
```bash
# 1. Authenticate and get project ID
databasin auth whoami

# 2. Test connectors
databasin connectors test <source-id>
databasin connectors test <target-id>

# 3. Explore source data
databasin sql discover <source-id>

# 4. Create and validate configuration
databasin pipelines template > config.json
# ... edit config.json ...
databasin pipelines validate config.json

# 5. Create pipeline (use project ID)
databasin pipelines create config.json --project <id>

# 6. Test and monitor
databasin pipelines run <pipeline-id>
databasin pipelines logs <pipeline-id>
```

### Troubleshooting Pattern
```bash
# 1. Check logs (ALWAYS FIRST)
databasin pipelines logs <id>

# 2. Check execution history
databasin pipelines history <id> --limit 10

# 3. Test connectors
databasin connectors test <source-id>
databasin connectors test <target-id>

# 4. Verify configuration
databasin pipelines get <id>

# 5. Enable debug mode if needed
DATABASIN_DEBUG=true databasin pipelines run <id>
```

### Environment Promotion Pattern
```bash
# 1. Verify dev pipeline
databasin pipelines get <dev-pipeline-id>
databasin pipelines history <dev-pipeline-id>

# 2. Find production connectors
databasin connectors search "production" --project <prod-project-id>

# 3. Preview clone
databasin pipelines clone <dev-id> \
  --name "Production Pipeline" \
  --source <prod-source-id> \
  --target <prod-target-id> \
  --dry-run \
  --project <prod-project-id>

# 4. Create clone
databasin pipelines clone <dev-id> \
  --name "Production Pipeline" \
  --source <prod-source-id> \
  --target <prod-target-id> \
  --project <prod-project-id>

# 5. Test production pipeline
databasin pipelines run <new-pipeline-id>
databasin pipelines logs <new-pipeline-id>
```

## Tips and Best Practices

1. **Always authenticate first**: Run `databasin auth login` before starting work
2. **Use project IDs consistently**: Always pass `--project <id>` where required
3. **Inspect before building**: Use `databasin connectors inspect` to understand connectors
4. **Validate before deploying**: Use `databasin pipelines validate` to catch errors early
5. **Test connectors individually**: Verify each connector works before building pipelines
6. **Check logs for troubleshooting**: `databasin pipelines logs` is your best diagnostic tool
7. **Use dry-run for cloning**: Always preview changes with `--dry-run` first
8. **Monitor execution**: Check logs after every pipeline run
9. **Enable debug mode when stuck**: `DATABASIN_DEBUG=true` provides detailed diagnostics
10. **Create backups before changes**: Clone pipelines before modifying them

## Need Help?

- **CLI Documentation**: Run `databasin docs` or `databasin <command> --help`
- **GitHub**: [Databasin CLI Repository](https://github.com/Databasin-AI/databasin-cli)
- **Plugin Skills**: Use Claude Code skills for guided assistance

## Contributing Examples

Have a useful workflow or pattern? Consider contributing it to this examples directory.

Good examples should:
- Solve a real-world problem
- Include complete commands with expected output
- Emphasize using project IDs correctly
- Show both success and failure scenarios
- Include troubleshooting steps
- Demonstrate best practices
