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
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
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
