# ========== Imports ==========
import os
import dotenv
import discord
import aiohttp

from discord import app_commands
from commands.commands import register_commands
from commands.errors import register_errors

from tracking.storage import TrackManager
track = TrackManager()

# ========== Setup ==========
dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

http_session: aiohttp.ClientSession | None = None

tree = app_commands.CommandTree(client)


# ========== Startup ==========
token = os.getenv("DISCORD_TOKEN")
if token is None:
    raise RuntimeError("DISCORD_TOKEN environment variable not set")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    # open http_session
    global http_session
    if http_session is None:
        http_session = aiohttp.ClientSession()

    register_commands(tree, track, http_session)
    register_errors(tree)
    
    # sync with test server
    MY_GUILD = discord.Object(id=1461904966212911297)
    tree.copy_global_to(guild=MY_GUILD)
    await tree.sync(guild=MY_GUILD)

    # sync all joined guilds
    async for guild in client.fetch_guilds():
        track.add_guild(guild.id)
    track.save()


@client.event
async def on_guild_join(guild: discord.Guild):
    track.add_guild(guild.id)
    track.save()

@client.event
async def on_guild_remove(guild: discord.Guild):
    track.remove_guild(guild.id)
    track.save()

@client.event
async def on_disconnect():
    if http_session:
        await http_session.close()

if __name__ == "__main__":
    client.run(token)
