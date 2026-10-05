# realtime-sports-api (Python)

Official Python client for the [Realtime Sports API](https://www.realtimesportsapi.com/docs?utm_source=github&utm_medium=realtime-sports-api-python):
live scores, play-by-play, box scores, schedules, teams, athletes, injuries, news, betting odds,
webhooks and a WebSocket push stream for NFL, college football, NBA, men's college basketball, MLB,
NHL and 23 soccer competitions.

- Sync `Client` and async `AsyncClient` with the same methods, built on `httpx`
- Typed models (`TypedDict`s) and methods generated from the OpenAPI spec
- Retries with backoff for 5xx and network errors; short `Retry-After` waits on 429
- Optional managed WebSocket stream (the `[stream]` extra)
- Python 3.9+

> **Freshness:** data is aggregated from public sources and is typically 20-30 seconds behind live
> play. There is no SLA. It is not suitable for uses that need sub-second data.

> **Coverage:** 29 leagues monitored live: NFL, college football, NBA, men's college basketball, MLB,
> NHL and 23 soccer competitions. Betting odds come from a single source book. Not intended for
> sub-second in-play betting.

## Install

The package is **not yet on PyPI**. Install it straight from GitHub:

```bash
pip install "git+https://github.com/ElcoDevRepos/realtime-sports-api-python"
pip install "realtime-sports-api[stream] @ git+https://github.com/ElcoDevRepos/realtime-sports-api-python"   # adds the WebSocket helper (websockets)
```

In a `requirements.txt`:

```
realtime-sports-api @ git+https://github.com/ElcoDevRepos/realtime-sports-api-python
```

Append `@<commit-or-tag>` to the URL to pin a version.

Get a free key at <https://www.realtimesportsapi.com/signup?utm_source=github&utm_medium=realtime-sports-api-python>.

## Quickstart

```python
from realtime_sports_api import Client

client = Client(api_key="YOUR_KEY")  # or set REALTIME_SPORTS_API_KEY

for game in client.list_live_events("football", "nfl"):
    home, away = game.get("homeTeam", {}), game.get("awayTeam", {})
    print(f"{away.get('abbreviation')} {away.get('score')} @ {home.get('abbreviation')} {home.get('score')}  "
          f"{game.get('status', {}).get('detail')}")

week5 = client.get_season_schedule("football", "nfl", 2026, week=5, season_type=2)
```

Async:

```python
import asyncio
from realtime_sports_api import AsyncClient

async def main():
    async with AsyncClient() as client:
        live = await client.list_live_events("basketball", "nba", include_odds=True)
        print(len(live), "games live")

asyncio.run(main())
```

Use `with Client() as client:` (or `client.close()`) to release the connection pool. You can pass
your own `httpx.Client` / `httpx.AsyncClient` with `http_client=...`.

### Return values: `data` by default, `with_meta` for the envelope

Methods return the response's `data`. Prefix the call with `.with_meta` to get an `ApiResponse`
with `data`, `meta`, `status_code` and `headers`:

```python
res = client.with_meta.list_plays("football", "nfl", "401772982", limit=100)
print(res.rate_limit)                       # {'limit': ..., 'remaining': ..., 'reset': ...}
print(res.meta.get("pagination"))
plays = res.data
```

This works for every method, sync and async (`await client.with_meta.list_sports()`).

## Client options

```python
Client(
    api_key="...",                 # or REALTIME_SPORTS_API_KEY
    base_url="https://www.realtimesportsapi.com/api/v1",  # default
    timeout=30.0,                  # seconds, per attempt
    max_retries=2,                 # retries after the first attempt
    max_retry_after=60.0,          # longest Retry-After (s) the client will wait out on a 429
    use_api_key_header=False,      # send X-API-Key instead of Authorization: Bearer
    headers={"X-Trace": "1"},      # extra headers on every request
    http_client=None,              # bring your own httpx.Client
)
```

Every method also accepts `request_options={"timeout": 5, "max_retries": 0, "headers": {...}}`.

## Methods

Method names are the snake_case form of the OpenAPI `operationId`s. Path parameters are positional;
query parameters are keyword arguments in snake_case (`include_odds`, `season_type`, `page_size`,
`first_four`, `from_` for `from`). Required query parameters are positional (`query` for
`search_athletes`, `season` for `get_athlete_game_log`).

Sport slugs: `football` (American football), `basketball`, `baseball`, `hockey`, `soccer`. League
slugs include `nfl`, `college-football`, `nba`, `mens-college-basketball`, `mlb`, `nhl`, and soccer
competitions such as `eng.1`, `usa.1`, `uefa.champions`.

| Area | Methods |
| --- | --- |
| Sports and leagues | `list_sports()`, `list_leagues(sport)`, `get_league(sport, league)` |
| Events | `list_events(sport, league, limit=, include_odds=)`, `list_live_events(sport, league, include_odds=)`, `get_event(sport, league, event_id, include_odds=)` |
| Event detail | `get_event_box_score`, `get_event_win_probability(..., drives=)`, `get_event_roster(..., team=, starters=, enrich=)`, `list_plays(..., limit=, page=, enrich=)`, `list_penalties(..., enrich=)`, `get_event_odds`, `get_event_odds_history(..., limit=)` (all take `sport, league, event_id`) |
| Teams | `list_teams(sport, league, limit=, page=)`, `get_team(sport, league, team_id)`, `get_team_roster(..., season=)`, `get_team_depth_chart(..., season=)` |
| Athletes | `list_athletes(sport, league, limit=, page=, include=)`, `search_athletes(sport, league, query, limit=)`, `get_athlete(sport, league, athlete_id, season=, season_type=)`, `get_athlete_game_log(sport, league, athlete_id, season, week=, season_type=)`, `get_athlete_availability_history(..., limit=, from_=, to=)` |
| Injuries and availability | `get_injuries(sport, league, team=)`, `get_player_availability(sport, league, team=, status=)`, `get_player_availability_history(sport, league, team=, since=, status=, limit=)` |
| News and transactions | `get_news(sport, league, limit=, page=, team=, athlete=, since=, from_=, to=)`, `get_news_history(...)`, `get_transactions(sport, league, limit=, page=, team=, season=)` |
| Seasons and schedules | `get_current_season(sport, league)`, `list_seasons(sport, league, limit=, page=)`, `get_season(sport, league, season)`, `get_season_schedule(sport, league, season, week=, season_type=, include_odds=)`, `list_season_weeks(sport, league, season, season_type=)`, `list_season_types`, `get_season_type(..., type_id)`, `list_groups(..., type_id)`, `get_group(..., type_id, group_id)`, `list_group_teams(..., group_id, page_size=, page=)`, `list_team_season_events(sport, league, season, team_id, page=, page_size=, limit=)`, `get_tournament(sport, league, season, round=, region=, first_four=, start_date=, end_date=)` |
| Webhooks | `list_webhooks()`, `create_webhook(url, events, leagues=, frequency=, active=)`, `get_webhook(id)`, `update_webhook(id, url=, events=, leagues=, frequency=, active=)`, `delete_webhook(id)`, `get_webhook_secret(id)`, `rotate_webhook_secret(id)`, `test_webhook(id, event_type=, delivery_id=)`, `list_webhook_deliveries(id, limit=)` |
| Webhooks (namespace) | `client.webhooks.list/create/get/update/delete/get_secret/rotate_secret/test/deliveries` (same as above) |
| WebSocket | `create_websocket_token()`, `AsyncClient.stream(...)` |
| Escape hatch | `client.request("GET", "/path", query={...}, body=...)` returns an `ApiResponse` |

`season_type`: 1 = preseason, 2 = regular season, 3 = postseason. `week` applies to NFL and college
football. In `update_webhook`, omitted arguments are left unchanged and `leagues=None` means "all
leagues" (sent as JSON `null`).

### Types

`TypedDict` models are exported for every schema: `Event`, `EventTeam`, `EventStatus`, `Play`,
`Odds`, `Team`, `Athlete`, `Injury`, `NewsArticle`, `Webhook`, `WebhookInput`, `WebhookDelivery`, and
more. They are `total=False` (fields can be missing), so `.get()` is the safe way to read them.

```python
from realtime_sports_api import Event

def score_line(e: Event) -> str:
    return f"{e.get('awayTeam', {}).get('score')}-{e.get('homeTeam', {}).get('score')}"
```

## Errors and retries

Every failure raises `RealtimeSportsError` with `status` (HTTP status or `None`), `code` (API error
code such as `MISSING_TOKEN`, `rate_limit_exceeded`, or `NETWORK_ERROR` / `TIMEOUT`), `message`,
`hint`, `retry_after` (seconds, from `Retry-After`), and the helpers `is_rate_limited` /
`is_auth_error`.

```python
from realtime_sports_api import RealtimeSportsError

try:
    client.list_live_events("hockey", "nhl")
except RealtimeSportsError as e:
    if e.is_rate_limited:
        print(f"Monthly quota exhausted; retry in {e.retry_after}s or upgrade.")
    else:
        raise
```

Retry behavior (`max_retries`, default 2):

- **5xx, network errors and timeouts:** retried with exponential backoff and jitter (about 0.5 s,
  1 s, 2 s ..., capped at 8 s) for `GET`/`DELETE`. `POST`/`PATCH` are not retried on 5xx or network
  errors, to avoid creating duplicate webhooks.
- **429:** returned when the **monthly** quota is exhausted, with `Retry-After`. If `Retry-After` is at
  most `max_retry_after` (default 60 s) the client waits and retries; if it is longer or missing, the
  error is raised immediately, because a monthly quota will not clear in seconds.
- **Other 4xx:** raised immediately.

## Streaming (WebSocket)

Install the extra: `pip install "realtime-sports-api[stream] @ git+https://github.com/ElcoDevRepos/realtime-sports-api-python"`. The stream is async:

```python
import asyncio
from realtime_sports_api import AsyncClient

async def main():
    async with AsyncClient() as client:
        subs = [
            {"event": "event_score_change", "filters": {"sport": "football", "league": "nfl"}},
            {"event": "event_final", "filters": {"sport": "football", "league": "nfl"}},
        ]
        async with client.stream(subs, on_error=print, on_subscribed=print) as stream:
            async for msg in stream:
                d = msg["data"]
                print(msg["type"], d.get("name"), d.get("awayTeam", {}).get("score"), d.get("homeTeam", {}).get("score"))

asyncio.run(main())
```

The stream calls `POST /api/websocket/auth`, connects to `{url}?token={token}`, sends your
subscriptions, keeps the connection alive with WebSocket pings, and reconnects with backoff,
re-authenticating when the 1-hour token is near expiry or was rejected, then resubscribing.

| Option | Default | Description |
| --- | --- | --- |
| `subscriptions` | `()` | `{"event", "filters": {"sport", "league", "eventId"}, "frequency"}` |
| `on_error` | `None` | Called with `RealtimeSportsError` for server `error` messages, `quota_exceeded`, connection failures |
| `on_subscribed` | `None` | Called with the server's acknowledgement; check `warnings` (e.g. a league that is not monitored) |
| `include_control` | `False` | Also yield control messages (`subscribed`, `pong`, ...) |
| `reconnect` | `True` | Reconnect after disconnects |
| `max_reconnect_attempts` | `None` (unlimited) | Consecutive failures before giving up |
| `initial_delay` / `max_delay` | `1.0` / `30.0` | Backoff bounds in seconds |
| `ping_interval` / `ping_timeout` | `20.0` / `20.0` | Passed to `websockets.connect` |

Use `await stream.subscribe({...})` / `await stream.unsubscribe({...})` to change subscriptions while
connected. Event types: `event_score_change`, `event_live`, `event_status_change`, `event_play`,
`event_final`, `event_odds_change`.

Notes:

- WebSocket access requires a plan that includes it. A key without access makes the iterator raise
  `RealtimeSportsError` (status 401/403, or code `WEBSOCKET_FORBIDDEN`) instead of retrying forever.
- **Each delivered event message counts toward your monthly quota.** Narrow filters and the
  server-side `frequency` throttle (`30s`, `1m`, `5m`, `10m`, `30m`) keep usage down.
- Soccer uses `"sport": "soccer"`; `"football"` is American football only.
- Events that arrive while disconnected are not replayed.

## Quotas and polling

Monthly quotas as of October 2026: Free 125 calls (1,000 during the first 30 days), Starter 10,000,
Growth 25,000, Pro 50,000, Scale 500,000. Current numbers are on the
[pricing page](https://www.realtimesportsapi.com/pricing?utm_source=github&utm_medium=realtime-sports-api-python). Every successful REST call counts as one call.

| Pattern (one league) | Calls |
| --- | --- |
| `list_live_events` every 30 s for a 3.5-hour game window | 420 |
| ... every 60 s | 210 |
| Idle check every 15 min, all day | 96 per day (~2,900 per month) |

Poll every 30-60 s only while something is live, back off to 10-15 minutes when nothing is, and
prefer the WebSocket stream or webhooks for continuous updates. Polling faster than ~20 s gains
nothing: the data is typically 20-30 s behind live play.

## Regenerating from the spec

`_types.py` and `_operations.py` are generated from the OpenAPI spec (standard library only):

```bash
python scripts/generate.py                                  # https://www.realtimesportsapi.com/openapi.json
SPEC=/path/to/openapi.json python scripts/generate.py       # local file
```

## Development

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m build && twine check dist/*
```

## Links

- Free API key: [https://www.realtimesportsapi.com/signup](https://www.realtimesportsapi.com/signup?utm_source=github&utm_medium=realtime-sports-api-python)
- API docs: [https://www.realtimesportsapi.com/docs](https://www.realtimesportsapi.com/docs?utm_source=github&utm_medium=realtime-sports-api-python)
- Pricing and quotas: [https://www.realtimesportsapi.com/pricing](https://www.realtimesportsapi.com/pricing?utm_source=github&utm_medium=realtime-sports-api-python)
- Hosted MCP server for AI assistants: [https://www.realtimesportsapi.com/docs/mcp](https://www.realtimesportsapi.com/docs/mcp?utm_source=github&utm_medium=realtime-sports-api-python)
- JavaScript/TypeScript SDK: [ElcoDevRepos/realtime-sports-api-js](https://github.com/ElcoDevRepos/realtime-sports-api-js)
- Runnable examples (curl, JS, Python, MCP configs): [ElcoDevRepos/realtime-sports-api-examples](https://github.com/ElcoDevRepos/realtime-sports-api-examples)

## License

MIT
