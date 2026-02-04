"""Connects all 5 layers (see image)"""

# ========== Imports ==========
import discord
from typing import Optional

from riot.api import get_match_data, get_match_id
from riot.extractors import *
from track_manager.track_data import TrackManager


# ========== Function ==========
async def generate_image(
        discord_id: int,
        guild_id: Optional[int],
        tracker: TrackManager,
        image_type: str
) -> Optional[discord.File]:
    
    # 1. TRIGGER LAYER
    # Trigger layer is the command that called this function.

    # 2. IDENTITY LAYER
    guild = tracker.get_guild(guild_id)
    if not guild:
        return None
    
    user = guild.get_member(discord_id)
    if not user:
        return None
    

    # 3. DATA LAYER
    match_id = await get_match_id(user.puuid, user.region)
    if not match_id or match_id in user.matches:
        return None
    
    match_data = await get_match_data(match_id, user.region)
    if not match_data:
        return None
    
    # 4. INTERPRETATION LAYER
    # We always need to generate an overview


