import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_custom_field_items_create_custom_field_items(body: dict) -> str:
        """Create Custom Field Items.

        API: POST /customfielditems

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/customfielditems", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_custom_field_items_retrieve_custom_field_items(customfield_id: str, ids: str | None = None, active: str | None = None, name: str | None = None, modified_before: str | None = None, modified_since: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Custom Field Items.

        API: GET /customfielditems

        Args:
            customfield_id: Required. Id of the custom field whose items you'd like to list.
            ids: Optional. Comma separated list of one or more customfielditem ids you'd like to filter on. Only customfielditems with an id set to one of these values will be returned. If omitted, all customfielditems matching other specified filters are returned.
            active: Optional. 'yes', 'no', or 'both'. Default is 'yes'. If a customfielditem is active, it is available for selection during time entry.
            name: Optional. * will be interpreted as a wild card. Starts matching from the beginning of the string.
            modified_before: Optional. Only customfielditems modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            modified_since: Optional. Only customfielditems modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"customfield_id": customfield_id, "ids": ids, "active": active, "name": name, "modified_before": modified_before, "modified_since": modified_since, "supplemental_data": supplemental_data, "limit": limit, "page": page}
        try:
            result = await client.get("/customfielditems", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_custom_field_items_update_custom_field_items(body: dict) -> str:
        """Update Custom Field Items.

        API: PUT /customfielditems

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.put("/customfielditems", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
