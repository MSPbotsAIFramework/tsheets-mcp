import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import TSheetsClient, TSheetsError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], TSheetsClient | None]) -> None:

    @mcp.tool()
    async def tsheets_last_modified_retrieve_last_modified_timestamps(endpoints: str | None = None) -> str:
        """Retrieve Last Modified Timestamps.

        API: GET /last_modified_timestamps

        Args:
            endpoints: Optional. Comma separated list of one or more endpoints. You can specify any endpoint - see each respective endpoint for the endpoint 'name' that you can use in this list. E.g. if you wanted to only check for changed timesheets and jobcodes, you'd specify _'timesheets,timesheets_deleted,jobcodes'_ as the value of this filter.If a list of endpoints is not specified, then the following list is returned by default.:current_usercustomfieldscustomfielditemseffective_settingsgeolocationsjobcodesjobcode_assignmentstimesheetstimesheets_deletedusersreminderslocationsgeofence_configs
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"endpoints": endpoints}
        try:
            result = await client.get("/last_modified_timestamps", params=params)
            return json.dumps(result, indent=2, default=str)
        except TSheetsError as e:
            return f"Error: {e}"
