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
    async def tsheets_users_create_users(
        body: Annotated[dict, Field(description=_BODY_DESC)],
    ) -> str:
        """Create one or more users (employees/staff)."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post("/users", params={}, json_body=body)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def tsheets_users_retrieve_users(
        ids: Annotated[
            str | None, Field(description="Comma-separated user ids to filter on.")
        ] = None,
        not_ids: Annotated[
            str | None, Field(description="Comma-separated user ids to exclude.")
        ] = None,
        employee_numbers: Annotated[
            str | None, Field(description="Comma-separated employee numbers to filter on.")
        ] = None,
        usernames: Annotated[
            str | None, Field(description="Comma-separated usernames to filter on.")
        ] = None,
        group_ids: Annotated[
            str | None, Field(description="Comma-separated group ids to filter on.")
        ] = None,
        not_group_ids: Annotated[
            str | None, Field(description="Comma-separated group ids to exclude.")
        ] = None,
        payroll_ids: Annotated[
            str | None, Field(description="Comma-separated payroll ids to filter on.")
        ] = None,
        active: Annotated[
            str | None, Field(description="'yes', 'no', or 'both'. Default 'yes'.")
        ] = None,
        first_name: Annotated[
            str | None, Field(description="First name filter; trailing '*' is a wildcard.")
        ] = None,
        last_name: Annotated[
            str | None, Field(description="Last name filter; trailing '*' is a wildcard.")
        ] = None,
        modified_before: Annotated[
            str | None,
            Field(description="Only users modified before this ISO 8601 date/time."),
        ] = None,
        modified_since: Annotated[
            str | None,
            Field(description="Only users modified since this ISO 8601 date/time."),
        ] = None,
        supplemental_data: Annotated[
            str | None, Field(description="'yes' or 'no'. Default 'yes'.")
        ] = None,
        limit: Annotated[
            int | None, Field(description="Results per page. Default 50, max 200.")
        ] = None,
        page: Annotated[int | None, Field(description="Page number. Default 1.")] = None,
    ) -> str:
        """List users (employees/staff) in the account, optionally filtered."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {
            "ids": ids,
            "not_ids": not_ids,
            "employee_numbers": employee_numbers,
            "usernames": usernames,
            "group_ids": group_ids,
            "not_group_ids": not_group_ids,
            "payroll_ids": payroll_ids,
            "active": active,
            "first_name": first_name,
            "last_name": last_name,
            "modified_before": modified_before,
            "modified_since": modified_since,
            "supplemental_data": supplemental_data,
            "limit": clamp_limit(limit),
            "page": page,
        }
        try:
            result = await client.get("/users", params=params)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True))
    async def tsheets_users_update_users(
        body: Annotated[dict, Field(description=_BODY_DESC)],
    ) -> str:
        """Update one or more existing users."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put("/users", params={}, json_body=body)
            return dump_json_capped(result)
        except TSheetsError as e:
            return e.to_envelope()
