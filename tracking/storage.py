# ========== Imports ==========
import os
import json
from typing import Optional

from tracking.models import Guild


# ========== Constants ==========
FILE = "tracking/track.json"


# ========== Class TrackManager ==========
class TrackManager:
    """
    TrackManager is a class where your able to add a new guild with an ID or get a guild with a specific ID and save it in the json file.

    *Functions*:
        `get_guild()`: you can get a specific guild with an ID.
        `add_guild()`: you add a guild.
        `save()`: save your changes to the json.
    
    **IMPORTANT**
        When ever your with editing or adding to the json you're forced to use the `save()` function or else your changes won't go through!!
    """

    def __init__(self):
        self.path = FILE
        self.data = self._load()

    def _load(self) -> dict:
        if not os.path.exists(self.path):
            return {"guilds": {}}

        with open(self.path, "r") as f:
            data = json.load(f)
        
        # Ensure "guilds" key exists
        if "guilds" not in data or not isinstance(data["guilds"], dict):
            data["guilds"] = {}
        
        return data

    
    def save(self):
        """Saves the changes made to the json file.
        """
        # Ensure directory exists
        dirname = os.path.dirname(self.path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)

        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)
    
    def get_guild(self, guild_id: int) -> Optional[Guild]:
        """Returns Guild loaded from the json if it exists, else None"""
        key = str(guild_id)
        guild_data = self.data["guilds"].get(key)
        if guild_data is None:
            guild_data = {"users": {}}
            self.data["guilds"][key] = guild_data

        return Guild(key, guild_data)


    def add_guild(self, guild_id: int):
        """Adds a discord Guild to the track.json. Needs its ID.
        """
        self.data["guilds"].setdefault(str(guild_id), {"users": {}})
        return
    
    def remove_guild(self, guild_id: int) -> bool:
        """Removes a discord Guild from the track.json. Needs its ID.
        Returns:
            bool: True if success, False if Guilds doesn't exist.
        """
        if self.data["guilds"].pop(str(guild_id), None) is not None:
            return True
        return False
