# ========== Imports ==========
import os
import discord
from track_manager.track_data import *

DEV_TOKEN = os.getenv("DEV_TOKEN")


# ========== Functions ==========
def get_guild_from_interaction(interaction: discord.Interaction, track: TrackManager) -> Optional[Guild]:
    """If the guild_id - where the interaction is being sent from - exists in the database, return its info. Else None.
    """
    if interaction.guild_id is None:
        return None
    return track.get_guild(interaction.guild_id)

def validate_user(interaction: discord.Interaction) -> bool:
    """Checks if the user is allowed to use the following command, this means its part of the env file"""
    if DEV_TOKEN:
        return str(interaction.user.id) in DEV_TOKEN
    return False