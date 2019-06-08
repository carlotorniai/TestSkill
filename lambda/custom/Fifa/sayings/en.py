responses = {
    "LIVE_MATCH_INTENT": {
        "MATCH_STATUS": (
            "In the {} {} match at <say-as interpret-as='time'>{}00\"</say-as> the score is {} {} <break strength='strong'/> {} {}" # team1, team2, time, team1 team1_score, team2, team2_score
        ),
        "MATCH_STATUS_CONTINUED": (
            "And In the {} {} match at <say-as interpret-as='time'>{}00\"</say-as> the score is {} {} <break strength='strong'/> {} {}" # team1, team2, time, team1 team1_score, team2, team2_score
        ),
        "NO_MATCHES": (
            "There are no games currently in progress"
        ),
    },
    "STATS_INTENT": {
        "OVERALL_LEADER": (
            "{} of {} leads the championship with {} {}" # player, country, count, stat
        ),
        "TEAM_LEADER": (
            "{} leads {} with {} {}" # player, country, count, stat
        ),
        "MATCHES_CONTINUED": (
            "{} plays {}" # team1, team2
        ),
        "NO_MATCHES": (
            "I have no record of games on <say-as interpret-as='date'>????{}</say-as>."
        ),
    },
    "MATCH_SEARCH_INTENT": {
        "MATCH_DATE": (
            "{} plays {} on <say-as interpret-as='date'>????{}</say-as>."
            "<break strength='strong'/> Do you want to know when this game is on?"
        ),
        # Array if you want to random choice
        "SAMPLE_WITH_LIST": [
            "Hey {}",
            "Hi there, {}",
            "Hello, {}",
        ],
    },
    "MATCHES_INTENT": {
        "MATCHES_DATE": (
            "on <say-as interpret-as='date'>????{}</say-as> {} plays {}" # date, team1, team2
        ),
        "MATCHES_RELATIVE": (
            "{} {} plays {}" # date, team1, team2
        ),
        "MATCHES_CONTINUED": (
            "{} plays {}" # team1, team2
        ),
        "NO_MATCHES": (
            "I have no record of games on <say-as interpret-as='date'>????{}</say-as>."
        ),
    },
    "RESULTS_INTENT": {
        "RESULTS": (
            "on <say-as interpret-as='date'>????{}</say-as> {} beat {} {} to {}" # date, team1, team2, team1_score, team2_score
        ),
        "RESULTS_DRAW": (
            "on <say-as interpret-as='date'>????{}</say-as> {} drew with {} {} to {}" # date, team1, team2, team1_score, team2_score
        ),
        "RESULTS_RELATIVE": (
            "{} {} beat {} {} to {}" # date, team1, team2, team1_score, team2_score
        ),
        "RESULTS_RELATIVE_DRAW": (
            "{} {} drew with {} {} to {}" # date, team1, team2, team1_score, team2_score
        ),
        "RESULTS_CONTINUED": (
            "{} {} drew with {} {} to {}" # date, team1, team2, team1_score, team2_score
        ),
        "RESULTS_CONTINUED_DRAW": (
            "{} {} drew with {} {} to {}" # date, team1, team2, team1_score, team2_score
        ),
        "NO_RESULTS": (
            "I have no record of results on <say-as interpret-as='date'>????{}</say-as>."
        ),
    },
    "WHERE_TO_WATCH_INTENT": {
        "WHERE_BY_CC": (
            "In {} matches are shown on {}" # Country, channel(s) [concatenated if necessary]
        ),
        "WHERE_BY_CC_AND_MATCH": (
            "In {} the {} {} match is shown on {}" # Country, team1, team2, channel(s) [concatenated if necessary]
        )
    },
    "YES_INTENT": {
        "MATCH_DAY_TIME": (
            "The {} {} match is at {} on <say-as interpret-as='date'>????{}</say-as>" # team1, team2, time, date
        )
    }
}
