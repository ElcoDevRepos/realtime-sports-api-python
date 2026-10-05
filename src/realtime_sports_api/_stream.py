"""Managed WebSocket stream. Requires the optional extra: ``pip install realtime-sports-api[stream]``."""
from __future__ import annotations

import asyncio
import json
import re
import time
from urllib.parse import quote
from typing import TYPE_CHECKING, Any, AsyncIterator, Callable, Dict, List, Optional, Sequence, TypedDict

from ._base import backoff_delay
from ._errors import RealtimeSportsError

if TYPE_CHECKING:
    from ._client import AsyncClient

EVENT_TYPES = (
    "event_score_change",
    "event_live",
    "event_status_change",
    "event_play",
    "event_final",
    "event_odds_change",
)

_TOKEN_REFRESH_MARGIN = 60.0
_FATAL_REASON = re.compile(r"tier|subscription|not found", re.I)


class SubscriptionFilters(TypedDict, total=False):
    sport: str
    league: str
    eventId: str


class Subscription(TypedDict, total=False):
    """``{"event": "event_score_change", "filters": {"sport": "football", "league": "nfl"}, "frequency": "asap"}``"""

    event: str
    filters: SubscriptionFilters
    frequency: str


class StreamMessage(TypedDict, total=False):
    type: str
    timestamp: str
    data: Dict[str, Any]


def _key(sub: Subscription) -> str:
    f = sub.get("filters") or {}
    return json.dumps([sub.get("event"), f.get("sport"), f.get("league"), f.get("eventId")])


def _default_connect() -> Callable[..., Any]:
    try:
        import websockets
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise ImportError(
            "Streaming needs the 'websockets' package: pip install 'realtime-sports-api[stream]'"
        ) from exc
    return websockets.connect


