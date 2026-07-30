import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_jobcodes_create_jobcodes(body: dict) -> str:
        """Create Jobcodes.

        API: POST /jobcodes

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.post("/jobcodes", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_jobcodes_retrieve_jobcodes(ids: str | None = None, parent_ids: str | None = None, name: str | None = None, type: str | None = None, active: str | None = None, customfields: str | None = None, modified_before: str | None = None, modified_since: str | None = None, supplemental_data: str | None = None, limit: str | None = None, page: str | None = None) -> str:
        """Retrieve Jobcodes.

        API: GET /jobcodes

        Args:
            ids: Optional. Comma separated list of one or more jobcode ids you'd like to filter on. Only jobcodes with an id set to one of these values will be returned. If omitted, all jobcodes matching other specified filters are returned.
            parent_ids: Optional. Default is _-1_ (meaning all jobcodes will be returned regardless of parent_id).Comma separated list of one or more jobcode parent_ids you'd like to filter on. Only jobcodes with a parent_id set to one of these values will be returned. Additionally you can use _0_ to get only the top-level jobcodes. Then get the id of any results with has_children=_yes_ and feed that in as the value of parent_ids for your next request to get the 2nd level of jobcodes, and so on, to traverse an entire tree of jobcodes.Use _-1_ to return all jobcodes regardless of parent_id. This is especially useful when combined with the modified_since filter. When parent_ids is _-1_, you'll have the jobcode records needed to trace each result back to it's top level parent in the supplemental_data section of the response.
            name: Optional. * will be interpreted as a wild card. Starts matching from the beginning of the string.
            type: Optional. Indicates jobcode type. One of 'regular', 'pto', 'paid_break', 'unpaid_break', or 'all'.  Default is 'regular'.
            active: Optional. 'yes', 'no', or 'both'. Default is 'yes'. If a jobcode is active, it is available for selection during time entry.
            customfields: Optional. _true_ or _false_. If _true_, custom fields for this jobcode will be returned. If _false_, the customfields object will be omitted.
            modified_before: Optional. Only jobcodes modified before this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            modified_since: Optional. Only jobcodes modified since this date/time will be returned, in ISO 8601 format (YYYY-MM-DDThh:mm:ss±hh:mm).
            supplemental_data: Optional. 'yes' or 'no'. Default is 'yes'. Indicates whether supplemental data should be returned.
            limit: Optional. Represents how many results you'd like to retrieve per request. Default is 200. Max is 200.If present, this value must be: an integer, greater than zero, and not greater than 200.Setting limit less than 1 or greater than 200 will result in an error.
            page: Optional. Represents the page of results you'd like to retrieve. Default is 1.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"ids": ids, "parent_ids": parent_ids, "name": name, "type": type, "active": active, "customfields": customfields, "modified_before": modified_before, "modified_since": modified_since, "supplemental_data": supplemental_data, "limit": limit, "page": page}
        try:
            result = await client.get("/jobcodes", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def tsheets_jobcodes_update_jobcodes(body: dict) -> str:
        """Update Jobcodes.

        API: PUT /jobcodes

        Args:
            body: Required. JSON request payload — TSheets bulk endpoints expect {"data": [ {...}, ... ]}. See the QuickBooks Time API reference for exact object fields.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {}
        try:
            result = await client.put("/jobcodes", params=params, json_body=body)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
