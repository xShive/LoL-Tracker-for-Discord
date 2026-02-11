# ========== Imports ==========
import aiohttp

from riot.api import get_puuid, get_match_id, REGIONS_ROUTING, get_rank_data
from riot.extractors import get_both_ranks
from riot.riot_types import RankData
from typing import Optional, Tuple


# ========== Functions ==========
def split_riot_name(riot_name: str) -> Optional[Tuple[str, str]]:
    """Returns a tuple with the username and the tag. Returns None if username is invalid."""
    if "#" not in riot_name:
        return None

    game_name, tag = riot_name.split("#", 1)
    return game_name, tag


def validate_region(region: str) -> bool:
    """Returns True if the region is valid, else False."""
    region = region.upper()
    return True if region in REGIONS_ROUTING else False


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
    region = region.upper()

    puuid = await get_puuid(game_name, tag, region, session)
    if not puuid:
        return None, None

    match_id = await get_match_id(puuid, region, session)
    if not match_id:
        return None, None

    return puuid, match_id


async def get_both_ranks_for_puuid(
        puuid: str,
        region: str,
        session: aiohttp.ClientSession
) -> Tuple[Optional[RankData], Optional[RankData], str]:
    """Fetches both Solo and Flex rank entries in a single API call.

    Returns a tuple of (solo_rank, flex_rank). Each can be None if not found.
    """
    entries, status = await get_rank_data(puuid, region, session)

    if status != "ok":
        return None, None, status

    solo_rank, flex_rank = get_both_ranks(entries)
    return solo_rank, flex_rank, "ok"

