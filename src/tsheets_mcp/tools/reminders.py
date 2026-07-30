import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_reminders_create_reminders(body: dict) -> str:
        """Create Reminders.

        API: POST /reminders

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/reminders", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_reminders_retrieve_reminders(user_ids: str, reminder_types: str | None = None, modified_since: str | None = None, supplemental_data: str | None = None) -> str:
        """Retrieve Reminders.

        API: GET /reminders

        Args:
            user_ids: Required. Comma-separated list of one or more user ids to retrieve reminders for. Include a user_id of _0_ to retrieve company-wide reminders.
            reminder_types: Optional. Comma-separated list of one or more reminder types to retrieve reminders for. Current legal values are 'clock-in' and 'clock-out'. For example, specify 'clock-in,clock-out' to retrieve both clock-in and clock-out reminders.
            modified_since: Optional. Only reminders modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm)
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"user_ids": user_ids, "reminder_types": reminder_types, "modified_since": modified_since, "supplemental_data": supplemental_data}
        try:
            result = await client.get("/reminders", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_reminders_update_reminders(body: dict) -> str:
        """Update Reminders.

        API: PUT /reminders

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.put("/reminders", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
