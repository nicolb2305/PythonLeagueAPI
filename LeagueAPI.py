import requests as re
import json
from ratelimit import rate_limited
import os
import time
import sys

SEASONS = {0 : "Preseason 3",
		   1 : "Season 3",
		   2 : "Preseason 4",
		   3 : "Season 4",
		   4 : "Preseason 5",
		   5 : "Season 5",
		   6 : "Preseason 6",
		   7 : "Season 6",
		   8 : "Preseason 7",
		   9 : "Season 7",
		   10 : "Preseason 8",
		   11 : "Season 8"}
QUEUES = {0 : ["Custom game", "Custom"],
	      2 : ["Summoner's Rift", "5v5 Blind Pick"],
	      4 : ["Summoner's Rift", "5v5 Ranked Solo"],
		  6 : ["Summoner's Rift", "5v5 Ranked Premade"],
		  7 : ["Summoner's Rift", "Co-op vs AI"],
		  8 : ["Twisted Treeline", "3v3 Normal"],
		  9 : ["Twisted Treeline", "3v3 Ranked Flex"],
		  14 : ["Summoner's Rift", "5v5 Draft Pick"],
		  16 : ["Crystal Scar", "5v5 Dominion Blind Pick"],
		  17 : ["Crystal Scar", "5v5 Dominion Draft Pick"],
		  25 : ["Crystal Scar", "Dominion Co-op vs AI"],
		  31 : ["Summoner's Rift", "Co-op vs AI Intro Bot"],
		  32 : ["Summoner's Rift", "Co-op vs AI Beginner Bot"],
		  33 : ["Summoner's Rift", "Co-op vs AI Intermediate Bot"],
		  41 : ["Twisted Treeline", "3v3 Ranked Team"],
		  42 : ["Summoner's Rift", "5v5 Ranked Team"],
		  52 : ["Twisted Treeline", "Co-op vs AI"],
		  61 : ["Summoner's Rift", "5v5 Team Builder"],
		  65 : ["Howling Abyss", "5v5 ARAM"],
		  70 : ["Summoner's Rift", "One for All"],
		  72 : ["Howling Abyss", "1v1 Snowdown Showdown"],
		  73 : ["Howling Abyss", "2v2 Snowdown Showdown"],
		  75 : ["Summoner's Rift", "6v6 Hexakill"],
		  76 : ["Summoner's Rift", "Ultra Rapid Fire"],
		  78 : ["Howling Abyss", "One For All: Mirror Mode"],
		  83 : ["Summoner's Rift", "Co-op vs AI Ultra Rapid Fire"],
		  91 : ["Summoner's Rift", "Doom Bots Rank 1"],
		  92 : ["Summoner's Rift", "Doom Bots Rank 2"],
		  93 : ["Summoner's Rift", "Doom Bots Rank 5"],
		  96 : ["Crystal Scar", "Ascension"],
		  98 : ["Twisted Treeline", "6v6 Hexakill"],
		  100 : ["Butcher's Bridge", "5v5 ARAM"],
		  300 : ["Howling Abyss", "Legend of the Poro King"],
		  310 : ["Summoner's Rift", "Nemesis Draft"],
		  313 : ["Summoner's Rift", "Black Market Brawlers"],
		  315 : ["Summoner's Rift", "Nexus Siege"],
		  317 : ["Crystal Scar", "Definitely Not Dominion"],
		  318 : ["Summoner's Rift", "All Random Ultra Rapid Fire"],
		  325 : ["Summoner's Rift", "All Random Summoner's Rift"],
		  400 : ["Summoner's Rift", "5v5 Draft Pick"],
		  410 : ["Summoner's Rift", "5v5 Ranked Dynamic"],
		  420 : ["Summoner's Rift", "5v5 Ranked Solo"],
		  430 : ["Summoner's Rift", "5v5 Blind Pick"],
		  440 : ["Summoner's Rift", "5v5 Ranked Flex"],
		  450 : ["Howling Abyss", "5v5 ARAM"],
		  460 : ["Twisted Treeline", "3v3 Blind Pick"],
		  470 : ["Twisted Treeline", "3v3 Ranked Flex"],
		  600 : ["Summoner's Rift", "Hunt of the Blood Moon"],
		  610 : ["Cosmic Ruins", "Dark Star: Singularity"],
		  800 : ["Twisted Treeline", "Co-op vs. AI Intermediate Bot"],
		  810 : ["Twisted Treeline", "Co-op vs. AI Intro Bot"],
		  820 : ["Twisted Treeline", "Co-op vs. AI Beginner Bot"],
		  830 : ["Summoner's Rift", "Co-op vs. AI Intro Bot"],
		  840 : ["Summoner's Rift", "Co-op vs. AI Beginner Bot"],
		  850 : ["Summoner's Rift", "Co-op vs. AI Intermediate Bot"],
		  900 : ["Summoner's Rift", "All Random Ultra Rapid Fire"],
		  910 : ["Crystal Scar", "Ascension"],
		  920 : ["Howling Abyss", "Legend of the Poro King"],
		  940 : ["Summoner's Rift", "Nexus Siege"],
		  950 : ["Summoner's Rift", "Doom Bots: The Gauntlet"],
		  960 : ["Summoner's Rift", "Doom Bots"],
		  980 : ["Valoran City Park", "Star Guardian Invasion: Normal"],
		  990 : ["Valoran City Park", "Star Guardian Invasion: Onslaught"],
		  1000 : ["Substructure 43", "PROJECT: Hunters"],
		  1010 : ["Summoner's Rift", "Snow All Random Ultra Rapid Fire"]}
