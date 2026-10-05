"""Operation methods generated from the Realtime Sports API OpenAPI spec. Do not edit by hand.

Regenerate with `python scripts/generate.py`.
"""
# ruff: noqa: E501
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from ._base import NOT_GIVEN, ApiResponse, NotGiven, RequestOptions, _p

if TYPE_CHECKING:
    from typing import Literal

    from ._types import (
        Athlete,
        AthleteSearchResult,
        AvailabilityState,
        AvailabilityTransition,
        BoxScore,
        DepthChart,
        ErrorBody,
        Event,
        EventStatus,
        EventTeam,
        GameLogEntry,
        GameRoster,
        Group,
        Injury,
        InjuryReport,
        League,
        LeagueDetail,
        NewsArticle,
        Odds,
        OddsHistoryEntry,
        Pagination,
        Play,
        PlayAthlete,
        PlayerAvailability,
        PlayerAvailabilityReport,
        RateLimit,
        Roster,
        RosterAthlete,
        Season,
        SeasonSummary,
        SeasonType,
        Sport,
        Team,
        TournamentGame,
        Transactions,
        Webhook,
        WebhookDelivery,
        WebhookEventType,
        WebhookFrequency,
        WebhookInput,
        Week,
        WinProbability,
    )


class _SyncWebhooks:
    """`client.webhooks` namespace (aliases of the `*_webhook*` methods)."""

    def __init__(self, parent: "_SyncOperations") -> None:
        self._parent = parent

    def list(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Webhook"]:
        """`listWebhooks` - GET /webhooks: List your webhooks"""
        return self._parent.list_webhooks(request_options=request_options)

    def create(
        self,
        url: str,
        events: List["WebhookEventType"],
        *,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> "Webhook":
        """`createWebhook` - POST /webhooks: Create a webhook"""
        return self._parent.create_webhook(url, events, leagues=leagues, frequency=frequency, active=active, request_options=request_options)

    def get(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "Webhook":
        """`getWebhook` - GET /webhooks/{webhookId}: Get a webhook"""
        return self._parent.get_webhook(webhook_id, request_options=request_options)

    def update(
        self,
        webhook_id: Union[str, int],
        *,
        url: Union[str, NotGiven] = NOT_GIVEN,
        events: Union[List["WebhookEventType"], NotGiven] = NOT_GIVEN,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> "Webhook":
        """`updateWebhook` - PATCH /webhooks/{webhookId}: Update a webhook"""
        return self._parent.update_webhook(webhook_id, url=url, events=events, leagues=leagues, frequency=frequency, active=active, request_options=request_options)

    def delete(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`deleteWebhook` - DELETE /webhooks/{webhookId}: Delete a webhook"""
        return self._parent.delete_webhook(webhook_id, request_options=request_options)

    def get_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`getWebhookSecret` - GET /webhooks/{webhookId}/secret: Reveal the signing secret"""
        return self._parent.get_webhook_secret(webhook_id, request_options=request_options)

    def rotate_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`rotateWebhookSecret` - POST /webhooks/{webhookId}/secret: Rotate the signing secret"""
        return self._parent.rotate_webhook_secret(webhook_id, request_options=request_options)

    def test(
        self,
        webhook_id: Union[str, int],
        *,
        event_type: Union["WebhookEventType", NotGiven] = NOT_GIVEN,
        delivery_id: Union[str, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`testWebhook` - POST /webhooks/{webhookId}/test: Send a test delivery"""
        return self._parent.test_webhook(webhook_id, event_type=event_type, delivery_id=delivery_id, request_options=request_options)

    def deliveries(
        self,
        webhook_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["WebhookDelivery"]:
        """`listWebhookDeliveries` - GET /webhooks/{webhookId}/deliveries: List failed deliveries"""
        return self._parent.list_webhook_deliveries(webhook_id, limit=limit, request_options=request_options)


class _SyncOperations:
    """Generated API methods. Mixed into the client classes."""

    _websocket_auth_url: str

    def _request_data(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:  # pragma: no cover
        raise NotImplementedError

    def _request_with_meta(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:  # pragma: no cover
        raise NotImplementedError

    @property
    def webhooks(self) -> _SyncWebhooks:
        """Webhook management: list/create/get/update/delete/get_secret/rotate_secret/test/deliveries."""
        return _SyncWebhooks(self)

    def list_sports(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Sport"]:
        """`listSports` - GET /sports: List sports"""
        return self._request_data("GET", "/sports", query=None, body=NOT_GIVEN, request_options=request_options)

    def list_leagues(
        self,
        sport: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List["League"]:
        """`listLeagues` - GET /sports/{sport}/leagues: List leagues for a sport"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_league(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "LeagueDetail":
        """`getLeague` - GET /sports/{sport}/leagues/{league}: Get league details"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}", query=None, body=NOT_GIVEN, request_options=request_options)

    def list_events(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Event"]:
        """`listEvents` - GET /sports/{sport}/leagues/{league}/events: List events for a league"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events", query={"limit": limit, "includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    def list_live_events(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Event"]:
        """`listLiveEvents` - GET /sports/{sport}/leagues/{league}/events/live: List live events"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/live", query={"includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    def get_event(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "Event":
        """`getEvent` - GET /sports/{sport}/leagues/{league}/events/{eventId}: Get an event"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}", query={"includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    def get_event_box_score(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "BoxScore":
        """`getEventBoxScore` - GET /sports/{sport}/leagues/{league}/events/{eventId}/boxscore: Get box score"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/boxscore", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_event_win_probability(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        drives: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "WinProbability":
        """`getEventWinProbability` - GET /sports/{sport}/leagues/{league}/events/{eventId}/winprobability: Get win probability"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/winprobability", query={"drives": drives}, body=NOT_GIVEN, request_options=request_options)

    def get_event_roster(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        team: Optional[str] = None,
        starters: Optional[bool] = None,
        enrich: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "GameRoster":
        """`getEventRoster` - GET /sports/{sport}/leagues/{league}/events/{eventId}/roster: Get game rosters"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/roster", query={"team": team, "starters": starters, "enrich": enrich}, body=NOT_GIVEN, request_options=request_options)

    def list_plays(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        enrich: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Play"]:
        """`listPlays` - GET /sports/{sport}/leagues/{league}/events/{eventId}/plays: Get play-by-play"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/plays", query={"limit": limit, "page": page, "enrich": enrich}, body=NOT_GIVEN, request_options=request_options)

    def list_penalties(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        enrich: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Play"]:
        """`listPenalties` - GET /sports/{sport}/leagues/{league}/events/{eventId}/penalties: Get penalty plays"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/penalties", query={"enrich": enrich}, body=NOT_GIVEN, request_options=request_options)

    def get_event_odds(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Optional["Odds"]:
        """`getEventOdds` - GET /sports/{sport}/leagues/{league}/events/{eventId}/odds: Get current odds"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/odds", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_event_odds_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["OddsHistoryEntry"]:
        """`getEventOddsHistory` - GET /sports/{sport}/leagues/{league}/events/{eventId}/odds/history: Get odds history"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/odds/history", query={"limit": limit}, body=NOT_GIVEN, request_options=request_options)

    def list_teams(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Team"]:
        """`listTeams` - GET /sports/{sport}/leagues/{league}/teams: List teams"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams", query={"limit": limit, "page": page}, body=NOT_GIVEN, request_options=request_options)

    def get_team(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        team_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "Team":
        """`getTeam` - GET /sports/{sport}/leagues/{league}/teams/{teamId}: Get a team"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams/{_p(team_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_team_roster(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        team_id: Union[str, int],
        *,
        season: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "Roster":
        """`getTeamRoster` - GET /sports/{sport}/leagues/{league}/teams/{teamId}/roster: Get team roster"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams/{_p(team_id)}/roster", query={"season": season}, body=NOT_GIVEN, request_options=request_options)

    def get_team_depth_chart(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        team_id: Union[str, int],
        *,
        season: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "DepthChart":
        """`getTeamDepthChart` - GET /sports/{sport}/leagues/{league}/teams/{teamId}/depthchart: Get depth chart"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams/{_p(team_id)}/depthchart", query={"season": season}, body=NOT_GIVEN, request_options=request_options)

    def list_athletes(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        include: Optional[Literal["statistics"]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Athlete"]:
        """`listAthletes` - GET /sports/{sport}/leagues/{league}/athletes: List athletes"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes", query={"limit": limit, "page": page, "include": include}, body=NOT_GIVEN, request_options=request_options)

    def search_athletes(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        query: str,
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["AthleteSearchResult"]:
        """`searchAthletes` - GET /sports/{sport}/leagues/{league}/athletes/search: Search athletes by name"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/search", query={"query": query, "limit": limit}, body=NOT_GIVEN, request_options=request_options)

    def get_athlete(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        athlete_id: Union[str, int],
        *,
        season: Optional[int] = None,
        season_type: Optional[Literal[1, 2, 3]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "Athlete":
        """`getAthlete` - GET /sports/{sport}/leagues/{league}/athletes/{athleteId}: Get an athlete"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/{_p(athlete_id)}", query={"season": season, "seasonType": season_type}, body=NOT_GIVEN, request_options=request_options)

    def get_athlete_game_log(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        athlete_id: Union[str, int],
        season: int,
        *,
        week: Optional[int] = None,
        season_type: Optional[Literal[1, 2, 3]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["GameLogEntry"]:
        """`getAthleteGameLog` - GET /sports/{sport}/leagues/{league}/athletes/{athleteId}/gamelog: Get athlete game log"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/{_p(athlete_id)}/gamelog", query={"season": season, "week": week, "seasonType": season_type}, body=NOT_GIVEN, request_options=request_options)

    def get_athlete_availability_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        athlete_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`getAthleteAvailabilityHistory` - GET /sports/{sport}/leagues/{league}/athletes/{athleteId}/availability-history: Get athlete availability history"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/{_p(athlete_id)}/availability-history", query={"limit": limit, "from": from_, "to": to}, body=NOT_GIVEN, request_options=request_options)

    def get_injuries(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        team: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "InjuryReport":
        """`getInjuries` - GET /sports/{sport}/leagues/{league}/injuries: Get injury report"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/injuries", query={"team": team}, body=NOT_GIVEN, request_options=request_options)

    def get_player_availability(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        team: Optional[str] = None,
        status: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "PlayerAvailabilityReport":
        """`getPlayerAvailability` - GET /sports/{sport}/leagues/{league}/player-availability: Get normalized player availability"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/player-availability", query={"team": team, "status": status}, body=NOT_GIVEN, request_options=request_options)

    def get_player_availability_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        team: Optional[str] = None,
        since: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["AvailabilityTransition"]:
        """`getPlayerAvailabilityHistory` - GET /sports/{sport}/leagues/{league}/player-availability/history: Get availability changes feed"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/player-availability/history", query={"team": team, "since": since, "status": status, "limit": limit}, body=NOT_GIVEN, request_options=request_options)

    def get_news(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        team: Optional[str] = None,
        athlete: Optional[str] = None,
        since: Optional[str] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["NewsArticle"]:
        """`getNews` - GET /sports/{sport}/leagues/{league}/news: Get latest news"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/news", query={"limit": limit, "page": page, "team": team, "athlete": athlete, "since": since, "from": from_, "to": to}, body=NOT_GIVEN, request_options=request_options)

    def get_news_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        team: Optional[str] = None,
        athlete: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["NewsArticle"]:
        """`getNewsHistory` - GET /sports/{sport}/leagues/{league}/news/history: Get archived news"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/news/history", query={"from": from_, "to": to, "team": team, "athlete": athlete, "limit": limit, "page": page}, body=NOT_GIVEN, request_options=request_options)

    def get_transactions(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        team: Optional[str] = None,
        season: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "Transactions":
        """`getTransactions` - GET /sports/{sport}/leagues/{league}/transactions: Get transactions"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/transactions", query={"limit": limit, "page": page, "team": team, "season": season}, body=NOT_GIVEN, request_options=request_options)

    def get_current_season(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "Season":
        """`getCurrentSeason` - GET /sports/{sport}/leagues/{league}/season: Get the active season"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/season", query=None, body=NOT_GIVEN, request_options=request_options)

    def list_seasons(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["SeasonSummary"]:
        """`listSeasons` - GET /sports/{sport}/leagues/{league}/seasons: List seasons"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons", query={"limit": limit, "page": page}, body=NOT_GIVEN, request_options=request_options)

    def get_season(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "Season":
        """`getSeason` - GET /sports/{sport}/leagues/{league}/seasons/{season}: Get a season"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_season_schedule(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        week: Optional[int] = None,
        season_type: Optional[Literal[1, 2, 3]] = None,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Event"]:
        """`getSeasonSchedule` - GET /sports/{sport}/leagues/{league}/seasons/{season}/schedule: Get season schedule"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/schedule", query={"week": week, "seasonType": season_type, "includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    def list_season_weeks(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        season_type: Optional[Literal[1, 2, 3]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Week"]:
        """`listSeasonWeeks` - GET /sports/{sport}/leagues/{league}/seasons/{season}/weeks: List weeks in a season"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/weeks", query={"seasonType": season_type}, body=NOT_GIVEN, request_options=request_options)

    def list_season_types(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List["SeasonType"]:
        """`listSeasonTypes` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types: List season types"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_season_type(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "SeasonType":
        """`getSeasonType` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}: Get a season type"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    def list_groups(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Group"]:
        """`listGroups` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}/groups: List groups (conferences/divisions)"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}/groups", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_group(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        group_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "Group":
        """`getGroup` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}/groups/{groupId}: Get a group"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}/groups/{_p(group_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    def list_group_teams(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        group_id: Union[str, int],
        *,
        page_size: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Team"]:
        """`listGroupTeams` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}/groups/{groupId}/teams: List teams in a group"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}/groups/{_p(group_id)}/teams", query={"pageSize": page_size, "page": page}, body=NOT_GIVEN, request_options=request_options)

    def list_team_season_events(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        team_id: Union[str, int],
        *,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Event"]:
        """`listTeamSeasonEvents` - GET /sports/{sport}/leagues/{league}/seasons/{season}/teams/{teamId}/events: List a team's events in a season"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/teams/{_p(team_id)}/events", query={"page": page, "pageSize": page_size, "limit": limit}, body=NOT_GIVEN, request_options=request_options)

    def get_tournament(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        round: Optional[str] = None,
        region: Optional[str] = None,
        first_four: Optional[bool] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["TournamentGame"]:
        """`getTournament` - GET /sports/{sport}/leagues/{league}/seasons/{season}/tournament: Get NCAA tournament games"""
        return self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/tournament", query={"round": round, "region": region, "firstFour": first_four, "startDate": start_date, "endDate": end_date}, body=NOT_GIVEN, request_options=request_options)

    def list_webhooks(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Webhook"]:
        """`listWebhooks` - GET /webhooks: List your webhooks"""
        return self._request_data("GET", "/webhooks", query=None, body=NOT_GIVEN, request_options=request_options)

    def create_webhook(
        self,
        url: str,
        events: List["WebhookEventType"],
        *,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> "Webhook":
        """`createWebhook` - POST /webhooks: Create a webhook"""
        return self._request_data("POST", "/webhooks", query=None, body={"url": url, "events": events, "leagues": leagues, "frequency": frequency, "active": active}, request_options=request_options)

    def get_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "Webhook":
        """`getWebhook` - GET /webhooks/{webhookId}: Get a webhook"""
        return self._request_data("GET", f"/webhooks/{_p(webhook_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    def update_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        url: Union[str, NotGiven] = NOT_GIVEN,
        events: Union[List["WebhookEventType"], NotGiven] = NOT_GIVEN,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> "Webhook":
        """`updateWebhook` - PATCH /webhooks/{webhookId}: Update a webhook"""
        return self._request_data("PATCH", f"/webhooks/{_p(webhook_id)}", query=None, body={"url": url, "events": events, "leagues": leagues, "frequency": frequency, "active": active}, request_options=request_options)

    def delete_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`deleteWebhook` - DELETE /webhooks/{webhookId}: Delete a webhook"""
        return self._request_data("DELETE", f"/webhooks/{_p(webhook_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_webhook_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`getWebhookSecret` - GET /webhooks/{webhookId}/secret: Reveal the signing secret"""
        return self._request_data("GET", f"/webhooks/{_p(webhook_id)}/secret", query=None, body=NOT_GIVEN, request_options=request_options)

    def rotate_webhook_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`rotateWebhookSecret` - POST /webhooks/{webhookId}/secret: Rotate the signing secret"""
        return self._request_data("POST", f"/webhooks/{_p(webhook_id)}/secret", query=None, body=NOT_GIVEN, request_options=request_options)

    def test_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        event_type: Union["WebhookEventType", NotGiven] = NOT_GIVEN,
        delivery_id: Union[str, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`testWebhook` - POST /webhooks/{webhookId}/test: Send a test delivery"""
        return self._request_data("POST", f"/webhooks/{_p(webhook_id)}/test", query=None, body={"eventType": event_type, "deliveryId": delivery_id}, request_options=request_options)

    def list_webhook_deliveries(
        self,
        webhook_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["WebhookDelivery"]:
        """`listWebhookDeliveries` - GET /webhooks/{webhookId}/deliveries: List failed deliveries"""
        return self._request_data("GET", f"/webhooks/{_p(webhook_id)}/deliveries", query={"limit": limit}, body=NOT_GIVEN, request_options=request_options)

    def create_websocket_token(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`createWebSocketToken` - POST /websocket/auth: Get a WebSocket token"""
        return self._request_data("POST", self._websocket_auth_url, query=None, body=NOT_GIVEN, request_options=request_options)


class _SyncWebhooksWithMeta:
    """`client.webhooks` namespace (aliases of the `*_webhook*` methods)."""

    def __init__(self, parent: "_SyncOperationsWithMeta") -> None:
        self._parent = parent

    def list(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Webhook"]]:
        """`listWebhooks` - GET /webhooks: List your webhooks"""
        return self._parent.list_webhooks(request_options=request_options)

    def create(
        self,
        url: str,
        events: List["WebhookEventType"],
        *,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Webhook"]:
        """`createWebhook` - POST /webhooks: Create a webhook"""
        return self._parent.create_webhook(url, events, leagues=leagues, frequency=frequency, active=active, request_options=request_options)

    def get(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Webhook"]:
        """`getWebhook` - GET /webhooks/{webhookId}: Get a webhook"""
        return self._parent.get_webhook(webhook_id, request_options=request_options)

    def update(
        self,
        webhook_id: Union[str, int],
        *,
        url: Union[str, NotGiven] = NOT_GIVEN,
        events: Union[List["WebhookEventType"], NotGiven] = NOT_GIVEN,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Webhook"]:
        """`updateWebhook` - PATCH /webhooks/{webhookId}: Update a webhook"""
        return self._parent.update_webhook(webhook_id, url=url, events=events, leagues=leagues, frequency=frequency, active=active, request_options=request_options)

    def delete(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`deleteWebhook` - DELETE /webhooks/{webhookId}: Delete a webhook"""
        return self._parent.delete_webhook(webhook_id, request_options=request_options)

    def get_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`getWebhookSecret` - GET /webhooks/{webhookId}/secret: Reveal the signing secret"""
        return self._parent.get_webhook_secret(webhook_id, request_options=request_options)

    def rotate_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`rotateWebhookSecret` - POST /webhooks/{webhookId}/secret: Rotate the signing secret"""
        return self._parent.rotate_webhook_secret(webhook_id, request_options=request_options)

    def test(
        self,
        webhook_id: Union[str, int],
        *,
        event_type: Union["WebhookEventType", NotGiven] = NOT_GIVEN,
        delivery_id: Union[str, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`testWebhook` - POST /webhooks/{webhookId}/test: Send a test delivery"""
        return self._parent.test_webhook(webhook_id, event_type=event_type, delivery_id=delivery_id, request_options=request_options)

    def deliveries(
        self,
        webhook_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["WebhookDelivery"]]:
        """`listWebhookDeliveries` - GET /webhooks/{webhookId}/deliveries: List failed deliveries"""
        return self._parent.list_webhook_deliveries(webhook_id, limit=limit, request_options=request_options)


class _SyncOperationsWithMeta:
    """Generated API methods. Mixed into the client classes."""

    _websocket_auth_url: str

    def _request_data(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:  # pragma: no cover
        raise NotImplementedError

    def _request_with_meta(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:  # pragma: no cover
        raise NotImplementedError

    @property
    def webhooks(self) -> _SyncWebhooksWithMeta:
        """Webhook management: list/create/get/update/delete/get_secret/rotate_secret/test/deliveries."""
        return _SyncWebhooksWithMeta(self)

    def list_sports(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Sport"]]:
        """`listSports` - GET /sports: List sports"""
        return self._request_with_meta("GET", "/sports", query=None, body=NOT_GIVEN, request_options=request_options)

    def list_leagues(
        self,
        sport: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["League"]]:
        """`listLeagues` - GET /sports/{sport}/leagues: List leagues for a sport"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_league(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["LeagueDetail"]:
        """`getLeague` - GET /sports/{sport}/leagues/{league}: Get league details"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}", query=None, body=NOT_GIVEN, request_options=request_options)

    def list_events(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Event"]]:
        """`listEvents` - GET /sports/{sport}/leagues/{league}/events: List events for a league"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events", query={"limit": limit, "includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    def list_live_events(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Event"]]:
        """`listLiveEvents` - GET /sports/{sport}/leagues/{league}/events/live: List live events"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/live", query={"includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    def get_event(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Event"]:
        """`getEvent` - GET /sports/{sport}/leagues/{league}/events/{eventId}: Get an event"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}", query={"includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    def get_event_box_score(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["BoxScore"]:
        """`getEventBoxScore` - GET /sports/{sport}/leagues/{league}/events/{eventId}/boxscore: Get box score"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/boxscore", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_event_win_probability(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        drives: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["WinProbability"]:
        """`getEventWinProbability` - GET /sports/{sport}/leagues/{league}/events/{eventId}/winprobability: Get win probability"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/winprobability", query={"drives": drives}, body=NOT_GIVEN, request_options=request_options)

    def get_event_roster(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        team: Optional[str] = None,
        starters: Optional[bool] = None,
        enrich: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["GameRoster"]:
        """`getEventRoster` - GET /sports/{sport}/leagues/{league}/events/{eventId}/roster: Get game rosters"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/roster", query={"team": team, "starters": starters, "enrich": enrich}, body=NOT_GIVEN, request_options=request_options)

    def list_plays(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        enrich: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Play"]]:
        """`listPlays` - GET /sports/{sport}/leagues/{league}/events/{eventId}/plays: Get play-by-play"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/plays", query={"limit": limit, "page": page, "enrich": enrich}, body=NOT_GIVEN, request_options=request_options)

    def list_penalties(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        enrich: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Play"]]:
        """`listPenalties` - GET /sports/{sport}/leagues/{league}/events/{eventId}/penalties: Get penalty plays"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/penalties", query={"enrich": enrich}, body=NOT_GIVEN, request_options=request_options)

    def get_event_odds(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Optional["Odds"]]:
        """`getEventOdds` - GET /sports/{sport}/leagues/{league}/events/{eventId}/odds: Get current odds"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/odds", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_event_odds_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["OddsHistoryEntry"]]:
        """`getEventOddsHistory` - GET /sports/{sport}/leagues/{league}/events/{eventId}/odds/history: Get odds history"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/odds/history", query={"limit": limit}, body=NOT_GIVEN, request_options=request_options)

    def list_teams(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Team"]]:
        """`listTeams` - GET /sports/{sport}/leagues/{league}/teams: List teams"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams", query={"limit": limit, "page": page}, body=NOT_GIVEN, request_options=request_options)

    def get_team(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        team_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Team"]:
        """`getTeam` - GET /sports/{sport}/leagues/{league}/teams/{teamId}: Get a team"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams/{_p(team_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_team_roster(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        team_id: Union[str, int],
        *,
        season: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Roster"]:
        """`getTeamRoster` - GET /sports/{sport}/leagues/{league}/teams/{teamId}/roster: Get team roster"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams/{_p(team_id)}/roster", query={"season": season}, body=NOT_GIVEN, request_options=request_options)

    def get_team_depth_chart(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        team_id: Union[str, int],
        *,
        season: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["DepthChart"]:
        """`getTeamDepthChart` - GET /sports/{sport}/leagues/{league}/teams/{teamId}/depthchart: Get depth chart"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams/{_p(team_id)}/depthchart", query={"season": season}, body=NOT_GIVEN, request_options=request_options)

    def list_athletes(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        include: Optional[Literal["statistics"]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Athlete"]]:
        """`listAthletes` - GET /sports/{sport}/leagues/{league}/athletes: List athletes"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes", query={"limit": limit, "page": page, "include": include}, body=NOT_GIVEN, request_options=request_options)

    def search_athletes(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        query: str,
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["AthleteSearchResult"]]:
        """`searchAthletes` - GET /sports/{sport}/leagues/{league}/athletes/search: Search athletes by name"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/search", query={"query": query, "limit": limit}, body=NOT_GIVEN, request_options=request_options)

    def get_athlete(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        athlete_id: Union[str, int],
        *,
        season: Optional[int] = None,
        season_type: Optional[Literal[1, 2, 3]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Athlete"]:
        """`getAthlete` - GET /sports/{sport}/leagues/{league}/athletes/{athleteId}: Get an athlete"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/{_p(athlete_id)}", query={"season": season, "seasonType": season_type}, body=NOT_GIVEN, request_options=request_options)

    def get_athlete_game_log(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        athlete_id: Union[str, int],
        season: int,
        *,
        week: Optional[int] = None,
        season_type: Optional[Literal[1, 2, 3]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["GameLogEntry"]]:
        """`getAthleteGameLog` - GET /sports/{sport}/leagues/{league}/athletes/{athleteId}/gamelog: Get athlete game log"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/{_p(athlete_id)}/gamelog", query={"season": season, "week": week, "seasonType": season_type}, body=NOT_GIVEN, request_options=request_options)

    def get_athlete_availability_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        athlete_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`getAthleteAvailabilityHistory` - GET /sports/{sport}/leagues/{league}/athletes/{athleteId}/availability-history: Get athlete availability history"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/{_p(athlete_id)}/availability-history", query={"limit": limit, "from": from_, "to": to}, body=NOT_GIVEN, request_options=request_options)

    def get_injuries(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        team: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["InjuryReport"]:
        """`getInjuries` - GET /sports/{sport}/leagues/{league}/injuries: Get injury report"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/injuries", query={"team": team}, body=NOT_GIVEN, request_options=request_options)

    def get_player_availability(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        team: Optional[str] = None,
        status: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["PlayerAvailabilityReport"]:
        """`getPlayerAvailability` - GET /sports/{sport}/leagues/{league}/player-availability: Get normalized player availability"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/player-availability", query={"team": team, "status": status}, body=NOT_GIVEN, request_options=request_options)

    def get_player_availability_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        team: Optional[str] = None,
        since: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["AvailabilityTransition"]]:
        """`getPlayerAvailabilityHistory` - GET /sports/{sport}/leagues/{league}/player-availability/history: Get availability changes feed"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/player-availability/history", query={"team": team, "since": since, "status": status, "limit": limit}, body=NOT_GIVEN, request_options=request_options)

    def get_news(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        team: Optional[str] = None,
        athlete: Optional[str] = None,
        since: Optional[str] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["NewsArticle"]]:
        """`getNews` - GET /sports/{sport}/leagues/{league}/news: Get latest news"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/news", query={"limit": limit, "page": page, "team": team, "athlete": athlete, "since": since, "from": from_, "to": to}, body=NOT_GIVEN, request_options=request_options)

    def get_news_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        team: Optional[str] = None,
        athlete: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["NewsArticle"]]:
        """`getNewsHistory` - GET /sports/{sport}/leagues/{league}/news/history: Get archived news"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/news/history", query={"from": from_, "to": to, "team": team, "athlete": athlete, "limit": limit, "page": page}, body=NOT_GIVEN, request_options=request_options)

    def get_transactions(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        team: Optional[str] = None,
        season: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Transactions"]:
        """`getTransactions` - GET /sports/{sport}/leagues/{league}/transactions: Get transactions"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/transactions", query={"limit": limit, "page": page, "team": team, "season": season}, body=NOT_GIVEN, request_options=request_options)

    def get_current_season(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Season"]:
        """`getCurrentSeason` - GET /sports/{sport}/leagues/{league}/season: Get the active season"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/season", query=None, body=NOT_GIVEN, request_options=request_options)

    def list_seasons(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["SeasonSummary"]]:
        """`listSeasons` - GET /sports/{sport}/leagues/{league}/seasons: List seasons"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons", query={"limit": limit, "page": page}, body=NOT_GIVEN, request_options=request_options)

    def get_season(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Season"]:
        """`getSeason` - GET /sports/{sport}/leagues/{league}/seasons/{season}: Get a season"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_season_schedule(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        week: Optional[int] = None,
        season_type: Optional[Literal[1, 2, 3]] = None,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Event"]]:
        """`getSeasonSchedule` - GET /sports/{sport}/leagues/{league}/seasons/{season}/schedule: Get season schedule"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/schedule", query={"week": week, "seasonType": season_type, "includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    def list_season_weeks(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        season_type: Optional[Literal[1, 2, 3]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Week"]]:
        """`listSeasonWeeks` - GET /sports/{sport}/leagues/{league}/seasons/{season}/weeks: List weeks in a season"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/weeks", query={"seasonType": season_type}, body=NOT_GIVEN, request_options=request_options)

    def list_season_types(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["SeasonType"]]:
        """`listSeasonTypes` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types: List season types"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_season_type(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["SeasonType"]:
        """`getSeasonType` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}: Get a season type"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    def list_groups(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Group"]]:
        """`listGroups` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}/groups: List groups (conferences/divisions)"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}/groups", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_group(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        group_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Group"]:
        """`getGroup` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}/groups/{groupId}: Get a group"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}/groups/{_p(group_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    def list_group_teams(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        group_id: Union[str, int],
        *,
        page_size: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Team"]]:
        """`listGroupTeams` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}/groups/{groupId}/teams: List teams in a group"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}/groups/{_p(group_id)}/teams", query={"pageSize": page_size, "page": page}, body=NOT_GIVEN, request_options=request_options)

    def list_team_season_events(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        team_id: Union[str, int],
        *,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Event"]]:
        """`listTeamSeasonEvents` - GET /sports/{sport}/leagues/{league}/seasons/{season}/teams/{teamId}/events: List a team's events in a season"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/teams/{_p(team_id)}/events", query={"page": page, "pageSize": page_size, "limit": limit}, body=NOT_GIVEN, request_options=request_options)

    def get_tournament(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        round: Optional[str] = None,
        region: Optional[str] = None,
        first_four: Optional[bool] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["TournamentGame"]]:
        """`getTournament` - GET /sports/{sport}/leagues/{league}/seasons/{season}/tournament: Get NCAA tournament games"""
        return self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/tournament", query={"round": round, "region": region, "firstFour": first_four, "startDate": start_date, "endDate": end_date}, body=NOT_GIVEN, request_options=request_options)

    def list_webhooks(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Webhook"]]:
        """`listWebhooks` - GET /webhooks: List your webhooks"""
        return self._request_with_meta("GET", "/webhooks", query=None, body=NOT_GIVEN, request_options=request_options)

    def create_webhook(
        self,
        url: str,
        events: List["WebhookEventType"],
        *,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Webhook"]:
        """`createWebhook` - POST /webhooks: Create a webhook"""
        return self._request_with_meta("POST", "/webhooks", query=None, body={"url": url, "events": events, "leagues": leagues, "frequency": frequency, "active": active}, request_options=request_options)

    def get_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Webhook"]:
        """`getWebhook` - GET /webhooks/{webhookId}: Get a webhook"""
        return self._request_with_meta("GET", f"/webhooks/{_p(webhook_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    def update_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        url: Union[str, NotGiven] = NOT_GIVEN,
        events: Union[List["WebhookEventType"], NotGiven] = NOT_GIVEN,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Webhook"]:
        """`updateWebhook` - PATCH /webhooks/{webhookId}: Update a webhook"""
        return self._request_with_meta("PATCH", f"/webhooks/{_p(webhook_id)}", query=None, body={"url": url, "events": events, "leagues": leagues, "frequency": frequency, "active": active}, request_options=request_options)

    def delete_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`deleteWebhook` - DELETE /webhooks/{webhookId}: Delete a webhook"""
        return self._request_with_meta("DELETE", f"/webhooks/{_p(webhook_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    def get_webhook_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`getWebhookSecret` - GET /webhooks/{webhookId}/secret: Reveal the signing secret"""
        return self._request_with_meta("GET", f"/webhooks/{_p(webhook_id)}/secret", query=None, body=NOT_GIVEN, request_options=request_options)

    def rotate_webhook_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`rotateWebhookSecret` - POST /webhooks/{webhookId}/secret: Rotate the signing secret"""
        return self._request_with_meta("POST", f"/webhooks/{_p(webhook_id)}/secret", query=None, body=NOT_GIVEN, request_options=request_options)

    def test_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        event_type: Union["WebhookEventType", NotGiven] = NOT_GIVEN,
        delivery_id: Union[str, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`testWebhook` - POST /webhooks/{webhookId}/test: Send a test delivery"""
        return self._request_with_meta("POST", f"/webhooks/{_p(webhook_id)}/test", query=None, body={"eventType": event_type, "deliveryId": delivery_id}, request_options=request_options)

    def list_webhook_deliveries(
        self,
        webhook_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["WebhookDelivery"]]:
        """`listWebhookDeliveries` - GET /webhooks/{webhookId}/deliveries: List failed deliveries"""
        return self._request_with_meta("GET", f"/webhooks/{_p(webhook_id)}/deliveries", query={"limit": limit}, body=NOT_GIVEN, request_options=request_options)

    def create_websocket_token(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`createWebSocketToken` - POST /websocket/auth: Get a WebSocket token"""
        return self._request_with_meta("POST", self._websocket_auth_url, query=None, body=NOT_GIVEN, request_options=request_options)


class _AsyncWebhooks:
    """`client.webhooks` namespace (aliases of the `*_webhook*` methods)."""

    def __init__(self, parent: "_AsyncOperations") -> None:
        self._parent = parent

    async def list(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Webhook"]:
        """`listWebhooks` - GET /webhooks: List your webhooks"""
        return await self._parent.list_webhooks(request_options=request_options)

    async def create(
        self,
        url: str,
        events: List["WebhookEventType"],
        *,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> "Webhook":
        """`createWebhook` - POST /webhooks: Create a webhook"""
        return await self._parent.create_webhook(url, events, leagues=leagues, frequency=frequency, active=active, request_options=request_options)

    async def get(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "Webhook":
        """`getWebhook` - GET /webhooks/{webhookId}: Get a webhook"""
        return await self._parent.get_webhook(webhook_id, request_options=request_options)

    async def update(
        self,
        webhook_id: Union[str, int],
        *,
        url: Union[str, NotGiven] = NOT_GIVEN,
        events: Union[List["WebhookEventType"], NotGiven] = NOT_GIVEN,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> "Webhook":
        """`updateWebhook` - PATCH /webhooks/{webhookId}: Update a webhook"""
        return await self._parent.update_webhook(webhook_id, url=url, events=events, leagues=leagues, frequency=frequency, active=active, request_options=request_options)

    async def delete(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`deleteWebhook` - DELETE /webhooks/{webhookId}: Delete a webhook"""
        return await self._parent.delete_webhook(webhook_id, request_options=request_options)

    async def get_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`getWebhookSecret` - GET /webhooks/{webhookId}/secret: Reveal the signing secret"""
        return await self._parent.get_webhook_secret(webhook_id, request_options=request_options)

    async def rotate_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`rotateWebhookSecret` - POST /webhooks/{webhookId}/secret: Rotate the signing secret"""
        return await self._parent.rotate_webhook_secret(webhook_id, request_options=request_options)

    async def test(
        self,
        webhook_id: Union[str, int],
        *,
        event_type: Union["WebhookEventType", NotGiven] = NOT_GIVEN,
        delivery_id: Union[str, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`testWebhook` - POST /webhooks/{webhookId}/test: Send a test delivery"""
        return await self._parent.test_webhook(webhook_id, event_type=event_type, delivery_id=delivery_id, request_options=request_options)

    async def deliveries(
        self,
        webhook_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["WebhookDelivery"]:
        """`listWebhookDeliveries` - GET /webhooks/{webhookId}/deliveries: List failed deliveries"""
        return await self._parent.list_webhook_deliveries(webhook_id, limit=limit, request_options=request_options)


class _AsyncOperations:
    """Generated API methods. Mixed into the client classes."""

    _websocket_auth_url: str

    async def _request_data(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:  # pragma: no cover
        raise NotImplementedError

    async def _request_with_meta(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:  # pragma: no cover
        raise NotImplementedError

    @property
    def webhooks(self) -> _AsyncWebhooks:
        """Webhook management: list/create/get/update/delete/get_secret/rotate_secret/test/deliveries."""
        return _AsyncWebhooks(self)

    async def list_sports(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Sport"]:
        """`listSports` - GET /sports: List sports"""
        return await self._request_data("GET", "/sports", query=None, body=NOT_GIVEN, request_options=request_options)

    async def list_leagues(
        self,
        sport: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List["League"]:
        """`listLeagues` - GET /sports/{sport}/leagues: List leagues for a sport"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_league(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "LeagueDetail":
        """`getLeague` - GET /sports/{sport}/leagues/{league}: Get league details"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}", query=None, body=NOT_GIVEN, request_options=request_options)

    async def list_events(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Event"]:
        """`listEvents` - GET /sports/{sport}/leagues/{league}/events: List events for a league"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events", query={"limit": limit, "includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    async def list_live_events(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Event"]:
        """`listLiveEvents` - GET /sports/{sport}/leagues/{league}/events/live: List live events"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/live", query={"includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    async def get_event(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "Event":
        """`getEvent` - GET /sports/{sport}/leagues/{league}/events/{eventId}: Get an event"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}", query={"includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    async def get_event_box_score(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "BoxScore":
        """`getEventBoxScore` - GET /sports/{sport}/leagues/{league}/events/{eventId}/boxscore: Get box score"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/boxscore", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_event_win_probability(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        drives: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "WinProbability":
        """`getEventWinProbability` - GET /sports/{sport}/leagues/{league}/events/{eventId}/winprobability: Get win probability"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/winprobability", query={"drives": drives}, body=NOT_GIVEN, request_options=request_options)

    async def get_event_roster(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        team: Optional[str] = None,
        starters: Optional[bool] = None,
        enrich: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "GameRoster":
        """`getEventRoster` - GET /sports/{sport}/leagues/{league}/events/{eventId}/roster: Get game rosters"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/roster", query={"team": team, "starters": starters, "enrich": enrich}, body=NOT_GIVEN, request_options=request_options)

    async def list_plays(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        enrich: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Play"]:
        """`listPlays` - GET /sports/{sport}/leagues/{league}/events/{eventId}/plays: Get play-by-play"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/plays", query={"limit": limit, "page": page, "enrich": enrich}, body=NOT_GIVEN, request_options=request_options)

    async def list_penalties(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        enrich: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Play"]:
        """`listPenalties` - GET /sports/{sport}/leagues/{league}/events/{eventId}/penalties: Get penalty plays"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/penalties", query={"enrich": enrich}, body=NOT_GIVEN, request_options=request_options)

    async def get_event_odds(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Optional["Odds"]:
        """`getEventOdds` - GET /sports/{sport}/leagues/{league}/events/{eventId}/odds: Get current odds"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/odds", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_event_odds_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["OddsHistoryEntry"]:
        """`getEventOddsHistory` - GET /sports/{sport}/leagues/{league}/events/{eventId}/odds/history: Get odds history"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/odds/history", query={"limit": limit}, body=NOT_GIVEN, request_options=request_options)

    async def list_teams(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Team"]:
        """`listTeams` - GET /sports/{sport}/leagues/{league}/teams: List teams"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams", query={"limit": limit, "page": page}, body=NOT_GIVEN, request_options=request_options)

    async def get_team(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        team_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "Team":
        """`getTeam` - GET /sports/{sport}/leagues/{league}/teams/{teamId}: Get a team"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams/{_p(team_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_team_roster(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        team_id: Union[str, int],
        *,
        season: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "Roster":
        """`getTeamRoster` - GET /sports/{sport}/leagues/{league}/teams/{teamId}/roster: Get team roster"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams/{_p(team_id)}/roster", query={"season": season}, body=NOT_GIVEN, request_options=request_options)

    async def get_team_depth_chart(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        team_id: Union[str, int],
        *,
        season: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "DepthChart":
        """`getTeamDepthChart` - GET /sports/{sport}/leagues/{league}/teams/{teamId}/depthchart: Get depth chart"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams/{_p(team_id)}/depthchart", query={"season": season}, body=NOT_GIVEN, request_options=request_options)

    async def list_athletes(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        include: Optional[Literal["statistics"]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Athlete"]:
        """`listAthletes` - GET /sports/{sport}/leagues/{league}/athletes: List athletes"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes", query={"limit": limit, "page": page, "include": include}, body=NOT_GIVEN, request_options=request_options)

    async def search_athletes(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        query: str,
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["AthleteSearchResult"]:
        """`searchAthletes` - GET /sports/{sport}/leagues/{league}/athletes/search: Search athletes by name"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/search", query={"query": query, "limit": limit}, body=NOT_GIVEN, request_options=request_options)

    async def get_athlete(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        athlete_id: Union[str, int],
        *,
        season: Optional[int] = None,
        season_type: Optional[Literal[1, 2, 3]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "Athlete":
        """`getAthlete` - GET /sports/{sport}/leagues/{league}/athletes/{athleteId}: Get an athlete"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/{_p(athlete_id)}", query={"season": season, "seasonType": season_type}, body=NOT_GIVEN, request_options=request_options)

    async def get_athlete_game_log(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        athlete_id: Union[str, int],
        season: int,
        *,
        week: Optional[int] = None,
        season_type: Optional[Literal[1, 2, 3]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["GameLogEntry"]:
        """`getAthleteGameLog` - GET /sports/{sport}/leagues/{league}/athletes/{athleteId}/gamelog: Get athlete game log"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/{_p(athlete_id)}/gamelog", query={"season": season, "week": week, "seasonType": season_type}, body=NOT_GIVEN, request_options=request_options)

    async def get_athlete_availability_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        athlete_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`getAthleteAvailabilityHistory` - GET /sports/{sport}/leagues/{league}/athletes/{athleteId}/availability-history: Get athlete availability history"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/{_p(athlete_id)}/availability-history", query={"limit": limit, "from": from_, "to": to}, body=NOT_GIVEN, request_options=request_options)

    async def get_injuries(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        team: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "InjuryReport":
        """`getInjuries` - GET /sports/{sport}/leagues/{league}/injuries: Get injury report"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/injuries", query={"team": team}, body=NOT_GIVEN, request_options=request_options)

    async def get_player_availability(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        team: Optional[str] = None,
        status: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "PlayerAvailabilityReport":
        """`getPlayerAvailability` - GET /sports/{sport}/leagues/{league}/player-availability: Get normalized player availability"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/player-availability", query={"team": team, "status": status}, body=NOT_GIVEN, request_options=request_options)

    async def get_player_availability_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        team: Optional[str] = None,
        since: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["AvailabilityTransition"]:
        """`getPlayerAvailabilityHistory` - GET /sports/{sport}/leagues/{league}/player-availability/history: Get availability changes feed"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/player-availability/history", query={"team": team, "since": since, "status": status, "limit": limit}, body=NOT_GIVEN, request_options=request_options)

    async def get_news(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        team: Optional[str] = None,
        athlete: Optional[str] = None,
        since: Optional[str] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["NewsArticle"]:
        """`getNews` - GET /sports/{sport}/leagues/{league}/news: Get latest news"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/news", query={"limit": limit, "page": page, "team": team, "athlete": athlete, "since": since, "from": from_, "to": to}, body=NOT_GIVEN, request_options=request_options)

    async def get_news_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        team: Optional[str] = None,
        athlete: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["NewsArticle"]:
        """`getNewsHistory` - GET /sports/{sport}/leagues/{league}/news/history: Get archived news"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/news/history", query={"from": from_, "to": to, "team": team, "athlete": athlete, "limit": limit, "page": page}, body=NOT_GIVEN, request_options=request_options)

    async def get_transactions(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        team: Optional[str] = None,
        season: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> "Transactions":
        """`getTransactions` - GET /sports/{sport}/leagues/{league}/transactions: Get transactions"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/transactions", query={"limit": limit, "page": page, "team": team, "season": season}, body=NOT_GIVEN, request_options=request_options)

    async def get_current_season(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "Season":
        """`getCurrentSeason` - GET /sports/{sport}/leagues/{league}/season: Get the active season"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/season", query=None, body=NOT_GIVEN, request_options=request_options)

    async def list_seasons(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["SeasonSummary"]:
        """`listSeasons` - GET /sports/{sport}/leagues/{league}/seasons: List seasons"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons", query={"limit": limit, "page": page}, body=NOT_GIVEN, request_options=request_options)

    async def get_season(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "Season":
        """`getSeason` - GET /sports/{sport}/leagues/{league}/seasons/{season}: Get a season"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_season_schedule(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        week: Optional[int] = None,
        season_type: Optional[Literal[1, 2, 3]] = None,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Event"]:
        """`getSeasonSchedule` - GET /sports/{sport}/leagues/{league}/seasons/{season}/schedule: Get season schedule"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/schedule", query={"week": week, "seasonType": season_type, "includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    async def list_season_weeks(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        season_type: Optional[Literal[1, 2, 3]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Week"]:
        """`listSeasonWeeks` - GET /sports/{sport}/leagues/{league}/seasons/{season}/weeks: List weeks in a season"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/weeks", query={"seasonType": season_type}, body=NOT_GIVEN, request_options=request_options)

    async def list_season_types(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List["SeasonType"]:
        """`listSeasonTypes` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types: List season types"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_season_type(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "SeasonType":
        """`getSeasonType` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}: Get a season type"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    async def list_groups(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Group"]:
        """`listGroups` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}/groups: List groups (conferences/divisions)"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}/groups", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_group(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        group_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "Group":
        """`getGroup` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}/groups/{groupId}: Get a group"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}/groups/{_p(group_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    async def list_group_teams(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        group_id: Union[str, int],
        *,
        page_size: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Team"]:
        """`listGroupTeams` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}/groups/{groupId}/teams: List teams in a group"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}/groups/{_p(group_id)}/teams", query={"pageSize": page_size, "page": page}, body=NOT_GIVEN, request_options=request_options)

    async def list_team_season_events(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        team_id: Union[str, int],
        *,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Event"]:
        """`listTeamSeasonEvents` - GET /sports/{sport}/leagues/{league}/seasons/{season}/teams/{teamId}/events: List a team's events in a season"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/teams/{_p(team_id)}/events", query={"page": page, "pageSize": page_size, "limit": limit}, body=NOT_GIVEN, request_options=request_options)

    async def get_tournament(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        round: Optional[str] = None,
        region: Optional[str] = None,
        first_four: Optional[bool] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["TournamentGame"]:
        """`getTournament` - GET /sports/{sport}/leagues/{league}/seasons/{season}/tournament: Get NCAA tournament games"""
        return await self._request_data("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/tournament", query={"round": round, "region": region, "firstFour": first_four, "startDate": start_date, "endDate": end_date}, body=NOT_GIVEN, request_options=request_options)

    async def list_webhooks(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List["Webhook"]:
        """`listWebhooks` - GET /webhooks: List your webhooks"""
        return await self._request_data("GET", "/webhooks", query=None, body=NOT_GIVEN, request_options=request_options)

    async def create_webhook(
        self,
        url: str,
        events: List["WebhookEventType"],
        *,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> "Webhook":
        """`createWebhook` - POST /webhooks: Create a webhook"""
        return await self._request_data("POST", "/webhooks", query=None, body={"url": url, "events": events, "leagues": leagues, "frequency": frequency, "active": active}, request_options=request_options)

    async def get_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> "Webhook":
        """`getWebhook` - GET /webhooks/{webhookId}: Get a webhook"""
        return await self._request_data("GET", f"/webhooks/{_p(webhook_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    async def update_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        url: Union[str, NotGiven] = NOT_GIVEN,
        events: Union[List["WebhookEventType"], NotGiven] = NOT_GIVEN,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> "Webhook":
        """`updateWebhook` - PATCH /webhooks/{webhookId}: Update a webhook"""
        return await self._request_data("PATCH", f"/webhooks/{_p(webhook_id)}", query=None, body={"url": url, "events": events, "leagues": leagues, "frequency": frequency, "active": active}, request_options=request_options)

    async def delete_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`deleteWebhook` - DELETE /webhooks/{webhookId}: Delete a webhook"""
        return await self._request_data("DELETE", f"/webhooks/{_p(webhook_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_webhook_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`getWebhookSecret` - GET /webhooks/{webhookId}/secret: Reveal the signing secret"""
        return await self._request_data("GET", f"/webhooks/{_p(webhook_id)}/secret", query=None, body=NOT_GIVEN, request_options=request_options)

    async def rotate_webhook_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`rotateWebhookSecret` - POST /webhooks/{webhookId}/secret: Rotate the signing secret"""
        return await self._request_data("POST", f"/webhooks/{_p(webhook_id)}/secret", query=None, body=NOT_GIVEN, request_options=request_options)

    async def test_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        event_type: Union["WebhookEventType", NotGiven] = NOT_GIVEN,
        delivery_id: Union[str, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`testWebhook` - POST /webhooks/{webhookId}/test: Send a test delivery"""
        return await self._request_data("POST", f"/webhooks/{_p(webhook_id)}/test", query=None, body={"eventType": event_type, "deliveryId": delivery_id}, request_options=request_options)

    async def list_webhook_deliveries(
        self,
        webhook_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> List["WebhookDelivery"]:
        """`listWebhookDeliveries` - GET /webhooks/{webhookId}/deliveries: List failed deliveries"""
        return await self._request_data("GET", f"/webhooks/{_p(webhook_id)}/deliveries", query={"limit": limit}, body=NOT_GIVEN, request_options=request_options)

    async def create_websocket_token(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """`createWebSocketToken` - POST /websocket/auth: Get a WebSocket token"""
        return await self._request_data("POST", self._websocket_auth_url, query=None, body=NOT_GIVEN, request_options=request_options)


class _AsyncWebhooksWithMeta:
    """`client.webhooks` namespace (aliases of the `*_webhook*` methods)."""

    def __init__(self, parent: "_AsyncOperationsWithMeta") -> None:
        self._parent = parent

    async def list(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Webhook"]]:
        """`listWebhooks` - GET /webhooks: List your webhooks"""
        return await self._parent.list_webhooks(request_options=request_options)

    async def create(
        self,
        url: str,
        events: List["WebhookEventType"],
        *,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Webhook"]:
        """`createWebhook` - POST /webhooks: Create a webhook"""
        return await self._parent.create_webhook(url, events, leagues=leagues, frequency=frequency, active=active, request_options=request_options)

    async def get(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Webhook"]:
        """`getWebhook` - GET /webhooks/{webhookId}: Get a webhook"""
        return await self._parent.get_webhook(webhook_id, request_options=request_options)

    async def update(
        self,
        webhook_id: Union[str, int],
        *,
        url: Union[str, NotGiven] = NOT_GIVEN,
        events: Union[List["WebhookEventType"], NotGiven] = NOT_GIVEN,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Webhook"]:
        """`updateWebhook` - PATCH /webhooks/{webhookId}: Update a webhook"""
        return await self._parent.update_webhook(webhook_id, url=url, events=events, leagues=leagues, frequency=frequency, active=active, request_options=request_options)

    async def delete(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`deleteWebhook` - DELETE /webhooks/{webhookId}: Delete a webhook"""
        return await self._parent.delete_webhook(webhook_id, request_options=request_options)

    async def get_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`getWebhookSecret` - GET /webhooks/{webhookId}/secret: Reveal the signing secret"""
        return await self._parent.get_webhook_secret(webhook_id, request_options=request_options)

    async def rotate_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`rotateWebhookSecret` - POST /webhooks/{webhookId}/secret: Rotate the signing secret"""
        return await self._parent.rotate_webhook_secret(webhook_id, request_options=request_options)

    async def test(
        self,
        webhook_id: Union[str, int],
        *,
        event_type: Union["WebhookEventType", NotGiven] = NOT_GIVEN,
        delivery_id: Union[str, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`testWebhook` - POST /webhooks/{webhookId}/test: Send a test delivery"""
        return await self._parent.test_webhook(webhook_id, event_type=event_type, delivery_id=delivery_id, request_options=request_options)

    async def deliveries(
        self,
        webhook_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["WebhookDelivery"]]:
        """`listWebhookDeliveries` - GET /webhooks/{webhookId}/deliveries: List failed deliveries"""
        return await self._parent.list_webhook_deliveries(webhook_id, limit=limit, request_options=request_options)


class _AsyncOperationsWithMeta:
    """Generated API methods. Mixed into the client classes."""

    _websocket_auth_url: str

    async def _request_data(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:  # pragma: no cover
        raise NotImplementedError

    async def _request_with_meta(self, method: str, path: str, *, query: Any, body: Any, request_options: Any) -> Any:  # pragma: no cover
        raise NotImplementedError

    @property
    def webhooks(self) -> _AsyncWebhooksWithMeta:
        """Webhook management: list/create/get/update/delete/get_secret/rotate_secret/test/deliveries."""
        return _AsyncWebhooksWithMeta(self)

    async def list_sports(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Sport"]]:
        """`listSports` - GET /sports: List sports"""
        return await self._request_with_meta("GET", "/sports", query=None, body=NOT_GIVEN, request_options=request_options)

    async def list_leagues(
        self,
        sport: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["League"]]:
        """`listLeagues` - GET /sports/{sport}/leagues: List leagues for a sport"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_league(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["LeagueDetail"]:
        """`getLeague` - GET /sports/{sport}/leagues/{league}: Get league details"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}", query=None, body=NOT_GIVEN, request_options=request_options)

    async def list_events(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Event"]]:
        """`listEvents` - GET /sports/{sport}/leagues/{league}/events: List events for a league"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events", query={"limit": limit, "includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    async def list_live_events(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Event"]]:
        """`listLiveEvents` - GET /sports/{sport}/leagues/{league}/events/live: List live events"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/live", query={"includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    async def get_event(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Event"]:
        """`getEvent` - GET /sports/{sport}/leagues/{league}/events/{eventId}: Get an event"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}", query={"includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    async def get_event_box_score(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["BoxScore"]:
        """`getEventBoxScore` - GET /sports/{sport}/leagues/{league}/events/{eventId}/boxscore: Get box score"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/boxscore", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_event_win_probability(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        drives: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["WinProbability"]:
        """`getEventWinProbability` - GET /sports/{sport}/leagues/{league}/events/{eventId}/winprobability: Get win probability"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/winprobability", query={"drives": drives}, body=NOT_GIVEN, request_options=request_options)

    async def get_event_roster(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        team: Optional[str] = None,
        starters: Optional[bool] = None,
        enrich: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["GameRoster"]:
        """`getEventRoster` - GET /sports/{sport}/leagues/{league}/events/{eventId}/roster: Get game rosters"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/roster", query={"team": team, "starters": starters, "enrich": enrich}, body=NOT_GIVEN, request_options=request_options)

    async def list_plays(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        enrich: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Play"]]:
        """`listPlays` - GET /sports/{sport}/leagues/{league}/events/{eventId}/plays: Get play-by-play"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/plays", query={"limit": limit, "page": page, "enrich": enrich}, body=NOT_GIVEN, request_options=request_options)

    async def list_penalties(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        enrich: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Play"]]:
        """`listPenalties` - GET /sports/{sport}/leagues/{league}/events/{eventId}/penalties: Get penalty plays"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/penalties", query={"enrich": enrich}, body=NOT_GIVEN, request_options=request_options)

    async def get_event_odds(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Optional["Odds"]]:
        """`getEventOdds` - GET /sports/{sport}/leagues/{league}/events/{eventId}/odds: Get current odds"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/odds", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_event_odds_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        event_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["OddsHistoryEntry"]]:
        """`getEventOddsHistory` - GET /sports/{sport}/leagues/{league}/events/{eventId}/odds/history: Get odds history"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/events/{_p(event_id)}/odds/history", query={"limit": limit}, body=NOT_GIVEN, request_options=request_options)

    async def list_teams(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Team"]]:
        """`listTeams` - GET /sports/{sport}/leagues/{league}/teams: List teams"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams", query={"limit": limit, "page": page}, body=NOT_GIVEN, request_options=request_options)

    async def get_team(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        team_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Team"]:
        """`getTeam` - GET /sports/{sport}/leagues/{league}/teams/{teamId}: Get a team"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams/{_p(team_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_team_roster(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        team_id: Union[str, int],
        *,
        season: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Roster"]:
        """`getTeamRoster` - GET /sports/{sport}/leagues/{league}/teams/{teamId}/roster: Get team roster"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams/{_p(team_id)}/roster", query={"season": season}, body=NOT_GIVEN, request_options=request_options)

    async def get_team_depth_chart(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        team_id: Union[str, int],
        *,
        season: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["DepthChart"]:
        """`getTeamDepthChart` - GET /sports/{sport}/leagues/{league}/teams/{teamId}/depthchart: Get depth chart"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/teams/{_p(team_id)}/depthchart", query={"season": season}, body=NOT_GIVEN, request_options=request_options)

    async def list_athletes(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        include: Optional[Literal["statistics"]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Athlete"]]:
        """`listAthletes` - GET /sports/{sport}/leagues/{league}/athletes: List athletes"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes", query={"limit": limit, "page": page, "include": include}, body=NOT_GIVEN, request_options=request_options)

    async def search_athletes(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        query: str,
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["AthleteSearchResult"]]:
        """`searchAthletes` - GET /sports/{sport}/leagues/{league}/athletes/search: Search athletes by name"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/search", query={"query": query, "limit": limit}, body=NOT_GIVEN, request_options=request_options)

    async def get_athlete(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        athlete_id: Union[str, int],
        *,
        season: Optional[int] = None,
        season_type: Optional[Literal[1, 2, 3]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Athlete"]:
        """`getAthlete` - GET /sports/{sport}/leagues/{league}/athletes/{athleteId}: Get an athlete"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/{_p(athlete_id)}", query={"season": season, "seasonType": season_type}, body=NOT_GIVEN, request_options=request_options)

    async def get_athlete_game_log(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        athlete_id: Union[str, int],
        season: int,
        *,
        week: Optional[int] = None,
        season_type: Optional[Literal[1, 2, 3]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["GameLogEntry"]]:
        """`getAthleteGameLog` - GET /sports/{sport}/leagues/{league}/athletes/{athleteId}/gamelog: Get athlete game log"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/{_p(athlete_id)}/gamelog", query={"season": season, "week": week, "seasonType": season_type}, body=NOT_GIVEN, request_options=request_options)

    async def get_athlete_availability_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        athlete_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`getAthleteAvailabilityHistory` - GET /sports/{sport}/leagues/{league}/athletes/{athleteId}/availability-history: Get athlete availability history"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/athletes/{_p(athlete_id)}/availability-history", query={"limit": limit, "from": from_, "to": to}, body=NOT_GIVEN, request_options=request_options)

    async def get_injuries(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        team: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["InjuryReport"]:
        """`getInjuries` - GET /sports/{sport}/leagues/{league}/injuries: Get injury report"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/injuries", query={"team": team}, body=NOT_GIVEN, request_options=request_options)

    async def get_player_availability(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        team: Optional[str] = None,
        status: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["PlayerAvailabilityReport"]:
        """`getPlayerAvailability` - GET /sports/{sport}/leagues/{league}/player-availability: Get normalized player availability"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/player-availability", query={"team": team, "status": status}, body=NOT_GIVEN, request_options=request_options)

    async def get_player_availability_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        team: Optional[str] = None,
        since: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["AvailabilityTransition"]]:
        """`getPlayerAvailabilityHistory` - GET /sports/{sport}/leagues/{league}/player-availability/history: Get availability changes feed"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/player-availability/history", query={"team": team, "since": since, "status": status, "limit": limit}, body=NOT_GIVEN, request_options=request_options)

    async def get_news(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        team: Optional[str] = None,
        athlete: Optional[str] = None,
        since: Optional[str] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["NewsArticle"]]:
        """`getNews` - GET /sports/{sport}/leagues/{league}/news: Get latest news"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/news", query={"limit": limit, "page": page, "team": team, "athlete": athlete, "since": since, "from": from_, "to": to}, body=NOT_GIVEN, request_options=request_options)

    async def get_news_history(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        team: Optional[str] = None,
        athlete: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["NewsArticle"]]:
        """`getNewsHistory` - GET /sports/{sport}/leagues/{league}/news/history: Get archived news"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/news/history", query={"from": from_, "to": to, "team": team, "athlete": athlete, "limit": limit, "page": page}, body=NOT_GIVEN, request_options=request_options)

    async def get_transactions(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        team: Optional[str] = None,
        season: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Transactions"]:
        """`getTransactions` - GET /sports/{sport}/leagues/{league}/transactions: Get transactions"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/transactions", query={"limit": limit, "page": page, "team": team, "season": season}, body=NOT_GIVEN, request_options=request_options)

    async def get_current_season(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Season"]:
        """`getCurrentSeason` - GET /sports/{sport}/leagues/{league}/season: Get the active season"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/season", query=None, body=NOT_GIVEN, request_options=request_options)

    async def list_seasons(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["SeasonSummary"]]:
        """`listSeasons` - GET /sports/{sport}/leagues/{league}/seasons: List seasons"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons", query={"limit": limit, "page": page}, body=NOT_GIVEN, request_options=request_options)

    async def get_season(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Season"]:
        """`getSeason` - GET /sports/{sport}/leagues/{league}/seasons/{season}: Get a season"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_season_schedule(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        week: Optional[int] = None,
        season_type: Optional[Literal[1, 2, 3]] = None,
        include_odds: Optional[bool] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Event"]]:
        """`getSeasonSchedule` - GET /sports/{sport}/leagues/{league}/seasons/{season}/schedule: Get season schedule"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/schedule", query={"week": week, "seasonType": season_type, "includeOdds": include_odds}, body=NOT_GIVEN, request_options=request_options)

    async def list_season_weeks(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        season_type: Optional[Literal[1, 2, 3]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Week"]]:
        """`listSeasonWeeks` - GET /sports/{sport}/leagues/{league}/seasons/{season}/weeks: List weeks in a season"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/weeks", query={"seasonType": season_type}, body=NOT_GIVEN, request_options=request_options)

    async def list_season_types(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["SeasonType"]]:
        """`listSeasonTypes` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types: List season types"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_season_type(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["SeasonType"]:
        """`getSeasonType` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}: Get a season type"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    async def list_groups(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Group"]]:
        """`listGroups` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}/groups: List groups (conferences/divisions)"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}/groups", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_group(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        group_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Group"]:
        """`getGroup` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}/groups/{groupId}: Get a group"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}/groups/{_p(group_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    async def list_group_teams(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        type_id: Union[str, int],
        group_id: Union[str, int],
        *,
        page_size: Optional[int] = None,
        page: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Team"]]:
        """`listGroupTeams` - GET /sports/{sport}/leagues/{league}/seasons/{season}/types/{typeId}/groups/{groupId}/teams: List teams in a group"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/types/{_p(type_id)}/groups/{_p(group_id)}/teams", query={"pageSize": page_size, "page": page}, body=NOT_GIVEN, request_options=request_options)

    async def list_team_season_events(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        team_id: Union[str, int],
        *,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Event"]]:
        """`listTeamSeasonEvents` - GET /sports/{sport}/leagues/{league}/seasons/{season}/teams/{teamId}/events: List a team's events in a season"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/teams/{_p(team_id)}/events", query={"page": page, "pageSize": page_size, "limit": limit}, body=NOT_GIVEN, request_options=request_options)

    async def get_tournament(
        self,
        sport: Union[str, int],
        league: Union[str, int],
        season: Union[str, int],
        *,
        round: Optional[str] = None,
        region: Optional[str] = None,
        first_four: Optional[bool] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["TournamentGame"]]:
        """`getTournament` - GET /sports/{sport}/leagues/{league}/seasons/{season}/tournament: Get NCAA tournament games"""
        return await self._request_with_meta("GET", f"/sports/{_p(sport)}/leagues/{_p(league)}/seasons/{_p(season)}/tournament", query={"round": round, "region": region, "firstFour": first_four, "startDate": start_date, "endDate": end_date}, body=NOT_GIVEN, request_options=request_options)

    async def list_webhooks(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["Webhook"]]:
        """`listWebhooks` - GET /webhooks: List your webhooks"""
        return await self._request_with_meta("GET", "/webhooks", query=None, body=NOT_GIVEN, request_options=request_options)

    async def create_webhook(
        self,
        url: str,
        events: List["WebhookEventType"],
        *,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Webhook"]:
        """`createWebhook` - POST /webhooks: Create a webhook"""
        return await self._request_with_meta("POST", "/webhooks", query=None, body={"url": url, "events": events, "leagues": leagues, "frequency": frequency, "active": active}, request_options=request_options)

    async def get_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Webhook"]:
        """`getWebhook` - GET /webhooks/{webhookId}: Get a webhook"""
        return await self._request_with_meta("GET", f"/webhooks/{_p(webhook_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    async def update_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        url: Union[str, NotGiven] = NOT_GIVEN,
        events: Union[List["WebhookEventType"], NotGiven] = NOT_GIVEN,
        leagues: Union[Optional[List[str]], NotGiven] = NOT_GIVEN,
        frequency: Union["WebhookFrequency", NotGiven] = NOT_GIVEN,
        active: Union[bool, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse["Webhook"]:
        """`updateWebhook` - PATCH /webhooks/{webhookId}: Update a webhook"""
        return await self._request_with_meta("PATCH", f"/webhooks/{_p(webhook_id)}", query=None, body={"url": url, "events": events, "leagues": leagues, "frequency": frequency, "active": active}, request_options=request_options)

    async def delete_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`deleteWebhook` - DELETE /webhooks/{webhookId}: Delete a webhook"""
        return await self._request_with_meta("DELETE", f"/webhooks/{_p(webhook_id)}", query=None, body=NOT_GIVEN, request_options=request_options)

    async def get_webhook_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`getWebhookSecret` - GET /webhooks/{webhookId}/secret: Reveal the signing secret"""
        return await self._request_with_meta("GET", f"/webhooks/{_p(webhook_id)}/secret", query=None, body=NOT_GIVEN, request_options=request_options)

    async def rotate_webhook_secret(
        self,
        webhook_id: Union[str, int],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`rotateWebhookSecret` - POST /webhooks/{webhookId}/secret: Rotate the signing secret"""
        return await self._request_with_meta("POST", f"/webhooks/{_p(webhook_id)}/secret", query=None, body=NOT_GIVEN, request_options=request_options)

    async def test_webhook(
        self,
        webhook_id: Union[str, int],
        *,
        event_type: Union["WebhookEventType", NotGiven] = NOT_GIVEN,
        delivery_id: Union[str, NotGiven] = NOT_GIVEN,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`testWebhook` - POST /webhooks/{webhookId}/test: Send a test delivery"""
        return await self._request_with_meta("POST", f"/webhooks/{_p(webhook_id)}/test", query=None, body={"eventType": event_type, "deliveryId": delivery_id}, request_options=request_options)

    async def list_webhook_deliveries(
        self,
        webhook_id: Union[str, int],
        *,
        limit: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[List["WebhookDelivery"]]:
        """`listWebhookDeliveries` - GET /webhooks/{webhookId}/deliveries: List failed deliveries"""
        return await self._request_with_meta("GET", f"/webhooks/{_p(webhook_id)}/deliveries", query={"limit": limit}, body=NOT_GIVEN, request_options=request_options)

    async def create_websocket_token(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> ApiResponse[Dict[str, Any]]:
        """`createWebSocketToken` - POST /websocket/auth: Get a WebSocket token"""
        return await self._request_with_meta("POST", self._websocket_auth_url, query=None, body=NOT_GIVEN, request_options=request_options)


OPERATION_IDS = ["listSports", "listLeagues", "getLeague", "listEvents", "listLiveEvents", "getEvent", "getEventBoxScore", "getEventWinProbability", "getEventRoster", "listPlays", "listPenalties", "getEventOdds", "getEventOddsHistory", "listTeams", "getTeam", "getTeamRoster", "getTeamDepthChart", "listAthletes", "searchAthletes", "getAthlete", "getAthleteGameLog", "getAthleteAvailabilityHistory", "getInjuries", "getPlayerAvailability", "getPlayerAvailabilityHistory", "getNews", "getNewsHistory", "getTransactions", "getCurrentSeason", "listSeasons", "getSeason", "getSeasonSchedule", "listSeasonWeeks", "listSeasonTypes", "getSeasonType", "listGroups", "getGroup", "listGroupTeams", "listTeamSeasonEvents", "getTournament", "listWebhooks", "createWebhook", "getWebhook", "updateWebhook", "deleteWebhook", "getWebhookSecret", "rotateWebhookSecret", "testWebhook", "listWebhookDeliveries", "createWebSocketToken"]
