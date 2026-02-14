"""constants.py

Contains the constants used for LoL assets and rendering.
This module contains all URLs, version info, mappings, and layout constants
used throughout the rendering system.
"""

# ========== Imports ==========
from pathlib import Path
from PIL import ImageFont


# ========== API & Asset URLs ==========
VERSION = "16.3.1"
DRAGON_URL = "https://ddragon.leagueoflegends.com/cdn/"
RANK_ICON_URL = "https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-emblem/emblem-"
PERK_DATA_URL = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json"      # rune database. contains id, name, iconPath
SPELL_DATA_URL = f"{DRAGON_URL}{VERSION}/data/en_US/summoner.json"
PERK_ICON_BASE = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default"


# ========== File Paths ==========
RENDERING_ROOT_DIR = Path(__file__).parent.parent   # current file parent = core, core parent = rendering
CACHE_DIR = RENDERING_ROOT_DIR / "assets" / "cache"
TEMPLATES_DIR = RENDERING_ROOT_DIR / "assets" / "templates"
FONTS_DIR = RENDERING_ROOT_DIR / "assets" / "fonts"


# ========== Fonts ==========
NAME_FONT = ImageFont.truetype(str(FONTS_DIR / "Sora" / "Sora-SemiBold.ttf"), 18)
RANK_FONT = ImageFont.truetype(str(FONTS_DIR / "Sora" / "Sora-Medium.ttf"), 12)


# ========== Data Mappings ==========
"""In ParticipantData, runes and spells are identified by an ID. The URL needs their name.
Riot gives you jsons with mappings: ID, NAME, PATH. This is PERK_DATA and SPELL_DATA_URL."""

RANK_LABELS = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4
}

STYLE_ICON_MAP = {
    8000: "7201_precision.png",
    8100: "7200_domination.png",
    8200: "7202_sorcery.png",
    8300: "7203_whimsy.png",
    8400: "7204_resolve.png"
}

COLORS = {
    "IRON": (75, 75, 75, 255),
    "BRONZE": (200, 136, 73, 255),
    "SILVER": (192, 192, 192, 255),
    "GOLD": (255, 215, 0, 255),
    "PLATINUM": (37, 150, 190, 255),
    "EMERALD": (0, 200, 100, 255),
    "DIAMOND": (185, 242, 255, 255),
    "MASTER": (155, 89, 182, 255),
    "GRANDMASTER": (231, 76, 60, 255),
    "CHALLENGER": (241, 196, 15, 255),

    "WHITE": (255, 255, 255, 255),
    "BLACK": (0, 0, 0, 255),
    "SHADOW": (0, 0, 0, 100)
}


# ========== Render Sizes ==========
class ImageSizes:
    CHAMPION_ICON = 80
    CHAMPION_CIRCLE_INSET = 10  # The mask goes 10 pixels inwards

    RANK_ICON = (128, 72)
    RUNE_ICON = 30
    RUNE_SECONDARY = 25

    SPELL_ICON = 30

    