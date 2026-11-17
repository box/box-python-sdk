# AiSessionsManager

- [List AI sessions](#list-ai-sessions)
- [Delete AI session](#delete-ai-session)

## List AI sessions

Returns a marker-paginated list of the AI sessions that the authenticated
user can read and that were created through the Box public API. Entries are
ordered by `sort` and `direction`, defaulting to `updated_at` descending so
the most recently active session appears first.

The access token must have both the `ai.readwrite` and `root_readwrite`
scopes.

A page may contain fewer than `limit` entries while further pages remain.
Treat a non-null `next_marker` as the only signal that more results exist.

This operation is performed by calling function `get_ai_sessions_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/get-ai-sessions/).

_Currently we don't have an example for calling `get_ai_sessions_v2026_r0` in integration tests_

### Arguments

- source `GetAiSessionsV2026R0Source`
  - Restricts the list to AI sessions with this origin. The only supported value is `api`.
- marker `Optional[str]`
  - The position marker at which to begin returning results, as returned in `next_marker` by the previous page. Omit it for the first page. All other parameters must match the request that returned the marker.
- sort `Optional[GetAiSessionsV2026R0Sort]`
  - The field to sort results by. Possible values are `created_at`, `updated_at`, and `name`. Default is `updated_at`, which advances on each turn of session activity.
- direction `Optional[GetAiSessionsV2026R0Direction]`
  - The direction to sort results in, either ascending (`asc`) or descending (`desc`). Default is `desc`.
- limit `Optional[int]`
  - The maximum number of AI sessions to return per page. The maximum is `100`; larger values are treated as `100`. The server may return fewer entries than requested.
- client_ids `Optional[List[str]]`
  - A comma-separated list of OAuth client IDs. Restricts the list to AI sessions created by any of these applications. Client IDs that match no application are ignored, so the response is an empty list if none of them match. Empty entries are ignored, and an empty value is treated as if the parameter were not provided.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `AiSessionsV2026R0`.

Returns a paginated list of AI sessions.

## Delete AI session

Deletes an AI session created through the Box public API, together with its
agent tasks. The session's agent-generated files and uploaded files are
moved to the trash. Files attached as sources from elsewhere in Box are not
affected. Deleting a session does not stop a running task or notify the
agent.

The access token must have both the `ai.readwrite` and `root_readwrite`
scopes.

This operation is performed by calling function `delete_ai_session_by_id_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/delete-ai-sessions-id/).

_Currently we don't have an example for calling `delete_ai_session_by_id_v2026_r0` in integration tests_

### Arguments

- ai_session_id `str`
  - The unique identifier of the AI session. This is the same value returned as `id` by the list endpoint and used as the A2A `contextId`. Example: "23489723"
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the AI session was successfully deleted.
