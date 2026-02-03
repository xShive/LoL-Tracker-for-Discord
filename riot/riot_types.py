# ========== Imports ==========
from typing import TypedDict, Any, List, Dict

# ========== Helper TypeDicts ==========
class BanData(TypedDict):
    championId: int
    pickTurn: int

class ObjectiveData(TypedDict):
    first: bool
    kills: int

class ObjectivesData(TypedDict):
    baron: ObjectiveData
    dragon: ObjectiveData
    tower: ObjectiveData
    riftHerald: ObjectiveData
    inhibitor: ObjectiveData

class TeamData(TypedDict):
    teamId: int
    win: bool
    bans: List[BanData]
    objectives: ObjectivesData

class PerksData(TypedDict, total=False):
    statPerks: Dict[str, int]
    styles: List[Dict[str, Any]]


# ========== Participant Data ==========
class ParticipantData(TypedDict, total=False):
    # Pings & Communication
    allInPings: int
    assistMePings: int
    baitPings: int 
    basicPings: int
    commandPings: int
    dangerPings: int
    enemyMissingPings: int
    enemyVisionPings: int
    getBackPings: int
    holdPings: int
    needVisionPings: int
    onMyWayPings: int
    pushPings: int
    visionClearedPings: int

    # Identity & Player Info
    puuid: str
    summonerName: str
    summonerId: str
    summonerLevel: int
    riotIdGameName: str
    riotIdTagline: str
    profileIcon: int
    participantId: int
    teamId: int
    
    # Champion & Game State
    championName: str
    championId: int
    championTransform: int
    champExperience: int
    champLevel: int
    role: str
    lane: str
    individualPosition: str
    teamPosition: str
    win: bool
    gameEndedInEarlySurrender: bool
    gameEndedInSurrender: bool
    teamEarlySurrendered: bool
    timePlayed: int
    
    # Kills / Deaths / Assists
    kills: int
    deaths: int
    assists: int
    kda: float
    killingSprees: int
    largestKillingSpree: int
    largestMultiKill: int
    doubleKills: int
    tripleKills: int
    quadraKills: int
    pentaKills: int
    unrealKills: int
    firstBloodAssist: bool
    firstBloodKill: bool
    firstTowerAssist: bool
    firstTowerKill: bool
    bountyLevel: int
    
    # Damage Dealt
    totalDamageDealt: int
    totalDamageDealtToChampions: int
    physicalDamageDealt: int
    physicalDamageDealtToChampions: int
    magicDamageDealt: int
    magicDamageDealtToChampions: int
    trueDamageDealt: int
    trueDamageDealtToChampions: int
    damageDealtToBuildings: int
    damageDealtToObjectives: int
    damageDealtToTurrets: int
    largestCriticalStrike: int
    timeCCingOthers: int
    totalTimeCCDealt: int

    # Damage Taken & Healing
    totalDamageTaken: int
    physicalDamageTaken: int
    magicDamageTaken: int
    trueDamageTaken: int
    damageSelfMitigated: int
    totalHeal: int
    totalHealsOnTeammates: int
    totalUnitsHealed: int
    totalDamageShieldedOnTeammates: int
    longestTimeSpentLiving: int
    totalTimeSpentDead: int

    # Vision
    visionScore: int
    wardsPlaced: int
    wardsKilled: int
    detectorWardsPlaced: int
    visionWardsBoughtInGame: int
    sightWardsBoughtInGame: int

    # Economy & Items
    goldEarned: int
    goldSpent: int
    consumablesPurchased: int
    itemsPurchased: int
    item0: int
    item1: int
    item2: int
    item3: int
    item4: int
    item5: int
    item6: int

    # Minions & Jungle
    totalMinionsKilled: int
    neutralMinionsKilled: int
    totalAllyJungleMinionsKilled: int
    totalEnemyJungleMinionsKilled: int
    
    # Objectives
    turretKills: int
    turretTakedowns: int
    turretsLost: int
    inhibitorKills: int
    inhibitorTakedowns: int
    inhibitorsLost: int
    nexusKills: int
    nexusTakedowns: int
    nexusLost: int
    dragonKills: int
    baronKills: int
    objectivesStolen: int
    objectivesStolenAssists: int

    # Spell Casts
    spell1Casts: int
    spell2Casts: int
    spell3Casts: int
    spell4Casts: int
    summoner1Casts: int
    summoner1Id: int
    summoner2Casts: int
    summoner2Id: int

    # Arena / Special Modes
    playerAugment1: int
    playerAugment2: int
    playerAugment3: int
    playerAugment4: int
    playerSubteamId: int
    subteamPlacement: int
    placement: int

    # Complex Objects
    # Challenges has hundreds of dynamic keys, so we use Dict[str, Any]
    challenges: Dict[str, Any] 
    missions: Dict[str, Any]
    perks: PerksData

    # Scores (Dominion/Old Modes)
    playerScore0: int
    playerScore1: int
    playerScore2: int
    playerScore3: int
    playerScore4: int
    playerScore5: int
    playerScore6: int
    playerScore7: int
    playerScore8: int
    playerScore9: int
    playerScore10: int
    playerScore11: int
    eligibleForProgression: bool

# ========== Match Wrappers ==========
class GameInfo(TypedDict):
    gameStartTimestamp: int
    gameDuration: int
    gameMode: str
    teams: List[TeamData]
    participants: List[ParticipantData]

class MatchMetadata(TypedDict):
    matchId: str
    participants: List[str]

class MatchData(TypedDict):
    metadata: MatchMetadata
    info: GameInfo