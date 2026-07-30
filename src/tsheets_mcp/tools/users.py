import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_users_create_users(body: dict) -> str:
        """Create Users.

        API: POST /users

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/users", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_users_retrieve_users(ids: str | None = None, not_ids: str | None = None, employee_numbers: str | None = None, usernames: str | None = None, group_ids: str | None = None, not_group_ids: str | None = None, payroll_ids: str | None = None, active: str | None = None, first_name: str | None = None, last_name: str | None = None, modified_before: str | None = None, modified_since: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Users.

        API: GET /users

        Args:
            ids: Optional. Comma separated list of one or more user ids you'd like to filter on.
            not_ids: Optional. Comma separated list of one or more user ids you'd like to filter on. Specifically, the user ids you'd like to exclude.
            employee_numbers: Optional. Comma separated list of one or more employee numbers you'd like to filter on.
            usernames: Optional. Comma separated list of one or more usernames you'd like to filter on.
            group_ids: Optional. Comma separated list of one or more group ids you'd like to filter on.
            not_group_ids: Optional. Comma separated list of one or more group ids you'd like to filter on. Specifically, the group ids you'd like to exclude.
            payroll_ids: Optional. A comma-separated string of payroll ids. Only users with these payroll ids will be returned.
            active: Optional. 'yes', 'no', or 'both'. Default is 'yes'.
            first_name: Optional. * will be interpreted as a wild card. Starts matching from the beginning of the string.
            last_name: Optional. * will be interpreted as a wild card. Starts matching from the beginning of the string.
            modified_before: Optional. Only users modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            modified_since: Optional. Only users modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "not_ids": not_ids, "employee_numbers": employee_numbers, "usernames": usernames, "group_ids": group_ids, "not_group_ids": not_group_ids, "payroll_ids": payroll_ids, "active": active, "first_name": first_name, "last_name": last_name, "modified_before": modified_before, "modified_since": modified_since, "supplemental_data": supplemental_data, "limit": limit, "page": page}
        try:
            result = await client.get("/users", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_users_update_users(body: dict) -> str:
        """Update Users.

        API: PUT /users

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.put("/users", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
