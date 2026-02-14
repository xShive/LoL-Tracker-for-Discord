# ========== Imports ==========
import asyncio
import time
from PIL import ImageDraw, Image
from io import BytesIO

from rendering.components import ranks, champion, runes, spells
from rendering.core.utils import draw_text_with_shadow
from rendering.core.cache_manager import AssetCache
from riot.extractors import get_participants
from riot.riot_types import MatchData
from riot.services import get_both_ranks_for_puuid
from tracking.models import User
import aiohttp
from rendering.core.constants import RANK_FONT, NAME_FONT, TEMPLATES_DIR
from rendering.core.cache_manager import global_cache


async def generate_overview_image(tracked_user: User, match_data: MatchData, session: aiohttp.ClientSession):
    # Setup
    start_total = time.time()

    template = Image.open(TEMPLATES_DIR / "overview.png")
    draw = ImageDraw.Draw(template)
    cache = global_cache
    participants = get_participants(match_data)
    
    # Loop: draw champs, runes, spells, names
    champions_positions = []
    rune_pairs = []
    spell_pairs = []
    
    for i, participant in enumerate(participants):
        # Calculate common values
        is_right = i >= 5
        row = i - 5 if is_right else i
        champ_x = 1730 if is_right else 109
        champ_y = 139 + row * 190
        name_x = 1730 if is_right else 190
        name_y = 142 + row * 190
        
        # Collect all champions + their positions in a tuple
        champions_positions.append((participant["championName"], champ_x, champ_y))
        
        # Draw names
        draw_text_with_shadow(
            draw,
            (name_x, name_y),
            participant["riotIdGameName"],
            NAME_FONT,
            anchor="ra" if is_right else "la"
        )
        
        #  Collect rune data
        perks = participant["perks"]["styles"]
        styles_map = {style["description"]: style for style in perks}

        primary_rune_id = styles_map["primaryStyle"]["selections"][0]["perk"]
        secondary_style_id = styles_map["subStyle"]["style"]

        center_x = champ_x + 40  # Center of champion icon
        rune_y = champ_y + 85
        rune_pairs.append((primary_rune_id, secondary_style_id, center_x, rune_y))
        
        # Collect spell data
        spell1_id = participant["summoner1Id"]
        spell2_id = participant["summoner2Id"]
        spell_y = 220 + row * 190
        spell_x = 190 if not is_right else (1730 - 30 - 4 - 30)
        spell_pairs.append((spell1_id, spell2_id, spell_x, spell_y))
    
    # DRAW EVERYTHING
    await asyncio.gather(
        champion.draw_multiple_champions(template, champions_positions, session, cache),
        runes.draw_multiple_rune_pairs(template, rune_pairs, session, cache),
        spells.draw_spell_pairs_batch(template, spell_pairs, session, cache)
    )

    # Parallel rank fetching
    rank_tasks = [get_both_ranks_for_puuid(p["puuid"], tracked_user.region, session) for p in participants]
    all_ranks = await asyncio.gather(*rank_tasks)
 
    # Parallel rank drawing
    rank_badge_tasks = []
    
    for i, (participant, (solo_rank, flex_rank, status)) in enumerate(zip(participants, all_ranks)):
        # Common values
        is_right = i >= 5
        row = i - 5 if is_right else i

        text_x = 1728 if is_right else 192
        anchor = "ra" if is_right else "la"

        solo_y_text = 168 + row * 190
        flex_y_text = 188 + row * 190

        solo_badge_y = 140 + row * 190
        flex_badge_y = 160 + row * 190

        # Error handling
        if status != "ok":
            draw_text_with_shadow(draw, (text_x, solo_y_text), status, RANK_FONT, anchor=anchor)
            draw_text_with_shadow(draw, (text_x, flex_y_text), status, RANK_FONT, anchor=anchor)
            continue

        # Solo Rank
        if solo_rank is None:
            draw_text_with_shadow(draw, (text_x, solo_y_text), "Unranked", RANK_FONT, anchor=anchor)
        else:
            if is_right:
                rank_badge_tasks.append(
                    ranks.draw_rank_badge_with_text(
                        template, draw, solo_rank,
                        1652, solo_badge_y, 1698, solo_y_text,
                        session, cache, RANK_FONT, "ra"
                    )
                )
            else:
                rank_badge_tasks.append(
                    ranks.draw_rank_badge_with_text(
                        template, draw, solo_rank,
                        140, solo_badge_y, 220, solo_y_text,
                        session, cache, RANK_FONT
                    )
                )

        # Flex Rank
        if flex_rank is None:
            draw_text_with_shadow(draw, (text_x, flex_y_text), "Unranked", RANK_FONT, anchor=anchor)
        else:
            if is_right:
                rank_badge_tasks.append(
                    ranks.draw_rank_badge_with_text(
                        template, draw, flex_rank,
                        1652, flex_badge_y, 1698, flex_y_text,
                        session, cache, RANK_FONT, "ra"
                    )
                )
            else:
                rank_badge_tasks.append(
                    ranks.draw_rank_badge_with_text(
                        template, draw, flex_rank,
                        140, flex_badge_y, 220, flex_y_text,
                        session, cache, RANK_FONT
                    )
                )
    
    # Draw all rank badges in parallel
    if rank_badge_tasks:
        await asyncio.gather(*rank_badge_tasks)
    
    buffer = BytesIO()
    template.save(buffer, format="PNG", optimize=False, compress_level=1)
    buffer.seek(0)

    total_time = time.time() - start_total
    print(f"TOTAL TIME: {total_time:.3f}s")

    return buffer