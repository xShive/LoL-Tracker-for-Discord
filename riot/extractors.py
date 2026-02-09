# ========== Imports ==========
from typing import Optional, List, Tuple
from riot.riot_types import *


# ========== Functions ==========
def get_match_metadata(data: MatchData) -> MatchMetadata:
    """Extracts MatchMetadata from MatchData. Always present in valid match data."""
    return data['metadata']

def get_match_info(data: MatchData) -> MatchInfo:
    """Extracts MatchInfo from MatchData. Always present in valid match data."""
    return data['info']

def get_participants(data: MatchData) -> List[ParticipantData]:
    """Extracts a list of ParticipantData from MatchData. Always contains exactly 10 players.
        ParticipantData contains all player statistics like kills, deaths, assists, etc."""
    return data['info']['participants']

def get_challenges_data(data: ParticipantData) -> Optional[ChallengesData]:
    """Extracts ChallengesData from ParticipantData. May return None if missing.
        Contains specialized statistics like epicMonsterKillsNearEnemyJungler, controlWardTimeCoverage, etc."""
    return data.get('challenges')

def get_missions_data(data: ParticipantData) -> Optional[MissionData]:
    """Extracts MissionData from ParticipantData. May return None if missing.
        Contains mission-related statistics for applicable game modes."""
    return data.get('missions')

def get_perks_data(data: ParticipantData) -> Optional[PerksData]:
    """Extracts PerksData from ParticipantData. May return None if missing.
        Contains rune and stat perk selections."""
    return data.get('perks')

def get_perk_stat_data(data: PerksData) -> Optional[PerkStatData]:
    """Extracts PerkStatData from PerksData. May return None if missing.
        Contains stat bonuses from defensive, flex, and offensive runes."""
    return data.get('statPerks')

def get_perk_style_data(data: PerksData) -> Optional[List[PerkStyleData]]:
    """Extracts a list of PerkStyleData from PerksData. May return None if missing.
        Contains primary and secondary rune tree information."""
    return data.get('styles')

def get_perk_style_selection_data(data: PerkStyleData) -> Optional[List[PerkStyleSelectionData]]:
    """Extracts a list of PerkStyleSelectionData from PerkStyleData. May return None if missing.
        Contains the individual perk selections within a rune style."""
    return data.get('selections')

def get_team_data(data: MatchInfo) -> List[TeamData]:
    """Extracts a list of TeamData from MatchInfo. May return None if missing.
        Contains team-level data like bans, objectives, and teamwide statistics."""
    return data['teams']

def get_bans_data(data: TeamData) -> Optional[list[BanData]]:
    """Returns a list of BanData from TeamData. May return None if missing.
        Contains champion bans for each team."""
    return data.get('bans')

def get_objectives_data(data: TeamData) -> Optional[ObjectivesData]:
    """Returns ObjectivesData from TeamData. May return None if missing.
        Contains team objectives like towers, dragons, barons, and inhibitors."""
    return data.get('objectives')

def get_both_ranks(
    entries: list[RankData]
) -> Tuple[Optional[RankData], Optional[RankData]]:
    """Extracts both Solo and Flex ranks from a list of RankData in a single pass.
    
    Returns a tuple of (solo_rank, flex_rank). Each can be None if not found.
    """
    solo_rank = None
    flex_rank = None
    
    for entry in entries:
        queue_type = entry.get("queueType")
        if queue_type == "RANKED_SOLO_5x5":
            solo_rank = entry
        elif queue_type == "RANKED_FLEX_SR":
            flex_rank = entry
    
    return solo_rank, flex_rank