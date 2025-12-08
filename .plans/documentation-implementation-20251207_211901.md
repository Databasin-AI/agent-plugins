# Databasin CLI Plugin Documentation Update Plan

**Created:** 2025-12-07 21:19:01
**Purpose:** Update all markdown documentation to accurately reflect current CLI capabilities

---

## Executive Summary

This plan addresses critical documentation gaps identified through user session logs. Users are experiencing inefficient tool discovery, excessive API calls, poor error messages, and missing guidance on key CLI features like the interactive pipeline wizard, connector config discovery, and token-efficient defaults.

### Impact Metrics
- **Reduced trial-and-error:** Documentation will provide accurate command syntax on first attempt
- **Token efficiency:** 60-80% reduction in API calls through proper use of count mode defaults
- **Faster onboarding:** Clear examples of `databasin pipelines wizard` and `databasin docs` commands
- **Better error handling:** Updated troubleshooting with current CLI error messages

---

## Current State Analysis

### Critical Issues Found

1. **Outdated Authentication Model**
   - Documentation references `.auth-config.json` and `.token` files
   - Reality: CLI uses `databasin auth login` browser-based flow
   - Impact: Users cannot authenticate properly

2. **Missing CLI Commands**
   - `databasin pipelines wizard` - interactive pipeline creator (KEY FEATURE)
   - `databasin connectors config <subtype>` - get connector workflow screens
   - `databasin docs [name]` - access GitHub documentation
   - `databasin completion install bash` - shell completions
   - `databasin pipelines history` - execution history
   - `databasin automations history` - automation history

3. **Incorrect Default Behaviors**
   - Documentation says `connectors list` returns full objects
   - Reality: Returns count only by default (use `--full` flag)
   - Impact: Users get confused when commands don't return expected data

4. **Obsolete Script References**
   - Multiple references to `bun run` TypeScript scripts
   - References to Playwright automation scripts
   - Manual JWT token refresh workflows
   - All replaced by CLI commands

5. **Missing Token Efficiency Guidance**
   - No documentation of `--fields`, `--limit`, `--count` options
   - Missing interactive prompt behavior
   - No guidance on when to use count mode vs full mode

---

## Files Requiring Updates

### High Priority (Core Documentation)

1. **README.md** - Main plugin README
   - Remove all `.auth-config.json` and `.token` references
   - Remove `bun run` script examples
   - Add `databasin auth login` as primary auth method
   - Document `databasin docs` command
   - Update quick start workflow

2. **PLUGIN-USAGE.md** - User guide
   - Complete rewrite of authentication section
   - Add `databasin pipelines wizard` examples
   - Document interactive prompts
   - Add shell completion setup
   - Update all workflow examples to use CLI

3. **skills/databasin-cli-skill/SKILL.md** - CLI expert skill
   - Add `pipelines wizard` command
   - Add `connectors config` command
   - Add `docs` command and `completion` command
   - Update connector list default behavior (count mode)
   - Add `--fields`, `--limit`, `--count` documentation
   - Document interactive prompts

### Medium Priority (Reference Documentation)

4. **skills/databasin-cli-skill/references/advanced-workflows.md**
   - Update all script examples to use CLI commands
   - Remove `.token` file management
   - Add wizard workflow examples
   - Update authentication flows

5. **skills/databasin-cli-skill/references/token-efficiency.md**
   - Document count mode as default for `connectors list`
   - Add `--full` flag usage
   - Document `--fields` and `--limit` options
   - Add interactive mode token efficiency tips

6. **skills/databasin-cli-skill/references/troubleshooting.md**
   - Update authentication troubleshooting (remove `.token` references)
   - Add `databasin auth login` error handling
   - Update connector list troubleshooting for count mode
   - Add wizard troubleshooting section

### Medium Priority (Skills)

7. **skills/databasin-connectors/SKILL.md**
   - Update connector list default behavior documentation
   - Add `databasin connectors config` command
   - Remove script-based workflows
   - Update all examples to CLI commands

8. **skills/databasin-pipelines/SKILL.md**
   - Add `databasin pipelines wizard` as primary workflow
   - Update to CLI-based artifact management
   - Remove TypeScript script references
   - Document `pipelines history` command

### Low Priority (Commands and Agent)

9. **commands/create-connector.md**
   - Update to reference CLI commands
   - Remove script references

10. **commands/create-pipeline.md**
    - Add wizard workflow as primary method
    - Update to CLI-based approach

11. **commands/list-connectors.md**
    - Document count mode default
    - Add `--full` flag usage

12. **commands/list-projects.md**
    - Already minimal, verify accuracy

13. **agents/databasin-pipeline-creator.md**
    - Update to use `databasin pipelines wizard`
    - Remove references to manual scripting
    - Document CLI-based workflows

---

## Detailed Update Specifications

