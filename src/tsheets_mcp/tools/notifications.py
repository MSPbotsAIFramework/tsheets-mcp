import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_notifications_create_notifications(body: dict) -> str:
        """Create Notifications.

        API: POST /notifications

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/notifications", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_notifications_delete_notifications(ids: str) -> str:
        """Delete Notifications.

        API: DELETE /notifications

        Args:
            ids: Required. Comma separated list of notification ids you'd like to delete. Note that notifications are actually deleted, not archived.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids}
        try:
            result = await client.delete("/notifications", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_notifications_retrieve_notifications(ids: str | None = None, delivery_before: str | None = None, delivery_after: str | None = None, user_id: str | None = None, msg_tracking_id: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Notifications.

        API: GET /notifications

        Args:
            ids: Optional. Comma separated list of one or more notification ids you'd like to filter on. Only notifications with an id set to one of these values will be returned.
            delivery_before: Optional. Only notifications with a delivery date/time before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            delivery_after: Optional. Only notifications with a delivery date/time after this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            user_id: Optional. Only notifications linked to this user ID will be returned.
            msg_tracking_id: Optional. Tracking ID string of a notification. Only the notification with this msg_tracking_id will be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "delivery_before": delivery_before, "delivery_after": delivery_after, "user_id": user_id, "msg_tracking_id": msg_tracking_id, "limit": limit, "page": page}
        try:
            result = await client.get("/notifications", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
