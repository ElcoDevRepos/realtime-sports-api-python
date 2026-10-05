from __future__ import annotations

import asyncio
import json
from typing import Any, List, Optional

import pytest

from realtime_sports_api import RealtimeSportsError

from .conftest import err, ok

END = object()


class FakeWS:
    def __init__(self, url: str) -> None:
        self.url = url
        self.sent: List[dict] = []
        self.incoming: "asyncio.Queue[Any]" = asyncio.Queue()
        self.close_code: Optional[int] = None
        self.close_reason = ""

    async def send(self, data: str) -> None:
        self.sent.append(json.loads(data))

    async def close(self) -> None:
        self.server_close(1000)

    # test helpers
    def push(self, msg: Any) -> None:
        self.incoming.put_nowait(json.dumps(msg) if not isinstance(msg, (str, bytes)) else msg)

    def server_close(self, code: int, reason: str = "") -> None:
        self.close_code, self.close_reason = code, reason
        self.incoming.put_nowait(END)

    def __aiter__(self) -> "FakeWS":
        return self

    async def __anext__(self) -> Any:
        item = await self.incoming.get()
        if item is END:
            raise StopAsyncIteration
        return item


class FakeConnector:
    def __init__(self) -> None:
        self.sockets: List[FakeWS] = []
        self.kwargs: List[dict] = []
        self.connected = asyncio.Event()

    def __call__(self, url: str, **kwargs: Any) -> "FakeConnector._CM":
        self.kwargs.append(kwargs)
        return FakeConnector._CM(self, url)

    class _CM:
        def __init__(self, outer: "FakeConnector", url: str) -> None:
            self.outer, self.url = outer, url

        async def __aenter__(self) -> FakeWS:
            ws = FakeWS(self.url)
            self.outer.sockets.append(ws)
            self.outer.connected.set()
            return ws

        async def __aexit__(self, *exc: Any) -> None:
            return None

    async def wait_for(self, n: int) -> FakeWS:
        for _ in range(200):
            if len(self.sockets) >= n:
                # let the stream send its subscribe messages
                await asyncio.sleep(0)
                await asyncio.sleep(0)
                return self.sockets[n - 1]
            await asyncio.sleep(0.001)
        raise AssertionError(f"expected {n} connections, got {len(self.sockets)}")


def token(n: int = 1, expires: int = 3600):
    return ok({"url": "wss://ws.example", "token": f"tok{n}", "expiresIn": expires})


async def _no_sleep(_s: float) -> None:
    await asyncio.sleep(0)


def make_stream(client, subs=(), **kw):
    conn = FakeConnector()
    s = client.stream(list(subs), connect=conn, **kw)
    s._sleep = _no_sleep
    return s, conn


NFL = {"event": "event_score_change", "filters": {"sport": "football", "league": "nfl"}, "frequency": "asap"}


async def test_auth_connect_subscribe_and_yield_events(make_async_client):
    client, rec, _ = make_async_client(token())
    errors: List[RealtimeSportsError] = []
    acks: List[dict] = []
    stream, conn = make_stream(client, [NFL], on_error=errors.append, on_subscribed=acks.append)
    async with stream:
        ws = await conn.wait_for(1)
        assert str(rec.requests[0].url) == "https://www.realtimesportsapi.com/api/websocket/auth"
        assert ws.url == "wss://ws.example?token=tok1"
        assert conn.kwargs[0] == {"ping_interval": 20.0, "ping_timeout": 20.0}
        assert ws.sent == [{"type": "subscribe", "event": "event_score_change", "filters": {"sport": "football", "league": "nfl"}, "frequency": "asap"}]
        ws.push({"type": "pong", "timestamp": "t", "data": {"message": "Connected"}})
        ws.push({"type": "subscribed", "timestamp": "t", "data": {"event": "event_score_change", "warnings": ["w"]}})
        ws.push({"type": "error", "timestamp": "t", "error": {"code": "UNKNOWN_MESSAGE_TYPE", "message": "bad"}})
        ws.push({"type": "quota_exceeded", "timestamp": "t", "data": {"message": "limit"}})
        ws.push("not json")
        ws.push(json.dumps({"type": "event_score_change", "timestamp": "t", "data": {"eventId": "401"}}).encode())
        it = stream.__aiter__()
        msg = await asyncio.wait_for(it.__anext__(), 1)
        assert msg["type"] == "event_score_change" and msg["data"]["eventId"] == "401"
    assert acks == [{"event": "event_score_change", "warnings": ["w"]}]
    assert [e.code for e in errors] == ["UNKNOWN_MESSAGE_TYPE", "quota_exceeded"]
    assert errors[1].status == 429


