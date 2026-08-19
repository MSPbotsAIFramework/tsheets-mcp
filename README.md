# tsheets-mcp

MCP server for **TSheets (QuickBooks Time)** — Intuit's time-tracking, scheduling, and PTO platform. Exposes the full public TSheets REST API v1 as MCP tools.

## Overview

- Stateless HTTP service. No credentials are ever persisted — each request supplies its own access token via a header, used only for the lifetime of that single request.
- Supports concurrent requests; per-request credential isolation is done via Python `contextvars`, not a global/shared client instance.
- Entry points: `POST /mcp` (MCP protocol) and `GET /health` (health check).
- Default port: `8080` (configurable via `MCP_HTTP_PORT`).
- **No path-template parameters exist anywhere in the TSheets API** — every identifier (`ids`, `user_id`, etc.) is passed as a query-string parameter, even for single-resource lookups. This is a genuine API design characteristic, not a simplification made by this server.

## Scope

**15 tools**, trimmed down from an original 85-tool full-API build (2026-08-04). MSPbots' own stored integration config for this vendor calls exactly **6** endpoints (Effective Settings, Jobcodes, Users, Customfielditem User Filters, Timesheets, Custom Fields — all `GET`, read-only). Per the "actual usage + same-category core CRUD" scope decision, this build keeps exactly those 6 categories in full — `effective_settings` (1, read-only, no CRUD verbs exist for this resource), `custom_field_item_user_filters` (1, same), `jobcodes` (3: create/retrieve/update), `users` (3: create/retrieve/update), `timesheets` (4: create/retrieve/update/delete), `custom_fields` (3: create/retrieve/update) — 15 tools total. Every other category from the original 85-tool build (Reports, Files, Time Off Requests (+ Entries), Schedule Events (+ Calendars), Reminders, Projects (+ Notes/Activities/Activity Replies/Activity Read Times), Notifications, Locations (+ Maps), Jobcode Assignments, Groups, Estimates (+ Items), Custom Field Items (+ Filters + Jobcode Filters), Geolocations, Timesheets Deleted, Managed Clients, Last Modified, Invitations, Geofence Configs, Current User — 28 categories, ~70 tools) was removed entirely as unused by MSPbots.

Source data for the kept tools was originally extracted by cloning the TSheets docs' own GitHub repository (`https://github.com/tsheetsteam/api_docs`) and parsing every per-endpoint Markdown/ERB partial file (`source/includes/APIReference/<Category>/_*.md.erb`) for its HTTP method, path, and parameter table — the same structured-extraction-then-codegen approach used for other large-API vendors in this program (ConnectSecure, Dynu, Jira Data Center, Opsgenie). If a removed category is needed later, that same source can be re-parsed the same way.

## Authentication

TSheets uses a static **access token** obtained via the vendor's own OAuth/API-app flow (see MSPbots' internal KB article linked from its own integration config). MSPbots' own integration convention sends this token as `Authorization: Bearer <accessToken>`, matching TSheets' own documented format, and this server forwards it exactly that way.

### HEADER 授权参数说明

| Header | 类型 | 是否必填 | 默认值 | 枚举值 | 字段描述 | Example |
|---|---|---|---|---|---|---|
| `X-TSheets-Access-Token` | string | 是 | 无 | 无 | TSheets 访问令牌，原样转发为上游 `Authorization: Bearer <accessToken>` 请求头 | `X-TSheets-Access-Token: S.17__xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

Missing the header returns `401`:
```json
{
  "error": "Missing credentials",
  "message": "This server requires the X-TSheets-Access-Token header",
  "required_headers": ["X-TSheets-Access-Token"],
  "optional_headers": []
}
```

## Environment Variables

| Variable | 类型 | 是否必填 | 默认值 | 说明 |
|---|---|---|---|---|
| `MCP_HTTP_PORT` | int | 否 | `8080` | HTTP 监听端口 |
| `MCP_HTTP_HOST` | string | 否 | `0.0.0.0` | HTTP 监听地址 |
| `TSHEETS_BASE_URL` | string | 否 | `https://rest.tsheets.com/api/v1` | TSheets API 基础 URL |

