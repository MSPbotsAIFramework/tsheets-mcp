import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_timesheets_create_timesheets(body: dict) -> str:
        """Create Timesheets.

        API: POST /timesheets

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/timesheets", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_timesheets_delete_timesheets(ids: str | None = None) -> str:
        """Delete Timesheets.

        API: DELETE /timesheets

        Args:
            ids: Optional. Comma separated list of timesheet ids you'd like to delete. Note that timesheets are actually _deleted_, not archived.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids}
        try:
            result = await client.delete("/timesheets", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_timesheets_retrieve_timesheets(ids: str | None = None, start_date: str | None = None, end_date: str | None = None, jobcode_ids: str | None = None, payroll_ids: str | None = None, user_ids: str | None = None, group_ids: str | None = None, on_the_clock: str | None = None, jobcode_type: str | None = None, modified_before: str | None = None, modified_since: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Timesheets.

        API: GET /timesheets

        Args:
            ids: Optional. Comma separated list of one or more timesheet ids you'd like to filter on. Only timesheets with an id set to one of these values will be returned. If omitted, all timesheets matching other specified filters are returned. [required (unless modified_before, modified_since, or start_date are set)]
            start_date: Optional. YYYY-MM-DD formatted date. Any timesheets with a date falling on or after this date will be returned. [required (unless modified_before, modified_since, or ids is set)]
            end_date: Optional. YYYY-MM-DD formatted date. Any timesheets with a date falling on or before this date will be returned.
            jobcode_ids: Optional. A comma-separated string of jobcode ids. Only time recorded against these jobcodes or one of their children will be returned.
            payroll_ids: Optional. A comma-separated string of payroll ids. Only time recorded against users with these payroll ids will be returned.
            user_ids: Optional. A comma-separated list of user ids. Only timesheets linked to these users will be returned.
            group_ids: Optional. A comma-separated list of group ids. Only timesheets linked to users from these groups will be returned.
            on_the_clock: Optional. 'yes', 'no', or 'both'. Default is 'no'. If a timesheet is on_the_clock, it means the user is currently working (has not clocked out yet).
            jobcode_type: Optional. 'regular', 'pto', 'paid_break', 'unpaid_break', or 'all'. Default is 'all'. Only timesheets linked to a jobcode of the given type are returned.
            modified_before: Optional. Only timesheets modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm). [required (unless modified_since, ids, or start_date are set)]
            modified_since: Optional. Only timesheets modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm). [required (unless modified_before, ids, or start_date are set)]
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "start_date": start_date, "end_date": end_date, "jobcode_ids": jobcode_ids, "payroll_ids": payroll_ids, "user_ids": user_ids, "group_ids": group_ids, "on_the_clock": on_the_clock, "jobcode_type": jobcode_type, "modified_before": modified_before, "modified_since": modified_since, "supplemental_data": supplemental_data, "limit": limit, "page": page}
        try:
            result = await client.get("/timesheets", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_timesheets_update_timesheets(body: dict) -> str:
        """Update Timesheets.

        API: PUT /timesheets

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.put("/timesheets", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
