# ========== Imports ==========
import discord
from tracking import models


# ========== Functions6 ==========
async def show_tracking_info(
        interaction: discord.Interaction,
        tracked_users_list: list[models.User],
) -> discord.Embed:
    
    guild_name = interaction.guild.name if interaction.guild else "Unknown server"
    
    embed = discord.Embed(
        title=f"🎯 There are currently {len(tracked_users_list)} users being tracked in {guild_name}:",
        color= discord.Color.gold()
    )

    for tracked_user in tracked_users_list:
        username = (await interaction.client.fetch_user(int(tracked_user.discord_id))).name
        embed.add_field(
            name=username,
            value=f"Discord ID: {tracked_user.discord_id}\nPUUID: {tracked_user.puuid}\nRegion: {tracked_user.region}",
            inline=False
        )
    
    return embed