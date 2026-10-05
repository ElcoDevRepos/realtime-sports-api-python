"""Typed models generated from the Realtime Sports API OpenAPI spec. Do not edit by hand.

Regenerate with `python scripts/generate.py`. Every TypedDict is `total=False`: the API may omit
fields, so read them with `.get()` when in doubt. Nested inline objects are typed as plain dicts.
"""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict


class ErrorBody(TypedDict, total=False):
    success: bool
    error: Dict[str, Any]


class RateLimit(TypedDict, total=False):
    limit: int
    remaining: int
    reset: int


class Pagination(TypedDict, total=False):
    page: int
    pageSize: int
    total: int
    totalPages: int
    pageCount: int
    hasNextPage: bool
    hasPreviousPage: bool


class Sport(TypedDict, total=False):
    id: str
    name: str
    slug: str
    displayName: str


class League(TypedDict, total=False):
    id: str
    name: str
    slug: str
    abbreviation: str
    shortName: str
    isTournament: bool
    currentSeason: int


class LeagueDetail(TypedDict, total=False):
    id: str
    name: str
    displayName: str
    abbreviation: str
    shortName: str
    slug: str
    currentSeason: Dict[str, Any]
    endpoints: Dict[str, Any]


class EventTeam(TypedDict, total=False):
    id: str
    name: str
    abbreviation: str
    logo: Optional[str]
    color: str
    alternateColor: str
    winner: bool
    record: str
    score: int


class EventStatus(TypedDict, total=False):
    state: Literal["pre", "in", "post"]
    completed: bool
    period: int
    clock: str
    detail: str
    halftime: bool
    firstHalfEnded: bool


class Event(TypedDict, total=False):
    id: str
    uid: str
    name: str
    shortName: str
    date: str
    status: "EventStatus"
    homeTeam: "EventTeam"
    awayTeam: "EventTeam"
    competition: Dict[str, Any]
    venue: Optional[Dict[str, Any]]
    notes: List[str]
    season: Dict[str, Any]
    broadcasts: List[Dict[str, Any]]
    officials: List[Dict[str, Any]]
    odds: "Odds"


class PlayAthlete(TypedDict, total=False):
    id: str
    name: str
    displayName: str
    shortName: str
    position: str
    team: Dict[str, Any]
    role: str
    type: str
    order: int


class Play(TypedDict, total=False):
    id: str
    sequenceNumber: str
    text: str
    shortText: str
    alternativeText: str
    type: Dict[str, Any]
    period: int
    clock: Dict[str, Any]
    wallClock: str
    homeScore: int
    awayScore: int
    scoringPlay: bool
    scoreValue: int
    scoringType: str
    situation: Optional[Dict[str, Any]]
    endSituation: Optional[Dict[str, Any]]
    yardsGained: int
    teamId: str
    athletes: List["PlayAthlete"]
    priority: bool
    modified: str


class Odds(TypedDict, total=False):
    provider: str
    spread: Optional[Dict[str, Any]]
    moneyline: Optional[Dict[str, Any]]
    overUnder: Optional[Dict[str, Any]]
    updatedAt: str


class OddsHistoryEntry(TypedDict, total=False):
    odds: "Odds"
    timestamp: str
    changeType: List[str]


class BoxScore(TypedDict, total=False):
    homeTeam: Dict[str, Any]
    awayTeam: Dict[str, Any]
    homePlayers: List[Dict[str, Any]]
    awayPlayers: List[Dict[str, Any]]
    periodScores: Dict[str, Any]


class WinProbability(TypedDict, total=False):
    eventId: str
    winProbability: List[Dict[str, Any]]
    drives: List[Dict[str, Any]]


class GameRoster(TypedDict, total=False):
    eventId: str
    teams: List[Dict[str, Any]]


class Team(TypedDict, total=False):
    id: str
    uid: str
    slug: str
    location: str
    name: str
    nickname: str
    abbreviation: str
    displayName: str
    shortDisplayName: str
    color: str
    alternateColor: str
    logos: List[Dict[str, Any]]
    record: str
    standingSummary: str
    league: Dict[str, Any]
    venue: Optional[Dict[str, Any]]
    isActive: bool
    isAllStar: bool


class RosterAthlete(TypedDict, total=False):
    id: str
    displayName: str
    firstName: str
    lastName: str
    jersey: str
    position: str
    age: int
    height: str
    weight: str
    experience: int
    status: str
    headshot: str


class Roster(TypedDict, total=False):
    team: Dict[str, Any]
    season: int
    count: int
    groups: List[Dict[str, Any]]
    athletes: List["RosterAthlete"]


class DepthChart(TypedDict, total=False):
    formations: List[Dict[str, Any]]


class Athlete(TypedDict, total=False):
    id: str
    displayName: str
    firstName: str
    lastName: str
    position: str
    jersey: str
    age: int
    team: Dict[str, Any]
    headshot: str
    hasStats: bool
    statistics: Dict[str, Any]
    statisticsScope: Dict[str, Any]


class AthleteSearchResult(TypedDict, total=False):
    id: str
    displayName: str
    shortName: str
    jersey: str
    sport: str
    league: str
    image: str
    team: Dict[str, Any]


