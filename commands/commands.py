# ========== Imports ==========
import discord

from helpers.riot_helpers import validate_region, get_puuid_and_match_id
from helpers.discord_helpers import get_guild_from_interaction, track


# ========== Command Registry ==========
def register_commands(tree):
    @tree.command(name="add_user", description="Adds a user to the list ~dev-only")
    async def add_user(
        interaction: discord.Interaction,
        discord_user: discord.User,
        riot_name: str,
        region: str,
    ):
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
        guild = get_guild_from_interaction(interaction)
        if not guild:
            await interaction.response.send_message("Guild does not exist.", ephemeral=True)
            return

        if not guild.remove_member(discord_user.id):
            await interaction.response.send_message("User does not exist or could not be removed.", ephemeral=True)
            return

        track.save()
        await interaction.response.send_message("User has been successfully removed.", ephemeral=True,)
