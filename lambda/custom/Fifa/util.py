from collections import namedtuple
import logging
import urllib.parse
from iso3166 import countries_by_name
from datetime import *
import dateutil.parser
import calendar

player = namedtuple(
    "player", ["player_name", "team_name", "goals_scored", "id_player", "id_team"]
)
team = namedtuple("team", ["team_name", "id_team"])


def has_season_started(season):
    """ Return a boolean which can be used to politely remind the user that the
        season hasn't started if they ask for stats or results
    """
    if season == "278513":
        # The season starts on June 7 @19:00UTC
        if datetime.utcnow() > datetime(2019, 6, 7, 19, 00):
            return True
        else:
            return False
    elif season == "254645":
        return True


def has_season_ended(season):
    """ Return a boolean which can be used to politely remind the user that the
        season has started if they ask for match schedules
    """
    if season == "278513":
        # The season ends on July 7 sometime
        if datetime.utcnow() > datetime(2019, 7, 8, 00, 00):
            return True
        else:
            return False
    elif season == "254645":
        return True

def date_parse(date):
    return dateutil.parser.parse(date)


def day_delta(date1, date2=None):
    """ Given 1 or 2 datetime objects, returns a named tuple containing the
        day delta & friendly name.
    """
    day_delta = namedtuple("day_delta", ["int", "friendly_name"])
    date2 = date2 or datetime.today()
    delta = (date1.date() - date2.date()).days

    if delta == -1:
        friendly_name = "yesterday"
    elif delta == 0:
        friendly_name = "today"
    elif delta == 1:
        friendly_name = "tomorrow"
    else:
        friendly_name = date1.strftime("%m%d")

    return day_delta(int=delta, friendly_name=friendly_name)


def country_iso(country):
    """ Return the country codes. 
        Somewhat tricky
    """
    country = country.upper()
    result = []
    try:
        result.append(countries_by_name[country])
    except KeyError:
        for k, v in countries_by_name.items():
            if country == v.apolitical_name.upper():
                result.append(v)
                continue
            elif country == v.alpha3.upper():
                result.append(v)
                continue
            elif country == v.alpha2.upper():
                result.append(v)
                continue
            elif country in v.name.upper():
                result.append(v)
                continue

    return result[0]


def matches(match_data):
    """ Common logic for loading a matches object from the various APIs
    """
    match = namedtuple(
        "match",
        [
            "home_team_name",
            "home_team_id",
            "home_team_score",
            "away_team_name",
            "away_team_id",
            "away_team_score",
            "group_name",
            "id_group",
            "stage_name",
            "id_stage",
            "id_match",
            "dt",  # <== A datetime object
        ],
    )
    return match(
        id_stage=match_data["IdStage"],
        id_match=match_data["IdMatch"],
        stage_name=match_data["StageName"][0]["Description"],
        id_group=match_data["IdGroup"],
        group_name=match_data["GroupName"][0]["Description"],
        home_team_score=match_data["HomeTeamScore"],
        home_team_name=match_data["Home"]["TeamName"][0]["Description"],
        home_team_id=match_data["Home"]["IdTeam"],
        away_team_score=match_data["AwayTeamScore"],
        away_team_name=match_data["Away"]["TeamName"][0]["Description"],
        away_team_id=match_data["Away"]["IdTeam"],
        dt=date_parse(match_data["LocalDate"]),
    )


def matches_by_date(
    API, id_season, id_competition, on_date, id_team=None, language="en-GB", count=10
):
    """ Attempts to returns matches on a given date.
    
        The API does not allow for passing a date range, so we just get a
        number of matches and then return matches based on date (a datetime object)
    """
    args = {
        "id_season": id_season,
        "id_competition": id_competition,
        "language": language,
        "count": count,
    }

    if id_team:
        args["id_team"] = id_team
        response = API.calendar_matches_team(**args).get()
    else:
        response = API.calendar_matches(**args).get()

    results = []
    for r in response.Results().data:
        match = matches(r)
        if on_date.date() == match.dt.date():
            results.append(match)

    return results


def matches_next(
    API,
    id_season,
    id_competition,
    next_count=1,
    prev_count=0,
    id_team=None,
    language="en-GB",
    count=1,
):
    """ Returns next matches or next matches for team also
        returns previous matches or previous matches for team
    """
    args = {
        "id_season": id_season,
        "id_competition": id_competition,
        "language": language,
        "next_count": next_count,
        "prev_count": prev_count,
    }

    if id_team:
        args["id_team"] = id_team
        response = API.calendar_nextmatches_team(**args).get()
    else:
        response = API.calendar_nextmatches(**args).get()

    results = []
    for i in range(count):
        match_data = response.Results().data[i]

        results.append(matches(match_data))

    return results


