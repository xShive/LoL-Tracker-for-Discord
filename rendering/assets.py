# fetch all images from ddragons
# ========== Imports ==========
import aiohttp
from PIL import Image, ImageDraw
from io import BytesIO
from typing import Optional
import os

DRAGON_URL = "https://ddragon.leagueoflegends.com/cdn/"
RANK_ICON_URL = "https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-emblem/emblem-"
CACHE_DIR = "rendering/assets/cache/"
VERSION = "16.3.1"

"""
1. Fetch: raw bytes. discord nor pillow can read.
2. Wrap in BytesIO. discord and pillow can read
3. Open with pillow -> converts to PIL object
4. Save back to BytesIO. discord and pillow can read.
5. Discord has its own type. Use function."""

"""TODO: fix linux"""

async def _fetch_image(
        url_to_fetch: str,
        session: aiohttp.ClientSession
) -> Optional[BytesIO]:
    async with session.get(url_to_fetch) as response:
        if response.status == 200:
            content = await response.read()
            return BytesIO(content)
    return None
    


def _check_cache(identity: str | int, category: str) -> Optional[Image.Image]:
    if os.path.exists(CACHE_DIR + f"{category}_icons/{identity}.png"):
        return Image.open(CACHE_DIR + f"{category}_icons/{identity}.png").convert("RGBA")
    return None


async def get_image(identity: str | int,
                    category: str,
                    session: aiohttp.ClientSession
            ) -> Optional[Image.Image]:
    # identity = Ahri, DrMundo, 4132, Exhaust, ...
    # category = champion, item, rune, spell, rank (passed by user)

    cached = _check_cache(identity, category)
    if cached:
        return cached

    print("not cached")
    if category == "rank":
        url = RANK_ICON_URL + f"{identity}.png"
    else:
        url = DRAGON_URL + f"{VERSION}/img/{category}/{identity}.png"
        
    img_bytes = await _fetch_image(url, session)
    if img_bytes is None:
        return None
    
    img = Image.open(img_bytes).convert("RGBA")
    img.save(CACHE_DIR + f"{category}_icons/{identity}.png")

    return img