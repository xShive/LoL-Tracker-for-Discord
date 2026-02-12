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

rank_labels = {
    "I" : 1,
    "II" : 2,
    "III" : 3,
    "IV" : 4
}


# ========== Functions ==========
def _crop_to_circle(img: Image.Image) -> Image.Image:
    img = img.resize((80, 80))
    mask = Image.new("L", (80, 80), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((10, 10, 70, 70), fill=255)
    img.putalpha(mask)
    return img

def draw_text_with_shadow(
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill=(255, 255, 255, 255),
    shadow_color=(0, 0, 0, 180),
    offset=2,
    anchor="la"
):
    x, y = position

    # Shadow
    draw.text((x + offset, y + offset), text, font=font, fill=shadow_color, anchor=anchor)

    # Main text
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)



async def generate_overview_image(tracked_user: User, match_data: MatchData, session: aiohttp.ClientSession):
    # 0. Folder setup
    current_folder = os.path.dirname(__file__)
    template_path = os.path.join(current_folder, "assets/templates/overview design v2.png")
    font_path_name = os.path.join(current_folder, "assets/fonts/Sora/Sora-SemiBold.ttf")
    font_path_rank = os.path.join(current_folder, "assets/fonts/Sora/Sora-Medium.ttf")

    # 1. Open template as RGBA object (for transparency)
    template = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(template)
    name_font = ImageFont.truetype(font_path_name, 18)
    rank_font = ImageFont.truetype(font_path_rank, 12)

    # 2. Extract match info and participants
    participants = get_participants(match_data)

    # 3. Fetch all champion images
    y = 139
    for i, participant in enumerate(participants):
        champ_img = await get_image(participant["championName"], "champion", session)
        if not champ_img:
            return
 
        champ_img_circle = _crop_to_circle(champ_img)
        template.paste(
            champ_img_circle,
            ((109 if i < 5 else 1730), y + ((i if i < 5 else i - 5) * 190)),
            champ_img_circle
        )
    
    # 4. Fetch all names
    y = 142
    for i, participant in enumerate(participants):
        player_name = participant["riotIdGameName"]

        draw_text_with_shadow(
            draw,
            ((190 if i < 5 else 1730), y + (i if i < 5 else i - 5) * 190),
            player_name,
            name_font,
            anchor="ra" if (i >= 5) else "la"
        )

        
    # 5. Fetch and draw ranks for each participant
    # Starting positions
    for i, participant in enumerate(participants):
        solo_rank, flex_rank, status = await get_both_ranks_for_puuid(participant["puuid"], tracked_user.region, session)

        # Row offsets
        row_offset = (i if i < 5 else i - 5) * 190
        is_right = i >= 5


        # --- Prepare texts and images ---
        if status == "unfetchable":
            solo_text = flex_text = "Not Fetchable"
            rank_img_solo = rank_img_flex = None
        elif status == "error":
            solo_text = flex_text = "Error"
            rank_img_solo = rank_img_flex = None
        else:
            # Solo
            if solo_rank:
                tier = solo_rank.get("tier", "")
                rank_label = solo_rank.get("rank", "")
                lp = solo_rank.get("leaguePoints", "")
                solo_text = f"{tier[0]}{rank_labels[rank_label]} · {lp}LP"
                rank_img_solo = await get_image(tier.lower(), "rank", session)
            else:
                solo_text = "Unranked"
                rank_img_solo = None

            # Flex
            if flex_rank:
                tier = flex_rank.get("tier", "")
                rank_label = flex_rank.get("rank", "")
                lp = flex_rank.get("leaguePoints", "")
                flex_text = f"{tier[0]}{rank_labels[rank_label]} · {lp}LP"
                rank_img_flex = await get_image(tier.lower(), "rank", session)
            else:
                flex_text = "Unranked"
                rank_img_flex = None

        if not is_right:
            # If user has rank
            if rank_img_solo:
                icon_resized = rank_img_solo.resize((128, 72))
                template.paste(icon_resized, (140, 140 + i * 190), icon_resized)
                draw_text_with_shadow(draw, (218, 168 + i * 190), solo_text, rank_font)

            # Else Unranked / Unfetchable
            else:
                draw_text_with_shadow(draw, (192, 168 + i * 190), solo_text, rank_font)
            
            if rank_img_flex:
                icon_resized = rank_img_flex.resize((128, 72))
                template.paste(icon_resized, (140, 160 + i * 190), icon_resized)
                draw_text_with_shadow(draw, (218, 188 + i * 190), flex_text, rank_font)

            else:
                draw_text_with_shadow(draw, (192, 188 + i * 190), flex_text, rank_font)



            
            



    # 5. Save buffer
    buffer = BytesIO()
    template.save(buffer, format="png")
    buffer.seek(0)
    return buffer
