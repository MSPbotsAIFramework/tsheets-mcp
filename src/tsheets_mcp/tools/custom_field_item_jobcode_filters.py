import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_custom_field_item_jobcode_filters_retrieve_jobcode_filters(jobcode_ids: str | None = None, modified_before: str | None = None, modified_since: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Jobcode Filters.

        API: GET /customfielditem_jobcode_filters

        Args:
            jobcode_ids: Optional. Comma separated list of one or more jobcode ids you'd like to filter on.
            modified_before: Optional. Only customfielditem filters modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            modified_since: Optional. Only customfielditem filters modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"jobcode_ids": jobcode_ids, "modified_before": modified_before, "modified_since": modified_since, "limit": limit, "page": page}
        try:
            result = await client.get("/customfielditem_jobcode_filters", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