MAPID = {1 : ["Summoner's Rift", "Original Summer Variant"],
		 2 : ["Summoner's Rift", "Original Autumn Variant"],
		 3 : ["The Proving Grounds", "Tutorial Map"],
		 4 : ["Twisted Treeline", "Original Version"],
		 8 : ["Crystal Scar", "Dominion Map"],
		 10 : ["Twisted Treeline", "Current Version"],
		 11 : ["Summoner's Rift", "Current Version"],
		 12 : ["Howling Abyss", "ARAM Map"],
		 14 : ["Butcher's Bridge", "ARAM Map"],
		 16 : ["Cosmic Ruins", "Dark Star: Singularity Map"],
		 18 : ["Valoran City Park", "Star Guardian Invasion Map"],
		 19 : ["Substructure 43", "PROJECT: Hunters Map"]}
GAMEMODE = {"CLASSIC" : "Classic Summoner's Rift and Twisted Treeline games",
			"ODIN" : "Dominion/Crystal Scar games",
			"ARAM" : "ARAM games",
			"TUTORIAL" : "Tutorial games",
			"URF" : "URF games",
			"DOOMBOTSTEEMO" : "Doom Bots games",
			"ONEFORALL" : "One for All games",
			"ASCENSION" : "Ascension games",
			"FIRSTBLOOD" : "Snowdown Showdown games",
			"KINGPORO" : "Legend of the Poro King games",
			"SIEGE" : "Nexus Siege games",
			"ASSASSINATE" : "Blood Hunt Assassin games",
			"ARSR" : "All Random Summoner's Rift games",
			"DARKSTAR" : "Dark Star: Singularity games",
			"STARGUARDIAN" : "Star Guardian Invasion games",
			"PROJECT" : "PROJECT: Hunters games"}
GAMETYPE = {"CUSTOM_GAME" : "Custom games",
			"TUTORIAL_GAME" : "Tutorial games",
			"MATCHED_GAME" : "Matched games"}
rateLimit = [[20, 1], [100, 120]]

