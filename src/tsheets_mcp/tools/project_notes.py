import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_project_notes_create_project_notes(body: dict) -> str:
        """Create Project Notes.

        API: POST /project_notes

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/project_notes", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_project_notes_retrieve_project_notes(project_id: str, ids: str | None = None, user_ids: str | None = None, active: str | None = None, modified_before: str | None = None, modified_since: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Project Notes.

        API: GET /project_notes

        Args:
            project_id: Required. ID for one project you’d like to filter on. Only notes with a project_id set to this will be returned.
            ids: Optional. Comma separated list of one or more notes ids you would like to filter on. Only notes with an id set to one of these values will be returned. If omitted, all notes matching other specified filters are returned.
            user_ids: Optional. Comma separated list of one or more user ids you would like to filter on. Only notes with a user id set to one of these values will be returned. If omitted, all notes matching other specified filters are returned.
            active: Optional. 'yes', 'no', or 'both'. Default is 'yes'. If a note is active, it is available for selection during time entry.
            modified_before: Optional. Only notes modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm)
            modified_since: Optional. Only notes modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm)
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you would like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"project_id": project_id, "ids": ids, "user_ids": user_ids, "active": active, "modified_before": modified_before, "modified_since": modified_since, "supplemental_data": supplemental_data, "limit": limit, "page": page}
        try:
            result = await client.get("/project_notes", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_project_notes_update_project_notes(body: dict) -> str:
        """Update Project Notes.

        API: PUT /project_notes

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.put("/project_notes", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
