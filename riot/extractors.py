# ========== Imports ==========
from typing import Optional, List
from riot.riot_types import MatchData, GameInfo, ParticipantData, TeamData


# ========== Functions ==========
def get_game_info(data: MatchData) -> GameInfo:
    return data['info']

def get_teams(data: MatchData) -> List[TeamData]:
    return data['info']['teams']

def get_participants(data: MatchData) -> List[ParticipantData]:
    return data['info']['participants']

def get_player_stats(data: MatchData, target_puuid: str) -> Optional[ParticipantData]:
    participants = data['info']['participants']
    
    for player in participants:
        if player.get('puuid') == target_puuid:
            return player
            
    return None