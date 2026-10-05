from __future__ import annotations

import httpx
import pytest

from realtime_sports_api import OPERATION_IDS, Client, RealtimeSportsError
from realtime_sports_api._base import backoff_delay, parse_retry_after

from .conftest import err, ok

BASE = "https://www.realtimesportsapi.com/api/v1"


def snake(name: str) -> str:
    import re

    name = name.replace("WebSocket", "Websocket")
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", name).lower()


# ------------------------------------------------------------------ auth & request building


def test_bearer_auth_and_data(make_client):
    client, rec, _ = make_client(ok([{"slug": "football"}]))
    assert client.list_sports() == [{"slug": "football"}]
    req = rec.requests[0]
    assert str(req.url) == f"{BASE}/sports"
    assert req.headers["authorization"] == "Bearer test_key"
    assert "x-api-key" not in req.headers
    assert req.method == "GET"
    assert req.headers["user-agent"].startswith("realtime-sports-api-python/")


def test_x_api_key_header(make_client):
    client, rec, _ = make_client(ok([]), use_api_key_header=True)
    client.list_sports()
    assert rec.requests[0].headers["x-api-key"] == "test_key"
    assert "authorization" not in rec.requests[0].headers


def test_missing_key(monkeypatch):
    monkeypatch.delenv("REALTIME_SPORTS_API_KEY", raising=False)
    with pytest.raises(RealtimeSportsError) as e:
        Client()
    assert e.value.code == "MISSING_API_KEY"


def test_env_key(monkeypatch):
    monkeypatch.setenv("REALTIME_SPORTS_API_KEY", "env_key")
    seen = []

    def handler(req: httpx.Request) -> httpx.Response:
        seen.append(req)
        return ok([])

    with Client(http_client=httpx.Client(transport=httpx.MockTransport(handler))) as c:
        c.list_sports()
    assert seen[0].headers["authorization"] == "Bearer env_key"


def test_query_params(make_client):
    client, rec, _ = make_client(ok([]))
    client.list_live_events("football", "nfl", include_odds=True)
    assert str(rec.requests[0].url) == f"{BASE}/sports/football/leagues/nfl/events/live?includeOdds=true"
    client.get_season_schedule("football", "nfl", 2026, week=5, season_type=2)
    assert str(rec.requests[1].url) == f"{BASE}/sports/football/leagues/nfl/seasons/2026/schedule?week=5&seasonType=2"
    client.list_plays("football", "nfl", "401", page=2, enrich=False)
    assert str(rec.requests[2].url) == f"{BASE}/sports/football/leagues/nfl/events/401/plays?page=2&enrich=false"
    client.get_news("football", "nfl", from_="2026-09-01", team="12")
    assert rec.requests[3].url.params["from"] == "2026-09-01"
    assert rec.requests[3].url.params["team"] == "12"
    assert "limit" not in rec.requests[3].url.params


def test_required_query_params_are_positional(make_client):
    client, rec, _ = make_client(ok([]))
    client.search_athletes("basketball", "nba", "le bron", limit=5)
    assert rec.requests[0].url.params["query"] == "le bron"
    assert rec.requests[0].url.params["limit"] == "5"
    client.get_athlete_game_log("football", "nfl", "3139477", 2025, season_type=2)
    assert rec.requests[1].url.params["season"] == "2025"


def test_path_encoding(make_client):
    client, rec, _ = make_client(ok([]))
    client.list_live_events("soccer", "eng.1")
    assert rec.requests[0].url.raw_path == b"/api/v1/sports/soccer/leagues/eng.1/events/live"
    client.get_team("football", "nfl", "a/b c")
    assert rec.requests[1].url.raw_path == b"/api/v1/sports/football/leagues/nfl/teams/a%2Fb%20c"
    with pytest.raises(ValueError):
        client.get_event("football", "nfl", "")


def test_custom_base_url(make_client):
    client, rec, _ = make_client(ok([]), base_url="http://localhost:3000/api/v1/")
    client.list_sports()
    assert str(rec.requests[0].url) == "http://localhost:3000/api/v1/sports"
    assert client._websocket_auth_url == "http://localhost:3000/api/websocket/auth"


