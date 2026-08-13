# Databasin plugin

Shared Databasin MCP-oriented skills for Claude Code and Codex/OpenAI. The plugin helps an agent discover authorized resources, understand schemas and approved semantics, inspect aggregate profiles, validate read-oriented SQL plans, and manage bounded asynchronous SQL operations.

## Package layout

```text
plugins/databasin/
├── .claude-plugin/plugin.json       # Claude Code manifest
├── .codex-plugin/plugin.json        # Codex/OpenAI manifest
├── agents/                          # Claude Code agent metadata
├── commands/                        # Claude Code command metadata
├── skills/                          # Shared skills for both runtimes
└── MCP-SETUP.md                     # Deployment-gated MCP setup notes
```

Both plugin manifests are version `0.8.1` and discover the shared `skills/` directory. The Claude Code manifest also discovers the command and agent metadata under `commands/` and `agents/`. The Codex interface metadata uses the OpenAI `Data & Analytics` category and the 21-character short description `Explore governed data`.

## Skills

- `databasin-query-assistant` — data discovery and natural-language query guidance.
- `databasin-connectors` — connector inspection and redacted change-planning guidance.
- `databasin-pipelines` — pipeline inspection and redacted planning guidance.
- `databasin-automations` — automation inspection and planning guidance.

The skills are packaged guidance. Installing the plugin does not require a local Databasin CLI. To perform live operations, the host must provide an authorized Databasin access path.

## Supported MCP tool catalog

The supported remote MCP catalog is:

1. `databasin_get_context`
2. `databasin_search`
3. `databasin_describe_resource`
4. `databasin_browse_schema`
5. `databasin_get_semantic_context`
6. `databasin_profile_table`
7. `databasin_validate_plan`
8. `databasin_run_sql`
9. `databasin_get_operation`
10. `databasin_cancel_operation`

The production server may advertise only the subset enabled by its deployment
configuration and backend capabilities. These names are a design catalog, not a
claim that all ten tools are always present; use the production `tools/list`
response as the source of truth for calls and submission tests.

## Remote MCP setup

Remote MCP wiring is added only after the MCP service is deployed and registered with the target host. This repository intentionally omits `.mcp.json` and `.app.json`: no real deployment endpoint or app registration value is available yet.

After deployment and registration, add the host-approved configuration using the actual values supplied by that registration. Do not add guessed production URLs, app IDs, privacy or terms URLs, or visual assets.

See [`MCP-SETUP.md`](MCP-SETUP.md) for the checklist. See [`SUBMISSION.md`](SUBMISSION.md) for the OpenAI review requirements and the exact five-positive/three-negative reviewer matrix.

## Claude Code commands

Claude Code also discovers the existing command metadata for:

- `/databasin:list-projects`
- `/databasin:list-connectors`
- `/databasin:create-connector`
- `/databasin:create-pipeline`

## License

This plugin is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
