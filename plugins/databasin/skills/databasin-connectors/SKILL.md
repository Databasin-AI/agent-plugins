---
name: databasin-connectors
description: Discover and inspect caller-visible Databasin connectors and schemas, then draft redacted proposals for unsupported connector changes. Use for connector inventory, schema browsing, or connector change planning.
---

# Databasin Connectors

Use this skill to find connectors, understand their safe metadata, browse exposed schemas, and plan connector work without collecting secrets.

## Tools

Treat the connected server's `tools/list` response as authoritative. Authenticate
with the client-local `databasin_auth_status` and `databasin_login` tools when
needed, then call `databasin_get_capabilities` before product tools.

- Use `databasin_get_context` for caller-visible projects and connector summaries.
- Use `databasin_search` for bounded connector, pipeline, and automation metadata.
- Use `databasin_get_schema` for bounded catalog, schema, table, and column
  metadata on an accessible connector.

The current MCP does not create, update, test, clone, or delete connectors. Do not invoke a shell, CLI, generic HTTP client, or arbitrary API route to work around that boundary.

## Workflow

1. Call `databasin_get_capabilities`, then `databasin_get_context`, and use only
   projects and connector identifiers returned for the caller.
2. Use `databasin_search` to narrow the connector set. Never guess a project or connector ID.
3. Use `databasin_get_schema` only when schema information is relevant. Request
   one bounded level at a time in catalog, schema, table, then column order.
4. For a requested create, update, test, clone, or delete, return a redacted
   proposal and clearly state that execution is unavailable.

Never ask for, repeat, store, or place passwords, tokens, API keys, private keys, OAuth codes, connection strings, hosts, or credentials in tool arguments. Secret collection must occur through a future trusted first-party UI or OAuth flow, not the conversation.

## Proposal requirements

Separate observed MCP evidence from assumptions and proposed values. Include only the selected project, connector type, non-secret requirements, dependencies, unresolved secret references, risks, and validation checks. Never claim the proposal was applied or tested.

Any future connector mutation must use a dedicated fixed-purpose MCP tool, server-side validation, explicit user approval, and an idempotency key or stable plan hash.