@rate_limited(rateLimit[0][0], rateLimit[0][1])
@rate_limited(rateLimit[1][0], rateLimit[1][1])
def apiRequest(url, region, headers, parameters=None):
	if parameters != None:
		url += "?"
		for parameter in parameters:
			if parameters[parameter] == None:
				continue
			url += parameter + "=" + str(parameters[parameter]) + "&"
		url = url[:-1]
	data = re.get("https://" + region.lower() + ".api.riotgames.com" + url, headers=headers)
	try:
		rateLimits = data.headers["X-App-Rate-Limit"].split(",")
		global rateLimit
		rateLimit[0][0] = rateLimits[0].split(":")[0]
		rateLimit[0][1] = rateLimits[0].split(":")[1]
		rateLimit[1][0] = rateLimits[1].split(":")[0]
		rateLimit[1][1] = rateLimits[1].split(":")[1]
	except KeyError:
		pass
	if data.status_code != re.codes.ok:
		data.raise_for_status()
	return data

def getKDA(playerStats):
	kills = playerStats["stats"]["kills"]
	deaths = playerStats["stats"]["deaths"]
	assists = playerStats["stats"]["assists"]
	if deaths == 0:
		return None
	else:
		return (kills+assists)/deaths

class LeagueAPI:
	def __init__(self, apiKey, region, locale="en_US", version=None):
		self.apiKey = apiKey
		self.region = region
		self.headers = {"X-Riot-Token" : self.apiKey}
		self.locale = locale
		self.version = version

	def championData(self):
		if time.time() - os.path.getmtime("championData.json") < 24*60*60:
			with open("championData.json", "r") as infile:
				championDataDict = json.loads(infile.read())
		else:
			championDataResponse = apiRequest("/lol/static-data/v3/champions", self.region, self.headers, parameters={"champListData" : "all", "version" : self.version, "dataById" : "false", "locale" : self.locale})
			with open("championData.json", "w") as outfile:
				outfile.write(championDataResponse.text)
			championDataDict = json.loads(championDataResponse.text)
		championsByName = {}
		championsByKey = {}
		championsById = {}
		for championData in championDataDict["data"]:
			champion = Champion(championDataDict["data"][championData])
			championsByName[championDataDict["data"][championData]["name"]] = champion
			championsByKey[championDataDict["data"][championData]["key"]] = champion
			championsById[championDataDict["data"][championData]["id"]] = champion
		return {"name" : championsByName, "key" : championsByKey, "id" : championsById}

	def getSummoner(self, url):
		summonerDataResponse = apiRequest(url, self.region, self.headers)
		summonerDataDict = json.loads(summonerDataResponse.text)
		return Summoner(summonerDataDict, self.apiKey, self.region)

	def summonerByName(self, summonerName):
		return self.getSummoner("/lol/summoner/v3/summoners/by-name/" + summonerName)

	def summonerByAccountId(self, accountId):
		return self.getSummoner("/lol/summoner/v3/summoners/by-account/" + accountId)

	def summonerBySummonerId(self, summonerId):
		return self.getSummoner("/lol/summoner/v3/summoners/" + summonerId)


class Summoner:
	def __init__(self, summonerData, apiKey, region):
		self.apiKey = apiKey
		self.region = region
		self.headers = {"X-Riot-Token" : self.apiKey}
		try:
			self.profileIconId = summonerData["profileIconId"]
			self.name = summonerData["name"]
			self.summonerLevel = summonerData["summonerLevel"]
			self.accountId = summonerData["accountId"]
			self.revisionData = summonerData["revisionDate"]
			self.id = summonerData["id"]
		except KeyError:
			self.profileIconId = summonerData["profileIcon"]
			self.name = summonerData["summonerName"]
			self.accountId = summonerData["accountId"]
			self.id = summonerData["summonerId"]

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.name

	def getMatchHistory(self, queue=None, season=None, champion=None):
		matchHistoryData = apiRequest("/lol/match/v3/matchlists/by-account/" + str(self.accountId), self.region, self.headers, {"queue" : queue, "season" : season, "champion" : champion.id})
		matchHistory = [json.loads(matchiHistoryData.text)]
		endIndex = matchHistory[0]["endIndex"]
		totalGames = matchHistory[0]["totalGames"]
		while endIndex < totalGames:
			matchHistory.append(json.loads(apiRequest("/lol/match/v3/matchlists/by-account/" + str(self.accountId), self.region, self.headers, {"queue" : queue, "season" : season, "champion" : champion.id, "beginIndex" : endIndex}).text))
			endIndex = matchHistory[-1]["endIndex"]
		return matchHistory

	def getRecentMatchHistory(self):
		matchHistoryData = apiRequest("/lol/match/v3/matchlists/by-account/" + str(self.accountId) + "/recent/", self.region, self.headers)
		matchHistory = json.loads(matchHistoryData.text)
		matches = []
		for match in matchHistory["matches"]:
			matches.append(Match(match, self.apiKey, self.region))
		return matches

	def championMasteryOneChampion(self, champion):
		championMasteryResponse = apiRequest("/lol/champion-mastery/v3/champion-masteries/by-summoner/" + str(self.id) + "/by-champion/" + str(champion.id), self.region, self.headers)
		return json.loads(championMasteryResponse.text)

