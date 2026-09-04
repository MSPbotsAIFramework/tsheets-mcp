import contextvars
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from .api_client import TSheetsClient
from .config import Settings

# Per-request credential isolation via contextvars.
# GatewayTokenMiddleware sets this before the MCP handler runs.
# Python asyncio copies context per task, so concurrent SSE connections are isolated.
_gateway_creds_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "tsheets_gateway_creds", default=None
)

_INSTRUCTIONS = (
    "TSheets (QuickBooks Time) is Intuit's time-tracking, scheduling, and PTO "
    "platform: it tracks employee hours against jobs/customers for payroll "
    "and billing. Core concepts and how the 6 tool groups relate: users "
    "(employees/staff) log time as timesheets (clock-in/out or manual "
    "entries) against jobcodes (the jobs/customers/tasks time is billed to, "
    "arranged in a parent/child tree). custom_fields let an org attach extra "
    "structured data (e.g. a customer PO or ticket number) to timesheets, "
    "users, or jobcodes; custom_field_item_user_filters restrict which of "
    "those field values a given user/group may pick from. "
    "effective_settings resolves the actual account/timesheet/approval "
    "configuration that applies to a specific user, since settings can be "
    "overridden at multiple levels. "
    "Typical flow: retrieve users/jobcodes to identify who/what time is "
    "tracked against, then retrieve or create timesheets filtered by "
    "user_ids/jobcode_ids/date range for reporting or entry. Check "
    "custom_fields and custom_field_item_user_filters when a workflow needs "
    "custom tracking fields, and effective_settings to confirm what an org "
    "or user is configured to allow before attempting an operation."
)


def get_client_from_context(settings: Settings) -> TSheetsClient | None:
    """Resolve the active TSheetsClient for the current request context."""
    access_token = _gateway_creds_var.get()
    if not access_token:
        return None
    return TSheetsClient(access_token, settings.tsheets_base_url)


class GatewayTokenMiddleware:
    """ASGI middleware.

    Reads X-TSheets-Access-Token (required) from request headers and stores
    it in the contextvar. Returns 401 if the header is missing on /mcp
    requests.
    """

    def __init__(self, app: ASGIApp, settings: Settings):
        self.app = app
        self.settings = settings

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        if not path.startswith("/mcp"):
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        access_token = request.headers.get("x-tsheets-access-token")
        if not access_token:
            response = JSONResponse(
                {
                    "error": "Missing credentials",
                    "message": "This server requires the X-TSheets-Access-Token header",
                    "required_headers": ["X-TSheets-Access-Token"],
                    "optional_headers": [],
                },
                status_code=401,
            )
            await response(scope, receive, send)
            return

        ctx_token = _gateway_creds_var.set(access_token)
        try:
            await self.app(scope, receive, send)
        finally:
            _gateway_creds_var.reset(ctx_token)


def create_mcp_server(settings: Settings) -> FastMCP:
    """Build the FastMCP server instance and register all TSheets tools."""
    # DNS-rebinding protection is a browser-oriented safeguard that rejects
    # non-localhost Host headers with 421. Disable it so the server works
    # correctly behind a reverse proxy or docker network.
    mcp = FastMCP(
        name="tsheets-mcp",
        instructions=_INSTRUCTIONS,
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
        stateless_http=True,
        json_response=True,
    )

    client_factory: Callable[[], TSheetsClient | None] = lambda: get_client_from_context(settings)

    from .tools import (
        custom_field_item_user_filters,
        custom_fields,
        effective_settings,
        jobcodes,
        timesheets,
        users,
    )

    for mod in (
        custom_field_item_user_filters,
        custom_fields,
        effective_settings,
        jobcodes,
        timesheets,
        users,
    ):
        mod.register(mcp, client_factory)

    return mcp