## MCP Endpoint

- `POST /mcp` — MCP protocol (streamable HTTP transport)
- `GET /health` — health check, returns exactly `{"status": "ok"}`. This is a pure local probe — it does not call the TSheets API, so TSheets outages never mark the container unhealthy.

## Errors and pagination

- Tool errors are returned as an in-band JSON envelope (not a raised exception or protocol-level error): `{"error": {"code": "...", "message": "...", "retryable": true|false}}`. `code` is one of `not_configured` / `unauthorized` / `not_found` / `invalid_argument` / `rate_limited` / `upstream_error`, mapped from the upstream HTTP status.
- Outbound calls to the TSheets API use a 5s connect / 30s read timeout, retry up to 3 times with capped exponential backoff on `429`/`5xx` (honoring `Retry-After`), and reuse a single connection pool for the process lifetime.
- Every `retrieve_*` tool's `limit` parameter defaults to **50** and is clamped to TSheets' own documented per-page maximum of **200** if a caller asks for more (TSheets' own API also defaults to/maxes out at 200, so the two ceilings agree here).

## Tool List

Tool names are `tsheets_<category>_<operation>`, derived from each operation's `## Heading` in the source docs (e.g. "Retrieve Timesheets" in the `timesheets` category → `tsheets_timesheets_retrieve_timesheets`). Several `retrieve` filter parameters are documented as "required (unless X, Y, or Z is set)" — a one-of-N requirement that can't be cleanly expressed as a single hard-required Python parameter, so those are modeled as optional and the OR-constraint is spelled out in the tool's own docstring instead. `body` parameters for create/update endpoints are accepted as a generic `dict` — TSheets' own convention wraps these in `{"data": [ {...}, ... ]}` (bulk create/update of up to 50 objects per call), documented per-tool.

| Category | Tool | 功能 | 方法+路径 | 参数 |
|---|---|---|---|---|
| custom_field_item_user_filters | `tsheets_custom_field_item_user_filters_retrieve_user_filters` | Retrieve User Filters. | GET /customfielditem_user_filters | user_id(可选), group_id(可选), include_user_group(可选), modified_before(可选), modified_since(可选), limit(可选), page(可选) |
| custom_fields | `tsheets_custom_fields_create_custom_fields` | Create Custom Fields. | POST /customfields | body(必填) |
| custom_fields | `tsheets_custom_fields_retrieve_custom_fields` | Retrieve Custom Fields. | GET /customfields | ids(可选), active(可选), applies_to(可选), value_type(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| custom_fields | `tsheets_custom_fields_update_custom_fields` | Update Custom Fields. | PUT /customfields | body(必填) |
| effective_settings | `tsheets_effective_settings_retrieve_effective_settings` | Retrieve Effective Settings. | GET /effective_settings | user_id(可选), modified_before(可选), modified_since(可选) |
| jobcodes | `tsheets_jobcodes_create_jobcodes` | Create Jobcodes. | POST /jobcodes | body(必填) |
| jobcodes | `tsheets_jobcodes_retrieve_jobcodes` | Retrieve Jobcodes. | GET /jobcodes | ids(可选), parent_ids(可选), name(可选), type(可选), active(可选), customfields(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| jobcodes | `tsheets_jobcodes_update_jobcodes` | Update Jobcodes. | PUT /jobcodes | body(必填) |
| timesheets | `tsheets_timesheets_create_timesheets` | Create Timesheets. | POST /timesheets | body(必填) |
| timesheets | `tsheets_timesheets_delete_timesheets` | Delete Timesheets. | DELETE /timesheets | ids(可选) |
| timesheets | `tsheets_timesheets_retrieve_timesheets` | Retrieve Timesheets. | GET /timesheets | ids(可选), start_date(可选), end_date(可选), jobcode_ids(可选), payroll_ids(可选), user_ids(可选), group_ids(可选), on_the_clock(可选), jobcode_type(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| timesheets | `tsheets_timesheets_update_timesheets` | Update Timesheets. | PUT /timesheets | body(必填) |
| users | `tsheets_users_create_users` | Create Users. | POST /users | body(必填) |
| users | `tsheets_users_retrieve_users` | Retrieve Users. | GET /users | ids(可选), not_ids(可选), employee_numbers(可选), usernames(可选), group_ids(可选), not_group_ids(可选), payroll_ids(可选), active(可选), first_name(可选), last_name(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| users | `tsheets_users_update_users` | Update Users. | PUT /users | body(必填) |

## 测试示例

```bash
# Health check
curl -s http://localhost:8080/health

# Call a tool via the MCP protocol (streamable HTTP) — requires an
# initialize handshake first per the MCP spec; abbreviated example below
# shows the tool-call request body only:
curl -s -X POST http://localhost:8080/mcp \
  -H "X-TSheets-Access-Token: <your-tsheets-access-token>" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: <session-id-from-initialize>" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "tsheets_jobcodes_retrieve_jobcodes",
      "arguments": {}
    }
  }'
```

**Live-verified** (2026-07-30): a first test access token turned out to be expired (`401 invalid_grant`, confirmed identical via direct `curl` — see the bug note below for what that run caught). A second, freshly-issued access token was then tested end-to-end through this running server and returned **real account data**: `tsheets_current_user_retrieve_the_current_user` returned the actual current user record (name, permissions, PTO balances) plus supplemental jobcode data, and `tsheets_jobcodes_retrieve_jobcodes` (matching one of MSPbots' own 6 configured endpoints) returned real jobcode records. Both confirm the full request/auth/response pipeline works correctly against the live API.

**Bug fixed during self-test**: the initial `_raise_for_status` error parser assumed TSheets always nests error details as `{"error": {"message": "..."}}`, but TSheets actually returns an OAuth-style flat `{"error": "invalid_grant", "error_description": "..."}` for auth failures — calling `.get()` on the string `"invalid_grant"` crashed with `'str' object has no attribute 'get'`. This was caught and fixed using the first (expired) test token, before this server was considered done.

## API Reference

- Overview: https://tsheetsteam.github.io/api_docs/
- Source (incl. official Postman collection): https://github.com/tsheetsteam/api_docs

## Known Gaps

- **Trimmed from 85 to 15 tools on 2026-08-04.** The original build covered
  the full public API across 34 categories per an earlier scope decision.
  A later scope decision cut this back to exactly MSPbots' actually-used 6
  categories (all kept in full — no per-category trimming was needed since
  none exceeded a handful of tools) — see the Scope section above for the
  full list of the 28 removed categories (~70 tools). If a removed category
  is needed later, the source docs (`https://github.com/tsheetsteam/api_docs`)
  can be re-parsed the same way the kept tools were generated.
- `tsheets_timesheets_delete_timesheets` **permanently deletes** timesheet
  records per the vendor's own docs — treat as destructive/irreversible and
  confirm with a human before invoking. The other kept `create`/`update`
  tools also mutate real TSheets data (jobcodes, users, custom fields).
- **One-of-N "required" filter groups are modeled as all-optional** — several `Retrieve` endpoints document a param as "required (unless X, Y, or Z is set)"; enforcing that as a real constraint isn't expressible in a plain function signature, so all such params are optional in the tool signature and the OR-requirement is spelled out in the docstring instead. Callers must supply at least one per the documented constraint or the live API will reject the request.
- **`body` parameters are untyped (`dict`)** rather than fully modeled — TSheets' own docs show per-type field variants (e.g. "Regular Timesheets" vs "Manual Timesheets" have different required fields within the same `data` array), which don't map cleanly onto fixed typed parameters; the vendor's own reference (linked above) documents the exact schema per resource.
