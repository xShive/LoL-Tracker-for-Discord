# ========== Imports ==========
import aiohttp

from riot.api import get_puuid, get_match_id, REGIONS
from typing import Optional, Tuple


# ========== Functions ==========
def split_riot_name(riot_name: str) -> Optional[Tuple[str, str]]:
    """Returns a tuple with the username and the tag. Returns None if username is invalid."""
    if "#" not in riot_name:
        return None
    return (riot_name.split("#")[0], riot_name.split("#")[1])


def validate_region(region: str) -> bool:
    """Returns True if the region is valid, else False."""
    region = region.upper()
    return True if region in REGIONS else False


async def get_puuid_and_match_id(
        riot_name: str, 
        region: str,
        session: aiohttp.ClientSession
) -> Tuple[Optional[str], Optional[str]]:
    """Returns a tuple with the puuid and the match_id. Returns None if either of them fail."""
    parsed = split_riot_name(riot_name)
    if not parsed:
        return None, None

    game_name, tag = parsed

    puuid = await get_puuid(game_name, tag, region, session)
    if not puuid:
        return None, None

    match_id = await get_match_id(puuid, region, session)
    if not match_id:
        return None, None

    return puuid, match_id