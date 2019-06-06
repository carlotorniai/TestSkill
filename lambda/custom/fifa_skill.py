# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK.
# import logging
import random
from collections import namedtuple, defaultdict
from datetime import *

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value, get_slot
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

import Fifa as fifa

API = fifa.FifaApiWrapper()

LOGGER = fifa.util.configure_logger(__name__)

sb = SkillBuilder()

""" TODO: German
    TODO: Session lifetime
"""

# Some defaults
count = 1
# What should be passed to the FIFA APIs
default_language = "en-GB"
# If we don't get something from Alexa
default_locale = "en-GB"
# What we say back. Keyed by locale
language_sayings = {
    "en": fifa.sayings.en.responses,
    "en-US": fifa.sayings.en.responses,
    "en-GB": fifa.sayings.en.responses,
    # "de": fifa.sayings.de.responses,
}
default_sayings = language_sayings["en"]
event = namedtuple("event", ["season", "competition", "age", "football_type", "gender"])
EVENTS = defaultdict(lambda: event("278513", "103", 7, 0, 2))
EVENTS["278513"] = event("278513", "103", 7, 0, 2)
EVENTS["254645"] = event("254645", "17", 7, 0, 1)
SEASON_NAMES = {
    "278513": "FIFA Women's World Cup France 2019",
    "254645": "2018 FIFA World Cup Russia",
}


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    speech_intros = [
        "Welcome to the official FIFA skill. What would you like to know about the current matches?",
        "Hi, this is FIFA. What would you like to know?",
        "Hello, welcome to FIFA. Ask me anything.",
    ]
    speech_text = random.choice(speech_intros)
    handler_input.response_builder.speak(speech_text).ask(speech_text)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("Matches"))
def matches_intent_handler(handler_input):
    sayings = default_sayings["MATCHES_INTENT"]

    # This is an 'id' that should represent the season id
    try:
        event_id = (
            get_slot(handler_input=handler_input, slot_name="event")
            .resolutions.resolutions_per_authority[0]
            .values[0]
            .value.id
        )
    except:
        event_id = "default"

    event = EVENTS[event_id]
    if fifa.util.has_season_ended(event.season):
        # Short circuit if the season already ended
        speech_text = "Sorry, the {} has already ended".format(
            SEASON_NAMES[event.season]
        )
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

    timeframe_dt = fifa.util.date_parse(
        get_slot_value(handler_input=handler_input, slot_name="timeframe")
    )
    delta = fifa.util.day_delta(timeframe_dt)
    if delta.friendly_name == "today" or delta.friendly_name == "tomorrow":
        s = sayings["MATCHES_RELATIVE"]
    else:
        s = sayings["MATCHES_DATE"]

    speech_text = ""
    results = fifa.util.matches_by_date(
        API, event.season, event.competition, on_date=timeframe_dt
    )
    for i, v in enumerate(results, 1):
        if i == len(results):
            s = sayings["MATCHES_CONTINUED"]
            speech_text += " and " + s.format(v.home_team_name, v.away_team_name)
        elif i > 1:
            s = sayings["MATCHES_CONTINUED"]
            speech_text += ", " + s.format(v.home_team_name, v.away_team_name)
            continue
        else:
            speech_text += s.format(
                delta.friendly_name, v.home_team_name, v.away_team_name
            )

    if not results:
        s = sayings["NO_MATCHES"]
        speech_text = s.format(timeframe_dt.strftime("%m%d"))

    LOGGER.info("Sending: {}".format(speech_text))
    handler_input.response_builder.speak(speech_text).set_should_end_session(False)

    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("Matchsearch"))
