"""
riot_types.py

==========

This module contains TypeDict definitions for the Riot Games API (Match-V5: https://developer.riotgames.com/apis#match-v5).
These classes map the raw JSON response from Riot to strict Python types.

Primarily used to enable autocomplete when getting specific data from the huge JSON response.
"""

# ========== Imports ==========
from typing import TypedDict, List


# ========== Perks Wrappers ==========
class PerkStatData(TypedDict):
    defense: int
    flex: int
    offense: int

class PerkStyleSelectionData(TypedDict):
    perk: int
    var1: int
    var2: int
    var3: int

class PerkStyleData(TypedDict):
    description: str
    selections: List[PerkStyleSelectionData]
    style: int

class PerksData(TypedDict):
    statPerks: PerkStatData
    styles: List[PerkStyleData]


# ========== Challenges Data ==========
class ChallengesData(TypedDict, total=False):
    abilityUses: int
    acesBefore15Minutes: int
    alliedJungleMonsterKills: float
    
    baronBuffGoldAdvantageOverThreshold: int
    baronTakedowns: int
    blastConeOppositeOpponentCount: int
    bountyGold: int
    buffsStolen: int
    
    completeSupportQuestInTime: int
    controlWardTimeCoverageInRiverOrEnemyHalf: float
    controlWardsPlaced: int
    
    damagePerMinute: float
    damageTakenOnTeamPercentage: float
    dancedWithRiftHerald: int
    deathsByEnemyChamps: int
    dodgeSkillShotsSmallWindow: int
    doubleAces: int
    dragonTakedowns: int
    
    earliestBaron: int
    earliestDragonTakedown: int
    earliestElderDragon: int
    earlyLaningPhaseGoldExpAdvantage: int
    effectiveHealAndShielding: float
    elderDragonKillsWithOpposingSoul: int
    elderDragonMultikills: int
    enemyChampionImmobilizations: int
    enemyJungleMonsterKills: float
    epicMonsterKillsNearEnemyJungler: int
    epicMonsterKillsWithin30SecondsOfSpawn: int
    epicMonsterSteals: int
    epicMonsterStolenWithoutSmite: int
    
    fasterSupportQuestCompletion: int
    fastestLegendary: int
    firstTurretKilled: int
    firstTurretKilledTime: float
    fistBumpParticipation: int
    flawlessAces: int
    fullTeamTakedown: int
    
    gameLength: float
    getTakedownsInAllLanesEarlyJungleAsLaner: int
    goldPerMinute: float
    
    hadAfkTeammate: int
    hadOpenNexus: int
    highestChampionDamage: int
    highestCrowdControlScore: int
    highestWardKills: int
    
    immobilizeAndKillWithAlly: int
    InfernalScalePickup: int
    initialBuffCount: int
    initialCrabCount: int
    
    jungleCsBefore10Minutes: float
    junglerKillsEarlyJungle: int
    junglerTakedownsNearDamagedEpicMonster: int
    
    kda: float
    killAfterHiddenWithAlly: int
    killedChampTookFullTeamDamageSurvived: int
    killingSprees: int
    killParticipation: float
    killsNearEnemyTurret: int
    killsOnLanersEarlyJungleAsJungler: int
    killsOnOtherLanesEarlyJungleAsLaner: int
    killsOnRecentlyHealedByAramPack: int
    killsUnderOwnTurret: int
    killsWithHelpFromEpicMonster: int
    knockEnemyIntoTeamAndKill: int
    kTurretsDestroyedBeforePlatesFall: int
    
    landSkillShotsEarlyGame: int
    laneMinionsFirst10Minutes: int
    laningPhaseGoldExpAdvantage: int
    legendaryCount: int
    legendaryItemUsed: List[int]
    lostAnInhibitor: int
    
    maxCsAdvantageOnLaneOpponent: float
    maxKillDeficit: int
    maxLevelLeadLaneOpponent: int
    mejaisFullStackInTime: int
    moreEnemyJungleThanOpponent: float
    mostWardsDestroyedOneSweeper: int
    multiKillOneSpell: int
    multikills: int
    multikillsAfterAggressiveFlash: int
    multiTurretRiftHeraldCount: int
    mythicItemUsed: int
    
    outerTurretExecutesBefore10Minutes: int
    outnumberedKills: int
    outnumberedNexusKill: int
    
    perfectDragonSoulsTaken: int
    perfectGame: int
    pickKillWithAlly: int
    playedChampSelectPosition: int
    poroExplosions: int
    
    quickCleanse: int
    quickFirstTurret: int
    quickSoloKills: int
    
    riftHeraldTakedowns: int
    
    saveAllyFromDeath: int
    scuttleCrabKills: int
    shortestTimeToAceFromFirstTakedown: float
    skillshotsDodged: int
    skillshotsHit: int
    snowballsHit: int
    soloBaronKills: int
    soloKills: int
    soloTurretsLategame: int
    stealthWardsPlaced: int
    survivedSingleDigitHpCount: int
    survivedThreeImmobilizesInFight: int
    SWARM_DefeatAatrox: int
    SWARM_DefeatBriar: int
    SWARM_DefeatMiniBosses: int
    SWARM_EvolveWeapon: int
    SWARM_Have3Passives: int
    SWARM_KillEnemy: int
    SWARM_PickupGold: float
    SWARM_ReachLevel50: int
    SWARM_Survive15Min: int
    SWARM_WinWith5EvolvedWeapons: int
    
    takedownOnFirstTurret: int
    takedowns: int
    takedownsAfterGainingLevelAdvantage: int
    takedownsBeforeJungleMinionSpawn: int
    takedownsFirst25Minutes: int
    takedownsFirstXMinutes: int
    takedownsInAlcove: int
    takedownsInEnemyFountain: int
    teamBaronKills: int
    teamDamagePercentage: float
    teamElderDragonKills: int
    teamRiftHeraldKills: int
    teleportTakedowns: int
    thirdInhibitorDestroyedTime: int
    threeWardsOneSweeperCount: int
    tookLargeDamageSurvived: int
    turretPlatesTaken: int
    turretsTakenWithRiftHerald: int
    turretTakedowns: int
    twentyMinionsIn3SecondsCount: int
    twoWardsOneSweeperCount: int
    
    unseenRecalls: int
    
    visionScoreAdvantageLaneOpponent: float
    visionScorePerMinute: float
    voidMonsterKill: int
    
    wardsGuarded: int
    wardTakedowns: int
    wardTakedownsBefore20M: int


