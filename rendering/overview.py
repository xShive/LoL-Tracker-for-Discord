# ========== Imports ==========
import os

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from rendering.components import ranks, champion, runes, spells
from rendering.core.utils import draw_text_with_shadow
from rendering.core.cache_manager import AssetCache
from riot.extractors import get_participants
from riot.riot_types import MatchData
from riot.services import get_both_ranks_for_puuid
from tracking.models import User
import aiohttp
from rendering.core.constants import RANK_LABELS, FONTS_DIR, TEMPLATES_DIR


# ========== Functions ==========
async def generate_overview_image(tracked_user: User, match_data: MatchData, session: aiohttp.ClientSession):

    # 1. Images and Fonts setup
    template = Image.open(TEMPLATES_DIR / "overview.png").convert("RGBA")
    draw = ImageDraw.Draw(template)
    name_font = ImageFont.truetype(FONTS_DIR / "Sora" / "Sora-SemiBold.ttf", 18)
    rank_font = ImageFont.truetype(FONTS_DIR / "Sora" / "Sora-Medium.ttf", 12)

    cache = AssetCache()

    # 2. Extract match info and participants
    participants = get_participants(match_data)

    # 3. raw all chanpions
    champions_positions = []
    for i, participant in enumerate(participants):
        x = 109 if i < 5 else 1730
        y = 139 + ((i if i < 5 else i - 5) * 190)
        champions_positions.append((participant["championName"], x, y))

    await champion.draw_multiple_champions(template, champions_positions, session, cache)

    # 4.Draw all names
    y = 142
    for i, participant in enumerate(participants):
        x = 190 if i < 5 else 1730
        y = 142 + ((i if i < 5 else i - 5) * 190)
        player_name = participant["riotIdGameName"]

        draw_text_with_shadow(draw, (x, y), player_name, name_font, anchor=("la" if i < 5 else "ra"))

        
    # 5. Fetch and draw ranks for each participant
    # Starting positions
    for i, participant in enumerate(participants):
        solo_rank, flex_rank, status = await get_both_ranks_for_puuid(participant["puuid"], tracked_user.region, session)

        # Check which side
        is_right = i >= 5

        # Prepare text and images
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
                draw_text_with_shadow(draw, (220, 168 + i * 190), solo_text, rank_font)

            # Else Unranked / Unfetchable
            else:
                draw_text_with_shadow(draw, (192, 168 + i * 190), solo_text, rank_font)
            
            if rank_img_flex:
                icon_resized = rank_img_flex.resize((128, 72))
                template.paste(icon_resized, (140, 160 + i * 190), icon_resized)
                draw_text_with_shadow(draw, (220, 188 + i * 190), flex_text, rank_font)

            else:
                draw_text_with_shadow(draw, (192, 188 + i * 190), flex_text, rank_font)
        
        else:
            row = (i - 5) * 190     # reset index

            # If user has rank
            if rank_img_solo:
                icon_resized = rank_img_solo.resize((128, 72))
                template.paste(icon_resized, (1652, 140 + row), icon_resized)
                draw_text_with_shadow(draw, (1698, 168 + row), solo_text, rank_font, anchor="ra")

            # Else Unranked / Unfetchable
            else:
                draw_text_with_shadow(draw, (1728, 168 + row), solo_text, rank_font, anchor="ra")

            if rank_img_flex:
                icon_resized = rank_img_flex.resize((128, 72))
                template.paste(icon_resized, (1652, 160 + row), icon_resized)
                draw_text_with_shadow(draw, (1698, 188 + row), flex_text, rank_font, anchor="ra")

            else:
                draw_text_with_shadow(draw, (1728, 188 + row), flex_text, rank_font, anchor="ra")
        


    RUNE_SPELL_SIZE = 30
    RUNE_SPELL_GAP = 4    # Space between the two runes

    for i, participant in enumerate(participants):
        # a) prepare data
        perks = participant["perks"]["styles"]
        styles_map = {style["description"]: style for style in perks}
        primary_style = styles_map["primaryStyle"]
        sub_style = styles_map["subStyle"]

        primary_rune_id = primary_style["selections"][0]["perk"]
        secondary_style_id = sub_style["style"]

        rune_img_1 = await get_image(primary_rune_id, "rune", session)
        rune_img_2 = await get_image(secondary_style_id, "rune", session)
        
        if rune_img_1: rune_img_1 = rune_img_1.resize((RUNE_SPELL_SIZE, RUNE_SPELL_SIZE))
        if rune_img_2: rune_img_2 = rune_img_2.resize((RUNE_SPELL_SIZE - 5, RUNE_SPELL_SIZE - 5))

        # b) calculate position
        # find champion position
        champ_x = 109 if i < 5 else 1730
        champ_y = 139 + ((i if i < 5 else i - 5) * 190)

        # higher y = below champ icon
        rune_y = champ_y + 85

        # center over icon width
        start_x = int((champ_x + 40) - ((RUNE_SPELL_SIZE * 2 + RUNE_SPELL_GAP) / 2))

        # c) paste images
        if rune_img_1:
            template.paste(rune_img_1, (start_x, rune_y), rune_img_1)
        
        if rune_img_2:
            second_rune_x = start_x + RUNE_SPELL_SIZE + RUNE_SPELL_GAP
            template.paste(rune_img_2, (second_rune_x, rune_y + 1), rune_img_2)



    y_offset = 220
    
    for i, participant in enumerate(participants):
        spell1 = participant["summoner1Id"]
        spell2 = participant["summoner2Id"] 

        spell1_img = await get_image(spell1, "spell", session) 
        spell2_img = await get_image(spell2, "spell", session)
        
        # determine y position
        row_y = y_offset + ((i if i < 5 else i - 5) * 190)

        # Left side
        if i < 5:
            s1_x = 190
            s2_x = 190 + RUNE_SPELL_SIZE + RUNE_SPELL_GAP

        # Right side
        else:
            s2_x = 1730 - RUNE_SPELL_SIZE 
            s1_x = s2_x - RUNE_SPELL_GAP - RUNE_SPELL_SIZE

        # Paste Spell 1
        if spell1_img:
            spell1_img = spell1_img.resize((RUNE_SPELL_SIZE, RUNE_SPELL_SIZE))
            template.paste(spell1_img, (s1_x, row_y))

        # Paste Spell 2
        if spell2_img:
            spell2_img = spell2_img.resize((RUNE_SPELL_SIZE, RUNE_SPELL_SIZE))
            template.paste(spell2_img, (s2_x, row_y))

        

    # 5. Save buffer
    buffer = BytesIO()
    template.save(buffer, format="png")
    buffer.seek(0)
    return buffer