def match_search_intent_handler(handler_input):
    sayings = default_sayings["MATCH_SEARCH_INTENT"]
    session_attr = handler_input.attributes_manager.session_attributes
    country_value = get_slot_value(handler_input=handler_input, slot_name="country")

    # This is an 'id' that should represent the season id
    try:
        event_id = (
            get_slot(handler_input=handler_input, slot_name="event")
            .resolutions.resolutions_per_authority[0]
            .values[0]
            .value.id
        )
    except:
        event_id = "default"

    event = EVENTS[event_id]
    if fifa.util.has_season_ended(event.season):
        # Short circuit if the season already ended
        speech_text = "Sorry, the {} has already ended".format(
            SEASON_NAMES[event.season]
        )
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

    team_info = fifa.util.team_lookup_by_keyword(
        API,
        country_value,
        gender=event.gender,
        football_type=event.football_type,
        age=event.age,
    )[0]

    # Get the next match for this team
    results = fifa.util.matches_next(
        API, event.season, event.competition, id_team=team_info.id_team
    )
    for r in results:
        # We want to say the requested team first
        team1 = team_info.team_name
        if team_info.team_name == r.home_team_name:
            team2 = r.away_team_name
        else:
            team2 = r.home_team_name

        s = sayings["MATCH_DATE"]
        speech_text = s.format(country_value, team2, r.dt.strftime("%m%d"))
        # Prep for a Yes Intent
        session_attr["selected_country"] = country_value
        # You can't just store a datetime object because the ask sdk serializes it to a string :(
        session_attr["match_date"] = r.dt.strftime("%m%d")
        session_attr["match_time"] = str(r.dt.time())
        session_attr["vs_team"] = team2

    if not results:
        speech_text = "Sorry, I don't have that statistic"

    LOGGER.info("Sending: {}".format(speech_text))

    handler_input.response_builder.speak(speech_text).set_should_end_session(False)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("LiveMatches"))
def live_matches_intent_handler(handler_input):
    # This endpoint uses the Mock endpoint
    MOCK_API = fifa.FifaApiWrapper(mock=True)
    API = MOCK_API
    sayings = default_sayings["LIVE_MATCH_INTENT"]
    # This is an 'id' that should represent the season id
    try:
        event_id = (
            get_slot(handler_input=handler_input, slot_name="event")
            .resolutions.resolutions_per_authority[0]
            .values[0]
            .value.id
        )
    except:
        event_id = "default"

    event = EVENTS[event_id]
    # if not fifa.util.has_season_started(event.season):
    #     # Short circuit if the season hasn't started
    #     speech_text = "Sorry, the {} hasn't started yet".format(
    #         SEASON_NAMES[event.season]
    #     )
    #     handler_input.response_builder.speak(speech_text).set_should_end_session(False)
    #     return handler_input.response_builder.response

    speech_text = ""
    live_matches = fifa.util.live_scores(API, event.season)

    for i, v in enumerate(live_matches, 1):
        if i > 1:
            s = sayings["MATCH_STATUS_CONTINUED"]
            speech_text += " " + s.format(
                v.home_team_name,
                v.away_team_name,
                v.match_time,
                v.home_team_name,
                v.home_team_score,
                v.away_team_name,
                v.away_team_score,
            )
        else:
            s = sayings["MATCH_STATUS"]
            speech_text += s.format(
                v.home_team_name,
                v.away_team_name,
                v.match_time,
                v.home_team_name,
                v.home_team_score,
                v.away_team_name,
                v.away_team_score,
            )

    if not live_matches:
        speech_text = sayings["NO_MATCHES"]

    LOGGER.info("Sending: {}".format(speech_text))
    handler_input.response_builder.speak(speech_text).set_should_end_session(False)

    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("Results"))