def test_webhook_bodies(make_client):
    client, rec, _ = make_client(ok({"id": "wh_1", "secret": "s"}, status=201))
    wh = client.webhooks.create("https://example.com/h", ["event.final"], leagues=["nfl"])
    assert wh["id"] == "wh_1"
    assert rec.requests[0].method == "POST"
    assert rec.requests[0].headers["content-type"] == "application/json"
    assert rec.json_body(0) == {"url": "https://example.com/h", "events": ["event.final"], "leagues": ["nfl"]}

    client.update_webhook("wh_1", active=False)
    assert rec.requests[1].method == "PATCH"
    assert str(rec.requests[1].url) == f"{BASE}/webhooks/wh_1"
    assert rec.json_body(1) == {"active": False}

    client.webhooks.update("wh_1", leagues=None)  # None is sent as JSON null (= all leagues)
    assert rec.json_body(2) == {"leagues": None}

    client.webhooks.test("wh_1", event_type="event.score_change")
    assert rec.json_body(3) == {"eventType": "event.score_change"}
    client.webhooks.test("wh_1")
    assert rec.json_body(4) == {}

    client.webhooks.deliveries("wh_1", limit=10)
    assert str(rec.requests[5].url) == f"{BASE}/webhooks/wh_1/deliveries?limit=10"
    client.webhooks.delete("wh_1")
    assert rec.requests[6].method == "DELETE"
    client.webhooks.rotate_secret("wh_1")
    assert rec.requests[7].method == "POST" and rec.requests[7].url.path.endswith("/secret")


def test_websocket_token_url(make_client):
    client, rec, _ = make_client(ok({"url": "wss://x", "token": "t", "expiresIn": 3600}))
    assert client.create_websocket_token()["token"] == "t"
    assert str(rec.requests[0].url) == "https://www.realtimesportsapi.com/api/websocket/auth"
    assert rec.requests[0].method == "POST"


def test_with_meta(make_client):
    meta = {"rateLimit": {"limit": 10000, "remaining": 9876, "reset": 1767225600000}}
    client, _, _ = make_client(ok([{"id": "1"}], meta))
    res = client.with_meta.list_live_events("basketball", "nba")
    assert res.data == [{"id": "1"}]
    assert res.meta == meta
    assert res.rate_limit["remaining"] == 9876
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/json"
    res2 = client.with_meta.webhooks.list()
    assert res2.status_code == 200


def test_every_operation_has_a_method():
    c = Client(api_key="k")
    missing = [op for op in OPERATION_IDS if not callable(getattr(c, snake(op), None))]
    assert missing == []
    assert len(OPERATION_IDS) >= 50
    meta_missing = [op for op in OPERATION_IDS if not callable(getattr(c.with_meta, snake(op), None))]
    assert meta_missing == []
    for alias in ["list", "create", "get", "update", "delete", "get_secret", "rotate_secret", "test", "deliveries"]:
        assert callable(getattr(c.webhooks, alias))
    c.close()


# ------------------------------------------------------------------ errors


def test_error_mapping(make_client):
    client, rec, sleeps = make_client(err(401, "MISSING_TOKEN", "Authorization required", hint="Use Bearer"))
    with pytest.raises(RealtimeSportsError) as e:
        client.list_sports()
    assert e.value.status == 401
    assert e.value.code == "MISSING_TOKEN"
    assert e.value.message == "Authorization required"
    assert e.value.hint == "Use Bearer"
    assert e.value.is_auth_error
    assert "MISSING_TOKEN" in str(e.value)
    assert len(rec.requests) == 1 and sleeps == []


def test_success_false_on_200(make_client):
    client, _, _ = make_client(err(200, "BAD", "bad"))
    with pytest.raises(RealtimeSportsError) as e:
        client.list_sports()
    assert e.value.code == "BAD"


def test_non_json_error(make_client):
    client, _, _ = make_client(httpx.Response(404, text="Not Found"))
    with pytest.raises(RealtimeSportsError) as e:
        client.get_event("football", "nfl", "1")
    assert e.value.status == 404 and e.value.code == "HTTP_404" and e.value.message == "Not Found"


def test_4xx_not_retried(make_client):
    client, rec, _ = make_client(err(404, "NOT_FOUND"))
    with pytest.raises(RealtimeSportsError):
        client.get_team("football", "nfl", "999")
    assert len(rec.requests) == 1


# ------------------------------------------------------------------ retries


def test_retry_5xx_then_success(make_client):
    client, rec, sleeps = make_client(err(500, "INTERNAL"), httpx.Response(503), ok(["ok"]))
    assert client.list_sports() == ["ok"]
    assert len(rec.requests) == 3
    assert sleeps == [0.375, 0.75]


