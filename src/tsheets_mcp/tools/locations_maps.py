import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_locations_maps_retrieve_locations_maps(ids: str | None = None, active: str | None = None, modified_before: str | None = None, modified_since: str | None = None, limit: str | None = None, page: str | None = None, by_jobcode_assignment: str | None = None) -> str:
        """Retrieve Locations Maps.

        API: GET /locations_map

        Args:
            ids: Optional. Comma separated list of one or more locations map ids you'd like to filter on. Only locations maps with an id set to one of these values will be returned. If omitted, all locations maps matching other specified filters are returned.
            active: Optional. 'yes', 'no', or 'both'. Default is 'yes'.
            modified_before: Optional. Only locations maps modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm)
            modified_since: Optional. Only locations maps modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm)
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve.
            by_jobcode_assignment: Optional. true or false. If specified only locations maps mapped to a jobcode the user is assigned to will be returned.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "active": active, "modified_before": modified_before, "modified_since": modified_since, "limit": limit, "page": page, "by_jobcode_assignment": by_jobcode_assignment}
        try:
            result = await client.get("/locations_map", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
