# Databasin plugin

Connect Claude Code or Codex to Databasin's production MCP service for governed
data discovery, read-only analysis, metadata-agent runs, and support tickets.

## Requirements

- Node.js 22.20+ or Node.js 24.
- An available OS-protected credential store. Linux requires an unlocked Secret
  Service/libsecret keyring; the client does not fall back to plaintext storage.
- A Databasin account authorized through the production Auth0 login.

The plugin starts `@databasin/mcp-client@0.2.1` from [`.mcp.json`](.mcp.json).
On first use, call `databasin_login` and follow the DataBasin Auth0 device sign-in
instructions. Never provide credentials or tokens in chat.

## Capabilities

The production server owns the tool schemas and advertises them through
`tools/list`. The current server catalog contains:

- Discovery: `databasin_get_capabilities`, `databasin_get_context`,
  `databasin_search`, and `databasin_get_schema`.
- Metadata agent: `databasin_run_agent`, `databasin_get_agent_run`, and
  `databasin_cancel_agent_run`.
- Read-only SQL: `databasin_run_query`, `databasin_get_query_status`, and
  `databasin_cancel_query`.
- Bounded assistant: `databasin_run_assistant`.
- Support: `databasin_get_support_context`,
  `databasin_list_support_tickets`, `databasin_get_support_ticket`,
  `databasin_create_support_ticket`, `databasin_add_support_ticket_message`,
  `databasin_update_support_ticket`, `databasin_list_support_notifications`,
  `databasin_mark_support_notification_read`, and
  `databasin_mark_all_support_notifications_read`.

The local MCP client also provides `databasin_auth_status` and
`databasin_login`. These are authentication helpers, not remote product tools.

Ticket detail and message results include email addresses. Treat them as
personal data: show them only when relevant, do not infer identity from them,
and never copy unrelated addresses into new tickets or messages.

## Skills and Claude Code commands

Shared skills cover query assistance, connector inspection, pipeline planning,
automation planning, and support tickets. Claude Code also provides:

- `/databasin:list-projects`
- `/databasin:list-connectors`
- `/databasin:create-connector`
- `/databasin:create-pipeline`

The create commands are planning-only because MCP does not expose connector,
pipeline, or automation mutations.

See [PLUGIN-USAGE.md](PLUGIN-USAGE.md) for operating guidance,
[MCP-SETUP.md](MCP-SETUP.md) for connection details, and
[SUBMISSION.md](SUBMISSION.md) for release gates.

## License

This plugin is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
