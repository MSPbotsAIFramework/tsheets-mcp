import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_schedule_events_create_schedule_events(body: dict) -> str:
        """Create Schedule Events.

        API: POST /schedule_events

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/schedule_events", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_schedule_events_retrieve_schedule_events(schedule_calendar_ids: str, ids: str | None = None, users_ids: str | None = None, jobcode_ids: str | None = None, start: str | None = None, end: str | None = None, active: str | None = None, active_users: str | None = None, draft: str | None = None, team_events: str | None = None, modified_before: str | None = None, modified_since: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Schedule Events.

        API: GET /schedule_events

        Args:
            schedule_calendar_ids: Required. Comma separated list of one or more schedule calendar ids you'd like to filter on. Only schedule events with a schedule calendar id set to one of these values will be returned.
            ids: Optional. Comma separated list of one or more schedule event ids you'd like to filter on. Only schedule events with an id set to one of these values will be returned. [required (unless modified_before, modified_since, or start are set)]
            users_ids: Optional. Comma-separated list of one or more user ids to retrieve schedule events for.
            jobcode_ids: Optional. A comma-separated string of jobcode ids. Only schedule events with these jobcodes will be returned.
            start: Optional. Only schedule events starting on or after this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm). [required (unless ids, modified_before, or modified_since are set)]
            end: Optional. Only schedule events ending on or before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            active: Optional. 'yes', 'no' or 'both'. Default is 'both'. Only schedule events whose active state match the requested filter will be returned.
            active_users: Optional. '0', '-1' or '1' . Default is '1'. Only schedule events whose users are active will be returned by default. 0 will return events for inactive users. -1 will return events for active and inactive users.
            draft: Optional. 'yes', 'no' or 'both'. Default is 'no'. Only schedule events whose draft state match the requested filter will be returned.
            team_events: Optional. 'base' or 'instance'. Default is 'instance'. If 'instance' is specified, events that are assigned to multiple users will be returned as individual single events for each assigned user. If 'base' is specified, events that are assigned to multiple users will be returned as one combined event for all assignees.
            modified_before: Optional. Only schedule events modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm). [required (unless ids, modified_since, or start are set)]
            modified_since: Optional. Only schedule events modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm). [required (unless ids, modified_before, or start are set)]
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "users_ids": users_ids, "schedule_calendar_ids": schedule_calendar_ids, "jobcode_ids": jobcode_ids, "start": start, "end": end, "active": active, "active_users": active_users, "draft": draft, "team_events": team_events, "modified_before": modified_before, "modified_since": modified_since, "supplemental_data": supplemental_data, "limit": limit, "page": page}
        try:
            result = await client.get("/schedule_events", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_schedule_events_update_schedule_events(body: dict) -> str:
        """Update Schedule Events.

        API: PUT /schedule_events

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.put("/schedule_events", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
