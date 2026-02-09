# ========== Imports ==========
import os
import discord

from tracking.storage import TrackManager
from tracking.models import Guild
from typing import Optional

DEV_IDS = {int(x) for x in os.getenv("DEV_IDS", "").split(",") if x.strip()}


# ========== Functions ==========
def get_guild_from_interaction(interaction: discord.Interaction, track: TrackManager) -> Optional[Guild]:
    """If the guild_id - where the interaction is being sent from - exists in the database, return its info. Else None.
    """
    if interaction.guild_id is None:
        return None
    return track.get_guild(interaction.guild_id)

async def validate_user(interaction: discord.Interaction) -> bool:
    """Checks if the user is allowed to use the following command, this means its part of the env file"""
    return bool(DEV_IDS and interaction.user.id in DEV_IDS)