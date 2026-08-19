from collections.abc import Callable
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .._json import dump_json_capped
from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN, clamp_limit

_BODY_DESC = (
    "JSON request payload. TSheets bulk endpoints expect "
    '{"data": [ {...}, ... ]} — see the QuickBooks Time API reference for '
    "exact object fields."
)


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
    async def tsheets_custom_fields_create_custom_fields(
        body: Annotated[dict, Field(description=_BODY_DESC)],
    ) -> str:
        """Create one or more custom fields (org-defined data attached to timesheets/users/jobcodes)."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post("/customfields", params={}, json_body=body)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def tsheets_custom_fields_retrieve_custom_fields(
        ids: Annotated[
            str | None, Field(description="Comma-separated custom field ids to filter on.")
        ] = None,
        active: Annotated[
            str | None, Field(description="'yes', 'no', or 'both'. Default 'yes'.")
        ] = None,
        applies_to: Annotated[
            str | None,
            Field(description="'timesheet', 'user', 'jobcode', or 'all'. Default 'timesheet'."),
        ] = None,
        value_type: Annotated[
            str | None,
            Field(description="'managed-list', 'free-form', or 'both'. Default 'both'."),
        ] = None,
        modified_before: Annotated[
            str | None,
            Field(description="Only fields modified before this ISO 8601 date/time."),
        ] = None,
        modified_since: Annotated[
            str | None,
            Field(description="Only fields modified since this ISO 8601 date/time."),
        ] = None,
        supplemental_data: Annotated[
            str | None, Field(description="'yes' or 'no'. Default 'yes'.")
        ] = None,
        limit: Annotated[
            int | None, Field(description="Results per page. Default 50, max 200.")
        ] = None,
        page: Annotated[int | None, Field(description="Page number. Default 1.")] = None,
    ) -> str:
        """List custom fields defined for this account, optionally filtered."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "ids": ids,
            "active": active,
            "applies_to": applies_to,
            "value_type": value_type,
            "modified_before": modified_before,
            "modified_since": modified_since,
            "supplemental_data": supplemental_data,
            "limit": clamp_limit(limit),
            "page": page,
        }
        try:
            result = await client.get("/customfields", params=params)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True))
    async def tsheets_custom_fields_update_custom_fields(
        body: Annotated[dict, Field(description=_BODY_DESC)],
    ) -> str:
        """Update one or more existing custom fields."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put("/customfields", params={}, json_body=body)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()
