# ========== Imports ==========
import discord

from discord import app_commands
from riot import get_puuid


# ========== Commands registry ==========
def register_commands(tree):
    @tree.command(name="recent_matches", description="show recent league of legends matches for a gamer")
    async def recent_matches(interaction: discord.Interaction, riot_name: str, region: str):
        await interaction.response.defer()

        if '#' not in riot_name:
            await interaction.edit_original_response(content="Invalid Riot name. Please include the tagline (#)")
            return

        name_parts = riot_name.split("#")

        puuid = get_puuid(name_parts[0], name_parts[1], region)
        if puuid is None:
            await interaction.edit_original_response(content="Unexpected error.")

        await interaction.edit_original_response(content=f"Your PUUID: {puuid}")
        return

