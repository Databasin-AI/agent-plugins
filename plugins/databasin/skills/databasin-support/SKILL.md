---
name: databasin-support
description: Work with caller-visible Databasin support tickets, ticket messages, email-bearing ticket data, and notifications. Use to list, read, create, reply to, or update support tickets and to review or mark support notifications.
---

# Databasin Support

Use this skill for support, bug, and enhancement tickets. Ticket and message
records can contain email addresses; treat them as personal data and surface
them only when relevant to the user's request.

## Workflow

1. Authenticate with `databasin_auth_status` and `databasin_login` when needed.
2. Call `databasin_get_capabilities`, then `databasin_get_support_context` before
   support mutations. Respect the returned permissions, ticket types,
   priorities, and statuses.
3. Use `databasin_list_support_tickets` and `databasin_get_support_ticket` for
   caller-visible tickets. The detail response can include creator and message
   email addresses. Do not infer identity from an address or expose unrelated
   addresses.
4. Use `databasin_create_support_ticket` only for an explicit request to create
   a human-visible support, bug, or enhancement ticket. Confirm ambiguous
   subject, description, type, or priority before creating it.
5. Use `databasin_add_support_ticket_message` only for an explicit request to
   post a human-visible reply. Set `isInternal` only when the caller is support
   staff and explicitly requests an internal note.
6. Use `databasin_update_support_ticket` only when the support context permits
   it. Never invent an assignee. Unassignment is not supported.
7. Use `databasin_list_support_notifications`,
   `databasin_mark_support_notification_read`, and
   `databasin_mark_all_support_notifications_read` only for the signed-in user's
   notification state.

Creating a ticket, posting a message, updating a ticket, or marking a
notification read changes state. Report the server's returned result and do not
claim success after an error or denied permission. Never place credentials,
tokens, private configuration, or unrelated personal data in a ticket.
