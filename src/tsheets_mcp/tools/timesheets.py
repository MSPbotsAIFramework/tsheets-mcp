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
    async def tsheets_timesheets_create_timesheets(
        body: Annotated[dict, Field(description=_BODY_DESC)],
    ) -> str:
        """Create one or more timesheet entries (clock-in/out or manual time)."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post("/timesheets", params={}, json_body=body)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True))
    async def tsheets_timesheets_delete_timesheets(
        ids: Annotated[
            str | None,
            Field(description="Comma-separated timesheet ids to permanently delete."),
        ] = None,
    ) -> str:
        """Permanently delete specific timesheets by id (not archived — irreversible)."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids}
        try:
            result = await client.delete("/timesheets", params=params)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def tsheets_timesheets_retrieve_timesheets(
        ids: Annotated[
            str | None,
            Field(description="Comma-separated timesheet ids to filter on."),
        ] = None,
        start_date: Annotated[
            str | None, Field(description="YYYY-MM-DD; returns timesheets on or after this date.")
        ] = None,
        end_date: Annotated[
            str | None, Field(description="YYYY-MM-DD; returns timesheets on or before this date.")
        ] = None,
        jobcode_ids: Annotated[
            str | None, Field(description="Comma-separated jobcode ids (includes their children).")
        ] = None,
        payroll_ids: Annotated[
            str | None, Field(description="Comma-separated payroll ids to filter by user.")
        ] = None,
        user_ids: Annotated[
            str | None, Field(description="Comma-separated user ids to filter on.")
        ] = None,
        group_ids: Annotated[
            str | None, Field(description="Comma-separated group ids to filter on.")
        ] = None,
        on_the_clock: Annotated[
            str | None,
            Field(description="'yes', 'no', or 'both'. Default 'no'. 'yes' means still clocked in."),
        ] = None,
        jobcode_type: Annotated[
            str | None,
            Field(
                description="'regular', 'pto', 'paid_break', 'unpaid_break', or 'all'. Default 'all'."
            ),
        ] = None,
        modified_before: Annotated[
            str | None,
            Field(description="Only timesheets modified before this ISO 8601 date/time."),
        ] = None,
        modified_since: Annotated[
            str | None,
            Field(description="Only timesheets modified since this ISO 8601 date/time."),
        ] = None,
        supplemental_data: Annotated[
            str | None, Field(description="'yes' or 'no'. Default 'yes'.")
        ] = None,
        limit: Annotated[
            int | None, Field(description="Results per page. Default 50, max 200.")
        ] = None,
        page: Annotated[int | None, Field(description="Page number. Default 1.")] = None,
    ) -> str:
        """List timesheets, optionally filtered by user/jobcode/date range.

        At least one of ids, start_date, modified_before, or modified_since
        must be provided — the upstream API rejects a call with none of them.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "ids": ids,
            "start_date": start_date,
            "end_date": end_date,
            "jobcode_ids": jobcode_ids,
            "payroll_ids": payroll_ids,
            "user_ids": user_ids,
            "group_ids": group_ids,
            "on_the_clock": on_the_clock,
            "jobcode_type": jobcode_type,
            "modified_before": modified_before,
            "modified_since": modified_since,
            "supplemental_data": supplemental_data,
            "limit": clamp_limit(limit),
            "page": page,
        }
        try:
            result = await client.get("/timesheets", params=params)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True))
    async def tsheets_timesheets_update_timesheets(
        body: Annotated[dict, Field(description=_BODY_DESC)],
    ) -> str:
        """Update one or more existing timesheets."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put("/timesheets", params={}, json_body=body)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()
