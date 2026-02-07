# ========== Imports ==========
from discord import app_commands
import discord

from riot.service import validate_region, get_puuid_and_match_id
from utils.discord import validate_user, get_guild_from_interaction
from track_manager.track_data import TrackManager
from commands.embeds import *
from main import http_session

# ========== Command Registry ==========
def register_commands(tree, track: TrackManager):

    @tree.command(name="add_user", description="Adds a user to the list ~dev-only")
    @app_commands.check(validate_user)
    async def add_user(
        interaction: discord.Interaction,
        discord_user: discord.User,
        riot_name: str,
        region: str,
    ):
        if http_session is None:
            await interaction.response.send_message("Bot is not ready yet.", ephemeral=True)
            return
        
        region = region.upper()
        if not validate_region(region):
            await interaction.response.send_message("Invalid region.", ephemeral=True)
            return
            
        puuid, match_id = await get_puuid_and_match_id(riot_name, region, http_session)
        if not puuid or not match_id:
            await interaction.response.send_message("Invalid Riot name or failed to fetch player data.", ephemeral=True)
            return

        guild = get_guild_from_interaction(interaction, track)
        if not guild:
            await interaction.response.send_message("This command must be used in a server.", ephemeral=True)
            return

        user = guild.add_member(discord_user.id, puuid, region)
        if not user:
            await interaction.response.send_message(f"User {discord_user.id} already exists.", ephemeral=True)
            return

        user.puuid = puuid
        user.matches = match_id

        track.save()
        await interaction.response.send_message("User has been successfully added.", ephemeral=True)


    @tree.command(name="remove_user", description="Removes a user from the list ~dev-only")
    @app_commands.check(validate_user)
    async def remove_user(
        interaction: discord.Interaction,
        discord_user: discord.User,
    ):

        guild = get_guild_from_interaction(interaction, track)
        if not guild:
            await interaction.response.send_message("Guild does not exist.", ephemeral=True)
            return

        if not guild.remove_member(discord_user.id):
            await interaction.response.send_message("User does not exist or could not be removed.", ephemeral=True)
            return

        track.save()
        await interaction.response.send_message("User has been successfully removed.", ephemeral=True,)

    @tree.command(name="show_all_users", description="Shows all added users in the guild")
    @app_commands.check(validate_user)
    async def show_all_users(interaction: discord.Interaction):
        guild = get_guild_from_interaction(interaction, track)
        if not guild:
            await interaction.response.send_message("Guild does not exist.", ephemeral=True)
            return

        user_list = guild.get_all_members()
        
        await interaction.response.send_message(embed= await All_User_embed(interaction, int(guild.guild_id), user_list))