def test_retry_exhausted(make_client):
    client, rec, sleeps = make_client(err(500, "INTERNAL", "boom"), max_retries=3)
    with pytest.raises(RealtimeSportsError) as e:
        client.list_sports()
    assert e.value.status == 500 and e.value.code == "INTERNAL"
    assert len(rec.requests) == 4 and len(sleeps) == 3


def test_per_request_max_retries(make_client):
    client, rec, _ = make_client(err(500, "INTERNAL"))
    with pytest.raises(RealtimeSportsError):
        client.list_sports(request_options={"max_retries": 0})
    assert len(rec.requests) == 1


def test_post_patch_not_retried_on_5xx(make_client):
    client, rec, _ = make_client(err(500, "INTERNAL"))
    with pytest.raises(RealtimeSportsError):
        client.create_webhook("https://x.test", ["event.final"])
    with pytest.raises(RealtimeSportsError):
        client.update_webhook("w", active=True)
    assert len(rec.requests) == 2


def test_network_error_retried(make_client):
    client, rec, _ = make_client(httpx.ConnectError("boom"), ok([1]))
    assert client.list_sports() == [1]
    assert len(rec.requests) == 2


def test_network_error_exhausted(make_client):
    client, _, _ = make_client(httpx.ConnectError("boom"), max_retries=1)
    with pytest.raises(RealtimeSportsError) as e:
        client.list_sports()
    assert e.value.code == "NETWORK_ERROR" and e.value.status is None


def test_timeout(make_client):
    client, _, _ = make_client(httpx.ReadTimeout("slow"), max_retries=0)
    with pytest.raises(RealtimeSportsError) as e:
        client.list_sports()
    assert e.value.code == "TIMEOUT"


def test_429_short_retry_after_is_waited_out(make_client):
    client, rec, sleeps = make_client(err(429, "rate_limit_exceeded", headers={"Retry-After": "2"}), ok(["after"]))
    assert client.list_sports() == ["after"]
    assert len(rec.requests) == 2
    assert sleeps == [2.0]


def test_429_long_retry_after_raises_immediately(make_client):
    client, rec, sleeps = make_client(err(429, "rate_limit_exceeded", "Monthly quota exhausted", headers={"Retry-After": "86400"}))
    with pytest.raises(RealtimeSportsError) as e:
        client.list_sports()
    assert e.value.status == 429 and e.value.is_rate_limited
    assert e.value.retry_after == 86400
    assert e.value.code == "rate_limit_exceeded"
    assert len(rec.requests) == 1 and sleeps == []


def test_429_custom_cap(make_client):
    client, rec, sleeps = make_client(err(429, "rate_limit_exceeded", headers={"Retry-After": "90"}), ok([]), max_retry_after=120)
    assert client.list_sports() == []
    assert sleeps == [90.0]
    client2, rec2, _ = make_client(err(429, "rate_limit_exceeded", headers={"Retry-After": "90"}))
    with pytest.raises(RealtimeSportsError) as e:
        client2.list_sports()
    assert e.value.retry_after == 90 and len(rec2.requests) == 1


def test_429_without_retry_after_not_retried(make_client):
    client, rec, _ = make_client(err(429, "rate_limit_exceeded"))
    with pytest.raises(RealtimeSportsError) as e:
        client.list_sports()
    assert e.value.retry_after is None and len(rec.requests) == 1


def test_short_429_retried_for_post(make_client):
    client, rec, _ = make_client(err(429, "rate_limit_exceeded", headers={"Retry-After": "1"}), ok({"id": "w"}))
    assert client.webhooks.rotate_secret("w") == {"id": "w"}
    assert len(rec.requests) == 2


def test_parse_retry_after_and_backoff():
    assert parse_retry_after("30") == 30
    assert parse_retry_after(None) is None
    assert parse_retry_after("garbage") is None
    import email.utils

    now = 1_790_000_000.0
    assert parse_retry_after(email.utils.formatdate(now + 60, usegmt=True), now=now) == 60
    assert backoff_delay(0, rand=0.0) == 0.25
    assert backoff_delay(10, rand=1.0) == 8.0


def test_escape_hatch_request(make_client):
    client, rec, _ = make_client(ok({"x": 1}))
    res = client.request("GET", "/sports", query={"a": True})
    assert res.data == {"x": 1}
    assert str(rec.requests[0].url) == f"{BASE}/sports?a=true"
