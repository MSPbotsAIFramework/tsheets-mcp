import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_current_user_retrieve_the_current_user() -> str:
        """Retrieve the Current User.

        API: GET /current_user

        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.get("/current_user", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
