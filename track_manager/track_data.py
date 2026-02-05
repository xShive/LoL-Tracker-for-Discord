# ========== Imports ==========
import json
import os
from typing import Optional

FILE = "track_manager/track.json"

# ========== Classes ==========
class User:
    """
    This class makes sure you can edit the data in the user itself

    *Function:*
        getters/setters for the following:
        - `discord_id` only has a getter
        - `puuid`
        - `region`
        - `matches`
        - `recent_match` only has a getter

    **IMPORTANT**
        Whenever you're with editing or adding to the json you're forced to use the `save()` function from `TrackManager()` or else your changes won't go through!!
    """

    def __init__(self, discord_id: str, data: dict):
        self._id = discord_id
        self._data = data
    
    # GETTERS:
    @property
    def discord_id(self) -> str:
        return self._id

    @property
    def puuid(self) -> str:
        return self._data["puuid"]
    
    @property
    def region(self) -> str:
        return self._data["region"]
    
    @property
    def matches(self) -> list[str]:
        # Returns a copy so outside code doesn't break the internal list
        return list(self._data["matches"])
    
    @property
    def recent_match(self) -> Optional[str]:
        matches = self._data["matches"]
        # Check if list is NOT empty before accessing [0]
        if matches:  
            return matches[0]
        
        return None
    
    # SETTERS:
    @puuid.setter
    def puuid(self, new_puuid: str):
        self._data["puuid"] = new_puuid
    
    @region.setter
    def region(self, new_region: str):
        self._data["region"] = new_region

    @matches.setter
    def matches(self, match_id: str):
        matches_list = self._data["matches"]

        # Check if match_id is in the list, or if it equals the latest one
        # If the match is already the most recent one, we skip adding it
        if matches_list and matches_list[0] == match_id:
            return 
        
        # Insert at the top (newest match)
        matches_list.insert(0, match_id)

        # Keep only the last 10 matches
        if len(matches_list) > 10:
            matches_list.pop()
            

class Guild:
    """
    The guild class gives you access to the members inside of it.

    *Functions:*
        `guild_id`: gets you the guild id your working in
        `get_member()`: gets the member with the corresponding id
        `add_member()`: adds a member with the corresponding id, puuid, region
        `remove_member()`: removes a member with a corresponding id
    
    **IMPORTANT**
        Whenever you are editing or adding to the json you're forced to use the `save()` 
        function from `TrackManager()` or else your changes won't go through!!
    """

    def __init__(self, guild_id: str, guild_data: dict):
        self._id = guild_id
        self._data = guild_data

    @property
    def guild_id(self) -> str:
        return self._id

    def get_member(self, discord_id: int) -> Optional[User]:
        """
        Gets the member from the guild with a specified id.

        *Note: Save your changes with `save()` from `TrackManager`*

        Args:
            discord_id (int): the member you want to get

        Returns:
            User | None: The user when found, otherwise None
        """
        discord_id_str = str(discord_id)
        users = self._data["users"]

        if discord_id_str in users:
            return User(discord_id_str, users[discord_id_str])
        
        return None
    
    def add_member(self, discord_id: int, puuid: str, region: str) -> Optional[User]:
        """
        Adds a member to the guild with specified data.

        *Note: Save your changes with `save()` from `TrackManager`*

        Args:
            discord_id (int): the user's discord ID
            puuid (str): the user's puuid
            region (str): the region that the user is located at

        Returns:
            User: The added user
        """
        discord_id_str = str(discord_id)
        users = self._data["users"]

        # Add if user doesn't exist yet
        if discord_id_str not in users:
            users[discord_id_str] = {
                "puuid": puuid,
                "region": region,
                "matches": []
            }
            return User(discord_id_str, users[discord_id_str])
        
        return None

    
    def remove_member(self, discord_id: int) -> bool:
        """
        Removes a member from the guild.

        *Note: Save your changes with `save()` from `TrackManager`*

        Args:
            discord_id (int): the member you want to remove

        Returns:
            bool: True if it got removed, otherwise False
        """
        discord_id_str = str(discord_id)
        users = self._data["users"]

        if discord_id_str in users:
            del users[discord_id_str]
            return True

        return False
    
    def get_all_members(self) -> list[User]:
        """
        Get a list of all members in the guild.

        *Note: Save your changes with `save()` from `TrackManager`*

        Returns:
            list: The list of members in the guild
        """
        all_users = []
        # We iterate over the dictionary items to get both ID and Data
        for discord_id_str, user_data in self._data["users"].items():
            user_object = User(discord_id_str, user_data)
            all_users.append(user_object)
            
        return all_users
    
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
        self._filepath = FILE
        self._data = self._load()

    def _load(self) -> Optional[dict]:
        """
        Loads the content in the json file

        Returns:
            
            `dict | None`: The json itself or nothing whenever it got an error loading
        """

        # check if the file exists
        if not os.path.exists(self._filepath):
            print(f"ERROR: could not find the following path: {self._filepath}")
            return None
        
        try:
            with open(self._filepath, "r") as file:
                jsonfile = json.load(file)
            
            if jsonfile == {}:
                jsonfile = {
                    "guilds": {

                    }
                }
            
            return jsonfile
            
        except json.JSONDecodeError:
            print(f"ERROR: {self._filepath} might be corrupted.")
            return None
    

    def get_guild(self, guild_id_int: int) -> Optional[Guild]:
        """
        Gets the json content from a specific guild

        *Note: Save your changes you made with `save()`*

        Args:
            guild_id (int): The id of the guild

        Returns:

            `Guild | None`: The guild class or Nothing whenever faced with a problem
        """
        guild_id_str = str(guild_id_int)

        if self._data is None:
            return None
        
        if not self._data.get("guilds"):
            self._data["guilds"] = {}

        guild_map = self._data["guilds"]

        if not guild_map.get(guild_id_str):
            return None

        return Guild(guild_id_str, guild_map[guild_id_str])
    
    def add_guild(self, guid_id_int: int) -> Optional[Guild]:
        """
        Adds a new guild to the json and returns the guild you added

        *Note: Save your changes you made with `save()`*

        Args:
            guid_id (int): the guild id you want to add

        Returns:
            Guild: the added guild or already existing guild
        """
        guid_id_str = str(guid_id_int)

        if self._data is None:
            return None

        guild_map = self._data.get("guilds")

        if guild_map is None:
            self._data["guilds"] = {}
            return None

        if not guild_map.get(guid_id_str):
            guild_map[guid_id_str] = {
                "users": {
                }
            }
        
        return Guild(guid_id_str, guild_map[guid_id_str])
    
    def remove_guild(self, guild_id_int: int) -> bool:
        """
        Removes a guild from the json

        *Note: Save your changes you made with `save()`*

        Args:
            guild_id (int): the id you want to remove

        Returns:
            bool: True if the guild was deleted, otherwise False
        """
        guild_id_str = str(guild_id_int) 

        if self._data is None:
            return False

        guild_map = self._data.get("guilds")

        if guild_map == None:
            return False

        if guild_map.get(guild_id_str):
            del guild_map[guild_id_str]
            return True
        
        return False

    def save(self):
        """
        Saves the changes you made in json file
        """
        with open(self._filepath, 'w') as File:
            json.dump(self._data, File, indent=4)
        print("Track.json has been saved")