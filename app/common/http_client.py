from logging import getLogger

import httpx

from app.common.tracing import ctx_trace_id
from app.config import config

logger = getLogger(__name__)


async def async_hook_request_tracing(request):
    trace_id = ctx_trace_id.get(None)
    if trace_id:
        request.headers[config.tracing_header] = trace_id


def hook_request_tracing(request):
    trace_id = ctx_trace_id.get(None)
    if trace_id:
        request.headers[config.tracing_header] = trace_id


# Provides an instacne of httpx.AsyncClient with preconfigured hooks for
# propagating the x-cdp-request-id header to allow requets to be traced across
# service boundaries as well as adding in request/response logging.
def async_client():
    return httpx.AsyncClient(event_hooks={"request": [async_hook_request_tracing]})


def client():
    return httpx.Client(event_hooks={"request": [hook_request_tracing]})
