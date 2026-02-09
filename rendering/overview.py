# ========== Imports ==========
import os

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from rendering.assets import get_image
import riot.extractors
from riot.riot_types import *


# ========== Functions ==========
def _crop_to_circle(img: Image.Image) -> Image.Image:
    # circles have a radius of 50px (diameter 100px)
    img = img.resize((100, 100))

    # Create a circular mask that matches the resized image dimensions
    mask = Image.new("L", (100, 100), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 100, 100), fill=255)

    # Apply the mask
    img.putalpha(mask)
    return img


async def generate_overview_image(match_data: MatchData):
    current_folder = os.path.dirname(__file__)
    template_path = os.path.join(current_folder, "assets/templates/overview design.png")

    # 1. Open template as FIL object
    template = Image.open(template_path).convert("RGBA")

    # 2. Extract match info and participants
    participants = riot.extractors.get_participants(match_data)
    
    # 3. Fetch all champion names asynchronously
    y = 50
    for i, participant in enumerate(participants):
        champ_img = await get_image(participant["championName"], "champion")
        if not champ_img:
            return

        champ_img_circle = _crop_to_circle(champ_img)
        template.paste(champ_img_circle, (50, y + i * 70), champ_img_circle)

    buffer = BytesIO()
    template.save(buffer, format="png")
    buffer.seek(0)

    return buffer