class AsyncStream:
    """Async iterator over WebSocket event messages, with auth, resubscribe and reconnect handled.

    >>> async with client.stream([{"event": "event_score_change",
    ...                            "filters": {"sport": "football", "league": "nfl"}}]) as stream:
    ...     async for msg in stream:
    ...         print(msg["type"], msg["data"].get("name"))

    Each delivered event message counts toward your monthly quota.
    """

    def __init__(
        self,
        client: "AsyncClient",
        subscriptions: Sequence[Subscription] = (),
        *,
        reconnect: bool = True,
        max_reconnect_attempts: Optional[int] = None,
        initial_delay: float = 1.0,
        max_delay: float = 30.0,
        ping_interval: Optional[float] = 20.0,
        ping_timeout: Optional[float] = 20.0,
        include_control: bool = False,
        on_error: Optional[Callable[[RealtimeSportsError], Any]] = None,
        on_subscribed: Optional[Callable[[Dict[str, Any]], Any]] = None,
        connect: Optional[Callable[..., Any]] = None,
    ) -> None:
        self._client = client
        self._subs: Dict[str, Subscription] = {_key(s): s for s in subscriptions}
        self._reconnect = reconnect
        self._max_attempts = max_reconnect_attempts
        self._initial_delay = initial_delay
        self._max_delay = max_delay
        self._ping_interval = ping_interval
        self._ping_timeout = ping_timeout
        self._include_control = include_control
        self._on_error = on_error
        self._on_subscribed = on_subscribed
        self._connect = connect
        self._queue: "asyncio.Queue[Any]" = asyncio.Queue()
        self._task: Optional["asyncio.Task[None]"] = None
        self._ws: Any = None
        self._closed = False
        self._token: Optional[Dict[str, Any]] = None
        self._sleep = asyncio.sleep
        self._random: Optional[float] = None
        self.reconnects = 0

    # -- public API -------------------------------------------------------------------------
    @property
    def subscriptions(self) -> List[Subscription]:
        return list(self._subs.values())

    @property
    def connected(self) -> bool:
        return self._ws is not None

    async def subscribe(self, sub: Subscription) -> None:
        """Add a subscription (sent now if connected, and again after every reconnect)."""
        self._subs[_key(sub)] = sub
        await self._send(self._sub_message("subscribe", sub))

    async def unsubscribe(self, sub: Subscription) -> None:
        self._subs.pop(_key(sub), None)
        await self._send(self._sub_message("unsubscribe", sub))

    def start(self) -> "AsyncStream":
        if self._task is None:
            self._task = asyncio.ensure_future(self._run())
        return self

    async def close(self) -> None:
        self._closed = True
        ws = self._ws
        if ws is not None:
            try:
                await ws.close()
            except Exception:  # pragma: no cover
                pass
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except (asyncio.CancelledError, Exception):
                pass
        self._queue.put_nowait(_END)

    async def __aenter__(self) -> "AsyncStream":
        return self.start()

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    def __aiter__(self) -> AsyncIterator[StreamMessage]:
        self.start()
        return self

    async def __anext__(self) -> StreamMessage:
        item = await self._queue.get()
        if item is _END:
            self._queue.put_nowait(_END)
            raise StopAsyncIteration
        if isinstance(item, BaseException):
            self._queue.put_nowait(_END)
            raise item
        return item

    # -- internals --------------------------------------------------------------------------
    def _sub_message(self, type_: str, sub: Subscription) -> Dict[str, Any]:
        msg: Dict[str, Any] = {"type": type_, "event": sub["event"]}
        if sub.get("filters"):
            msg["filters"] = sub["filters"]
        if type_ == "subscribe" and sub.get("frequency"):
            msg["frequency"] = sub["frequency"]
        return msg

    async def _send(self, msg: Dict[str, Any]) -> None:
        if self._ws is not None:
            await self._ws.send(json.dumps(msg))

    def _emit_error(self, err: RealtimeSportsError) -> None:
        if self._on_error is not None:
            try:
                self._on_error(err)
            except Exception:  # pragma: no cover - user callback
                pass

    async def _get_token(self) -> Dict[str, Any]:
        if self._token and self._token["expires_at"] - _TOKEN_REFRESH_MARGIN > time.time():
            return self._token
        data = await self._client.create_websocket_token()
        if not isinstance(data, dict) or not data.get("url") or not data.get("token"):
            raise RealtimeSportsError("WebSocket auth response missing url/token", code="BAD_RESPONSE")
        self._token = {
            "url": data["url"],
            "token": data["token"],
            "expires_at": time.time() + float(data.get("expiresIn") or 3600),
        }
        return self._token

    def _fail(self, err: BaseException) -> None:
        self._closed = True
        self._queue.put_nowait(err)

    async def _backoff(self, attempts: int) -> bool:
        """Sleep before the next attempt. Returns False when we should give up."""
        if not self._reconnect or self._closed:
            return False
        if self._max_attempts is not None and attempts >= self._max_attempts:
            self._fail(RealtimeSportsError(f"Gave up reconnecting after {attempts} attempts", code="RECONNECT_FAILED"))
            return False
        self.reconnects += 1
        await self._sleep(backoff_delay(attempts, self._initial_delay, self._max_delay, rand=self._random))
        return not self._closed

    def _handle(self, msg: Dict[str, Any]) -> None:
        t = msg.get("type")
        if t == "subscribed" and self._on_subscribed is not None:
            self._on_subscribed(msg.get("data") or {})
        elif t == "error":
            body = msg.get("error") or (msg.get("data") or {}).get("error") or msg.get("data") or {}
            self._emit_error(RealtimeSportsError(body.get("message", "WebSocket error"), code=body.get("code", "WEBSOCKET_ERROR"), body=msg))
        elif t == "quota_exceeded":
            d = msg.get("data") or {}
            self._emit_error(RealtimeSportsError(d.get("message", "Monthly quota exhausted"), code="quota_exceeded", status=429, body=msg))
        if isinstance(t, str) and t.startswith("event_"):
            self._queue.put_nowait(msg)
        elif self._include_control:
            self._queue.put_nowait(msg)

    async def _run(self) -> None:
        connect = self._connect or _default_connect()
        attempts = 0
        while not self._closed:
            try:
                tok = await self._get_token()
            except RealtimeSportsError as err:
                self._emit_error(err)
                if err.status in (401, 403, 429):
                    self._fail(err)  # bad key, plan without WebSocket access, or exhausted quota
                    return
                if not await self._backoff(attempts):
                    break
                attempts += 1
                continue

            sep = "&" if "?" in tok["url"] else "?"
            url = f"{tok['url']}{sep}token={quote(tok['token'], safe='')}"
            code: Optional[int] = None
            reason = ""
            try:
                async with connect(url, ping_interval=self._ping_interval, ping_timeout=self._ping_timeout) as ws:
                    self._ws = ws
                    for sub in list(self._subs.values()):
                        await ws.send(json.dumps(self._sub_message("subscribe", sub)))
                    try:
                        async for raw in ws:
                            if isinstance(raw, (bytes, bytearray)):
                                raw = raw.decode("utf-8", "replace")
                            try:
                                msg = json.loads(raw)
                            except ValueError:
                                continue
                            attempts = 0  # only authenticated clients get messages
                            if isinstance(msg, dict):
                                self._handle(msg)
                    finally:
                        code = getattr(ws, "close_code", None)
                        reason = getattr(ws, "close_reason", "") or ""
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # connection refused, DNS, ConnectionClosedError, ...
                rcvd = getattr(exc, "rcvd", None)
                if rcvd is not None:
                    code, reason = getattr(rcvd, "code", code), getattr(rcvd, "reason", reason) or reason
                if code is None:
                    self._emit_error(RealtimeSportsError(f"WebSocket connection failed: {exc}", code="NETWORK_ERROR"))
            finally:
                self._ws = None

            if self._closed:
                break
            if code == 1008:  # policy violation: bad/expired token, or plan without WebSocket access
                self._token = None
                if _FATAL_REASON.search(reason or ""):
                    self._fail(RealtimeSportsError(f"WebSocket rejected: {reason}", code="WEBSOCKET_FORBIDDEN", status=403))
                    return
            if not await self._backoff(attempts):
                break
            attempts += 1
        if not self._closed:
            self._queue.put_nowait(_END)


class _EndMarker:
    pass


_END = _EndMarker()
