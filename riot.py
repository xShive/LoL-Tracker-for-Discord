# ========== Imports ==========
import os
import dotenv
import aiohttp


# ========== Configuration ==========
# we request data from riot. riot looks at headers to check for access.
# riot looks for "X-Riot-Token"
dotenv.load_dotenv()
RIOT_TOKEN = os.getenv("RIOT_TOKEN")
if RIOT_TOKEN is None: raise ValueError("RIOT_TOKEN not found in .env file.")

HEADERS = {
    "X-Riot-Token" : RIOT_TOKEN
}

# step 1: region. jayden is from a different server so fuck.
# (this is used to build the URL)
REGIONS = {
    # AMERICAS
    "NA": "https://americas.api.riotgames.com",
    "BR": "https://americas.api.riotgames.com",
    "LAN": "https://americas.api.riotgames.com",
    "LAS": "https://americas.api.riotgames.com",
    "OCE": "https://americas.api.riotgames.com",
    "PBE": "https://americas.api.riotgames.com",

    # EUROPES
    "EUW": "https://europe.api.riotgames.com",
    "EUNE": "https://europe.api.riotgames.com",
    "TR": "https://europe.api.riotgames.com",
    "RU": "https://europe.api.riotgames.com",

    # ASIA
    "KR": "https://asia.api.riotgames.com",
    "JP": "https://asia.api.riotgames.com",

    # RANDOMS ASIA
    "PH": "https://sea.api.riotgames.com",
    "SG": "https://sea.api.riotgames.com",
    "TW": "https://sea.api.riotgames.com",
    "TH": "https://sea.api.riotgames.com",
    "VN": "https://sea.api.riotgames.com",
}

# STEPS: PUUID -> MATCH ID -> DATA
# URL: REGION -> COMMAND -> INPUT


# ========== Functions ==========
async def get_puuid(game_name: str, tag_line: str, region_code: str) -> str | None:
    # 1. REGION URL
    region_url = REGIONS.get(region_code)
    if region_url is None: return

    # 2. COMMAND URL
    command_url = "riot/account/v1/accounts/by-riot-id"

    # 3. INPUT
    input_url = f"{game_name}/{tag_line}"

    full_url = f"{region_url}/{command_url}/{input_url}"

    # 'open browser'
    # closes automatically
    async with aiohttp.ClientSession() as session:

        # hit the URL
        # send request
        async with session.get(full_url, headers=HEADERS) as response:

            # 200 = ok, 404 not found (global HTTP)
            if response.status == 200:

                data = await response.json()

                return data['puuid']

            else:
                print(f"Error: {response.status}")
                return None