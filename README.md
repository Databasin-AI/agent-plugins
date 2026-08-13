# Databasin plugin

Databasin MCP-oriented skills packaged for both Claude Code and Codex/OpenAI. The shared skill content lives in [`plugins/databasin/skills/`](plugins/databasin/skills/), with host-specific manifests for each runtime.

This repository contains guidance and plugin metadata. It does not include credentials, a production MCP endpoint, an app registration, legal URLs, or visual assets.

## Install

For Claude Code, add the repository marketplace and install the `databasin` plugin:

```text
/plugin marketplace add databasin-ai/agent-plugins
```

For Codex/OpenAI, add this repository as a marketplace and install the `databasin` plugin:

```bash
codex plugin marketplace add Databasin-AI/agent-plugins
codex plugin add databasin@databasin-tools
```

The Codex package is declared by [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) and [`plugins/databasin/.codex-plugin/plugin.json`](plugins/databasin/.codex-plugin/plugin.json).

## What is included

- Shared skills for Databasin query assistance, connector inspection, pipeline planning, and automation planning.
- Claude Code command and agent metadata for the connector, pipeline, project, and connector-list planning workflows.
- A Codex manifest that discovers the shared `skills/` directory.

The plugin does not require a local Databasin CLI. Live operations require a host-provided, authenticated Databasin MCP connection; installing the plugin alone does not provide one.

## Supported MCP tool catalog

The supported Databasin MCP catalog contains these names:

- `databasin_get_context`
- `databasin_search`
- `databasin_describe_resource`
- `databasin_browse_schema`
- `databasin_get_semantic_context`
- `databasin_profile_table`
- `databasin_validate_plan`
- `databasin_run_sql`
- `databasin_get_operation`
- `databasin_cancel_operation`

The production MCP server may advertise only a deployment-enabled subset. These
names are not a claim that every deployment exposes every tool, and they are
not a local endpoint configuration. Use the production `tools/list` response as
the source of truth for calls and submission tests.

## Remote MCP wiring

Remote MCP wiring is intentionally deferred until the Databasin MCP service has been deployed and registered with the target host. At that point, add the real host-approved server configuration and any required app metadata to the appropriate runtime integration.

No `.mcp.json` or `.app.json` is included because this repository does not yet have a real deployed/registered value for either one. Do not replace this note with a guessed URL, app ID, privacy URL, terms URL, or asset path.

See [`plugins/databasin/MCP-SETUP.md`](plugins/databasin/MCP-SETUP.md) for the deployment-gated setup checklist.
See [`plugins/databasin/SUBMISSION.md`](plugins/databasin/SUBMISSION.md) for the OpenAI submission checklist, tool annotations, reviewer cases, and external gates.

## License

This plugin is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
