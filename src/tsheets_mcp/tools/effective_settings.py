import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_effective_settings_retrieve_effective_settings(user_id: str | None = None, modified_before: str | None = None, modified_since: str | None = None) -> str:
        """Retrieve Effective Settings.

        API: GET /effective_settings

        Args:
            user_id: Optional. User id for whom you'd like to retrieve effective settings. If none is specified, the currently logged in user's id will be used. Only effective settings that apply to this user_id will be returned. An admin will see more settings than a regular user will.
            modified_before: Optional. Only sections with settings modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            modified_since: Optional. Only sections with settings modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"user_id": user_id, "modified_before": modified_before, "modified_since": modified_since}
        try:
            result = await client.get("/effective_settings", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
