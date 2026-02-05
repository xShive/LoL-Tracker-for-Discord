import discord

from track_manager.track_data import User, Guild

async def All_User_embed(interaction: discord.Interaction, guild_id: int, user_list: list[User]):
    text = ""
    for user in user_list:
        discord_name = await interaction.client.fetch_user(int(user.discord_id))
        text += f"{discord_name}: {user.discord_id} \n"

    guild_name = interaction.client.get_guild(guild_id)
    embed = discord.Embed(
        title=f"All Users in {guild_name}",
        description= text,
        color= discord.Color.gold()
    )

    return embed