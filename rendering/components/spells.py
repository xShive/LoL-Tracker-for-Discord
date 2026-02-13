from typing import List, Tuple
import aiohttp
from PIL import Image

from rendering.core.cache_manager import AssetCache, get_image, get_multiple_images
from rendering.core.constants import ImageSizes


async def draw_spell_icon(
        template: Image.Image,
        spell_id: int,
        x: int,
        y: int,
        session: aiohttp.ClientSession,
        cache: AssetCache,
        size: int = ImageSizes.SPELL_ICON
) -> bool:
    
    # fetch single spell image
    spell_img = await get_image(spell_id, "spell", session, cache)
    if not spell_img:
        return False
    
    spell_img = spell_img.resize(size, size)
    template.paste(spell_img, (x, y), spell_img)
    return True


async def draw_spell_icon_pair(
        template: Image.Image,
        spell_ids: Tuple[int, int],
        x: int,
        y: int,
        session: aiohttp.ClientSession,
        cache: AssetCache,
        size: int = ImageSizes.SPELL_ICON,
        gap: int = 4
) -> Tuple[bool, bool]:
    
    
    spell_images = await get_multiple_images(
        [(spell_ids[0], "spell"), (spell_ids[1], "spell")],
        session,
        cache
    )

    success = []

    if spell_images[0]:
        spell_1_resized = spell_images[0].resize((size, size))
        template.paste(spell_1_resized, (x, y), spell_1_resized)
        success.append(True)
    
    if spell_images[1]:
        spell_2_resized = spell_images[1].resize((size, size))
        template.paste(spell_2_resized, (x + gap, y), spell_2_resized)
        success.append(True)
    
    return tuple(success)


async def draw_spell_pairs_batch(
    template: Image.Image,
    spell_pairs: List[Tuple[int, int, int, int]],
    session: aiohttp.ClientSession,
    cache: AssetCache,
    size: int = ImageSizes.SPELL_ICON,
    gap: int = 4,
) -> List[Tuple[bool, bool]]:
    """
    Draw multiple spell pairs efficiently.
    
    Args:
        template: Image to draw on
        spell_pairs: List of (spell1_id, spell2_id, x, y) tuples
        session: aiohttp session
        cache: Asset cache instance
        size: Icon size
        gap: Gap between icons
    
    Returns:
        List of success tuples
    """
    # Collect all spell IDs to fetch
    fetch_tasks = []
    for spell1_id, spell2_id, _, _ in spell_pairs:
        fetch_tasks.append((spell1_id, "spell"))
        fetch_tasks.append((spell2_id, "spell"))
    
    # Fetch all spells in parallel
    spell_images = await get_multiple_images(fetch_tasks, session, cache)
    
    # Draw each pair
    results = []
    for i, (spell1_id, spell2_id, x, y) in enumerate(spell_pairs):
        spell1_img = spell_images[2 * i]
        spell2_img = spell_images[2 * i + 1]
        
        # Draw first spell
        spell1_success = False
        if spell1_img:
            spell1_img = spell1_img.resize((size, size))
            template.paste(spell1_img, (x, y), spell1_img)
            spell1_success = True
        
        # Draw second spell
        spell2_success = False
        if spell2_img:
            spell2_img = spell2_img.resize((size, size))
            template.paste(spell2_img, (x + gap, y), spell2_img)
            spell2_success = True
        
        results.append((spell1_success, spell2_success))
    
    return results