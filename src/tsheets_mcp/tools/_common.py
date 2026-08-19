from .._json import error_envelope

NO_TOKEN = error_envelope(
    "not_configured", "No TSheets access token. Send the X-TSheets-Access-Token header.", False
)

# SOP fallback ceiling (list tools should default low and never exceed this),
# but TSheets' own API documents 200 as its real per-page maximum (and
# default) for every retrieve endpoint here, so 200 is used as the hard cap
# rather than the SOP's own 200 fallback happening to differ — they agree.
DEFAULT_LIMIT = 50
MAX_LIMIT = 200


def clamp_limit(limit: int | None) -> int:
    """Clamp a caller-supplied `limit` to TSheets' own documented bounds.

    Defaults to SOP's recommended 50 (well under TSheets' own default of
    200) when omitted, and clamps to TSheets' documented max of 200 (which
    also happens to be the SOP's hard cap) if the caller asks for more.
    """
    if limit is None:
        return DEFAULT_LIMIT
    if limit < 1:
        return 1
    if limit > MAX_LIMIT:
        return MAX_LIMIT
    return limit
