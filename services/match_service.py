"""Connects all 5 layers (see image)"""

# ========== Imports ==========
import discord
from typing import Optional, Tuple

from riot.api import get_match_data, get_match_id
from riot.extractors import *
from rendering.overview import generate_overview_image
from track_manager.track_data import TrackManager


# ========== Function ==========
async def generate_image(
        discord_id: int,
        guild_id: int,
        tracker: TrackManager,
        image_type: str
) -> Tuple[Optional[discord.File], str]:
    
    # 1. TRIGGER LAYER
    # Trigger layer is the command that called this function.

    # 2. IDENTITY LAYER
    guild = tracker.get_guild(guild_id)
    if not guild:
        return None, "Guild doesn't exist."
    
    user = guild.get_member(discord_id)
    if not user:
        return None, "You're not being tracked. Enable tracking by doing /add_user."
    

    # 3. DATA LAYER
    if user.recent_match is None:
        return None, "You have not played any recent matches."
    
    match_data = await get_match_data(user.recent_match, user.region)
    if not match_data:
        return None, "Unable to fetch match data."
    
    # 4. INTERPRETATION LAYER
    # We always need to generate an overview
    if image_type == "overview":
        image_buffer = generate_overview_image()
        discord_file = discord.File(fp=image_buffer, filename=f"overview_{user.recent_match}.png")
        return discord_file, ""
    
    return None, "Invalid image request."