class Champion:
	def __init__(self, championData):
		self.title = championData["title"]
		self.name = championData["name"]
		self.key = championData["key"]
		self.id = championData["id"]
		self.info = championData["info"]
		self.enemytips = championData["enemytips"]
		self.stats = championData["stats"]
		self.image = championData["image"]
		self.tags = championData["tags"]
		self.partype = championData["partype"]
		self.skins = championData["skins"]
		self.passive = championData["passive"]
		self.recommended = championData["recommended"]
		self.allytips = championData["allytips"]
		self.lore = championData["lore"]
		self.blurb = championData["blurb"]
		self.spells = championData["spells"]

	def __str__(self):
		return self.name + " " + self.title

	def __repr__(self):
		return self.name + " " + self.title

class Match:
	def __init__(self, matchData, apiKey, region):
		self.apiKey = apiKey
		self.region = region
		self.headers = {"X-Riot-Token" : self.apiKey}
		self.lane = matchData["lane"]
		self.gameId = matchData["gameId"]
		self.champion = matchData["champion"]
		self.platformId = matchData["platformId"]
		self.timestamp = matchData["timestamp"]
		self.queue = matchData["queue"]
		self.role = matchData["role"]
		self.season = matchData["season"]
		self.detailed = False

	def getMatchDetails(self):
		self.detailed = True
		matchDetailsResponse = apiRequest("/lol/match/v3/matches/" + str(self.gameId), self.region, self.headers)
		matchDetails = json.loads(matchDetailsResponse.text)
		self.participants = {}
		for i in range(0, 10):
			self.participants[matchDetails["participantIdentities"][i]["participantId"]] = Summoner(matchDetails["participantIdentities"][i]["player"], self.apiKey, self.region)
		self.version = matchDetails["gameVersion"]
		self.gameMode = matchDetails["gameMode"]
		self.mapId = matchDetails["mapId"]
		self.gameType = matchDetails["gameType"]
		self.blueTeam = matchDetails["teams"][0]
		self.redTeam = matchDetails["teams"][1]
		self.participantStats = matchDetails["participants"]

	def getPlayerStats(self, summoner):
		if not self.detailed:
			self.getMatchDetails()
		for participant in self.participants:
			if summoner.id == self.participants[participant].id:
				participantId = participant
				break
		for i in range(0, 10):
			if self.participantStats[i]["participantId"] == participantId:
				return self.participantStats[i]


if __name__ == "__main__":
	temp = LeagueAPI(sys.argv[1], "EUW1")
	me = temp.summonerByName("Posanimus")
	championData = temp.championData()
	championMastery = me.championMasteryOneChampion(championData["name"]["Bard"])
	print("Mastery points on " + repr(championData["name"]["Bard"]) + ": " + str(championMastery["championPoints"]))
	matches = me.getRecentMatchHistory()
	print("My KDA in my last game: %f" % getKDA(matches[0].getPlayerStats(me)))