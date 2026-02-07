# ========== Imports ==========
import os
import dotenv
import aiohttp

from typing import Optional
from riot.riot_types import MatchData


# ========== Configuration ==========
# we request data from riot. riot looks at headers to check for access.
# riot looks for "X-Riot-Token"
dotenv.load_dotenv()
RIOT_TOKEN = os.getenv("RIOT_TOKEN")
if RIOT_TOKEN is None: raise ValueError("RIOT_TOKEN not found in .env file.")

HEADERS = {
    "X-Riot-Token" : RIOT_TOKEN
}

RegionCode = str

REGIONS = {
    # AMERICAS
    "NA": "https://americas.api.riotgames.com",
    "BR": "https://americas.api.riotgames.com",
    "LAN": "https://americas.api.riotgames.com",
    "LAS": "https://americas.api.riotgames.com",
    "OCE": "https://americas.api.riotgames.com",
    "PBE": "https://americas.api.riotgames.com",

    # EUROPES
    "EUW": "https://europe.api.riotgames.com",
    "EUNE": "https://europe.api.riotgames.com",
    "TR": "https://europe.api.riotgames.com",
    "RU": "https://europe.api.riotgames.com",

    # ASIA
    "KR": "https://asia.api.riotgames.com",
    "JP": "https://asia.api.riotgames.com",

    # RANDOMS ASIA
    "PH": "https://sea.api.riotgames.com",
    "SG": "https://sea.api.riotgames.com",
    "TW": "https://sea.api.riotgames.com",
    "TH": "https://sea.api.riotgames.com",
    "VN": "https://sea.api.riotgames.com",
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

    region_url = REGIONS.get(region_code)
    if region_url is None:
        return None

    full_url = f"{region_url}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"

    async with session.get(full_url, headers=HEADERS) as response:
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
    
    region_url = REGIONS.get(region)
    if region_url is None:
        return None

    full_url = f"{region_url}/lol/match/v5/matches/by-puuid/{puuid}/ids"

    async with session.get(full_url, headers=HEADERS) as response:
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
        Optional[dict[str, Any]]: A dictionary where each key is a string describing the statistic and a value of type Any. Returns None if error.
    """

    region_url = REGIONS.get(region)
    if region_url is None:
        return None

    full_url = f"{region_url}/lol/match/v5/matches/{match_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(full_url, headers=HEADERS) as response:
            if response.status == 200:
                return await response.json()
            
            else:
                print(f"Error: {response.status}")
                return None