# ========== Mission Data ==========
class MissionData(TypedDict):
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

    
# ========== Participant Data ==========
# large participant data fields
# total = False so that it doesn't break if Riot changes things

class ParticipantData(TypedDict, total=False):
    allInPings: int
    assistMePings: int
    assists: int
    
    baronKills: int
    bountyLevel: int
    
    challenges: ChallengesData
    champExperience: int
    champLevel: int
    championId: int
    championName: str
    championTransform: int
    commandPings: int
    consumablesPurchased: int
    
    damageDealtToBuildings: int
    damageDealtToObjectives: int
    damageDealtToTurrets: int
    damageSelfMitigated: int
    deaths: int
    detectorWardsPlaced: int
    doubleKills: int
    dragonKills: int
    
    eligibleForProgression: bool
    enemyMissingPings: int
    enemyVisionPings: int
    
    firstBloodAssist: bool
    firstBloodKill: bool
    firstTowerAssist: bool
    firstTowerKill: bool
    
    gameEndedInEarlySurrender: bool
    gameEndedInSurrender: bool
    getBackPings: int
    goldEarned: int
    goldSpent: int
    
    holdPings: int
    
    individualPosition: str
    inhibitorKills: int
    inhibitorTakedowns: int
    inhibitorsLost: int
    item0: int
    item1: int
    item2: int
    item3: int
    item4: int
    item5: int
    item6: int
    itemsPurchased: int
    
    killingSprees: int
    kills: int
    
    lane: str
    largestCriticalStrike: int
    largestKillingSpree: int
    largestMultiKill: int
    longestTimeSpentLiving: int
    
    magicDamageDealt: int
    magicDamageDealtToChampions: int
    magicDamageTaken: int
    missions: MissionData
    
    needVisionPings: int
    neutralMinionsKilled: int
    nexusKills: int
    nexusLost: int
    nexusTakedowns: int
    
    objectivesStolen: int
    objectivesStolenAssists: int
    onMyWayPings: int
    
    participantId: int
    pentaKills: int
    perks: PerksData
    physicalDamageDealt: int
    physicalDamageDealtToChampions: int
    physicalDamageTaken: int
    placement: int
    playerAugment1: int
    playerAugment2: int
    playerAugment3: int
    playerAugment4: int
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
    playerSubteamId: int
    profileIcon: int
    pushPings: int
    puuid: str
    
    quadraKills: int
    
    riotIdGameName: str
    riotIdTagline: str
    role: str
    
    sightWardsBoughtInGame: int
    spell1Casts: int
    spell2Casts: int
    spell3Casts: int
    spell4Casts: int
    subteamPlacement: int
    summoner1Casts: int
    summoner1Id: int
    summoner2Casts: int
    summoner2Id: int
    summonerId: str
    summonerLevel: int
    summonerName: str
    
    teamEarlySurrendered: bool
    teamId: int
    teamPosition: str
    timeCCingOthers: int
    timePlayed: int
    totalAllyJungleMinionsKilled: int
    totalDamageDealt: int
    totalDamageDealtToChampions: int
    totalDamageShieldedOnTeammates: int
    totalDamageTaken: int
    totalEnemyJungleMinionsKilled: int
    totalHeal: int
    totalHealsOnTeammates: int
    totalMinionsKilled: int
    totalTimeCCDealt: int
    totalTimeSpentDead: int
    totalUnitsHealed: int
    tripleKills: int
    trueDamageDealt: int
    trueDamageDealtToChampions: int
    trueDamageTaken: int
    turretKills: int
    turretTakedowns: int
    turretsLost: int
    
    unrealKills: int
    
    visionClearedPings: int
    visionScore: int
    visionWardsBoughtInGame: int
    
    wardsKilled: int
    wardsPlaced: int
    win: bool


