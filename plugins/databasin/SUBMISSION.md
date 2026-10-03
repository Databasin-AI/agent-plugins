# Public directory submission checklist

This is the release handoff for Databasin plugin `0.9.4`. Installing from the
Databasin GitHub marketplace is separate from acceptance into a public directory.
Do not describe a prepared package or a registry entry as a Claude or OpenAI approval.

## Submission metadata

- Plugin name: `databasin`
- Display name: `Databasin`
- Version: `0.9.4`
- Publisher: Databasin Team (`info@databasin.co`)
- Homepage: <https://www.databasin.ai>
- Repository: <https://github.com/Databasin-AI/agent-plugins>
- Plugin source after merge:
  <https://github.com/Databasin-AI/agent-plugins/tree/main/plugins/databasin>
- Privacy policy: <https://www.databasin.ai/legal/privacy/>
- Terms of service: <https://www.databasin.ai/legal/tos/>
- License: CC-BY-4.0

The Claude manifest includes `displayName`, repository and publisher metadata,
and a bundled `.mcp.json`. The Codex manifest points to `.mcp.codex.json` with
the same pinned client and host-specific environment forwarding. Both include
matching website and legal metadata.

## MCP contract

The plugin pins `@databasin/mcp-client@0.2.3` and the production profile. The
client contributes `databasin_auth_status` and `databasin_login`, then discovers
the remote product contract from production `tools/list`.

The expected remote catalog is:

1. `databasin_get_capabilities`
2. `databasin_get_context`
3. `databasin_search`
4. `databasin_get_schema`
5. `databasin_run_agent`
6. `databasin_get_agent_run`
7. `databasin_cancel_agent_run`
8. `databasin_run_query`
9. `databasin_get_query_status`
10. `databasin_cancel_query`
11. `databasin_run_assistant`
12. `databasin_get_support_context`
13. `databasin_list_support_tickets`
14. `databasin_get_support_ticket`
15. `databasin_create_support_ticket`
16. `databasin_add_support_ticket_message`
17. `databasin_update_support_ticket`
18. `databasin_list_support_notifications`
19. `databasin_mark_support_notification_read`
20. `databasin_mark_all_support_notifications_read`

Do not maintain tool input or output schemas in this plugin. Before each
release, compare these names with production discovery and update the skills and
tests for any intentional rename or removal.

## Production deployment and external gates

Complete every item before submission:

1. Publish `@databasin/mcp-client@0.2.3` to npm and confirm `latest` resolves to
   that exact version. Do not submit against the NP-only beta or a mutable
   unverified client version.
2. Deploy the true-MCP implementation to `https://databasin.cloud/mcp` and
   verify protocol `2026-07-28` negotiation. The client intentionally has no
   REST or legacy-protocol fallback.
3. Run unauthenticated discovery and verify the exact 20 product tool names,
   descriptions, schemas, annotations, and timeout metadata.
4. Use a safe production reviewer account to exercise the five positive and
   three negative cases in
   [`../../tests/AGENT-BEHAVIOR-MATRIX.md`](../../tests/AGENT-BEHAVIOR-MATRIX.md).
   Retain only non-sensitive evidence and correlation IDs.
5. Confirm support ticket and message results include email addresses and that
   ordinary users cannot read internal notes or perform staff-only updates.
6. Confirm the website, privacy policy, terms, repository, and publisher email
   are public and current.

## Package validation

Run from the repository root:

```bash
python3 tests/validate_plugin.py
claude plugin validate plugins/databasin --strict
claude plugin validate .claude-plugin/marketplace.json --strict
python3 /home/founder3/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/databasin
```

Then test the exact release commit from a clean Claude Code profile:

1. Add the repository marketplace and install `databasin@databasin-tools`.
2. Confirm the plugin picker shows `Databasin`, version `0.9.4`, the description,
   publisher, and repository.
3. Confirm the MCP server starts with no plugin errors.
4. Run `databasin_auth_status`, complete `databasin_login`, then verify the two
   local tools and 20 remote tools are present.
5. Run the behavior matrix, restart Claude Code, and repeat a read-only discovery
   call to catch cache or first-run issues.
6. Remove the test profile and verify the normal user profile was not modified.

## Submit

### Claude Directory

Use <https://claude.ai/directory/manage> from an eligible paid account. Connect a
GitHub account with push access, select this repository and `plugins/databasin`,
and validate the release source before completing the listing and review form.
Complete required data-handling and legal attestations with the publisher.
See <https://claude.com/docs/plugins/submit>.

The Claude Directory submission route is not a promise of placement in the
separate `claude-plugins-official` marketplace. Do not promise a review date or
catalog-sync schedule.

### OpenAI / Codex public directory

Use <https://platform.openai.com/plugins> in the verified Databasin publisher
organization. The public MCP submission requires a remote HTTPS MCP service;
the GitHub marketplace's local stdio client is not a substitute for that service.
See <https://developers.openai.com/plugins/deploy/submission>.

Before submission, verify protected-resource discovery and authorization-code
sign-in with PKCE against the exact submitted URL. The resource identifier and
issued token audience must agree. Preserve existing UI and local-client login;
never relax token validation to make remote sign-in pass. Copy callback URLs
and domain-verification challenges from the portal, not from examples.

Provide a dedicated approved reviewer account and complete the behavior matrix,
including non-staff restrictions. Do not submit a production user's credentials,
claim an unverified test passed, or publish private verification evidence.

### Official MCP Registry

The client repository owns `server.json` and the registry-publication workflow:
<https://github.com/Databasin-AI/mcp-client>. Publish the exact npm version first,
then run `Publish MCP Registry` on `main` using GitHub OIDC. The namespace is
`io.github.Databasin-AI/mcp-client`. Verify the resulting public registry record.
This entry describes the local stdio package; it does not establish remote OAuth
compatibility or approval by Claude or OpenAI.

## Release notes for 0.9.0

- Added automatic production MCP wiring through the exact DataBasin client
  release.
- Replaced the retired ten-tool vocabulary with the server-owned 20-tool true
  MCP catalog and local authentication helpers.
- Added support-ticket and notification guidance, including safe handling of
  ticket/message email addresses.
- Updated discovery, schema, query, assistant, and metadata-agent workflows to
  match the live server contract.
- Added display, repository, publisher, website, privacy, and terms metadata.
- Expanded validation to reject retired tool names and MCP dependency drift.
