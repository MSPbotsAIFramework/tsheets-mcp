import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_estimate_items_create_estimate_items(body: dict) -> str:
        """Create Estimate Items.

        API: POST /estimate_items

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/estimate_items", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_estimate_items_retrieve_estimate_items(ids: str | None = None, estimate_ids: str | None = None, active: str | None = None, modified_before: str | None = None, modified_since: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Estimate Items.

        API: GET /estimate_items

        Args:
            ids: Optional. Comma-separated list of estimate item ids.
            estimate_ids: Optional. Comma-separated list of estimate ids associated with an estimate item.
            active: Optional. 'yes', 'no', or 'both'. Default is 'yes'.
            modified_before: Optional. Only estimate items modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm)
            modified_since: Optional. Only estimate items modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm)
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "estimate_ids": estimate_ids, "active": active, "modified_before": modified_before, "modified_since": modified_since, "supplemental_data": supplemental_data, "limit": limit, "page": page}
        try:
            result = await client.get("/estimate_items", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_estimate_items_update_estimate_items(body: dict) -> str:
        """Update Estimate Items.

        API: PUT /estimate_items

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.put("/estimate_items", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
