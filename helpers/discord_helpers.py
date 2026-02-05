# ========== Imports ==========
import discord
from track_manager.track_data import *


# ========== Global ==========
track = TrackManager()


# ========== Functions ==========
def get_guild_from_interaction(interaction: discord.Interaction) -> Optional[Guild]:
    """If the guild_id - where the interaction is being sent from - exists in the database, return its info. Else None.
    """
    if interaction.guild_id is None:
        return None
    return track.get_guild(interaction.guild_id)