async def test_reconnect_reuses_token_and_resubscribes(make_async_client):
    client, rec, _ = make_async_client(token(1), token(2))
    stream, conn = make_stream(client, [NFL])
    async with stream:
        ws1 = await conn.wait_for(1)
        final = {"event": "event_final", "filters": {"sport": "football", "league": "nfl"}}
        await stream.subscribe(final)
        assert [m["event"] for m in ws1.sent] == ["event_score_change", "event_final"]
        ws1.server_close(1006, "abnormal")
        ws2 = await conn.wait_for(2)
        assert len(rec.requests) == 1  # token still valid: no re-auth
        assert ws2.url.endswith("token=tok1")
        assert [(m["type"], m["event"]) for m in ws2.sent] == [("subscribe", "event_score_change"), ("subscribe", "event_final")]
        assert stream.reconnects == 1


async def test_1008_forces_reauth(make_async_client):
    client, rec, _ = make_async_client(token(1), token(2))
    stream, conn = make_stream(client)
    async with stream:
        ws1 = await conn.wait_for(1)
        ws1.server_close(1008, "Invalid authentication token")
        ws2 = await conn.wait_for(2)
        assert len(rec.requests) == 2
        assert ws2.url.endswith("token=tok2")


async def test_expiring_token_is_refreshed(make_async_client):
    client, rec, _ = make_async_client(token(1, expires=30), token(2))
    stream, conn = make_stream(client)
    async with stream:
        ws1 = await conn.wait_for(1)
        ws1.server_close(1006)
        ws2 = await conn.wait_for(2)
        assert len(rec.requests) == 2  # expiresIn 30 s is inside the 60 s refresh margin
        assert ws2.url.endswith("token=tok2")


async def test_plan_without_websocket_access_is_fatal(make_async_client):
    client, _, _ = make_async_client(token())
    stream, conn = make_stream(client)
    async with stream:
        ws = await conn.wait_for(1)
        ws.server_close(1008, "WebSocket access requires Starter, Pro, or Enterprise tier")
        with pytest.raises(RealtimeSportsError) as e:
            async for _ in stream:
                pass
        assert e.value.code == "WEBSOCKET_FORBIDDEN"
    assert len(conn.sockets) == 1


async def test_auth_403_is_fatal(make_async_client):
    client, rec, _ = make_async_client(err(403, "SUBSCRIPTION_INACTIVE", "inactive"))
    errors: List[RealtimeSportsError] = []
    stream, conn = make_stream(client, on_error=errors.append)
    with pytest.raises(RealtimeSportsError) as e:
        async for _ in stream:
            pass
    assert e.value.code == "SUBSCRIPTION_INACTIVE"
    assert len(rec.requests) == 1 and conn.sockets == []
    await stream.close()


async def test_auth_5xx_is_retried(make_async_client):
    client, rec, _ = make_async_client(err(500, "X"), token(), max_retries=0)
    stream, conn = make_stream(client)
    async with stream:
        await conn.wait_for(1)
        assert len(rec.requests) == 2


async def test_unsubscribe(make_async_client):
    client, _, _ = make_async_client(token())
    sub = {"event": "event_play", "filters": {"sport": "football", "league": "nfl", "eventId": "401"}}
    stream, conn = make_stream(client, [sub])
    async with stream:
        ws = await conn.wait_for(1)
        await stream.unsubscribe(sub)
        assert ws.sent[-1] == {"type": "unsubscribe", "event": "event_play", "filters": sub["filters"]}
        assert stream.subscriptions == []


async def test_reconnect_disabled_ends_iteration(make_async_client):
    client, _, _ = make_async_client(token())
    stream, conn = make_stream(client, reconnect=False)
    async with stream:
        ws = await conn.wait_for(1)
        ws.push({"type": "event_final", "timestamp": "t", "data": {}})
        ws.server_close(1006)
        got = [m async for m in stream]
        assert [m["type"] for m in got] == ["event_final"]
    assert len(conn.sockets) == 1


async def test_max_reconnect_attempts(make_async_client):
    client, _, _ = make_async_client(token())

    def failing_connect(url: str, **kw: Any):
        raise OSError("connection refused")

    stream = client.stream([], connect=failing_connect, max_reconnect_attempts=2)
    stream._sleep = _no_sleep
    with pytest.raises(RealtimeSportsError) as e:
        async for _ in stream:
            pass
    assert e.value.code == "RECONNECT_FAILED"
    await stream.close()
