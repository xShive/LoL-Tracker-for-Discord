# ========== Imports ==========
import discord

from riot.api import *
from services.match_service import generate_image
from track_manager.track_data import TrackManager


# ========== Commands registry ==========
def register_commands(tree):
    @tree.command(name="recent_match", description="show an overview of you most recent LoL game.")
    async def recent_matches(interaction: discord.Interaction):
        await interaction.response.defer()

        file = await generate_image(interaction.user.id, interaction.guild_id, TrackManager(), "overview")

        if file:
            await interaction.followup.send(file=file)
        else:
            await interaction.followup.send("Could not generate image.")