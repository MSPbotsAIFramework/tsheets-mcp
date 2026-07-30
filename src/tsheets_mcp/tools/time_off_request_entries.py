import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_time_off_request_entries_create_time_off_request_entries(body: dict) -> str:
        """Create Time Off Request Entries.

        API: POST /time_off_request_entries

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/time_off_request_entries", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_time_off_request_entries_retrieve_time_off_request_entries(ids: str | None = None, time_off_request_ids: str | None = None, approver_user_ids: str | None = None, status: str | None = None, date: str | None = None, start_time: str | None = None, end_time: str | None = None, jobcode_ids: str | None = None, user_ids: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Time Off Request Entries.

        API: GET /time_off_request_entries

        Args:
            ids: Optional. Comma separated list of one or more time off request entry ids you'd like to filter on. Only time off request entries with an id set to one of these values will be returned.
            time_off_request_ids: Optional. Comma separated list of one or more [Time Off Request](#the-time-off-request-object) ids you'd like to filter on. Only time off request entries associated with a time off request id set to one of these values will be returned.
            approver_user_ids: Optional. Comma separated list of one or more user ids. Only time off requests linked to one of these user ids will be returned. Only administrators or group managers may retrieve time off requests for users other than themselves. Furthermore, administrators or group managers may only retrieve time off requests for users that belong to their company.
            status: Optional. One of: 'pending', 'approved', 'denied', or 'canceled'.
            date: Optional. Only time off request entries set for this date will be returned (YYYY-MM-DD format).
            start_time: Optional. Only time off request entries with a start_time greater than or equal to this Date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            end_time: Optional. Only time off request entries with a start_time less than or equal to this Date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            jobcode_ids: Optional. Comma separated list of one or more jobcode ids you'd like to filter on. Only time off request entries with a jobcode id set to one of these values will be returned.
            user_ids: Optional. Comma separated list of one or more user ids. Only time off request entries linked to one of these user ids will be returned. Only administrators or group managers may retrieve time off request entries for users other than themselves. Furthermore, administrators or group managers may only retrieve time off request entries for users that belong to their company.
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "time_off_request_ids": time_off_request_ids, "approver_user_ids": approver_user_ids, "status": status, "date": date, "start_time": start_time, "end_time": end_time, "jobcode_ids": jobcode_ids, "user_ids": user_ids, "supplemental_data": supplemental_data, "limit": limit, "page": page}
        try:
            result = await client.get("/time_off_request_entries", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_time_off_request_entries_update_time_off_request_entries(body: dict) -> str:
        """Update Time Off Request Entries.

        API: PUT /time_off_request_entries

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.put("/time_off_request_entries", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
