import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_custom_field_item_user_filters_retrieve_user_filters(user_id: str | None = None, group_id: str | None = None, include_user_group: str | None = None, modified_before: str | None = None, modified_since: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve User Filters.

        API: GET /customfielditem_user_filters

        Args:
            user_id: Optional. Limits the returned filters to only those for the specified user_id. You can also include items for this user's group automatically if you include the include_user_group parameter.
            group_id: Optional. Limits the returned filters to only those for the specified group_id.
            include_user_group: Optional. _true_ or _false_. If a user_id is supplied, will return filters for that user's group as well.
            modified_before: Optional. Only customfielditem filters modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            modified_since: Optional. Only customfielditem filters modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"user_id": user_id, "group_id": group_id, "include_user_group": include_user_group, "modified_before": modified_before, "modified_since": modified_since, "limit": limit, "page": page}
        try:
            result = await client.get("/customfielditem_user_filters", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
