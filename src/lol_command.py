import os
import requests

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('RIOT_API')
header = {
    "X-Riot-Token": API_KEY,
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
}


def getData(URL):
    res = requests.get(url=URL, headers=header)
    if len(str(res.json())) > 100:
        return res.json()


def getSummonerId(summonerName):
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}"
    req = requests.get(url, headers=header).json()

    summonerId = req["id"]
    return summonerId


def getAccountId(summonerName):
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}"
    req = requests.get(url, headers=header).json()

    accountId = req["accountId"]
    return accountId


def getSummonerRankInfo(encryptedSummonerId):
    url = f"https://kr.api.riotgames.com//lol/league/v4/entries/by-summoner/{encryptedSummonerId}"
    req = requests.get(url, headers=header)
    rankinfos = req.json()

    for rankinfo in rankinfos:
        if rankinfo["queueType"] == "RANKED_SOLO_5x5":
            break

    tier = rankinfo["tier"]
    rank = rankinfo["rank"]
    LP = rankinfo['leaguePoints']
    win = rankinfo['wins']
    loss = rankinfo['losses']

    total = win + loss
    winRate = round(win / total * 100, 2)
    reslut = tier + " " + rank + " " + \
        str(LP) + "LP\n" + str(win) + "승 " + \
        str(loss) + "패" + " " + str(winRate) + "%"
    return reslut


def getRankEmblem(encryptedSummonerId):
    url = f"https://kr.api.riotgames.com//lol/league/v4/entries/by-summoner/{encryptedSummonerId}"
    req = requests.get(url, headers=header)
    rankinfos = req.json()

    for rankinfo in rankinfos:
        if rankinfo["queueType"] == "RANKED_SOLO_5x5":
            break

    tier = rankinfo["tier"]

    return tier


def getSummonerMatchHistory(encryptedAccountId):
    url = f"https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{encryptedAccountId}"
    req = requests.get(url, headers=header)

    matches = req.json()["matches"]
    matches = matches[:1]

    gameIds = []
    for matche in matches:
        gameIds.append(matche['gameId'])

    recentMatchs = []
    for gameId in gameIds:
        url_gameData = f"https://kr.api.riotgames.com/lol/match/v4/matches/{gameId}"
        res_gameData = requests.get(url=url_gameData, headers=header)
        participantIdentities = res_gameData.json()['participantIdentities']

        for i in range(0, 10):
            playerid = participantIdentities[i].get(
                'player').get('summonerName')
            print(playerid)
        # recentMatch = participants['stats']['win']

        # team = participants[0]['championId']
        # print(team)

        # if (recentMatch == True):
        #     recentMatchs.append('승리')
        # else:
        #     recentMatchs.append('패배')

    return recentMatchs


# getSummonerInfo = getSummonerId('hide on bush')
# summonerId = getSummonerInfo[0]
# rank = getSummonerRankInfo(summonerId)
# print(summonerId)
# print(rank)
# getSummonerId('hide on bush')
# print(getSummonerRankInfo('Q1kJ0lNUmO2V6P1H90FuSX0Jb6b7Nj4_b90mTJXewGVRbQI'))
# print(getSummonerRankInfo('pMQjXMt0HR2GWOUXIKtOcAb2L46A9J4IyuLrGgmbRfdqrQ'))
# print(getAccountId('푸네')) # Huk8SYTVMrqSEKvz59CDWvMDb-wGxVK9Fpqtmg-PHo0b
# print(getAccountId('좋은참깨죽은참깨')) # BD4Iv3TPyM6c7eSSPa_uwet7M7ztnyHBUcdTz7nrlM2C
# print(getSummonerMatchHistory('BD4Iv3TPyM6c7eSSPa_uwet7M7ztnyHBUcdTz7nrlM2C'))
# getRankEmblem('pMQjXMt0HR2GWOUXIKtOcAb2L46A9J4IyuLrGgmbRfdqrQ')
