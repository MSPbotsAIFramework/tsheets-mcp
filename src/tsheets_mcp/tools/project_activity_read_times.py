import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_project_activity_read_times_retrieve_project_activity_read_times(ids: str | None = None, modified_before: str | None = None, modified_since: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Project Activity Read Times.

        API: GET /project_activity_read_times

        Args:
            ids: Optional. Comma separated list of one or more project ids you would like to filter on. Only projects with an id set to one of these values will be returned. If omitted, all project_activity_read_times matching other specified filters are returned.
            modified_before: Optional. Only project_activity_read_times modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm)
            modified_since: Optional. Only project_activity_read_times modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm)
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you would like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "modified_before": modified_before, "modified_since": modified_since, "supplemental_data": supplemental_data, "limit": limit, "page": page}
        try:
            result = await client.get("/project_activity_read_times", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_project_activity_read_times_update_project_activity_read_time(body: dict) -> str:
        """Update Project Activity Read Time.

        API: POST /project_activity_read_times

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/project_activity_read_times", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
