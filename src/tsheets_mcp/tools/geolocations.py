import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_geolocations_create_geolocations(body: dict) -> str:
        """Create Geolocations.

        API: POST /geolocations

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/geolocations", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_geolocations_retrieve_geolocations(ids: str | None = None, modified_before: str | None = None, modified_since: str | None = None, user_ids: str | None = None, group_ids: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Geolocations.

        API: GET /geolocations

        Args:
            ids: Optional. Comma separated list of one or more geolocation ids you'd like to filter on. Only geolocations with an id set to one of these values will be returned. [required (unless modified_before or modified_since is set)]
            modified_before: Optional. Only geolocations modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm) [required (unless ids or modified_since is set)]
            modified_since: Optional. Only geolocations modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm) [required unless ids or modified_before is set)]
            user_ids: Optional. A comma-separated list of user ids. Only geolocations linked to these users will be returned.
            group_ids: Optional. A comma-separated list of group ids. Only geolocations linked to users from these groups will be returned.
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "modified_before": modified_before, "modified_since": modified_since, "user_ids": user_ids, "group_ids": group_ids, "supplemental_data": supplemental_data, "limit": limit, "page": page}
        try:
            result = await client.get("/geolocations", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
