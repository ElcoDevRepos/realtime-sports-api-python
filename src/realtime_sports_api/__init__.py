"""Official Python client for the Realtime Sports API (https://www.realtimesportsapi.com/docs).

>>> from realtime_sports_api import Client
>>> client = Client(api_key="...")
>>> client.list_live_events("football", "nfl")
"""
from ._base import DEFAULT_BASE_URL, NOT_GIVEN, ApiResponse, NotGiven, RequestOptions
from ._client import AsyncClient, Client
from ._errors import RealtimeSportsError
from ._operations import OPERATION_IDS
from ._stream import AsyncStream, StreamMessage, Subscription, SubscriptionFilters
from ._types import *  # noqa: F401,F403
from ._types import __all__ as _types_all
from ._version import __version__

__all__ = [
    "Client",
    "AsyncClient",
    "AsyncStream",
    "ApiResponse",
    "RealtimeSportsError",
    "RequestOptions",
    "Subscription",
    "SubscriptionFilters",
    "StreamMessage",
    "NOT_GIVEN",
    "NotGiven",
    "DEFAULT_BASE_URL",
    "OPERATION_IDS",
    "__version__",
    *_types_all,
]
