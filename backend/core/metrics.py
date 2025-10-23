from __future__ import annotations

import time
from typing import Callable

from fastapi import APIRouter, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "path"],
)


class MetricsMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        method = scope.get("method", "?")
        path = scope.get("path", "?")
        start = time.perf_counter()
        status_code_holder = {"code": 0}

        async def send_wrapper(message):
            if message.get("type") == "http.response.start":
                status_code_holder["code"] = message.get("status", 0)
                try:
                    REQUEST_COUNT.labels(method, path, str(status_code_holder["code"]))  # prime
                except Exception:
                    pass
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            elapsed = time.perf_counter() - start
            try:
                REQUEST_LATENCY.labels(method, path).observe(elapsed)
                REQUEST_COUNT.labels(method, path, str(status_code_holder["code"]))
            except Exception:
                pass


router = APIRouter()


@router.get("/metrics")
async def metrics_endpoint() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
