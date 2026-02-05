# ========== Imports ==========
import os
import dotenv
import discord

from helpers.riot_helpers import validate_region, get_puuid_and_match_id
from helpers.discord_helpers import get_guild_from_interaction, track


dotenv.load_dotenv()

DEV_TOKEN = os.getenv("DEV_TOKEN")
if not DEV_TOKEN is None:
    DEV_TOKEN_LIST = DEV_TOKEN.split(",")
else:
    print("ERROR: Enviroment variable for DEV_TOKEN is not properly set")
    DEV_TOKEN_LIST = []

# ========== Command Registry ==========
def register_commands(tree):
    @tree.command(name="add_user", description="Adds a user to the list ~dev-only")
    async def add_user(
        interaction: discord.Interaction,
        discord_user: discord.User,
        riot_name: str,
        region: str,
    ):
        if not str(discord_user.id) in DEV_TOKEN_LIST:
            await interaction.response.send_message("You're not authorized to use this feature.", ephemeral=True)
            return

        region = region.upper()
        if not validate_region(region):
            await interaction.response.send_message("Invalid region.", ephemeral=True)
            return
            
        puuid, match_id = await get_puuid_and_match_id(riot_name, region)
        if not puuid or not match_id:
            await interaction.response.send_message("Invalid Riot name or failed to fetch player data.",ephemeral=True)
            return

        guild = get_guild_from_interaction(interaction)
        if not guild:
            await interaction.response.send_message("This command must be used in a server.",ephemeral=True)
            return

        user = guild.add_member(discord_user.id, puuid, region)
        if not user:
            await interaction.response.send_message(f"User {discord_user.id} already exists.",ephemeral=True)
            return

        user.puuid = puuid
        user.matches = match_id

        track.save()
        await interaction.response.send_message("User has been successfully added.", ephemeral=True)


    @tree.command(name="remove_user", description="Removes a user from the list ~dev-only")
    async def remove_user(
        interaction: discord.Interaction,
        discord_user: discord.User,
    ):
        if not str(discord_user.id) in DEV_TOKEN_LIST:
            await interaction.response.send_message("You're not authorized to use this feature.", ephemeral=True)
            return

        guild = get_guild_from_interaction(interaction)
        if not guild:
            await interaction.response.send_message("Guild does not exist.", ephemeral=True)
            return

        if not guild.remove_member(discord_user.id):
            await interaction.response.send_message("User does not exist or could not be removed.", ephemeral=True)
            return

        track.save()
        await interaction.response.send_message("User has been successfully removed.", ephemeral=True,)