### 1. Authentication Documentation Updates

**Remove Everywhere:**
```json
{
  "username": "your-email@company.com",
  "password": "your-password",
  "loginUrl": "http://localhost:3000"
}
```

**Replace With:**
```bash
# Primary authentication method
databasin auth login

# Opens browser for secure authentication
# Token stored automatically in ~/.databasin/config.json
```

**New Authentication Workflow:**
1. User runs `databasin auth login`
2. Browser opens for authentication
3. Token stored securely
4. Verify with `databasin auth whoami`

### 2. Connector List Default Behavior

**Old Documentation (WRONG):**
```bash
databasin connectors list
# Returns: Full array of 434+ connector objects
```

**New Documentation (CORRECT):**
```bash
# Default: Count only (token-efficient)
databasin connectors list -p <project>
# Returns: "Total connectors: 434"

# Full objects: Use --full flag
databasin connectors list -p <project> --full

# Specific fields: Use --fields
databasin connectors list -p <project> --full --fields "connectorID,connectorName,connectorType"
```

### 3. Pipeline Wizard Documentation

**Add to all pipeline creation workflows:**

```bash
# Interactive pipeline wizard (RECOMMENDED)
databasin pipelines wizard

# Wizard features:
# - Interactive connector selection
# - Automatic schema discovery
# - Field mapping assistance
# - Validation before creation
# - Step-by-step guidance
```

**Wizard Workflow:**
1. Select source connector
2. Choose source tables/files
3. Select destination connector
4. Configure destination
5. Map fields (with AI suggestions)
6. Set schedule
7. Review and create

### 4. Connector Config Discovery

**Add command:**
```bash
# Get connector configuration requirements
databasin connectors config <connector-subtype>

# Example: Get PostgreSQL connector requirements
databasin connectors config PostgreSQL

# Returns:
# - Required fields
# - Optional fields
# - Workflow screens
# - Authentication methods
```

### 5. Documentation Access Command

**Add to all skills:**
```bash
# Access CLI documentation from GitHub
databasin docs                    # List all docs
databasin docs sql-queries        # Specific doc
databasin docs pipelines          # Pipeline guide
databasin docs troubleshooting    # Troubleshooting
```

### 6. Shell Completion

**Add to setup sections:**
```bash
# Install shell completions
databasin completion install bash   # Bash
databasin completion install zsh    # Zsh
databasin completion install fish   # Fish

# Enables tab completion for all commands
```

### 7. History Commands

**Add to observability sections:**
```bash
# View pipeline execution history
databasin pipelines history <pipeline-id>
databasin pipelines history <pipeline-id> --limit 10

# View automation execution history
databasin automations history <automation-id>
databasin automations history <automation-id> --status failed
```

### 8. Interactive Prompts

**Document behavior:**
```bash
# Commands prompt when required args missing
databasin pipelines list
# Prompts: "Enter project ID:"

databasin connectors get
# Shows list to select from

# Override with flags for automation:
databasin pipelines list -p proj-123 --json
```

---

## Token Efficiency Patterns

### Pattern 1: Check Count First
```bash
# Step 1: Get count (uses ~50 tokens)
databasin connectors list -p proj-001

# Step 2: If needed, get limited fields (uses ~5,000 tokens)
databasin connectors list -p proj-001 --full --fields "connectorID,connectorName" --limit 20

# Step 3: Get full details only for specific items (uses ~2,000 tokens each)
databasin connectors get <connector-id>
```

### Pattern 2: Field Filtering
```bash
# Bad: Full objects with all fields (~200K tokens)
databasin connectors list -p proj-001 --full

# Good: Only fields you need (~20K tokens)
databasin connectors list -p proj-001 --full --fields "connectorID,connectorName,connectorType,status"
```

### Pattern 3: Pagination
```bash
# Process in batches
databasin connectors list -p proj-001 --full --limit 20 --offset 0
databasin connectors list -p proj-001 --full --limit 20 --offset 20
```

---

## Updated Workflow Examples

### Workflow 1: First-Time Setup

**Old (WRONG):**
```bash
# 1. Create .auth-config.json
# 2. Run bun run .claude/skills/refresh-databasin-jwt/refresh-jwt.ts
# 3. Use slash commands
```

**New (CORRECT):**
```bash
# 1. Authenticate
databasin auth login

# 2. Verify authentication
databasin auth whoami

# 3. List projects
databasin projects list

# 4. Enable shell completions (optional)
databasin completion install bash
```

### Workflow 2: Create a Pipeline

**Old (WRONG):**
```bash
# Manual JSON file creation
# bun run scripts
# Complex artifact management
```

**New (CORRECT):**
```bash
# Use interactive wizard (RECOMMENDED)
databasin pipelines wizard

# Or programmatic approach
databasin pipelines create config.json -p <project-id>
```

