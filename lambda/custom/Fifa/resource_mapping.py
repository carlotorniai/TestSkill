# coding: utf-8

# All can take &language=de for german

RESOURCE_MAPPING = {
    "calendar_matches": {
        "resource": "calendar/matches?idSeason={id_season}&idCompetition={id_competition}&count={count}&language={language}",
        "methods": ["GET"],
        "docs": "https://givevoicetofootball.fifa.com/ApiFdcpSwagger/ui/index#!/Calendar/Calendar_GetMatches",
    },
    "calendar_matches_team": {
        "resource": "calendar/matches?idSeason={id_season}&idCompetition={id_competition}&idTeam={id_team}&count={count}&language={language}",
        "methods": ["GET"],
        "docs": "https://givevoicetofootball.fifa.com/ApiFdcpSwagger/ui/index#!/Calendar/Calendar_GetMatches",
    },
    "calendar_nextmatches": {
        "resource": "calendar/nextmatches?numberOfNextMatches={next_count}&numberOfPreviousMatches={prev_count}&idSeason={id_season}&idCompetition={id_competition}&language={language}",
        "methods": ["GET"],
        "docs": "https://givevoicetofootball.fifa.com/ApiFdcpSwagger/ui/index#!/Calendar/Calendar_GetNextAndPreviousMatches",
    },
    "calendar_nextmatches_team": {
        "resource": "calendar/nextmatches?numberOfNextMatches={next_count}&numberOfPreviousMatches={prev_count}&idSeason={id_season}&idCompetition={id_competition}&idTeam={id_team}&language={language}",
        "methods": ["GET"],
        "docs": "https://givevoicetofootball.fifa.com/ApiFdcpSwagger/ui/index#!/Calendar/Calendar_GetNextAndPreviousMatches",
    },
    "livematch_getnow": {
        "resource": "live/football/now?language={language}",
        "methods": ["GET"],
        "docs": "https://givevoicetofootball.fifa.com/ApiFdcpSwagger/ui/index#!/LiveMatch/LiveMatch_GetNow",
    },
    "teams_search_by_name": {
        "resource": "teams/search?name={team_name}&language={language}",
        "methods": ["GET"],
        "docs": "https://givevoicetofootball.fifa.com/ApiFdcpSwagger/ui/index#!/Teams/Teams_SearchTeamsByName",
    },
    "playerstats_lastlive": {
        "resource": "topseasonplayerstatistics/season/{idSeason}/topscorers?language={language}",
        "methods": ["GET"],
        "docs": "https://givevoicetofootball.fifa.com/ApiFdcpSwagger/ui/index#!/TopSeasonPlayersStats/TopSeasonPlayersStats_GetLastLivePlayerPlayerStatistics",
    },
    # This is a deprecated method but we use it to get top team scorer
    "playerstats_season_top_scorer": {
        "resource": "topscorers?idSeason={id_season}&idTeam={id_team}&count={count}&sortBy=goals&language={language}",
        "methods": ["GET"],
        "docs": "https://givevoicetofootball.fifa.com/ApiFdcpSwagger/ui/index#!/TopSeasonPlayersStats/TopSeasonPlayersStats_GetTopScorers",
    },
    "where_to_watch_by_cc": {
        "resource": "watch/season/{id_season}/{country_code}?language={language}",
        "methods": ["GET"],
        "docs": "https://givevoicetofootball.fifa.com/ApiFdcpSwagger/ui/index#!/WhereToWatch/WhereToWatch_WhereToWatchByMatchAndCountry",
    },
    "where_to_watch_by_cc_and_match": {
        "resource": "watch/match/{id_season}/{id_match}/{country_code}?language={language}",
        "methods": ["GET"],
        "docs": "https://givevoicetofootball.fifa.com/ApiFdcpSwagger/ui/index#!/WhereToWatch/WhereToWatch_WhereToWatchByMatchAndCountry",
    },
}
