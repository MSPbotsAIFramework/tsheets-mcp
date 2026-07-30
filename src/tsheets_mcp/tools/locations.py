import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_locations_create_locations(body: dict) -> str:
        """Create Locations.

        API: POST /locations

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/locations", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_locations_retrieve_locations(ids: str | None = None, active: str | None = None, geocoding_status: str | None = None, modified_before: str | None = None, modified_since: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None, by_jobcode_assignment: str | None = None) -> str:
        """Retrieve Locations.

        API: GET /locations

        Args:
            ids: Optional. Comma separated list of one or more location ids you'd like to filter on. Only locations with an id set to one of these values will be returned. If omitted, all locations matching other specified filters are returned.
            active: Optional. 'yes', 'no', or 'both'. Default is 'yes'. If a location is active, it is available for selection during time entry.
            geocoding_status: Optional. Comma separated list of one or more of the following values: 'none', 'in_progress', 'retry', 'error', or 'complete'. If omitted, all locations matching other specified filters are returned.
            modified_before: Optional. Only locations modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm)
            modified_since: Optional. Only locations modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm)
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
            by_jobcode_assignment: Optional. true or false. If specified, only locations mapped to a jobcode the user is assigned to will be returned.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "active": active, "geocoding_status": geocoding_status, "modified_before": modified_before, "modified_since": modified_since, "supplemental_data": supplemental_data, "limit": limit, "page": page, "by_jobcode_assignment": by_jobcode_assignment}
        try:
            result = await client.get("/locations", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_locations_update_locations(body: dict) -> str:
        """Update Locations.

        API: PUT /locations

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.put("/locations", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
