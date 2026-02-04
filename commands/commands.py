# ========== Imports ==========
import discord

from riot.api import get_puuid, get_match_id, REGIONS

from track_manager.track_data import TrackManager
track = TrackManager()

# ========== Commands registry ==========
def register_commands(tree):
    @tree.command(name="recent_matches", description="show recent league of legends matches for a gamer")
    async def recent_matches(interaction: discord.Interaction, riot_name: str, region: str):
        await interaction.response.defer()

        if '#' not in riot_name:
            await interaction.edit_original_response(content="Invalid Riot name. Please include the tagline (#)")
            return

        name_parts = riot_name.split("#")

        puuid = await get_puuid(name_parts[0], name_parts[1], region)
        if puuid is None:
            await interaction.edit_original_response(content="Unexpected error.")
            return
        
        match_id = await get_match_id(puuid, region)
        if match_id is None:
            await interaction.edit_original_response(content="Unexpected error.")
            return

        await interaction.edit_original_response(content=f"Your latest match ID: {match_id}")
        return

    @tree.command(name="add_user", description="Adds a user to the list ~admin-only")
    async def add_user(interaction: discord.Interaction, discord_user: discord.User, riot_name: str, region: str):
        if '#' not in riot_name:
            await interaction.response.send_message(content="Invalid Riot name. Please include the tagline (#).", ephemeral=True)
            return
        
        uppercase_region = region.upper()

        if not REGIONS.get(uppercase_region):
            await interaction.response.send_message(content="Invalid Region. Make sure it's a valid region.", ephemeral=True)
            return
        
        name_parts = riot_name.split("#")
        
        puuid = await get_puuid(name_parts[0], name_parts[1], uppercase_region)
        if puuid is None:
            await interaction.response.send_message(content="Unexpected error, couldn't fetch the puuid", ephemeral=True)
            return
        
        match_id = await get_match_id(puuid, uppercase_region)
        if match_id is None:
            await interaction.response.send_message(content="Unexpected error, couldn't fetch the match_id", ephemeral=True)
            return
        
        guild_id = interaction.guild_id

        if guild_id is None:
            await interaction.response.send_message(content="Unexpected error, couldn't fetch the guild_id", ephemeral=True)
            return

        guild = track.get_guild(guild_id)
        
        if guild is None:
            await interaction.response.send_message(content="Unexpected error, couldn't fetch the guild", ephemeral=True)
            return

        user = guild.add_member(discord_user.id, puuid, uppercase_region)

        if user is None:
            await interaction.response.send_message(content=f"User already exists {discord_user.id}", ephemeral=True)
            return

        user.puuid = puuid
        user.matches = match_id

        track.save()

        await interaction.response.send_message("Het werkt bitch", ephemeral=True)