def live_scores(API, season, language="en-GB"):
    """ The live scores API returns all games in progess for all competitions & seasons
        Given a season, return live-in-progress scores and match time.
    """
    response = API.livematch_getnow(language=language).get()
    live_matches = response.Results().data
    match = namedtuple(
        "match",
        [
            "home_team_name",
            "home_team_score",
            "away_team_name",
            "away_team_score",
            "match_time",  # Think this is the match progress
        ],
    )

    results = []
    for m in live_matches:
        if m["IdSeason"] == season:
            results.append(match(
                home_team_name=m["HomeTeam"]["TeamName"][0]["Description"],
                home_team_score=m["HomeTeam"]["Score"],
                away_team_name=m["AwayTeam"]["TeamName"][0]["Description"],
                away_team_score=m["AwayTeam"]["Score"],
                match_time=m["MatchTime"]
            ))

    if not live_matches:
        return None

    return results


def team_lookup_by_keyword(
    API, team_name, gender=1, football_type=0, age=7, language="en-GB"
):
    response = API.teams_search_by_name(
        team_name=urllib.parse.quote(team_name), language=language
    ).get()

    def filter_by_gender_and_type(l):
        if (
            l["Gender"] == gender
            and l["FootballType"] == football_type
            and l["AgeType"] == age
            and l["Name"][0]["Description"].lower() == team_name.lower()
        ):
            return True

    results = []
    for t in list(filter(filter_by_gender_and_type, response.Results().data)):
        results.append(team(team_name=t["Name"][0]["Description"], id_team=t["IdTeam"]))
    return results


def top_scorer(API, id_season, id_team=None, count=1, language="en-GB"):
    """ Returns a list of top scorers
    """
    results = []

    print("SEASON: {} TEAM: {}".format(id_season, id_team))

    def team_top_scorer(API, id_season, id_team, count=1, language="en-GB"):
        """ Returns a team's top scorer
        """
        response = API.playerstats_season_top_scorer(
            id_season=id_season, id_team=id_team, count=count, language=language
        ).get()

        results = []
        # Implement our own count since the API's doesn't seem to work
        for i in range(count):
            player_info = response.Results().data[i]
            results.append(
                player(
                    goals_scored=player_info["Goals"],
                    player_name=player_info["PlayerName"][0]["Description"],
                    id_player=player_info["IdPlayer"],
                    team_name=player_info["TeamName"][0]["Description"],
                    id_team=player_info["IdTeam"],
                )
            )

        return results

    def tournament_top_scorer(API, id_season, count=3, language="en-GB"):
        """ Returns a list of top scorers, goals, and country
        """
        response = API.playerstats_lastlive(
            idSeason=id_season, count=count, language=language
        ).get()

        results = []
        for i in range(count):
            player_info = response.PlayerStatsList().data[i]["PlayerInfo"]
            results.append(
                player(
                    goals_scored=response.PlayerStatsList().data[i]["GoalsScored"],
                    player_name=player_info["PlayerName"][0]["Description"],
                    id_player=player_info["IdPlayer"],
                    team_name=player_info["TeamName"][0]["Description"],
                    id_team=player_info["IdTeam"],
                )
            )

        return results

    if id_team:
        results = team_top_scorer(
            API, id_season, id_team=id_team, count=1, language=language
        )
    else:
        results = tournament_top_scorer(API, id_season, count=1, language=language)

    print(results)

    return results


def where_to_watch(API, id_season, country_code, id_match=None, language="en-GB"):
    """ Returns a list of TV Broadcaster names
    """
    tv_sources = namedtuple("tv_sources", ["sources"])
    sources = []
    if id_match:
        response = API.where_to_watch_by_cc_and_match(
            id_season=id_season,
            id_match=id_match,
            country_code=country_code,
            language=language,
        ).get()
        source_data = response.Sources().data
    else:
        response = API.where_to_watch_by_cc(
            id_season=id_season, country_code=country_code, language=language
        ).get()
        source_data = response.Matches[0].Sources().data

    for r in source_data:
        sources.append(r["Name"])

    return tv_sources(sources=sources)


def configure_logger(logger_name):
    """Configures a generic logger which can be imported and used as needed
    """

    # Create logger and define INFO as the log level
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Define our logging formatter
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s | (%(filename)s:%(lineno)d)"
    )

    # Create our stream handler and apply the formatting
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Add the stream handler to the logger
    logger.addHandler(stream_handler)

    return logger
