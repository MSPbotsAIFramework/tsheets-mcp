import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_timesheets_deleted_retrieve_timesheets_deleted(start_date: str | None = None, end_date: str | None = None, ids: str | None = None, modified_since: str | None = None, modified_before: str | None = None, group_ids: str | None = None, user_ids: str | None = None, username: str | None = None, jobcode_ids: str | None = None, jobcode_type: str | None = None, type: str | None = None, order_results_by: str | None = None, order_results_reverse: str | None = None, page: str | None = None, limit: str | None = None) -> str:
        """Retrieve Timesheets Deleted.

        API: GET /timesheets_deleted

        Args:
            start_date: Optional. YYYY-MM-DD formatted date. Beginning date for the report data (based off the date the timesheets were created for). [required (unless modified_before, modified_since, or ids is set)]
            end_date: Optional. YYYY-MM-DD formatted date. Ending date for the report data (based off the date the timesheets were created for). [required (unless modified_before, modified_since, or ids is set)]
            ids: Optional. Timesheet ids. This can be a single id, an array of ids, or a comma-separated string of ids. '' by default. [required (unless modified_before, modified_since, or start_date and end_date are set)]
            modified_since: Optional. Only timesheets deleted since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm). [required (unless modified_before, ids, or start_date and end_date  are set)]
            modified_before: Optional. Only timesheets deleted before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm). [required (unless modified_since, ids, or start_date and end_date  are set)]
            group_ids: Optional. This can be a single id, an array of ids, or a comma-separated string of ids. If present, only timesheets associated with the specified group(s) will be returned. '' by default.
            user_ids: Optional. This can be a single id, an array of ids, or a comma-separated string of ids. If present, only timesheets associated with the specified user(s) will be returned. '' by default.
            username: Optional. If present, only timesheets associated with the specified username will be returned. Overrides user_ids and group_ids. '' by default.
            jobcode_ids: Optional. This can be a single id, an array of ids, or a comma-separated string of ids. If present, only timesheets recorded against the specified jobcode(s) and any children will be returned. '' by default.
            jobcode_type: Optional. 'regular', 'pto', 'paid_break', 'unpaid_break', or 'all'. Default is 'all'. Only timesheets linked to a jobcode of the given type are returned.
            type: Optional. 'manual', 'regular', or 'both'. 'both' is the default.
            order_results_by: Optional. 'fname', 'lname', 'username', or 'date'. 'date' is the default. All are secondarily sorted by 'date', unless 'date' is the choice, in which case 'date' is the only field the timesheets are sorted by.
            order_results_reverse: Optional. 1 or 0. If set to 1, then results are returned in reverse order by whatever they're sorted on.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"start_date": start_date, "end_date": end_date, "ids": ids, "modified_since": modified_since, "modified_before": modified_before, "group_ids": group_ids, "user_ids": user_ids, "username": username, "jobcode_ids": jobcode_ids, "jobcode_type": jobcode_type, "type": type, "order_results_by": order_results_by, "order_results_reverse": order_results_reverse, "page": page, "limit": limit}
        try:
            result = await client.get("/timesheets_deleted", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
