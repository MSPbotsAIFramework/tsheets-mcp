from collections.abc import Callable
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .._json import dump_json_capped
from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN, clamp_limit


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def tsheets_custom_field_item_user_filters_retrieve_user_filters(
        user_id: Annotated[
            str | None, Field(description="Only return filters for this user id.")
        ] = None,
        group_id: Annotated[
            str | None, Field(description="Only return filters for this group id.")
        ] = None,
        include_user_group: Annotated[
            str | None,
            Field(
                description=(
                    "'true' or 'false'. If user_id is set, also return filters for "
                    "that user's group."
                )
            ),
        ] = None,
        modified_before: Annotated[
            str | None,
            Field(description="Only filters modified before this ISO 8601 date/time."),
        ] = None,
        modified_since: Annotated[
            str | None,
            Field(description="Only filters modified since this ISO 8601 date/time."),
        ] = None,
        limit: Annotated[
            int | None, Field(description="Results per page. Default 50, max 200.")
        ] = None,
        page: Annotated[int | None, Field(description="Page number. Default 1.")] = None,
    ) -> str:
        """Retrieve which custom-field-item values a user or group is allowed to pick from."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "user_id": user_id,
            "group_id": group_id,
            "include_user_group": include_user_group,
            "modified_before": modified_before,
            "modified_since": modified_since,
            "limit": clamp_limit(limit),
            "page": page,
        }
        try:
            result = await client.get("/customfielditem_user_filters", params=params)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()
