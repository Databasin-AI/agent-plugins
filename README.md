# Databasin plugin

The Databasin plugin connects Claude Code and Codex to Databasin through a
bundled MCP client. It provides governed data discovery, schema exploration,
bounded read-only SQL and assistant workflows, scoped metadata-agent runs, and
support-ticket tools.

## Install

Claude Code:

```text
/plugin marketplace add Databasin-AI/agent-plugins
/plugin install databasin@databasin-tools
```

Codex:

```bash
codex plugin marketplace add Databasin-AI/agent-plugins
codex plugin add databasin@databasin-tools
```

The plugin starts the exact MCP client version declared in
[`plugins/databasin/.mcp.json`](plugins/databasin/.mcp.json). The client uses
Auth0 device sign-in and keeps credentials in the operating system's
protected credential store. Enter credentials only on the sign-in page, never
in a chat or tool argument.

## Included workflows

- Discover authorized projects, connectors, pipelines, and automations.
- Browse bounded catalog, schema, table, and column metadata.
- Run one bounded read-only `SELECT` or `WITH` statement.
- Run the bounded Databasin assistant or fixed `metadata_readonly` agent profile.
- List, read, create, reply to, and update support tickets within returned
  permissions, including ticket/message email addresses where relevant.
- Review and mark the signed-in user's support notifications.
- Draft redacted connector, pipeline, and automation proposals. Those resource
  mutations are not currently exposed by MCP.

The live MCP `tools/list` response and `databasin_get_capabilities` are the
source of truth. The local client discovers product tools from the production
server rather than maintaining a second product-tool contract.

See [`plugins/databasin/README.md`](plugins/databasin/README.md) for usage and
[`plugins/databasin/SUBMISSION.md`](plugins/databasin/SUBMISSION.md) for the
release and community-marketplace checklist.

## License

This plugin is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
