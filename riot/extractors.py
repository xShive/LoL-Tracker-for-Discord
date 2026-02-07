# ========== Imports ==========
from typing import Optional, List
from riot.riot_types import *


# ========== Functions ==========
def get_match_metadata(data: MatchData) -> Optional[MatchMetadata]:
    """Extracts MatchMetadata from MatchData. Returns None if missing."""
    return data.get('metadata')

def get_match_info(data: MatchData) -> Optional[MatchInfo]:
    """Extracts MatchInfo from MatchData. Returns None if missing."""
    return data.get('info')

def get_participants(data: MatchInfo) -> Optional[List[ParticipantData]]:
    """Extracts a list of ParticipantData from Matchdata. Returns None if missing.
        ParticipantData contains all 'useful' player statistics like kills."""
    return data.get('participants')

def get_challenges_data(data: ParticipantData) -> Optional[ChallengesData]:
    """Extracts ChallengesData from ParticipantData. Returns None if missing.
        ChallengesData contains oddly specific player statistics like epicMonsterKillsNearEnemyJungler."""
    return data.get('challenges')

def get_missions_data(data: ParticipantData) -> Optional[MissionData]:
    """Extracts MissionsData from ParticipantData. Returns None if missing.
        I've got no fucking clue what this is."""
    return data.get('missions')

def get_perks_data(data: ParticipantData) -> Optional[PerksData]:
    """Extracts PerksData from ParticipantData. Returns None if missing."""
    return data.get('perks')

def get_perk_stat_data(data: PerksData) -> Optional[PerkStatData]:
    """Extracts PerkStatData from PerksData. Returns None if missing."""
    return data.get('statPerks')

def get_perk_style_data(data: PerksData) -> Optional[List[PerkStyleData]]:
    """Extracts a list of PerkStyleData from PerksData. Returns None if missing."""
    return data.get('styles')

def get_perk_style_selection_data(data: PerkStyleData) -> Optional[List[PerkStyleSelectionData]]:
    """Extracts a list of PerkStyleSelectionData from PerkStyleData. Returns None if missing.
        (no fucking clue what this is again)"""
    return data.get('selections')

def get_team_data(data: MatchInfo) -> Optional[List[TeamData]]:
    """Extracts a list of TeamData from MatchData. Returns None if missing.
        TeamData contains bans, objectives, ..."""
    return data.get('teams')

def get_bans_data(data: TeamData) -> Optional[list[BanData]]:
    """Returns a list of BanData from TeamData. Returns None if missing."""
    return data.get('bans')

def get_objectives_data(data: TeamData) -> Optional[ObjectivesData]:
    """Returns ObjectivesData from TeamData. Returns None if missing."""
    return data.get('objectives')