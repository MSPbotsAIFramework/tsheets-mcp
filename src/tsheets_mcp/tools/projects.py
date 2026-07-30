import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_projects_create_projects(body: dict) -> str:
        """Create Projects.

        API: POST /projects

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/projects", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_projects_retrieve_projects(ids: str | None = None, jobcode_ids: str | None = None, parent_jobcode_id: str | None = None, name: str | None = None, active: str | None = None, by_jobcode_assignment: str | None = None) -> str:
        """Retrieve Projects.

        API: GET /projects

        Args:
            ids: Optional. Comma-separated list of project ids.
            jobcode_ids: Optional. Comma-separated list of jobcode ids associated with a project.
            parent_jobcode_id: Optional. Id of a project jobcode's parent to use for filtering. Only projects whose jobcode has a parent_id set to this value will be returned.
            name: Optional. * will be interpreted as a wild card. Starts matching from the beginning of the string.
            active: Optional. 'yes', 'no', or 'both'. Default is 'yes'.
            by_jobcode_assignment: Optional. true or false. If specified, only projects with a jobcode_id the user is assigned to will be returned.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "jobcode_ids": jobcode_ids, "parent_jobcode_id": parent_jobcode_id, "name": name, "active": active, "by_jobcode_assignment": by_jobcode_assignment}
        try:
            result = await client.get("/projects", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_projects_update_projects(body: dict) -> str:
        """Update Projects.

        API: PUT /projects

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.put("/projects", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
