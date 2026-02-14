# ========== Imports ==========
from io import BytesIO
from typing import Optional, List, Tuple

import aiohttp
import asyncio
import time
from PIL import Image

from .constants import (
    ImageSizes,
    DRAGON_URL,
    RANK_ICON_URL,
    PERK_DATA_URL,
    SPELL_DATA_URL,
    PERK_ICON_BASE,
    STYLE_ICON_MAP,
    VERSION
)


# ========== Class ==========
class AssetCache:
    """
    Asset cache with RAM storage.
    All instances share the same cache.
    """
    
    def __init__(self):
        self._image_cache: dict[str, Image.Image] = {}
        self._perk_lookup: Optional[dict[int, str]] = None
        self._spell_lookup: Optional[dict[int, str]] = None
        self._runtime_start: float = time.time()
    
    def get_cached_image(self, identity: str | int, category: str) -> Optional[Image.Image]:
        """
        Get image from RAM cache (shared across all instances).
        
        Args:
            identity: Champion name, item ID, etc.
            category: Asset category (champion, item, rune, spell, rank)
        
        Returns:
            Cached image or None if not in cache.
        """
        cache_key = f"{category}:{identity}"
        return self._image_cache.get(cache_key)
    
    def save_to_cache(self, img: Image.Image, identity: str | int, category: str) -> None:
        """
        Save image to RAM cache (shared across all instances).
        
        Args:
            img: Image to cache
            identity: Champion name, item ID, etc.
            category: Asset category
        """
        cache_key = f"{category}:{identity}"
        self._image_cache[cache_key] = img
    
    def get_cache_stats(self) -> Optional[dict[str, int | str | float]]:
        if not self._image_cache:
            return None
        
        total_bytes = 0
        for img in self._image_cache.values():
            # Calculate RAM usage
            # RGBA has 4 slots, each 1 byte (255)
            # multiply by width and height to get total bytes
            total_bytes += img.size[0] * img.size[1] * 4
            
        total_mb = total_bytes / (1024 * 1024)
        return {
            "images": len(self._image_cache),
            "size_mb": f"{total_mb:.2f} MB",
            "runtime": time.time() - self._runtime_start
        }
    

    async def get_spell_map(self, session: aiohttp.ClientSession) -> dict[int, str]:
        """
        Fetch spell data mapping (shared across all instances).
        
        Args:
            session: aiohttp session for requests
        
        Returns:
            Dictionary mapping spell IDs to spell names (used in the URL)
        """
        if self._spell_lookup is not None:
            return self._spell_lookup
        
        try:
            async with session.get(SPELL_DATA_URL) as response:
                if response.status != 200:
                    print(f"Failed to fetch spell data: {response.status}")
                    return {}
                data = await response.json()
        except Exception as e:
            print(f"Error fetching spell data: {e}")
            return {}
        
        self._spell_lookup = {}
        for spell in data["data"].values():
            spell_key = int(spell["key"])
            spell_name = spell["id"]

            self._spell_lookup[spell_key] = spell_name
        
        return self._spell_lookup
    
    async def get_rune_map(self, session: aiohttp.ClientSession) -> dict[int, str]:
        """
        Fetch rune data mapping (shared across all instances).
        
        Args:
            session: aiohttp session for requests
        
        Returns:
            Dictionary mapping rune IDs to URLs
        """
        if self._perk_lookup is not None:
            return self._perk_lookup
        
        try:
            async with session.get(PERK_DATA_URL) as response:
                if response.status != 200:
                    print(f"Failed to fetch perk/rune data: {response.status}")
                    return {}
                data = await response.json()
        except Exception as e:
            print(f"Error fetching perk/rune data: {e}")
            return {}

        self._perk_lookup = {}
        
        # building a dictionary where keys = ID's, values = URLs
        # build lookup dictionary (1. keystone rune icons)
        for rune in data:
            rune_id = rune["id"]
            icon_path = rune["iconPath"].replace("/lol-game-data/assets", "").lower()
            self._perk_lookup[rune_id] = PERK_ICON_BASE + icon_path
        
        # build lookup dictionary (2. style icons (e.g. domination))
        for style_id_riot, filename_website in STYLE_ICON_MAP.items():
            self._perk_lookup[style_id_riot] = PERK_ICON_BASE + f"/v1/perk-images/styles/{filename_website}"

        return self._perk_lookup


async def _fetch_image(
        url_to_fetch: str,
        session: aiohttp.ClientSession
) -> Optional[BytesIO]:
    try:
        async with session.get(url_to_fetch) as response:
            if response.status == 200:
                data = await response.read()
                return BytesIO(data)
            else:
                print(f"Failed to fetch {url_to_fetch}: {response.status}")
    except Exception as e:
        print(f"Error fetching {url_to_fetch}: {e}")
    
    return None

async def get_image(    
    identity: str | int,
    category: str,
    session: aiohttp.ClientSession,
    cache: Optional[AssetCache] = None
) -> Optional[Image.Image]:
    """
    Fetch a game asset image by identity and category.
    
    Args:
        identity: Champion name, item ID, rune ID, spell ID, or rank tier
        category: One of "champion", "item", "rune", "spell", "rank"
        session: aiohttp session for making requests
        cache: AssetCache instance (creates new one if None)
    
    Returns:
        PIL Image object or None if fetch failed
    """
    if cache is None:
        cache = AssetCache()
    
    # Check cache
    cached = cache.get_cached_image(identity, category)
    if cached:
        return cached
    
    original_identity = identity

    if category == "rank":
        url = RANK_ICON_URL + f"{identity}.png"
    
    elif category == "rune":
        lookup = await cache.get_rune_map(session)
        if not lookup:
            print("Rune lookup went wrong.")
            return None
        
        url = lookup.get(int(identity))
        if not url:
            print("Rune lookup went wrong")
            return None
        
    else:
        if category == "spell":
            lookup = await cache.get_spell_map(session)
            identity = lookup[int(identity)]
        
        url = f"{DRAGON_URL}{VERSION}/img/{category}/{identity}.png"
    
    img_bytes = await _fetch_image(url, session)
    if img_bytes is None:
        return None
    
    try:
        img_pil = Image.open(img_bytes).convert("RGBA")
        
        # MEMORY OPTIMIZATION
        target_size = None

        if category == "rank":
            target_size = ImageSizes.RANK_ICON
        
        elif category == "rune":
            target_size = (ImageSizes.RUNE_ICON, ImageSizes.RUNE_ICON)
            
        if target_size:
            img_pil = img_pil.resize(target_size, Image.Resampling.LANCZOS)
            
        cache.save_to_cache(img_pil, original_identity, category)
        return img_pil
    
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

async def get_multiple_images(
        items: List[Tuple[str | int, str]],
        session: aiohttp.ClientSession,
        cache: Optional[AssetCache]
) -> list[Optional[Image.Image]]:
    """
    Fetch multiple images in parallel.
    
    Args:
        items: List of (identity, category) tuples
        session: aiohttp session
        cache: AssetCache instance
    
    Returns:
        List of Image objects (or None for failed fetches)
    
    Example:
        >>> images = await get_images_batch([
        ...     ("Ahri", "champion"),
        ...     ("Zed", "champion"),
        ...     (4, "spell")
        ... ], session, cache)
    """
    if cache is None:
        cache = AssetCache()
    
    # get_image has no await yet, so it hasn't ran. asyncio.gather does them all.
    tasks = [get_image(identity, category, session, cache) for identity, category in items]
    return await asyncio.gather(*tasks, return_exceptions=False)

# global cache
global_cache = AssetCache()