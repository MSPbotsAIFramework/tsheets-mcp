import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_jobcode_assignments_create_jobcode_assignments(body: dict) -> str:
        """Create Jobcode Assignments.

        API: POST /jobcode_assignments

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/jobcode_assignments", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_jobcode_assignments_delete_jobcode_assignments(ids: str | None = None) -> str:
        """Delete Jobcode Assignments.

        API: DELETE /jobcode_assignments

        Args:
            ids: Optional. Comma separated list of jobcode assignment ids you'd like to delete.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids}
        try:
            result = await client.delete("/jobcode_assignments", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_jobcode_assignments_retrieve_jobcode_assignments(user_ids: str | None = None, type: str | None = None, jobcode_id: str | None = None, jobcode_parent_id: str | None = None, active: str | None = None, active_jobcodes: str | None = None, modified_before: str | None = None, modified_since: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Jobcode Assignments.

        API: GET /jobcode_assignments

        Args:
            user_ids: Optional. Comma separated string of one or more user ids for whom you'd like to retrieve jobcode assignments. If none are specified, all jobcode assignments (which you have rights to view) will be returned. Only jobcode assignments belonging to these user_ids or where the jobcode assigned_to_all property is _true_ will be returned. Results where assigned_to_all is _true_ for a jobcode are indicated by a user_id value of _0_ for the jobcode_assignment object. To view jobcode assignments for users other than yourself you must be an admin or a group manager or have the manage_users permission or the manage_jobcodes permission.
            type: Optional. Refers to the jobcode type - 'regular', 'pto', 'unpaid_break', 'paid_break', or 'all'. Defaults to 'regular'.
            jobcode_id: Optional. If specified, only assignments for jobcodes with the given id are returned.
            jobcode_parent_id: Optional. When omitted, all jobcode assignments are returned regardless of jobcode parent. If specified, only assignments for jobcodes with the given jobcode parent_id are returned. To get a list of only top-level jobcode assignments, pass in a jobcode_parent_id of _0_.
            active: Optional. 'yes', 'no, or 'both'. Default is 'both'. 'yes' means the assignment is active, 'no' means it is deleted/inactive.
            active_jobcodes: Optional. 'yes', 'no, or 'both'. Default is 'both'. 'yes' means only assignments where the jobcode is active, 'no' means only assignments where jobcodes are inactive.
            modified_before: Optional. Only jobcode assignments modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            modified_since: Optional. Only jobcode assignments modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"user_ids": user_ids, "type": type, "jobcode_id": jobcode_id, "jobcode_parent_id": jobcode_parent_id, "active": active, "active_jobcodes": active_jobcodes, "modified_before": modified_before, "modified_since": modified_since, "supplemental_data": supplemental_data, "limit": limit, "page": page}
        try:
            result = await client.get("/jobcode_assignments", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
