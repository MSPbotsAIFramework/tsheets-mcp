import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_files_delete_files(ids: str | None = None) -> str:
        """Delete Files.

        API: DELETE /files

        Args:
            ids: Optional. Comma separated list of file ids you'd like to delete.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids}
        try:
            result = await client.delete("/files", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_files_download_a_file(id: str) -> str:
        """Download a File.

        API: GET /files/raw

        Args:
            id: Required. Id of the file to download.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"id": id}
        try:
            result = await client.get("/files/raw", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_files_retrieve_files(ids: str | None = None, uploaded_by_user_ids: str | None = None, linked_object_type: str | None = None, object_ids: str | None = None, active: str | None = None, modified_before: str | None = None, modified_since: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Files.

        API: GET /files

        Args:
            ids: Optional. Comma separated list of one or more file ids you'd like to filter on.
            uploaded_by_user_ids: Optional. Comma separated list of one or more user ids you'd like to filter on. Only files uploaded by these users will be returned. If uploaded_by_user_ids is not set, it will default to return files uploaded by the current user making the api request.
            linked_object_type: Optional. Only files linked to this object type are returned. Allowed values: 'timesheet'.
            object_ids: Optional. Comma separated list of one or more linked object ids you'd like to filter on.
            active: Optional. 'yes', 'no', or 'both'. Default is 'yes'.
            modified_before: Optional. Only files modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            modified_since: Optional. Only files modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "uploaded_by_user_ids": uploaded_by_user_ids, "linked_object_type": linked_object_type, "object_ids": object_ids, "active": active, "modified_before": modified_before, "modified_since": modified_since, "supplemental_data": supplemental_data, "limit": limit, "page": page}
        try:
            result = await client.get("/files", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_files_update_files(body: dict) -> str:
        """Update Files.

        API: PUT /files

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.put("/files", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_files_upload_files(body: dict) -> str:
        """Upload Files.

        API: POST /files

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/files", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
