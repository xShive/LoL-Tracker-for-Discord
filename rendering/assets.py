# fetch all images from ddragons
# ========== Imports ==========
import aiohttp
from PIL import Image, ImageDraw
from io import BytesIO
from typing import Optional
import os

DDRAGON_URL_TEMPLATE = "https://ddragon.leagueoflegends.com/cdn/"
CACHE_DIR = "rendering/assets/cache/"
VERSION = "16.3.1"

"""
1. Fetch: raw bytes. discord nor pillow can read.
2. Wrap in BytesIO. discord and pillow can read
3. Open with pillow -> converts to PIL object
4. Save back to BytesIO. discord and pillow can read.
5. Discord has its own type. Use function."""

"""TODO: fix linux"""

async def _fetch_image(url_to_fetch: str) -> Optional[BytesIO]:
    """Asynchronously fetches an image from a URL without blocking the event loop."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url_to_fetch) as response:
                if response.status == 200:
                    content = await response.read()
                    return BytesIO(content)
        return None
    except Exception as e:
        print(f"Error fetching image from {url_to_fetch}: {e}")
        return None


def _check_cache(identity: str | int, category: str) -> Optional[Image.Image]:
    if os.path.exists(CACHE_DIR + f"{category}_icons/{identity}.png"):
        return Image.open(CACHE_DIR + f"{category}_icons/{identity}.png").convert("RGBA")
    return None


async def get_image(identity: str | int, category: str) -> Optional[Image.Image]:
    # identity = Ahri, DrMundo, 4132, Exhaust, ...
    # category = champion, item, rune, spell (passed by user)

    cached = _check_cache(identity, category)
    if cached:
        return cached

    print("not cached")
    url = DDRAGON_URL_TEMPLATE + f"{VERSION}/img/{category}/{identity}.png"
    img_bytes = await _fetch_image(url)
    if img_bytes is None:
        return None
    
    img = Image.open(img_bytes).convert("RGBA")
    img.save(CACHE_DIR + f"{category}_icons/{identity}.png")

    return img