# ========== Imports ==========
import os

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from rendering.assets import get_image
from riot.extractors import get_participants
from riot.riot_types import MatchData
from riot.services import get_both_ranks_for_puuid
from tracking.models import User
import aiohttp


# ========== Functions ==========
def _crop_to_circle(img: Image.Image) -> Image.Image:
    img = img.resize((80, 80))
    mask = Image.new("L", (80, 80), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((10, 10, 70, 70), fill=255)
    img.putalpha(mask)
    return img


async def generate_overview_image(tracked_user: User, match_data: MatchData, session: aiohttp.ClientSession):
    # 0. Folder setup
    current_folder = os.path.dirname(__file__)
    template_path = os.path.join(current_folder, "assets/templates/overview design.png")

    # 1. Open template as RGBA object (for transparency)
    template = Image.open(template_path).convert("RGBA")

    # 2. Extract match info and participants
    participants = get_participants(match_data)

    # 3. Fetch all champion images
    y = 160
    for i, participant in enumerate(participants):
        champ_img = await get_image(participant["championName"], "champion")
        if not champ_img:
            return

        champ_img_circle = _crop_to_circle(champ_img)
        template.paste(
            champ_img_circle,
            ((130 if i < 5 else 1710), y + ((i if i < 5 else i - 5) * 190)),
            champ_img_circle
        )

    # 4. Fetch and draw ranks for each participant
    for i, participant in enumerate(participants):
        solo_rank, flex_rank = await get_both_ranks_for_puuid(participant["puuid"], tracked_user.region, session)

        # Prepare solo rank text
        if solo_rank:
            tier = solo_rank.get("tier", "")
            rank_label = solo_rank.get("rank", "")
            lp = solo_rank.get("leaguePoints", "")
            solo_text = f"Solo: {tier} {rank_label} {lp}LP"
        else:
            solo_text = "Solo: Unranked"

        # Prepare flex rank text
        if flex_rank:
            tier = flex_rank.get("tier", "")
            rank_label = flex_rank.get("rank", "")
            lp = flex_rank.get("leaguePoints", "")
            flex_text = f"Flex: {tier} {rank_label} {lp}LP"
        else:
            flex_text = "Flex: Unranked"

    # 5. Save buffer
    buffer = BytesIO()
    template.save(buffer, format="png")
    buffer.seek(0)
    return buffer
