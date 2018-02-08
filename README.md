# PythonLeagueAPI
League of Legends API for Python

Start by making a LeagueAPI object with your API key and region as parameters.

`generalAPIRequester = LeagueAPI({yourAPIKey}, "NA1")`

Make a Summoner object by calling LeagueAPI's summonerByName method.

`imaqtpie = generalAPIRequester.summonerByName("Imaqtpie")`
