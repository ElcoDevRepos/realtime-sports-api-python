from __future__ import annotations

from typing import Any, Optional


class RealtimeSportsError(Exception):
    """Raised for every failed request: API errors, network failures and timeouts.

    Attributes:
        status: HTTP status code, or ``None`` for network errors and timeouts.
        code: API error code (``MISSING_TOKEN``, ``rate_limit_exceeded``, ...) or
            ``NETWORK_ERROR`` / ``TIMEOUT``.
        message: Human-readable message.
        hint: Optional hint from the API on how to fix the request.
        retry_after: Seconds from the ``Retry-After`` header (429 responses), when present.
        body: Parsed response body, when there was one.
    """

    def __init__(
        self,
        message: str,
        *,
        code: str,
        status: Optional[int] = None,
        hint: Optional[str] = None,
        retry_after: Optional[float] = None,
        body: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = status
        self.hint = hint
        self.retry_after = retry_after
        self.body = body

    @property
    def is_rate_limited(self) -> bool:
        """True for 429 (monthly quota exhausted)."""
        return self.status == 429

    @property
    def is_auth_error(self) -> bool:
        """True for 401/403."""
        return self.status in (401, 403)

    def __repr__(self) -> str:
        return f"RealtimeSportsError(status={self.status!r}, code={self.code!r}, message={self.message!r})"

    def __str__(self) -> str:
        prefix = f"[{self.status} {self.code}] " if self.status else f"[{self.code}] "
        return prefix + self.message + (f" (hint: {self.hint})" if self.hint else "")
