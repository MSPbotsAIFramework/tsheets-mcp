"""tools/list snapshot + error-envelope mapping tests.

No network calls: tool enumeration goes through FastMCP's in-process
list_tools(), and the error-code mapping is tested directly against
TSheetsError, independent of any real HTTP request.
"""

import pytest

from tsheets_mcp.api_client import TSheetsError
from tsheets_mcp.config import Settings
from tsheets_mcp.server import create_mcp_server

# tool name -> (required params, expected readOnlyHint)
EXPECTED_TOOLS = {
    "tsheets_custom_field_item_user_filters_retrieve_user_filters": (set(), True),
    "tsheets_custom_fields_create_custom_fields": ({"body"}, False),
    "tsheets_custom_fields_retrieve_custom_fields": (set(), True),
    "tsheets_custom_fields_update_custom_fields": ({"body"}, False),
    "tsheets_effective_settings_retrieve_effective_settings": (set(), True),
    "tsheets_jobcodes_create_jobcodes": ({"body"}, False),
    "tsheets_jobcodes_retrieve_jobcodes": (set(), True),
    "tsheets_jobcodes_update_jobcodes": ({"body"}, False),
    "tsheets_timesheets_create_timesheets": ({"body"}, False),
    "tsheets_timesheets_delete_timesheets": (set(), False),
    "tsheets_timesheets_retrieve_timesheets": (set(), True),
    "tsheets_timesheets_update_timesheets": ({"body"}, False),
    "tsheets_users_create_users": ({"body"}, False),
    "tsheets_users_retrieve_users": (set(), True),
    "tsheets_users_update_users": ({"body"}, False),
}


@pytest.mark.asyncio
async def test_tools_list_snapshot():
    mcp = create_mcp_server(Settings())
    tools = await mcp.list_tools()
    names = {t.name for t in tools}
    assert names == set(EXPECTED_TOOLS), f"unexpected tool set: {names}"

    by_name = {t.name: t for t in tools}
    for name, (expected_required, expected_read_only) in EXPECTED_TOOLS.items():
        tool = by_name[name]
        required = set(tool.inputSchema.get("required", []))
        assert required == expected_required, f"{name}: required={required}"
        assert tool.annotations is not None
        assert tool.annotations.readOnlyHint is expected_read_only, (
            f"{name}: readOnlyHint={tool.annotations.readOnlyHint}"
        )
        assert len(tool.description or "") <= 500, f"{name}: description too long"
        first_line = (tool.description or "").strip().splitlines()[0]
        assert len(first_line) <= 100, f"{name}: first line too long: {first_line!r}"
        assert "API:" not in (tool.description or ""), (
            f"{name}: description leaks an implementation detail line: {tool.description!r}"
        )


@pytest.mark.asyncio
async def test_destructive_delete_tool_is_flagged():
    mcp = create_mcp_server(Settings())
    tools = await mcp.list_tools()
    by_name = {t.name: t for t in tools}
    delete_tool = by_name["tsheets_timesheets_delete_timesheets"]
    assert delete_tool.annotations.destructiveHint is True


@pytest.mark.asyncio
async def test_service_instructions_present_and_bounded():
    mcp = create_mcp_server(Settings())
    assert mcp.instructions
    assert len(mcp.instructions) <= 1500


@pytest.mark.parametrize(
    "status_code,expected_code,expected_retryable",
    [
        (0, "upstream_error", True),
        (400, "invalid_argument", False),
        (401, "unauthorized", False),
        (403, "unauthorized", False),
        (404, "not_found", False),
        (422, "invalid_argument", False),
        (429, "rate_limited", True),
        (500, "upstream_error", True),
        (503, "upstream_error", True),
    ],
)
def test_error_envelope_mapping(status_code, expected_code, expected_retryable):
    import json

    err = TSheetsError(status_code, "boom")
    envelope = json.loads(err.to_envelope())
    assert envelope["error"]["code"] == expected_code
    assert envelope["error"]["retryable"] is expected_retryable
    assert envelope["error"]["message"] == "boom"


@pytest.mark.parametrize(
    "given,expected",
    [
        (None, 50),
        (1, 1),
        (0, 1),
        (-5, 1),
        (200, 200),
        (500, 200),
    ],
)
def test_clamp_limit(given, expected):
    from tsheets_mcp.tools._common import clamp_limit

    assert clamp_limit(given) == expected
