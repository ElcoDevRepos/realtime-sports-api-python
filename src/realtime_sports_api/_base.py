from __future__ import annotations

import email.utils
import json
import os
import random
import time
from dataclasses import dataclass
from typing import Any, Dict, Generic, Mapping, Optional, Tuple, TypeVar, Union
from urllib.parse import quote

import httpx

from ._errors import RealtimeSportsError
from ._version import __version__

from typing import TypedDict

T = TypeVar("T")

DEFAULT_BASE_URL = "https://www.realtimesportsapi.com/api/v1"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 2
DEFAULT_MAX_RETRY_AFTER = 60.0
IDEMPOTENT = frozenset({"GET", "PUT", "DELETE", "HEAD"})


class NotGiven:
    """Sentinel for "argument not passed" (distinct from ``None``, which is sent as JSON null)."""

    _instance: Optional["NotGiven"] = None

    def __new__(cls) -> "NotGiven":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


NOT_GIVEN = NotGiven()


class RequestOptions(TypedDict, total=False):
    """Per-request overrides."""

    timeout: float
    max_retries: int
    headers: Dict[str, str]


@dataclass
class ApiResponse(Generic[T]):
    """Full response returned by ``client.with_meta.<method>(...)``."""

    data: T
    meta: Optional[Dict[str, Any]]
    status_code: int
    headers: httpx.Headers

    @property
    def rate_limit(self) -> Optional[Dict[str, Any]]:
        """``meta.rateLimit`` ({limit, remaining, reset}) when present."""
        return (self.meta or {}).get("rateLimit")


def _p(value: Union[str, int]) -> str:
    """Encode one path segment."""
    if value is None or value == "":
        raise ValueError("path parameters must be non-empty")
    return quote(str(value), safe="")


def parse_retry_after(value: Optional[str], now: Optional[float] = None) -> Optional[float]:
    """Parse a Retry-After header (delta-seconds or HTTP-date) into seconds."""
    if value is None or not value.strip():
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        pass
    try:
        dt = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if dt is None:
        return None
    now = time.time() if now is None else now
    return max(0.0, float(int(dt.timestamp() - now + 0.999)))


def backoff_delay(attempt: int, base: float = 0.5, cap: float = 8.0, rand: float | None = None) -> float:
    """Exponential backoff with jitter: uniform in [ceiling/2, ceiling], ceiling = min(cap, base * 2**attempt)."""
    ceiling = min(cap, base * (2**attempt))
    r = random.random() if rand is None else rand
    return ceiling * (0.5 + r * 0.5)


def clean_query(query: Optional[Mapping[str, Any]]) -> Optional[Dict[str, Any]]:
    if not query:
        return None
    out: Dict[str, Any] = {}
    for k, v in query.items():
        if v is None or isinstance(v, NotGiven):
            continue
        if isinstance(v, bool):
            out[k] = "true" if v else "false"
        else:
            out[k] = v
    return out or None


def clean_body(body: Any) -> Any:
    if isinstance(body, NotGiven):
        return NOT_GIVEN
    if isinstance(body, dict):
        return {k: v for k, v in body.items() if not isinstance(v, NotGiven)}
    return body