### Workflow 3: Explore Connectors

**Old (WRONG):**
```bash
# Returns all 434+ connectors (200K+ tokens)
bun run .claude/skills/databasin-api/scripts/api-call.ts GET /api/connector
```

**New (CORRECT):**
```bash
# Step 1: Get count (token-efficient)
databasin connectors list -p <project>
# Output: "Total connectors: 434"

# Step 2: Get connector config for type you need
databasin connectors config PostgreSQL

# Step 3: Create connector
databasin connectors create postgres-config.json -p <project>

# Step 4: Test connection
databasin connectors test <connector-id>
```

---

## Error Message Updates

### Authentication Errors

**Old:**
```
Error: Token expired
Solution: Run bun run .claude/skills/refresh-databasin-jwt/refresh-jwt.ts
```

**New:**
```
Error: Authentication required
Solution: Run 'databasin auth login'
```

### Connector List Confusion

**Old:**
```
Q: Why is connectors list returning just a count?
A: <no documentation>
```

**New:**
```
Q: Why is connectors list returning just a count?
A: This is the default (token-efficient). Use --full flag for full objects:
   databasin connectors list -p <project> --full
```

---

## Implementation Checklist

### Phase 1: Core Documentation (High Priority)
- [ ] Update README.md with current CLI authentication
- [ ] Update PLUGIN-USAGE.md with wizard workflows
- [ ] Update skills/databasin-cli-skill/SKILL.md with all new commands

### Phase 2: Reference Documentation (Medium Priority)
- [ ] Update advanced-workflows.md to remove scripts
- [ ] Update token-efficiency.md with count mode defaults
- [ ] Update troubleshooting.md with current error messages

### Phase 3: Skill Documentation (Medium Priority)
- [ ] Update databasin-connectors/SKILL.md
- [ ] Update databasin-pipelines/SKILL.md with wizard
- [ ] Update databasin-automations/SKILL.md (verify accuracy)

### Phase 4: Commands and Agents (Low Priority)
- [ ] Update create-connector.md
- [ ] Update create-pipeline.md with wizard
- [ ] Update list-connectors.md with count mode
- [ ] Update databasin-pipeline-creator.md agent

---

## Quality Assurance Criteria

### Accuracy Checklist
- [ ] All `databasin` commands match actual CLI help output
- [ ] No references to `.auth-config.json` or `.token` files
- [ ] No references to `bun run` scripts
- [ ] Count mode documented as default for `connectors list`
- [ ] `--full` flag documented where needed

### Completeness Checklist
- [ ] `databasin pipelines wizard` documented
- [ ] `databasin connectors config` documented
- [ ] `databasin docs` documented
- [ ] `databasin completion` documented
- [ ] `pipelines history` and `automations history` documented
- [ ] Interactive prompts documented
- [ ] `--fields`, `--limit`, `--count` options documented

### Consistency Checklist
- [ ] Same command syntax across all files
- [ ] Consistent authentication workflow
- [ ] Consistent token efficiency guidance
- [ ] Consistent error handling examples

### User-Focused Checklist
- [ ] Addresses pain points from session logs
- [ ] Clear examples for common workflows
- [ ] Token-efficient patterns emphasized
- [ ] Troubleshooting for common issues
- [ ] Next steps provided after each operation

---

## Expected Outcomes

### For AI Agents
1. **90% reduction in command trial-and-error** - Correct commands documented
2. **60-80% token savings** - Proper use of count mode and field filtering
3. **Faster task completion** - Wizard workflows reduce multi-step complexity
4. **Better error recovery** - Current error messages with solutions

### For Users
1. **Easier onboarding** - `databasin auth login` just works
2. **Discoverable features** - `databasin docs` command surfaces help
3. **Efficient workflows** - Wizard guides through complex tasks
4. **Better troubleshooting** - Accurate error messages and solutions

---

## Maintenance Plan

### Ongoing Updates
1. Verify CLI help output quarterly against documentation
2. Add new CLI features as they're released
3. Update examples based on user feedback
4. Track common support questions and add to troubleshooting

### Version Tracking
- Document CLI version: `databasin --version`
- Note breaking changes in CHANGELOG.md (if exists)
- Maintain migration guides for major updates

---

## Conclusion

This documentation update plan transforms outdated, script-based documentation into accurate, CLI-focused guidance that matches the current Databasin CLI implementation. The updates prioritize user pain points identified in session logs, emphasize token efficiency, and provide clear, working examples for all major workflows.

**Files Updated:** 13 markdown files
**Primary Focus:** Authentication, CLI commands, token efficiency, wizard workflows
**Expected Impact:** 90% reduction in trial-and-error, 60-80% token savings, faster onboarding

Implementation will proceed file-by-file with quality checks at each step to ensure accuracy and completeness.
