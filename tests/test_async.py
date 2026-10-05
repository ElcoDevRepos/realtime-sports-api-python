from __future__ import annotations

import httpx
import pytest

from realtime_sports_api import RealtimeSportsError

from .conftest import err, ok

BASE = "https://www.realtimesportsapi.com/api/v1"


async def test_async_data_and_auth(make_async_client):
    client, rec, _ = make_async_client(ok([{"id": "1"}]))
    async with client:
        assert await client.list_live_events("hockey", "nhl", include_odds=False) == [{"id": "1"}]
    req = rec.requests[0]
    assert str(req.url) == f"{BASE}/sports/hockey/leagues/nhl/events/live?includeOdds=false"
    assert req.headers["authorization"] == "Bearer test_key"


async def test_async_with_meta(make_async_client):
    client, _, _ = make_async_client(ok([], {"rateLimit": {"remaining": 5}}))
    res = await client.with_meta.get_season_schedule("football", "college-football", 2026, week=6)
    assert res.rate_limit == {"remaining": 5}
    res2 = await client.with_meta.webhooks.list()
    assert res2.data == []


async def test_async_retries_and_429_cap(make_async_client):
    client, rec, sleeps = make_async_client(err(502, "BAD_GATEWAY"), ok(["ok"]))
    assert await client.list_sports() == ["ok"]
    assert sleeps == [0.375]

    client2, rec2, sleeps2 = make_async_client(err(429, "rate_limit_exceeded", headers={"Retry-After": "3600"}))
    with pytest.raises(RealtimeSportsError) as e:
        await client2.list_sports()
    assert e.value.retry_after == 3600 and len(rec2.requests) == 1 and sleeps2 == []


async def test_async_network_error(make_async_client):
    client, rec, _ = make_async_client(httpx.ConnectError("x"), ok([1]))
    assert await client.list_sports() == [1]
    assert len(rec.requests) == 2


async def test_async_webhooks_namespace(make_async_client):
    client, rec, _ = make_async_client(ok({"id": "w", "secret": "s"}, status=201))
    wh = await client.webhooks.create("https://example.com/h", ["event.live"], frequency="1m")
    assert wh["id"] == "w"
    assert rec.json_body(0) == {"url": "https://example.com/h", "events": ["event.live"], "frequency": "1m"}
