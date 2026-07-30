import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_time_off_requests_create_time_off_requests(body: dict) -> str:
        """Create Time Off Requests.

        API: POST /time_off_requests

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/time_off_requests", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_time_off_requests_retrieve_time_off_requests(ids: str | None = None, user_ids: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Time Off Requests.

        API: GET /time_off_requests

        Args:
            ids: Optional. Comma separated list of one or more time off request ids you'd like to filter on. Only time off requests with an id set to one of these values will be returned.
            user_ids: Optional. Comma separated list of one or more user ids. Only time off requests linked to one of these user ids will be returned. Only administrators or group managers may retrieve time off requests for users other than themselves. Furthermore, administrators or group managers may only retrieve time off requests for users that belong to their company.
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "user_ids": user_ids, "supplemental_data": supplemental_data, "limit": limit, "page": page}
        try:
            result = await client.get("/time_off_requests", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_time_off_requests_update_time_off_requests(body: dict) -> str:
        """Update Time Off Requests.

        API: PUT /time_off_requests

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.put("/time_off_requests", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
