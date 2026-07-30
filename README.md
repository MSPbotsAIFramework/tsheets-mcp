# tsheets-mcp

MCP server for **TSheets (QuickBooks Time)** — Intuit's time-tracking, scheduling, and PTO platform. Exposes the full public TSheets REST API v1 as MCP tools.

## Overview

- Stateless HTTP service. No credentials are ever persisted — each request supplies its own access token via a header, used only for the lifetime of that single request.
- Supports concurrent requests; per-request credential isolation is done via Python `contextvars`, not a global/shared client instance.
- Entry points: `POST /mcp` (MCP protocol) and `GET /health` (health check).
- Default port: `8080` (configurable via `MCP_HTTP_PORT`).
- **No path-template parameters exist anywhere in the TSheets API** — every identifier (`ids`, `user_id`, etc.) is passed as a query-string parameter, even for single-resource lookups. This is a genuine API design characteristic, not a simplification made by this server.

## Scope

**85 tools** across 34 categories, generated from the official TSheets API documentation source (`https://github.com/tsheetsteam/api_docs`, cloned and parsed directly — the docs' own Postman collection lists 71 requests across 29 folders, but the underlying markdown source documents several additional categories not present in that collection, e.g. `TimeOffRequests`/`TimeOffRequestEntries`, `CustomFieldItemJobcodeFilters`, `Invitations`).

MSPbots' own stored integration config for this vendor calls exactly **6** endpoints (Effective Settings, Jobcodes, Users, Customfielditem User Filters, Timesheets, Custom Fields — all `GET`, read-only). Per explicit user decision, this build covers the **full public API including write operations** (create/update/delete across every resource, plus the six built-in payroll/project report endpoints), not just those 6 calls — see **Known Gaps** for which tools mutate real data.

Source data was extracted by cloning the TSheets docs' own GitHub repository and parsing every per-endpoint Markdown/ERB partial file (`source/includes/APIReference/<Category>/_*.md.erb`) for its HTTP method, path, and parameter table — the same structured-extraction-then-codegen approach used for other large-API vendors in this program (ConnectSecure, Dynu, Jira Data Center, Opsgenie).

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
- `GET /health` — health check, returns `{"status": "ok", "service": "tsheets-mcp", "transport": "http"}`

## Tool List

Tool names are `tsheets_<category>_<operation>`, derived from each operation's `## Heading` in the source docs (e.g. "Retrieve Timesheets" in the `timesheets` category → `tsheets_timesheets_retrieve_timesheets`). Several `retrieve` filter parameters are documented as "required (unless X, Y, or Z is set)" — a one-of-N requirement that can't be cleanly expressed as a single hard-required Python parameter, so those are modeled as optional and the OR-constraint is spelled out in the tool's own docstring instead. `body` parameters for create/update endpoints are accepted as a generic `dict` — TSheets' own convention wraps these in `{"data": [ {...}, ... ]}` (bulk create/update of up to 50 objects per call), documented per-tool.

| Category | Tool | 功能 | 方法+路径 | 参数 |
|---|---|---|---|---|
| current_user | `tsheets_current_user_retrieve_the_current_user` | Retrieve the Current User. | GET /current_user | 无 |
| custom_field_item_filters | `tsheets_custom_field_item_filters_create_item_filters` | Create Item Filters. | POST /customfielditem_filters | body(必填) |
| custom_field_item_filters | `tsheets_custom_field_item_filters_retrieve_item_filters` | Retrieve Item Filters. | GET /customfielditem_filters | jobcode_id(可选), user_id(可选), group_id(可选), include_user_group(可选), include_jobcode_filters(可选), ids(可选), active(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| custom_field_item_filters | `tsheets_custom_field_item_filters_update_item_filters` | Update Item Filters. | PUT /customfielditem_filters | body(必填) |
| custom_field_item_jobcode_filters | `tsheets_custom_field_item_jobcode_filters_retrieve_jobcode_filters` | Retrieve Jobcode Filters. | GET /customfielditem_jobcode_filters | jobcode_ids(可选), modified_before(可选), modified_since(可选), limit(可选), page(可选) |
| custom_field_item_user_filters | `tsheets_custom_field_item_user_filters_retrieve_user_filters` | Retrieve User Filters. | GET /customfielditem_user_filters | user_id(可选), group_id(可选), include_user_group(可选), modified_before(可选), modified_since(可选), limit(可选), page(可选) |
| custom_field_items | `tsheets_custom_field_items_create_custom_field_items` | Create Custom Field Items. | POST /customfielditems | body(必填) |
| custom_field_items | `tsheets_custom_field_items_retrieve_custom_field_items` | Retrieve Custom Field Items. | GET /customfielditems | customfield_id(必填), ids(可选), active(可选), name(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| custom_field_items | `tsheets_custom_field_items_update_custom_field_items` | Update Custom Field Items. | PUT /customfielditems | body(必填) |
| custom_fields | `tsheets_custom_fields_create_custom_fields` | Create Custom Fields. | POST /customfields | body(必填) |
| custom_fields | `tsheets_custom_fields_retrieve_custom_fields` | Retrieve Custom Fields. | GET /customfields | ids(可选), active(可选), applies_to(可选), value_type(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| custom_fields | `tsheets_custom_fields_update_custom_fields` | Update Custom Fields. | PUT /customfields | body(必填) |
| effective_settings | `tsheets_effective_settings_retrieve_effective_settings` | Retrieve Effective Settings. | GET /effective_settings | user_id(可选), modified_before(可选), modified_since(可选) |
| estimate_items | `tsheets_estimate_items_create_estimate_items` | Create Estimate Items. | POST /estimate_items | body(必填) |
| estimate_items | `tsheets_estimate_items_retrieve_estimate_items` | Retrieve Estimate Items. | GET /estimate_items | ids(可选), estimate_ids(可选), active(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| estimate_items | `tsheets_estimate_items_update_estimate_items` | Update Estimate Items. | PUT /estimate_items | body(必填) |
| estimates | `tsheets_estimates_create_estimates` | Create Estimates. | POST /estimates | body(必填) |
| estimates | `tsheets_estimates_retrieve_estimates` | Retrieve Estimates. | GET /estimates | ids(可选), active(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| estimates | `tsheets_estimates_update_estimates` | Update Estimates. | PUT /estimates | body(必填) |
| files | `tsheets_files_delete_files` | Delete Files. | DELETE /files | ids(可选) |
| files | `tsheets_files_download_a_file` | Download a File. | GET /files/raw | id(必填) |
| files | `tsheets_files_retrieve_files` | Retrieve Files. | GET /files | ids(可选), uploaded_by_user_ids(可选), linked_object_type(可选), object_ids(可选), active(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| files | `tsheets_files_update_files` | Update Files. | PUT /files | body(必填) |
| files | `tsheets_files_upload_files` | Upload Files. | POST /files | body(必填) |
| geofence_configs | `tsheets_geofence_configs_retrieve_geofence_configs` | Retrieve Geofence Configs. | GET /geofence_configs | ids(可选), type(可选), type_ids(可选), enabled(可选), active(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选), by_jobcode_assignment(可选) |
| geolocations | `tsheets_geolocations_create_geolocations` | Create Geolocations. | POST /geolocations | body(必填) |
| geolocations | `tsheets_geolocations_retrieve_geolocations` | Retrieve Geolocations. | GET /geolocations | ids(可选), modified_before(可选), modified_since(可选), user_ids(可选), group_ids(可选), supplemental_data(可选), limit(可选), page(可选) |
| groups | `tsheets_groups_create_groups` | Create Groups. | POST /groups | body(必填) |
| groups | `tsheets_groups_retrieve_groups` | Retrieve Groups. | GET /groups | ids(可选), active(可选), manager_ids(可选), name(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| groups | `tsheets_groups_update_groups` | Update Groups. | PUT /groups | body(必填) |
| invitations | `tsheets_invitations_create_invitations` | Create Invitations. | POST /invitations | body(必填) |
| jobcode_assignments | `tsheets_jobcode_assignments_create_jobcode_assignments` | Create Jobcode Assignments. | POST /jobcode_assignments | body(必填) |
| jobcode_assignments | `tsheets_jobcode_assignments_delete_jobcode_assignments` | Delete Jobcode Assignments. | DELETE /jobcode_assignments | ids(可选) |
| jobcode_assignments | `tsheets_jobcode_assignments_retrieve_jobcode_assignments` | Retrieve Jobcode Assignments. | GET /jobcode_assignments | user_ids(可选), type(可选), jobcode_id(可选), jobcode_parent_id(可选), active(可选), active_jobcodes(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| jobcodes | `tsheets_jobcodes_create_jobcodes` | Create Jobcodes. | POST /jobcodes | body(必填) |
| jobcodes | `tsheets_jobcodes_retrieve_jobcodes` | Retrieve Jobcodes. | GET /jobcodes | ids(可选), parent_ids(可选), name(可选), type(可选), active(可选), customfields(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| jobcodes | `tsheets_jobcodes_update_jobcodes` | Update Jobcodes. | PUT /jobcodes | body(必填) |
| last_modified | `tsheets_last_modified_retrieve_last_modified_timestamps` | Retrieve Last Modified Timestamps. | GET /last_modified_timestamps | endpoints(可选) |
| locations | `tsheets_locations_create_locations` | Create Locations. | POST /locations | body(必填) |
| locations | `tsheets_locations_retrieve_locations` | Retrieve Locations. | GET /locations | ids(可选), active(可选), geocoding_status(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选), by_jobcode_assignment(可选) |
| locations | `tsheets_locations_update_locations` | Update Locations. | PUT /locations | body(必填) |
| locations_maps | `tsheets_locations_maps_retrieve_locations_maps` | Retrieve Locations Maps. | GET /locations_map | ids(可选), active(可选), modified_before(可选), modified_since(可选), limit(可选), page(可选), by_jobcode_assignment(可选) |
| managed_clients | `tsheets_managed_clients_retrieve_managed_clients` | Retrieve Managed Clients. | GET /managed_clients | active(可选), limit(可选), page(可选) |
| notifications | `tsheets_notifications_create_notifications` | Create Notifications. | POST /notifications | body(必填) |
| notifications | `tsheets_notifications_delete_notifications` | Delete Notifications. | DELETE /notifications | ids(必填) |
| notifications | `tsheets_notifications_retrieve_notifications` | Retrieve Notifications. | GET /notifications | ids(可选), delivery_before(可选), delivery_after(可选), user_id(可选), msg_tracking_id(可选), limit(可选), page(可选) |
| project_activities | `tsheets_project_activities_retrieve_project_activity_objects` | Retrieve Project Activity objects. | GET /project_activities | project_id(可选), ids(可选), activity_types(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选), max_id(可选) |
| project_activity_read_times | `tsheets_project_activity_read_times_retrieve_project_activity_read_times` | Retrieve Project Activity Read Times. | GET /project_activity_read_times | ids(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| project_activity_read_times | `tsheets_project_activity_read_times_update_project_activity_read_time` | Update Project Activity Read Time. | POST /project_activity_read_times | body(必填) |
| project_activity_replies | `tsheets_project_activity_replies_create_project_activity_replies` | Create Project Activity Replies. | POST /project_activity_replies | body(必填) |
| project_activity_replies | `tsheets_project_activity_replies_retrieve_project_activity_replies` | Retrieve Project Activity Replies. | GET /project_activity_replies | project_activity_id(必填), ids(可选), user_ids(可选), active(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| project_activity_replies | `tsheets_project_activity_replies_update_project_activity_replies` | Update Project Activity Replies. | PUT /project_activity_replies | body(必填) |
| project_notes | `tsheets_project_notes_create_project_notes` | Create Project Notes. | POST /project_notes | body(必填) |
| project_notes | `tsheets_project_notes_retrieve_project_notes` | Retrieve Project Notes. | GET /project_notes | project_id(必填), ids(可选), user_ids(可选), active(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| project_notes | `tsheets_project_notes_update_project_notes` | Update Project Notes. | PUT /project_notes | body(必填) |
| projects | `tsheets_projects_create_projects` | Create Projects. | POST /projects | body(必填) |
| projects | `tsheets_projects_retrieve_projects` | Retrieve Projects. | GET /projects | ids(可选), jobcode_ids(可选), parent_jobcode_id(可选), name(可选), active(可选), by_jobcode_assignment(可选) |
| projects | `tsheets_projects_update_projects` | Update Projects. | PUT /projects | body(必填) |
| reminders | `tsheets_reminders_create_reminders` | Create Reminders. | POST /reminders | body(必填) |
| reminders | `tsheets_reminders_retrieve_reminders` | Retrieve Reminders. | GET /reminders | user_ids(必填), reminder_types(可选), modified_since(可选), supplemental_data(可选) |
| reminders | `tsheets_reminders_update_reminders` | Update Reminders. | PUT /reminders | body(必填) |
| reports | `tsheets_reports_retrieve_current_totals_report` | Retrieve Current Totals Report. | POST /reports/current_totals | body(必填) |
| reports | `tsheets_reports_retrieve_payroll_by_jobcode_report` | Retrieve Payroll by Jobcode Report. | POST /reports/payroll_by_jobcode | body(必填) |
| reports | `tsheets_reports_retrieve_payroll_report` | Retrieve Payroll Report. | POST /reports/payroll | body(必填) |
| reports | `tsheets_reports_retrieve_project_estimate_detail_reports` | Retrieve Project Estimate Detail Reports. | POST /reports/project_estimate_detail | body(必填) |
| reports | `tsheets_reports_retrieve_project_estimate_reports` | Retrieve Project Estimate Reports. | POST /reports/project_estimate | body(必填) |
| reports | `tsheets_reports_retrieve_project_report` | Retrieve Project Report. | POST /reports/project | body(必填) |
| schedule_calendars | `tsheets_schedule_calendars_retrieve_schedule_calendars` | Retrieve Schedule Calendars. | GET /schedule_calendars | ids(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| schedule_events | `tsheets_schedule_events_create_schedule_events` | Create Schedule Events. | POST /schedule_events | body(必填) |
| schedule_events | `tsheets_schedule_events_retrieve_schedule_events` | Retrieve Schedule Events. | GET /schedule_events | schedule_calendar_ids(必填), ids(可选), users_ids(可选), jobcode_ids(可选), start(可选), end(可选), active(可选), active_users(可选), draft(可选), team_events(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| schedule_events | `tsheets_schedule_events_update_schedule_events` | Update Schedule Events. | PUT /schedule_events | body(必填) |
| time_off_request_entries | `tsheets_time_off_request_entries_create_time_off_request_entries` | Create Time Off Request Entries. | POST /time_off_request_entries | body(必填) |
| time_off_request_entries | `tsheets_time_off_request_entries_retrieve_time_off_request_entries` | Retrieve Time Off Request Entries. | GET /time_off_request_entries | ids(可选), time_off_request_ids(可选), approver_user_ids(可选), status(可选), date(可选), start_time(可选), end_time(可选), jobcode_ids(可选), user_ids(可选), supplemental_data(可选), limit(可选), page(可选) |
| time_off_request_entries | `tsheets_time_off_request_entries_update_time_off_request_entries` | Update Time Off Request Entries. | PUT /time_off_request_entries | body(必填) |
| time_off_requests | `tsheets_time_off_requests_create_time_off_requests` | Create Time Off Requests. | POST /time_off_requests | body(必填) |
| time_off_requests | `tsheets_time_off_requests_retrieve_time_off_requests` | Retrieve Time Off Requests. | GET /time_off_requests | ids(可选), user_ids(可选), supplemental_data(可选), limit(可选), page(可选) |
| time_off_requests | `tsheets_time_off_requests_update_time_off_requests` | Update Time Off Requests. | PUT /time_off_requests | body(必填) |
| timesheets | `tsheets_timesheets_create_timesheets` | Create Timesheets. | POST /timesheets | body(必填) |
| timesheets | `tsheets_timesheets_delete_timesheets` | Delete Timesheets. | DELETE /timesheets | ids(可选) |
| timesheets | `tsheets_timesheets_retrieve_timesheets` | Retrieve Timesheets. | GET /timesheets | ids(可选), start_date(可选), end_date(可选), jobcode_ids(可选), payroll_ids(可选), user_ids(可选), group_ids(可选), on_the_clock(可选), jobcode_type(可选), modified_before(可选), modified_since(可选), supplemental_data(可选), limit(可选), page(可选) |
| timesheets | `tsheets_timesheets_update_timesheets` | Update Timesheets. | PUT /timesheets | body(必填) |
| timesheets_deleted | `tsheets_timesheets_deleted_retrieve_timesheets_deleted` | Retrieve Timesheets Deleted. | GET /timesheets_deleted | start_date(可选), end_date(可选), ids(可选), modified_since(可选), modified_before(可选), group_ids(可选), user_ids(可选), username(可选), jobcode_ids(可选), jobcode_type(可选), type(可选), order_results_by(可选), order_results_reverse(可选), page(可选), limit(可选) |
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
      "name": "tsheets_current_user_retrieve_the_current_user",
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

- **Full API coverage was an explicit user decision**, matching the pattern used for other large public APIs in this program. MSPbots itself only calls 6 read-only endpoints; every `create`/`update`/`delete` tool here mutates real TSheets data (timesheets, users, jobcodes, schedule events, files, etc.) or — for `tsheets_timesheets_delete_timesheets` and `tsheets_files_delete_files` in particular — **permanently deletes** records/attached files per the vendor's own docs. Treat any such tool as destructive/irreversible and confirm with a human before invoking.
- **One-of-N "required" filter groups are modeled as all-optional** — several `Retrieve` endpoints document a param as "required (unless X, Y, or Z is set)"; enforcing that as a real constraint isn't expressible in a plain function signature, so all such params are optional in the tool signature and the OR-requirement is spelled out in the docstring instead. Callers must supply at least one per the documented constraint or the live API will reject the request.
- **`body` parameters are untyped (`dict`)** rather than fully modeled — TSheets' own docs show per-type field variants (e.g. "Regular Timesheets" vs "Manual Timesheets" have different required fields within the same `data` array), which don't map cleanly onto fixed typed parameters; the vendor's own reference (linked above) documents the exact schema per resource.
- Source data comes from the docs' Markdown/ERB partials (not the API's actual OpenAPI/JSON-Schema, which TSheets doesn't publish) — the extraction was verified against the official Postman collection shipped in the same repository for cross-consistency (71 of 85 tools have a matching Postman request; the other 14 are documented-but-not-in-Postman categories like Time Off Requests).
