from typing import List, Tuple
import aiohttp
from PIL import Image

from rendering.core.cache_manager import AssetCache, get_image, get_multiple_images
from rendering.core.constants import ImageSizes

async def draw_rune_icon(
        template: Image.Image,
        rune_id: int,
        x: int,
        y: int,
        session: aiohttp.ClientSession,
        cache: AssetCache,
        size: int = ImageSizes.RUNE_ICON
) -> bool:
    rune_img = await get_image(rune_id, "rune", session, cache)
    if not rune_img:
        return False
    
    rune_img = rune_img.resize((size, size))
    template.paste(rune_img, (x, y), rune_img)
    return True


async def draw_rune_pair(
    template: Image.Image,
    primary_rune_id: int,
    secondary_style_id: int,
    center_x: int,
    y: int,
    session: aiohttp.ClientSession,
    cache: AssetCache,
    primary_size: int = ImageSizes.RUNE_ICON,
    secondary_size: int = ImageSizes.RUNE_SECONDARY,
    gap: int = 4
) -> Tuple[bool, bool]:
    """
    Draw primary rune and secondary style icons side by side, centered.
    
    Args:
        template: Image to draw on
        primary_rune_id: Primary rune ID
        secondary_style_id: Secondary style ID
        center_x: X position to center the pair around
        y: Y position
        session: aiohttp session
        cache: Asset cache instance
        primary_size: Primary rune size
        secondary_size: Secondary rune size
        gap: Gap between icons
    
    Returns:
        Tuple of (primary_success, secondary_success)
    """
    # Fetch both runes in parallel
    rune_images = await get_multiple_images(
        [(primary_rune_id, "rune"), (secondary_style_id, "rune")],
        session,
        cache
    )
    
    primary_img = rune_images[0]
    secondary_img = rune_images[1]
    
    # Calculate positions to center the pair
    start_x = center_x - (primary_size + gap + secondary_size // 2)
    
    # Draw primary rune
    primary_success = False
    if primary_img:
        primary_img = primary_img.resize((primary_size, primary_size))
        template.paste(primary_img, (start_x, y), primary_img)
        primary_success = True
    
    # Draw secondary rune (slightly offset vertically for alignment)
    secondary_success = False
    if secondary_img:
        secondary_img = secondary_img.resize((secondary_size, secondary_size))
        secondary_x = start_x + primary_size + gap
        secondary_y = y + ((primary_size - secondary_size) // 2)  # Center vertically
        template.paste(secondary_img, (secondary_x, secondary_y), secondary_img)
        secondary_success = True
    
    return primary_success, secondary_success


async def draw_multiple_rune_pairs(
        template: Image.Image,
        rune_pairs: List[Tuple[int, int, int, int]],
        session: aiohttp.ClientSession,
        cache: AssetCache,
        primary_size: int = ImageSizes.RUNE_ICON,
        secondary_size: int = ImageSizes.RUNE_SECONDARY,
        gap: int = 4
) -> List[Tuple[bool, bool]]:
    """
    Draw multiple rune pairs efficiently.
    
    Args:
        template: Image to draw on
        rune_pairs: List of (primary_id, secondary_id, center_x, y) tuples
        session: aiohttp session
        cache: Asset cache instance
        primary_size: Primary rune size
        secondary_size: Secondary rune size
        gap: Gap between icons
    
    Returns:
        List of success tuples
    """
    # Collect all rune IDs to fetch
    fetch_tasks = []
    for primary_id, secondary_id, _, _ in rune_pairs:
        fetch_tasks.append((primary_id, "rune"))
        fetch_tasks.append((secondary_id, "rune"))
    
    # Fetch all runes in parallel
    rune_images = await get_multiple_images(fetch_tasks, session, cache)
    
    # Draw each pair
    results = []
    for i, (primary_id, secondary_id, center_x, y) in enumerate(rune_pairs):
        primary_img = rune_images[i * 2]
        secondary_img = rune_images[i * 2 + 1]
        
        # Calculate positions
        total_width = primary_size + gap + secondary_size
        start_x = center_x - (total_width // 2)
        
        # Draw primary
        primary_success = False
        if primary_img:
            primary_img = primary_img.resize((primary_size, primary_size))
            template.paste(primary_img, (start_x, y), primary_img)
            primary_success = True
        
        # Draw secondary
        secondary_success = False
        if secondary_img:
            secondary_img = secondary_img.resize((secondary_size, secondary_size))
            secondary_x = start_x + primary_size + gap
            secondary_y = y + ((primary_size - secondary_size) // 2)
            template.paste(secondary_img, (secondary_x, secondary_y), secondary_img)
            secondary_success = True
        
        results.append((primary_success, secondary_success))
    
    return results