class BaseClient:
    """Shared configuration and response handling for the sync and async clients."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        websocket_auth_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        max_retry_after: float = DEFAULT_MAX_RETRY_AFTER,
        use_api_key_header: bool = False,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        api_key = api_key or os.environ.get("REALTIME_SPORTS_API_KEY")
        if not api_key:
            raise RealtimeSportsError(
                "Missing API key. Pass api_key=... or set REALTIME_SPORTS_API_KEY.", code="MISSING_API_KEY"
            )
        self._api_key = api_key
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        if websocket_auth_url:
            self._websocket_auth_url = websocket_auth_url
        else:
            root = self.base_url[:-3] if self.base_url.endswith("/v1") else self.base_url
            self._websocket_auth_url = f"{root}/websocket/auth"
        self.timeout = timeout
        self.max_retries = max(0, max_retries)
        self.max_retry_after = max_retry_after
        self._use_api_key_header = use_api_key_header
        self._extra_headers = dict(headers or {})
        # Overridable for tests.
        self._random: Any = None

    # -- request building ------------------------------------------------------------------
    def _headers(self, extra: Optional[Mapping[str, str]] = None, has_body: bool = False) -> Dict[str, str]:
        h = {"Accept": "application/json", "User-Agent": f"realtime-sports-api-python/{__version__}"}
        h.update(self._extra_headers)
        if self._use_api_key_header:
            h["X-API-Key"] = self._api_key
        else:
            h["Authorization"] = f"Bearer {self._api_key}"
        if has_body:
            h["Content-Type"] = "application/json"
        if extra:
            h.update(extra)
        return h

    def _url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self.base_url}{path}"

    def _prepare(
        self, method: str, path: str, query: Any, body: Any, request_options: Optional[RequestOptions]
    ) -> Tuple[Dict[str, Any], int, float]:
        opts = request_options or {}
        body = clean_body(body)
        has_body = not isinstance(body, NotGiven)
        kwargs: Dict[str, Any] = {
            "method": method,
            "url": self._url(path),
            "params": clean_query(query),
            "headers": self._headers(opts.get("headers"), has_body),
        }
        if has_body:
            kwargs["content"] = json.dumps(body).encode()
        max_retries = max(0, opts.get("max_retries", self.max_retries))
        timeout = opts.get("timeout", self.timeout)
        return kwargs, max_retries, timeout

    # -- response handling -----------------------------------------------------------------
    @staticmethod
    def _parse_body(response: httpx.Response) -> Any:
        if not response.content:
            return None
        try:
            return response.json()
        except ValueError:
            return response.text

    def _to_result(self, response: httpx.Response) -> ApiResponse[Any]:
        body = self._parse_body(response)
        if isinstance(body, dict):
            return ApiResponse(
                data=body.get("data", body),
                meta=body.get("meta"),
                status_code=response.status_code,
                headers=response.headers,
            )
        return ApiResponse(data=body, meta=None, status_code=response.status_code, headers=response.headers)

    def _is_success(self, response: httpx.Response) -> Tuple[bool, Any]:
        body = self._parse_body(response)
        ok = response.is_success and not (isinstance(body, dict) and body.get("success") is False)
        return ok, body

    def _to_error(self, response: httpx.Response, body: Any) -> RealtimeSportsError:
        err: Dict[str, Any] = {}
        if isinstance(body, dict) and isinstance(body.get("error"), dict):
            err = body["error"]
        retry_after = parse_retry_after(response.headers.get("retry-after"))
        if isinstance(err.get("message"), str) and err["message"]:
            message = err["message"]
        elif isinstance(body, str) and 0 < len(body) < 500:
            message = body
        else:
            message = f"HTTP {response.status_code} {response.reason_phrase}".strip()
        fallback = "rate_limit_exceeded" if response.status_code == 429 else f"HTTP_{response.status_code}"
        return RealtimeSportsError(
            message,
            code=str(err["code"]) if isinstance(err.get("code"), str) else fallback,
            status=response.status_code,
            hint=err.get("hint") if isinstance(err.get("hint"), str) else None,
            retry_after=retry_after,
            body=body,
        )

    def _retry_decision(
        self, method: str, attempt: int, error: RealtimeSportsError, network: bool
    ) -> Tuple[bool, float]:
        """Return (should_retry, delay_seconds) for a failed attempt."""
        if error.status == 429:
            ra = error.retry_after
            # Monthly quota exhaustion will not clear in seconds: only wait out short windows.
            return (ra is not None and ra <= self.max_retry_after), (ra or 0.0)
        delay = backoff_delay(attempt, rand=self._random)
        if network:
            return method in IDEMPOTENT, delay
        if error.status is not None and error.status >= 500:
            return method in IDEMPOTENT, delay
        return False, 0.0

    @staticmethod
    def _network_error(exc: Exception, timeout: float) -> RealtimeSportsError:
        if isinstance(exc, httpx.TimeoutException):
            return RealtimeSportsError(f"Request timed out after {timeout} s", code="TIMEOUT")
        return RealtimeSportsError(f"Network error: {exc}", code="NETWORK_ERROR")
