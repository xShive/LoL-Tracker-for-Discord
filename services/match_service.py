"""Connects all 5 layers (see image)"""

# ========== Imports ==========
import discord

from riot.api import get_match_data, get_match_id
from track_manager.track_data import TrackManager



# ========== Imports ==========
async def generate_image(
        discord_id: int,
        guild_id: int,
        tracker: TrackManager,
        image_type = str
):
    # 1. TRIGGER LAYER
    # Trigger layer is the command that called this function.

    # 2. IDENTITY LAYER
    """TODO: implement logic to get user"""

    # 3. DATA LAYER
    """TODO: get raw json response of type MatchData"""

    # 4. INTERPRETATION LAYER
    """TODO: extract meaningful stats"""

    if image_type == "overview":
        """TODO: call the overview.py (pass the meaningful data) function in rendering module which returns the generated image"""
        pass 