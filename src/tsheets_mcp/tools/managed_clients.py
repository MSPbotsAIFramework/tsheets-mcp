import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_managed_clients_retrieve_managed_clients(active: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Managed Clients.

        API: GET /managed_clients

        Args:
            active: Optional. 'yes', 'no', or 'both'. Default is 'yes'.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"active": active, "limit": limit, "page": page}
        try:
            result = await client.get("/managed_clients", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