def results_intent_handler(handler_input):
    sayings = default_sayings["RESULTS_INTENT"]
    # This is an 'id' that should represent the season id
    try:
        event_id = (
            get_slot(handler_input=handler_input, slot_name="event")
            .resolutions.resolutions_per_authority[0]
            .values[0]
            .value.id
        )
    except:
        event_id = "default"

    event = EVENTS[event_id]
    if not fifa.util.has_season_started(event.season):
        # Short circuit if the season hasn't started
        speech_text = "Sorry, the {} hasn't started yet".format(
            SEASON_NAMES[event.season]
        )
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

    timeframe_dt = fifa.util.date_parse(
        get_slot_value(handler_input=handler_input, slot_name="timeframe")
    )

    speech_text = ""
    results = fifa.util.matches_by_date(
        API, event.season, event.competition, on_date=timeframe_dt
    )
    for i, v in enumerate(results, 1):
        # Find out who the winner was
        draw_key_suffix = ""
        if v.home_team_score > v.away_team_score:
            winner_name, winner_score = v.home_team_name, v.home_team_score
            loser_name, loser_score = v.away_team_name, v.away_team_score
        elif v.away_team_score > v.home_team_score:
            winner_name, winner_score = v.away_team_name, v.away_team_score
            loser_name, loser_score = v.home_team_name, v.home_team_score
        elif v.away_team_score == v.home_team_score:
            draw_key_suffix = "_DRAW"

        # Send the results to be spoken
        if i == len(results):
            # This is the last element case
            s = sayings["RESULTS_CONTINUED" + draw_key_suffix]
            speech_text += " and " + s.format(
                delta.friendly_name, winner_name, loser_name, winner_score, loser_score
            )
        elif i > 1:
            s = sayings["RESULTS_CONTINUED" + draw_key_suffix]
            speech_text += ", " + s.format(
                delta.friendly_name, winner_name, loser_name, winner_score, loser_score
            )
            continue
        else:
            # This is the first element case
            # Find out if we should respond with a "friendly relative time (eg. yesterday)"
            delta = fifa.util.day_delta(timeframe_dt)
            date_key_suffix = ""
            if delta.friendly_name == "today" or delta.friendly_name == "tomorrow":
                date_key_suffix = "_RELATIVE"

            s = sayings["RESULTS" + date_key_suffix + draw_key_suffix]
            speech_text += s.format(
                delta.friendly_name, winner_name, loser_name, winner_score, loser_score
            )

    if not results:
        s = sayings["NO_RESULTS"]
        speech_text = s.format(timeframe_dt.strftime("%m%d"))

    LOGGER.info("Sending: {}".format(speech_text))
    handler_input.response_builder.speak(speech_text).set_should_end_session(False)

    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("WhereToWatch"))
def where_to_watch_intent_handler(handler_input):
    """ Get Broadcast information
    """
    sayings = default_sayings["WHERE_TO_WATCH_INTENT"]
    country = get_slot_value(handler_input=handler_input, slot_name="country")
    country_code = fifa.util.country_iso(country).alpha2
    team_name = get_slot_value(handler_input=handler_input, slot_name="team")
    speech_text = "I am unable to find viewing info for {}".format(country)

    # This is an 'id' that should represent the season id
    try:
        event_id = (
            get_slot(handler_input=handler_input, slot_name="event")
            .resolutions.resolutions_per_authority[0]
            .values[0]
            .value.id
        )
    except:
        event_id = "default"

    event = EVENTS[event_id]
    if fifa.util.has_season_ended(event.season):
        # Short circuit if the season already ended
        speech_text = "Sorry, the {} has already ended".format(
            SEASON_NAMES[event.season]
        )
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

    def concat_tv_sources(sources):
        """ Take a list and output a string of TV sources
        """
        tv_sources = ""
        for i, v in enumerate(sources, 1):
            if i == 1:
                # First element
                tv_sources += "{} ".format(v)
            elif i == len(sources):
                # Last element
                tv_sources += "or {}".format(v)
            else:
                tv_sources += ", {} ".format(v)
        return tv_sources

    if not team_name:
        # We should have a country at least. The interaction model validates this
        s = sayings["WHERE_BY_CC"]
        where_to_watch = fifa.util.where_to_watch(API, event.season, country_code)
        tv_sources = concat_tv_sources(where_to_watch.sources)
        speech_text = s.format(country, tv_sources)

    elif team_name:
        s = sayings["WHERE_BY_CC_AND_MATCH"]
        team_info = fifa.util.team_lookup_by_keyword(
            API,
            country,
            gender=event.gender,
            football_type=event.football_type,
            age=event.age,
        )[0]
        # Get the next match for this team
        match = fifa.util.matches_next(
            API, event.season, event.competition, id_team=team_info.id_team
        )[0]
        id_match = match.id_match
        where_to_watch = fifa.util.where_to_watch(
            API, event.season, country_code, id_match=id_match
        )
        tv_sources = concat_tv_sources(where_to_watch.sources)

        # We want to say the requested team first
        team1 = team_info.team_name
        if team_info.team_name == match.home_team_name:
            team2 = match.away_team_name
        else:
            team2 = match.home_team_name

        speech_text = s.format(country, team1, team2, tv_sources)

    LOGGER.info("Sending: {}".format(speech_text))

    handler_input.response_builder.speak(speech_text).set_should_end_session(False)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("Stats"))
