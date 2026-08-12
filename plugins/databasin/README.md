# Databasin plugin

Shared Databasin skills for Claude Code and Codex/OpenAI. The plugin helps an agent discover Databasin resources, understand schemas and table semantics, profile data, validate SQL plans, and manage asynchronous SQL operations.

## Package layout

```text
plugins/databasin/
├── .claude-plugin/plugin.json       # Claude Code manifest
├── .codex-plugin/plugin.json        # Codex/OpenAI manifest
├── agents/                          # Claude Code agent metadata
├── commands/                        # Claude Code command metadata
├── skills/                          # Shared skills for both runtimes
├── examples/                        # Workflow examples
└── MCP-SETUP.md                     # Deployment-gated MCP setup notes
```

Both manifests are version `0.8.0` and discover the shared `skills/` directory. The Claude Code manifest also discovers the existing `commands/` and `agents/` directories.

## Skills

- `databasin-query-assistant` — data discovery and natural-language query guidance.
- `databasin-connectors` — connector configuration and troubleshooting guidance.
- `databasin-pipelines` — pipeline planning and management guidance.
- `databasin-automations` — automation scheduling and troubleshooting guidance.
- `databasin-cli-skill` — Databasin CLI documentation and workflow reference.

The skills are packaged guidance. Installing the plugin does not require a local Databasin CLI. To perform live operations, the host must provide an authorized Databasin access path.

## Current MCP tools

The current remote MCP tool surface is:

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

The tool names are documented here for integration planning. They do not imply that a remote server is already connected.

## Remote MCP setup

Remote MCP wiring is added only after the MCP service is deployed and registered with the target host. This repository intentionally omits `.mcp.json` and `.app.json`: no real deployment endpoint or app registration value is available yet.

After deployment and registration, add the host-approved configuration using the actual values supplied by that registration. Do not add guessed production URLs, app IDs, privacy or terms URLs, or visual assets.

See [`MCP-SETUP.md`](MCP-SETUP.md) for the checklist.

## Claude Code commands

Claude Code also discovers the existing command metadata for:

- `/databasin:list-projects`
- `/databasin:list-connectors`
- `/databasin:create-connector`
- `/databasin:create-pipeline`

## Examples

The files under [`examples/`](examples/) preserve historical CLI workflows for human reference. They are not active MCP instructions, may be stale, and must not be used to bypass MCP authorization or unavailable capabilities.

## License

This plugin is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
