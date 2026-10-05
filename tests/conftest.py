from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional, Union

import httpx
import pytest

from realtime_sports_api import AsyncClient, Client

Reply = Union[httpx.Response, Exception, Callable[[httpx.Request], httpx.Response]]


def ok(data: Any, meta: Optional[Dict[str, Any]] = None, status: int = 200) -> httpx.Response:
    body: Dict[str, Any] = {"success": True, "data": data}
    if meta is not None:
        body["meta"] = meta
    return httpx.Response(status, json=body)


def err(status: int, code: str, message: str = "x", hint: Optional[str] = None, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
    e: Dict[str, Any] = {"code": code, "message": message}
    if hint:
        e["hint"] = hint
    return httpx.Response(status, json={"success": False, "error": e}, headers=headers or {})


class Recorder:
    """Replies with queued responses in order; the last one repeats."""

    def __init__(self, *replies: Reply) -> None:
        self.replies: List[Reply] = list(replies)
        self.requests: List[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        r = self.replies.pop(0) if len(self.replies) > 1 else self.replies[0]
        if isinstance(r, Exception):
            raise r
        if callable(r) and not isinstance(r, httpx.Response):
            return r(request)
        return r

    def json_body(self, i: int) -> Any:
        return json.loads(self.requests[i].content)


@pytest.fixture
def make_client():
    clients: List[Client] = []

    def factory(*replies: Reply, **kwargs: Any) -> "tuple[Client, Recorder, list]":
        rec = Recorder(*replies)
        sleeps: List[float] = []
        c = Client(api_key="test_key", http_client=httpx.Client(transport=httpx.MockTransport(rec)), **kwargs)
        c._sleep = sleeps.append  # type: ignore[assignment]
        c._random = 0.5
        clients.append(c)
        return c, rec, sleeps

    yield factory
    for c in clients:
        c._http.close()


@pytest.fixture
def make_async_client():
    def factory(*replies: Reply, **kwargs: Any) -> "tuple[AsyncClient, Recorder, list]":
        rec = Recorder(*replies)
        sleeps: List[float] = []

        async def fake_sleep(s: float) -> None:
            sleeps.append(s)

        c = AsyncClient(api_key="test_key", http_client=httpx.AsyncClient(transport=httpx.MockTransport(rec)), **kwargs)
        c._sleep = fake_sleep  # type: ignore[assignment]
        c._random = 0.5
        return c, rec, sleeps

    return factory
