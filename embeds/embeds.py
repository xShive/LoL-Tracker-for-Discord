import discord

from track_manager.track_data import User

async def All_User_embed(interaction: discord.Interaction, guild_id: int, user_list: list[User]):
    text = ""
    for user in user_list:
        if not interaction.guild:
            return
        
        member = interaction.guild.get_member(int(user.discord_id))
        name = member.display_name if member else user.discord_id

    guild_name = interaction.client.get_guild(guild_id)
    embed = discord.Embed(
        title=f"All Users in {guild_name}",
        description= text,
        color= discord.Color.gold()
    )

    return embed