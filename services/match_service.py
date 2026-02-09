# ========== Imports ==========
import discord
from typing import Optional

from riot.riot_types import MatchData
from rendering.overview import generate_overview_image
from tracking.models import User


# ========== Function ==========
async def generate_image_by_type(
        image_type: str,
        tracked_user: User,
        match_data: MatchData
) -> Optional[discord.File]:
    
    """when we will have different buttons in the future, each button should pass a different image_type
    when a button is clicked check if it exists. if not generate and save to disk.
    """

    if image_type == "overview":
        image_buffer = await generate_overview_image(match_data)
        if image_buffer:
            discord_file = discord.File(fp=image_buffer, filename=f"overview_{tracked_user.recent_match}.png")
            return discord_file
    
    return None

