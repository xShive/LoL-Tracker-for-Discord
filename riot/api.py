# ========== Imports ==========
import os
import aiohttp

from typing import Optional, Tuple
from riot.riot_types import MatchData, RankData


# ========== Configuration ==========
def _get_headers() -> dict:
    token = os.getenv("RIOT_TOKEN")
    if not token:
        raise RuntimeError("RIOT_TOKEN not set in environment")
    return {"X-Riot-Token": token}

RegionCode = str

# MatchV5 and AccountV1
# from here: https://eloking.com/blog/league-of-legends-all-server-location
REGIONS_ROUTING = {
    # AMERICAS
    "NA": "https://americas.api.riotgames.com",
    "BR": "https://americas.api.riotgames.com",
    "LAN": "https://americas.api.riotgames.com",
    "LAS": "https://americas.api.riotgames.com",
    "OCE": "https://americas.api.riotgames.com",
    "PBE": "https://americas.api.riotgames.com",       # public beta environment, not in platforms

    # EUROPES
    "EUW": "https://europe.api.riotgames.com",
    "EUNE": "https://europe.api.riotgames.com",
    "TR": "https://europe.api.riotgames.com",
    "RU": "https://europe.api.riotgames.com",

    # ASIA
    "KR": "https://asia.api.riotgames.com",
    "JP": "https://asia.api.riotgames.com",

    # SEA
    "PH": "https://sea.api.riotgames.com",
    "SG": "https://sea.api.riotgames.com",
    "TW": "https://sea.api.riotgames.com",
    "TH": "https://sea.api.riotgames.com",
    "VN": "https://sea.api.riotgames.com",
}


# SummonerV4 and LeagueV4
PLATFORM_ROUTING = {
    # AMERICAS
    "NA": "https://na1.api.riotgames.com",
    "BR": "https://br1.api.riotgames.com",
    "LAN": "https://la1.api.riotgames.com",
    "LAS": "https://la2.api.riotgames.com",
    "OCE": "https://oc1.api.riotgames.com",
    
    # EUROPE
    "EUW": "https://euw1.api.riotgames.com",
    "EUNE": "https://eun1.api.riotgames.com",
    "TR": "https://tr1.api.riotgames.com",
    "RU": "https://ru.api.riotgames.com",
    
    # ASIA
    "KR": "https://kr.api.riotgames.com",
    "JP": "https://jp1.api.riotgames.com",

    # SEA
    "PH": "https://ph2.api.riotgames.com",
    "SG": "https://sg2.api.riotgames.com",
    "TH": "https://th2.api.riotgames.com",
    "TW": "https://tw2.api.riotgames.com",
    "VN": "https://vn2.api.riotgames.com",
}

# ========== Functions ==========
async def get_puuid(
    game_name: str,
    tag_line: str,
    region_code: RegionCode,
    session: aiohttp.ClientSession
) -> Optional[str]:
    """Retrieves PUUID from name-tag and region.

    Args:
        game_name (str): Username
        tag_line (str): Tag (#)
        region_code (RegionCode): Region code in which the user resides.

    Returns:
        Optional[str]: The corresponding PUUID or None if error.
    """

    region_url = REGIONS_ROUTING.get(region_code)
    if region_url is None:
        return None

    full_url = f"{region_url}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"

    async with session.get(full_url, headers=_get_headers()) as response:
        if response.status == 200:
            data = await response.json()
            return data.get("puuid")

        else:
            print(f"Error: {response.status}")
            return None
            

async def get_match_id(
    puuid: str,
    region: RegionCode,
    session: aiohttp.ClientSession
) -> Optional[str]:
    """Retrieves most recent match from PUUID and region.

    Args:
        puuid (str): The user's PUUID
        region (RegionCode): Region code in which the user resides.

    Returns:
        Optional[str]: The corresponding match ID or None if error.
    """
    
    region_url = REGIONS_ROUTING.get(region)
    if region_url is None:
        return None

    full_url = f"{region_url}/lol/match/v5/matches/by-puuid/{puuid}/ids"

    async with session.get(full_url, headers=_get_headers()) as response:
        if response.status == 200:
            data: list[str] = await response.json()
        
            if not data:
                return None
            
            return data[0]
        
        else:
            print(f"Error: {response.status}")
            return None


async def get_match_data(
    match_id: str,
    region: RegionCode,
    session: aiohttp.ClientSession
) -> Optional[MatchData]:
    """Retrieves the data of a match ID and region.

    Args:
        match_id (str): The ID of the match.
        region (RegionCode): Region code in which the user resides.

    Returns:
        Optional[MatchData]: The raw response .json sent by riot. None if error.
    """

    region_url = REGIONS_ROUTING.get(region)
    if region_url is None:
        return None

    full_url = f"{region_url}/lol/match/v5/matches/{match_id}"

    async with session.get(full_url, headers=_get_headers()) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Error: {response.status}")
            return None
    

async def get_rank_data(
    puuid: str,
    region: RegionCode,
    session: aiohttp.ClientSession
) -> Tuple[list[RankData], str]:
    """Retrieves all rank entries for a summoner.

    Args:
        summoner_id (str): The summoner's ID
        region (RegionCode): Region code in which the user resides.
        session (aiohttp.ClientSession): HTTP session for making requests.

    Returns:
        Optional[list[RankData]]: List of rank entries (Solo, Flex, etc.) or None if error.
        Info: There are two queues: solo and flex. The list contains those two and their specific info
    """
    platform_url = PLATFORM_ROUTING.get(region)
    if not platform_url:
        return [], "error"

    full_url = f"{platform_url}/lol/league/v4/entries/by-puuid/{puuid}"

    async with session.get(full_url, headers=_get_headers()) as response:
        if response.status == 200:
            data = await response.json()
            return data or [], "ok"
        
        elif response.status == 403:
            return [], "unfetchable"
        
        else:
            print(f"Error: {response.status}")
            return [], "error"
