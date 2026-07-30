import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_project_activities_retrieve_project_activity_objects(project_id: str | None = None, ids: str | None = None, activity_types: str | None = None, modified_before: str | None = None, modified_since: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None, max_id: str | None = None) -> str:
        """Retrieve Project Activity objects.

        API: GET /project_activities

        Args:
            project_id: Optional. ID for one project you’d like to filter on. Only project_activity objects with a project_id set to this will be returned. [required (unless ids is set)]
            ids: Optional. Comma separated list of one or more project_activity ids you would like to filter on. Only project_activity objects with an id set to one of these values will be returned. If omitted, all project_activity records matching other specified filters are returned. [required (unless project_id is set)]
            activity_types: Optional. Comma separated list of one or more activity types you would like to filter on. Only  with a name set to one of these values will be returned.  If omitted, all project_activity objects matching other specified filters are returned.
            modified_before: Optional. Only project activities modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm)
            modified_since: Optional. Only project activities modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm)
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you would like to retrieve. Default is 1.
            max_id: Optional. Only project activities with an ID less than or equal to this will be returned.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"project_id": project_id, "ids": ids, "activity_types": activity_types, "modified_before": modified_before, "modified_since": modified_since, "supplemental_data": supplemental_data, "limit": limit, "page": page, "max_id": max_id}
        try:
            result = await client.get("/project_activities", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
