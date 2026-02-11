# ========== Imports ==========
import discord

from discord import app_commands
from aiohttp import ClientSession

from services.match_service import generate_image_by_type
from riot.api import get_match_data
from riot.services import validate_region, get_puuid_and_match_id
from utils.discord import validate_user, get_guild_from_interaction
from tracking.storage import TrackManager
from embeds.embeds import show_tracking_info

# ========== Command Registry ==========
def register_commands(
        tree: discord.app_commands.CommandTree,
        track: TrackManager,
        http_session: ClientSession):

    @tree.command(name="add_user", description="Adds a user to the list ~dev-only")
    @app_commands.check(validate_user)
    async def add_user(
        interaction: discord.Interaction,
        discord_user: discord.User,
        riot_name: str,
        region: str,
    ):
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
        await interaction.response.send_message("User has been successfully removed.", ephemeral=True)

    @tree.command(name="show_all_users", description="Shows all added users in the guild")
    @app_commands.check(validate_user)
    async def show_all_users(interaction: discord.Interaction):
        guild = get_guild_from_interaction(interaction, track)
        if not guild:
            await interaction.response.send_message("Guild does not exist.", ephemeral=True)
            return

        user_list = guild.get_all_members()
        embed = await show_tracking_info(interaction, user_list)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @tree.command(name="recent-match", description="Shows a recap of the most recent match a tracked user has played.")
    async def recent_match(
        interaction: discord.Interaction,
        discord_user: discord.User,
    ):
        await interaction.response.defer()

        guild = get_guild_from_interaction(interaction, track)
        if not guild:
            await interaction.edit_original_response(content="This Discord server isn't being tracked.")
            return

        tracked_user = guild.get_member(discord_user.id)
        if not tracked_user:
            await interaction.edit_original_response(content="This user isn't being tracked. Add them by doing /add_user.")
            return
        
        if not tracked_user.recent_match:
            await interaction.edit_original_response(content="This user has not played any matches.")
            return

        match_data = await get_match_data(tracked_user.recent_match, tracked_user.region, http_session)
        if not match_data:
            await interaction.edit_original_response(content="Something went wrong while fetching data.")
            return

        image = await generate_image_by_type("overview", tracked_user, match_data, http_session)
        if not image:
            await interaction.edit_original_response(content="Something went wrong while generating the image.")
            return
        
        channel_id = interaction.channel_id
        if channel_id is None:
            await interaction.edit_original_response(content="Can't send the image here.")
            return
        
        channel = await interaction.client.fetch_channel(channel_id)
        if not isinstance(channel, discord.abc.Messageable):
            await interaction.edit_original_response(content="Can't send the image here.")
            return
        
        await channel.send(file=image)
        await interaction.edit_original_response(content="Sent!")

        