class GameLogEntry(TypedDict, total=False):
    eventId: str
    name: str
    shortName: str
    date: str
    week: int
    seasonType: int
    teamId: str
    played: bool
    statistics: Dict[str, Any]


class AvailabilityState(TypedDict, total=False):
    athleteId: str
    name: str
    position: str
    teamId: str
    teamName: str
    availability: Literal["OUT", "DOUBTFUL", "QUESTIONABLE", "PROBABLE", "DAY_TO_DAY", "INJURED_RESERVE", "SUSPENDED", "AVAILABLE", "UNKNOWN"]
    status: str
    reason: str
    detail: str
    reportDate: str
    observedAt: str
    seasonYear: int
    seasonType: int
    week: int


class AvailabilityTransition(AvailabilityState, total=False):
    sport: str
    league: str
    previousAvailability: str
    previousStatus: str
    changeType: Literal["new", "change", "cleared"]


class Injury(TypedDict, total=False):
    athlete: Dict[str, Any]
    team: Dict[str, Any]
    status: str
    statusType: str
    fantasyStatus: str
    type: str
    bodyPart: str
    location: str
    detail: str
    side: str
    date: str
    shortComment: str
    longComment: str


class InjuryReport(TypedDict, total=False):
    count: int
    groups: List[Dict[str, Any]]
    injuries: List["Injury"]


class PlayerAvailability(TypedDict, total=False):
    athlete: Dict[str, Any]
    team: Dict[str, Any]
    availability: Literal["OUT", "DOUBTFUL", "QUESTIONABLE", "PROBABLE", "DAY_TO_DAY", "INJURED_RESERVE", "SUSPENDED", "AVAILABLE", "UNKNOWN"]
    status: str
    statusType: str
    reason: str
    detail: str
    date: str


class PlayerAvailabilityReport(TypedDict, total=False):
    count: int
    groups: List[Dict[str, Any]]
    players: List["PlayerAvailability"]


class NewsArticle(TypedDict, total=False):
    id: int
    headline: str
    description: str
    type: str
    published: str
    lastModified: str
    premium: bool
    images: List[Dict[str, Any]]
    link: str
    categories: List[str]
    athletes: List[Dict[str, Any]]
    teams: List[Dict[str, Any]]


class Transactions(TypedDict, total=False):
    count: int
    season: int
    page: int
    pageCount: int
    total: int
    transactions: List[Dict[str, Any]]


class Season(TypedDict, total=False):
    year: int
    startDate: str
    endDate: str
    displayName: str
    currentType: Optional[Dict[str, Any]]
    types: List[Dict[str, Any]]
    endpoints: Dict[str, Any]


class SeasonSummary(TypedDict, total=False):
    year: int
    startDate: str
    endDate: str
    displayName: str
    currentType: str
    slug: str


class SeasonType(TypedDict, total=False):
    id: str
    name: str
    abbreviation: str
    slug: str
    year: int
    startDate: str
    endDate: str
    hasGroups: bool
    hasStandings: bool
    endpoints: Dict[str, Any]


class Group(TypedDict, total=False):
    id: str
    name: str
    abbreviation: str
    endpoints: Dict[str, Any]


class Week(TypedDict, total=False):
    number: int
    seasonType: int
    label: str
    startDate: str
    endDate: str


class TournamentGame(Event, total=False):
    tournament: Dict[str, Any]


class Webhook(TypedDict, total=False):
    id: str
    url: str
    events: List["WebhookEventType"]
    leagues: Optional[List[str]]
    frequency: "WebhookFrequency"
    active: bool
    consecutiveFailures: int
    deactivatedReason: Optional[str]
    deactivatedAt: Optional[str]
    createdAt: str
    updatedAt: str


WebhookEventType = Literal["event.live", "event.score_change", "event.status_change", "event.play", "event.final"]

WebhookFrequency = Literal["asap", "30s", "1m", "5m", "10m", "30m"]

class WebhookInput(TypedDict, total=False):
    url: str
    events: List["WebhookEventType"]
    leagues: Optional[List[str]]
    frequency: "WebhookFrequency"
    active: bool


class WebhookDelivery(TypedDict, total=False):
    id: str
    eventType: str
    status: str
    attempts: int
    responseCode: Optional[int]
    error: Optional[str]
    eventId: Optional[str]
    league: Optional[str]
    createdAt: str


__all__ = [
    "ErrorBody",
    "RateLimit",
    "Pagination",
    "Sport",
    "League",
    "LeagueDetail",
    "EventTeam",
    "EventStatus",
    "Event",
    "PlayAthlete",
    "Play",
    "Odds",
    "OddsHistoryEntry",
    "BoxScore",
    "WinProbability",
    "GameRoster",
    "Team",
    "RosterAthlete",
    "Roster",
    "DepthChart",
    "Athlete",
    "AthleteSearchResult",
    "GameLogEntry",
    "AvailabilityState",
    "AvailabilityTransition",
    "Injury",
    "InjuryReport",
    "PlayerAvailability",
    "PlayerAvailabilityReport",
    "NewsArticle",
    "Transactions",
    "Season",
    "SeasonSummary",
    "SeasonType",
    "Group",
    "Week",
    "TournamentGame",
    "Webhook",
    "WebhookEventType",
    "WebhookFrequency",
    "WebhookInput",
    "WebhookDelivery",
]