# ========== Objective Data ==========
class ObjectiveData(TypedDict):
    first: bool
    kills: int

class ObjectivesData(TypedDict):
    baron: ObjectiveData
    champion: ObjectiveData
    dragon: ObjectiveData
    horde: ObjectiveData
    inhibitor: ObjectiveData
    riftHerald: ObjectiveData
    tower: ObjectiveData


# ========== Team Wrappers ==========
class BanData(TypedDict):
    championId: int
    pickTurn: int

class TeamData(TypedDict):
    bans: List[BanData]
    objectives: ObjectivesData
    teamId: int
    win: bool


# ========== Match Wrappers ==========
# (first three on https://developer.riotgames.com/apis#match-v5/GET_getMatch)

class MatchInfo(TypedDict):
    gameId: int
    gameCreation: int
    gameDuration: int
    gameStartTimestamp: int
    gameEndTimestamp: int   # timestamp for when match ends on game server (calculate length using Start + Duration)
    gameMode: str
    gameType: str
    gameName: str
    gameVersion: str        
    mapId: int              # refer to Game Constants documentation
    platformId: str         # platform where match was placed (e.g. EUW1)
    queueId: int            # refer to Game Constants documentation
    tournamentCode: str     # tournament code used to generate match
    endOfGameResult: str    # indicate if game ended in termination
    
    teams: List[TeamData]
    participants: List[ParticipantData]

class MatchMetadata(TypedDict):
    matchId: str
    dataVersion: str
    participants: List[str]     # List of participants PUUIDs

# THIS IS THE JSON RESPONSE
class MatchData(TypedDict):
    metadata: MatchMetadata
    info: MatchInfo