def stats_intent_handler(handler_input):
    """ Handle the stats intent
        TODO: Handle possives countries (eg. "Who is Germany's top scorer")
        TODO: Handle stats other than scorer
    """
    sayings = default_sayings["STATS_INTENT"]
    country_value = get_slot_value(handler_input=handler_input, slot_name="country")
    stat_value = get_slot_value(handler_input=handler_input, slot_name="stat")
    # This is an 'id' that should represent the season id
    try:
        event_id = (
            get_slot(handler_input=handler_input, slot_name="event")
            .resolutions.resolutions_per_authority[0]
            .values[0]
            .value.id
        )
    except:
        event_id = "default"

    event = EVENTS[event_id]
    if not fifa.util.has_season_started(event.season):
        # Short circuit if the season hasn't started
        speech_text = "Sorry, the {} hasn't started yet".format(
            SEASON_NAMES[event.season]
        )
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

    if country_value:
        id_team = fifa.util.team_lookup_by_keyword(
            API,
            country_value,
            gender=event.gender,
            football_type=event.football_type,
            age=event.age,
        )[0].id_team
    else:
        id_team = None

    print("event: {} team: {}".format(event.season, id_team))
    results = fifa.util.top_scorer(API, event.season, id_team=id_team, count=1)
    for r in results:
        goal_plural = "goals" if r.goals_scored > 1 else "goal"
        if id_team:
            s = sayings["TEAM_LEADER"]
        else:
            s = sayings["OVERALL_LEADER"]

        speech_text = s.format(r.player_name, r.team_name, r.goals_scored, goal_plural)
    if not results:
        speech_text = "Sorry, I don't have that statistic"

    LOGGER.info("Sending: {}".format(speech_text))

    handler_input.response_builder.speak(speech_text).set_should_end_session(False)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.YesIntent"))
def yes_intent_handler(handler_input):
    """Handler for Yes Intent."""
    sayings = default_sayings["YES_INTENT"]

    session_attr = handler_input.attributes_manager.session_attributes
    LOGGER.info("Session Attributes: {}".format(session_attr))
    country_value = session_attr["selected_country"]
    vs_team = session_attr["vs_team"]
    match_date = session_attr["match_date"]
    match_time = session_attr["match_time"]

    s = sayings["MATCH_DAY_TIME"]
    # speech_text = s.format(country_value, vs_team, match_date)
    speech_text = s.format(country_value, vs_team, match_time, match_date)

    session_attr["selected_country"] = ""
    session_attr["match_date"] = ""
    session_attr["match_time"] = ""
    session_attr["vs_team"] = ""

    handler_input.response_builder.speak(speech_text).set_should_end_session(False)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.NoIntent"))
def no_intent_handler(handler_input):
    """Handler for No Intent."""

    speech_text = "Ok"
    # handler_input.response_builder.speak(speech_text).ask(speech_text)
    handler_input.response_builder.speak(speech_text).set_should_end_session(True)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    speech_text = "You can say hello to me! How can I help?"
    handler_input.response_builder.speak(speech_text).ask(speech_text)
    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_or_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    speech_text = "Goodbye!"
    handler_input.response_builder.speak(speech_text)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_requesed_handler(handler_input):
    return handler_input.response_builder.response


# Generic error handling to capture any syntax or routing errors. If you receive an error
# stating the request handler chain is not found, you have not implemented a handler for
# the intent being invoked or included it in the skill builder below.
@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """ Catch-all exception handler, log exception and respond with custom
        message.
    """
    LOGGER.error(exception, exc_info=True)
    speech_text = "Sorry, I couldn't understand what you said. Please try again."
    handler_input.response_builder.speak(speech_text).ask(speech_text)
    return handler_input.response_builder.response


# The intent reflector is used for interaction model testing and debugging.
# It will simply repeat the intent the user said. You can create custom handlers
# for your intents by defining them above, then also adding them to the request
# handler chain below.

# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
@sb.request_handler(can_handle_func=is_request_type("IntentRequest"))
def intent_reflector_request(handler_input):
    # type: (HandlerInput) -> Response
    intent_name = handler_input.request_envelope.request.intent.name
    speech_text = ("You just triggered {}").format(intent_name)
    handler_input.response_builder.speak(speech_text).set_should_end_session(False)
    return handler_input.response_builder.response


handler = sb.lambda_handler()
