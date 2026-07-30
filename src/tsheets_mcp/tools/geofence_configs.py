import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_geofence_configs_retrieve_geofence_configs(ids: str | None = None, type: str | None = None, type_ids: str | None = None, enabled: str | None = None, active: str | None = None, modified_before: str | None = None, modified_since: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None, by_jobcode_assignment: str | None = None) -> str:
        """Retrieve Geofence Configs.

        API: GET /geofence_configs

        Args:
            ids: Optional. Comma separated list of one or more geofence config ids you'd like to filter on. Only geofence configs with an id set to one of these values will be returned. If omitted, all geofence configs matching other specified filters are returned.
            type: Optional. Comma separated list of one or more types. If specified only geofence configs of that type will be returned.
            type_ids: Optional. Comma separated list of one or more type ids you'd like to filter on. Only geofence configs with a type_id set to one of these values will be returned.
            enabled: Optional. _true_ or _false_. If specified only geofence configs with matching enabled values will be returned.
            active: Optional. 'yes', 'no', or 'both'. Default is 'yes'.
            modified_before: Optional. Only geofence configs modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            modified_since: Optional. Only geofence configs modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
            by_jobcode_assignment: Optional. _true_ or _false_. If specified, only geofence configs related to a location that is mapped to a jobcode the user is assigned to will be returned.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "type": type, "type_ids": type_ids, "enabled": enabled, "active": active, "modified_before": modified_before, "modified_since": modified_since, "supplemental_data": supplemental_data, "limit": limit, "page": page, "by_jobcode_assignment": by_jobcode_assignment}
        try:
            result = await client.get("/geofence_configs", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
