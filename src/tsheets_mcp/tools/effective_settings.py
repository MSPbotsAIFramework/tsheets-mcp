from collections.abc import Callable
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .._json import dump_json_capped
from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def tsheets_effective_settings_retrieve_effective_settings(
        user_id: Annotated[
            str | None,
            Field(
                description=(
                    "User id to resolve settings for. Defaults to the "
                    "currently authenticated user; an admin sees more "
                    "settings than a regular user."
                )
            ),
        ] = None,
        modified_before: Annotated[
            str | None,
            Field(description="Only sections modified before this ISO 8601 date/time."),
        ] = None,
        modified_since: Annotated[
            str | None,
            Field(description="Only sections modified since this ISO 8601 date/time."),
        ] = None,
    ) -> str:
        """Get the account/timesheet/approval settings that actually apply to a user.

        Settings can be overridden at multiple levels (account, group, user);
        this returns the final resolved values, not the raw override chain.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "user_id": user_id,
            "modified_before": modified_before,
            "modified_since": modified_since,
        }
        try:
            result = await client.get("/effective_settings", params=params)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()
