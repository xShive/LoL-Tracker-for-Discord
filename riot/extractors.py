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

def get_participant_data(data: MatchData) -> Optional[List[ParticipantData]]:
    """Extracts ParticipantData from Matchdata. Returns None if missing.
        ParticipantData contains all 'useful' player statistics like kills.
    """
    return data.get('info').get('participants')