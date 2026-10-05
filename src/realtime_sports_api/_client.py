from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING, Any, Mapping, Optional, Sequence

import httpx

from ._base import (
    DEFAULT_MAX_RETRIES,
    DEFAULT_MAX_RETRY_AFTER,
    DEFAULT_TIMEOUT,
    ApiResponse,
    BaseClient,
    RequestOptions,
)
from ._errors import RealtimeSportsError
from ._operations import (
    _AsyncOperations,
    _AsyncOperationsWithMeta,
    _SyncOperations,
    _SyncOperationsWithMeta,
)

if TYPE_CHECKING:
    from ._stream import AsyncStream, Subscription


class Client(BaseClient, _SyncOperations):
    """Synchronous client.

    Methods return the response ``data``. Use ``client.with_meta.<method>(...)`` to get an
    :class:`ApiResponse` with ``data``, ``meta`` (rate limit, pagination), ``status_code`` and ``headers``.

    >>> client = Client(api_key="...")
    >>> live = client.list_live_events("football", "nfl")
    """

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
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        super().__init__(
            api_key,
            base_url=base_url,
            websocket_auth_url=websocket_auth_url,
            timeout=timeout,
            max_retries=max_retries,
            max_retry_after=max_retry_after,
            use_api_key_header=use_api_key_header,
            headers=headers,
        )
        self._owns_http = http_client is None
        self._http = http_client or httpx.Client()
        self._sleep = time.sleep

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP connection pool (only if the client created it)."""
        if self._owns_http:
            self._http.close()

    @property
    def with_meta(self) -> "_SyncWithMeta":
        """Same methods, returning :class:`ApiResponse` (data + meta + status + headers)."""
        return _SyncWithMeta(self)

    def request(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Mapping[str, Any]] = None,
        body: Any = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Any]:
        """Escape hatch: call any path under the base URL with the same auth and retries."""
        from ._base import NOT_GIVEN

        return self._request(method, path, query=query, body=NOT_GIVEN if body is None else body, request_options=request_options)

    def _request(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> ApiResponse[Any]:
        kwargs, max_retries, timeout = self._prepare(method, path, query, body, request_options)
        attempt = 0
        while True:
            try:
                response = self._http.request(timeout=timeout, **kwargs)
            except httpx.TransportError as exc:
                error = self._network_error(exc, timeout)
                retry, delay = self._retry_decision(method, attempt, error, network=True)
                if not retry or attempt >= max_retries:
                    raise error from exc
            else:
                ok, body_ = self._is_success(response)
                if ok:
                    return self._to_result(response)
                error = self._to_error(response, body_)
                retry, delay = self._retry_decision(method, attempt, error, network=False)
                if not retry or attempt >= max_retries:
                    raise error
            self._sleep(delay)
            attempt += 1

    def _request_data(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:
        return self._request(method, path, query=query, body=body, request_options=request_options).data

    def _request_with_meta(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:
        return self._request(method, path, query=query, body=body, request_options=request_options)


class _SyncWithMeta(_SyncOperationsWithMeta):
    def __init__(self, client: Client) -> None:
        self._client = client
        self._websocket_auth_url = client._websocket_auth_url

    def _request_with_meta(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:
        return self._client._request(method, path, query=query, body=body, request_options=request_options)


class AsyncClient(BaseClient, _AsyncOperations):
    """Asynchronous client with the same methods as :class:`Client` (awaitable).

    >>> async with AsyncClient(api_key="...") as client:
    ...     live = await client.list_live_events("football", "nfl")
    """

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
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        super().__init__(
            api_key,
            base_url=base_url,
            websocket_auth_url=websocket_auth_url,
            timeout=timeout,
            max_retries=max_retries,
            max_retry_after=max_retry_after,
            use_api_key_header=use_api_key_header,
            headers=headers,
        )
        self._owns_http = http_client is None
        self._http = http_client or httpx.AsyncClient()
        self._sleep = asyncio.sleep

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    async def close(self) -> None:
        if self._owns_http:
            await self._http.aclose()

    @property
    def with_meta(self) -> "_AsyncWithMeta":
        """Same methods, returning :class:`ApiResponse` (data + meta + status + headers)."""
        return _AsyncWithMeta(self)

    async def request(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Mapping[str, Any]] = None,
        body: Any = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Any]:
        """Escape hatch: call any path under the base URL with the same auth and retries."""
        from ._base import NOT_GIVEN

        return await self._request(
            method, path, query=query, body=NOT_GIVEN if body is None else body, request_options=request_options
        )

    async def _request(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> ApiResponse[Any]:
        kwargs, max_retries, timeout = self._prepare(method, path, query, body, request_options)
        attempt = 0
        while True:
            try:
                response = await self._http.request(timeout=timeout, **kwargs)
            except httpx.TransportError as exc:
                error = self._network_error(exc, timeout)
                retry, delay = self._retry_decision(method, attempt, error, network=True)
                if not retry or attempt >= max_retries:
                    raise error from exc
            else:
                ok, body_ = self._is_success(response)
                if ok:
                    return self._to_result(response)
                error = self._to_error(response, body_)
                retry, delay = self._retry_decision(method, attempt, error, network=False)
                if not retry or attempt >= max_retries:
                    raise error
            await self._sleep(delay)
            attempt += 1

    async def _request_data(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:
        return (await self._request(method, path, query=query, body=body, request_options=request_options)).data

    async def _request_with_meta(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:
        return await self._request(method, path, query=query, body=body, request_options=request_options)

    def stream(
        self,
        subscriptions: Sequence["Subscription"] = (),
        **kwargs: Any,
    ) -> "AsyncStream":
        """Open a managed WebSocket stream (requires ``pip install realtime-sports-api[stream]``).

        Use as ``async with client.stream([...]) as stream: async for msg in stream: ...``.
        Each delivered event message counts toward your monthly quota.
        """
        from ._stream import AsyncStream

        return AsyncStream(self, subscriptions, **kwargs)


class _AsyncWithMeta(_AsyncOperationsWithMeta):
    def __init__(self, client: AsyncClient) -> None:
        self._client = client
        self._websocket_auth_url = client._websocket_auth_url

    async def _request_with_meta(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:
        return await self._client._request(method, path, query=query, body=body, request_options=request_options)


__all__ = ["Client", "AsyncClient", "RealtimeSportsError"]
