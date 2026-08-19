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
    async def tsheets_jobcodes_create_jobcodes(
        body: Annotated[dict, Field(description=_BODY_DESC)],
    ) -> str:
        """Create one or more jobcodes (the jobs/customers/tasks time is tracked against)."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post("/jobcodes", params={}, json_body=body)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def tsheets_jobcodes_retrieve_jobcodes(
        ids: Annotated[
            str | None, Field(description="Comma-separated jobcode ids to filter on.")
        ] = None,
        parent_ids: Annotated[
            str | None,
            Field(
                description=(
                    "Comma-separated parent jobcode ids to filter on. Use '0' for "
                    "top-level jobcodes only, or '-1' (default) for all jobcodes "
                    "regardless of parent — traverse the tree by feeding each "
                    "result's id back in as parent_ids when has_children is 'yes'."
                )
            ),
        ] = None,
        name: Annotated[
            str | None, Field(description="Name filter; trailing '*' is a wildcard.")
        ] = None,
        type: Annotated[
            str | None,
            Field(
                description=(
                    "'regular', 'pto', 'paid_break', 'unpaid_break', or 'all'. "
                    "Default 'regular'."
                )
            ),
        ] = None,
        active: Annotated[
            str | None,
            Field(description="'yes', 'no', or 'both'. Default 'yes'. Inactive jobcodes cannot be selected for new time entries."),
        ] = None,
        customfields: Annotated[
            str | None, Field(description="'true' or 'false'. Include each jobcode's custom fields.")
        ] = None,
        modified_before: Annotated[
            str | None,
            Field(description="Only jobcodes modified before this ISO 8601 date/time."),
        ] = None,
        modified_since: Annotated[
            str | None,
            Field(description="Only jobcodes modified since this ISO 8601 date/time."),
        ] = None,
        supplemental_data: Annotated[
            str | None, Field(description="'yes' or 'no'. Default 'yes'.")
        ] = None,
        limit: Annotated[
            int | None, Field(description="Results per page. Default 50, max 200.")
        ] = None,
        page: Annotated[int | None, Field(description="Page number. Default 1.")] = None,
    ) -> str:
        """List jobcodes (jobs/customers/tasks time is billed against), optionally filtered."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "ids": ids,
            "parent_ids": parent_ids,
            "name": name,
            "type": type,
            "active": active,
            "customfields": customfields,
            "modified_before": modified_before,
            "modified_since": modified_since,
            "supplemental_data": supplemental_data,
            "limit": clamp_limit(limit),
            "page": page,
        }
        try:
            result = await client.get("/jobcodes", params=params)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True))
    async def tsheets_jobcodes_update_jobcodes(
        body: Annotated[dict, Field(description=_BODY_DESC)],
    ) -> str:
        """Update one or more existing jobcodes."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put("/jobcodes", params={}, json_body=body)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()
