import json
import os

FILE = "track_manager/track.json"

class User:
    """
    This class makes sure you can edit the data in the user itself

    *Function:*
        getters/setters for the following:
        - `puuid`
        - `region`
        - `matches`
        - `recent_matches` only has a getter

    **IMPORTANT**
        When ever your with editing or adding to the json you're forced to use the `save()` function from `TrackManager()` or else your changes won't go through!!
    """

    def __init__(self, discord_id: str, data: str):
        self._id = discord_id
        self._data = data
    
    # GETTERS:

    # User.puuid 

    @property
    def puuid(self) -> str:
        return self._data["puuid"]
    
    @property
    def region(self) -> str:
        return self._data["region"]
    
    @property
    def matches(self) -> list:
        return list(self._data["matches"])
    
    @property
    def recent_match(self) -> str | None:
        if self._data["matches"] == None:
            return self._data["matches"][0]
    
    # SETTERS:

    @puuid.setter
    def puuid(self, new_puuid: str):
        self._data["puuid"] = new_puuid
    
    @region.setter
    def region(self, new_region: str):
        self._data["region"] = new_region

    @matches.setter
    def matches(self, match_id: str):
        matches_list =  self._data["matches"]

        if matches_list == match_id:
            return 
        
        matches_list.insert(0, match_id)

        if len(matches_list) >= 11:
            del matches_list[10]


class Guild:
    """
    The guild class gives you access to the members inside of it

    *Function:*
        `get_member()`: gets the member with the corresponding id
        `add_member()`: adds a member with the corresponding id, puuid, region
        `remove_member()`: removes a member with a corresponding id
    
    **IMPORTANT**
        When ever your with editing or adding to the json you're forced to use the `save()` function from `TrackManager()` or else your changes won't go through!!
    """

    def __init__(self, guild_id: str, guild_data: dict):
        self._id = guild_id
        self._data = guild_data

    def get_member(self, discord_id: int) -> User | None:
        """
        gets the member from the guild with an specified id

        *Note: Save your changes you made with `save()` from `TrackManager`*

        Args:
            discord_id (int): the member you want to get

        Returns:

            `User | None`: The user when found, otherwise None
        """
        discord_id = str(discord_id)

        users = self._data["users"]

        if discord_id in users:
            return User(discord_id, users[discord_id])
        return None
    
    def add_member(self, discord_id: int, puuid: str, region: str) -> User:
        """
        Adds a member to the guild with a specified data

        *Note: Save your changes you made with `save()` from `TrackManager`*

        Args:
            discord_id (int): the users discord ID
            puuid (str): the users puuid
            region (str): the region that the user is located at

        Returns:
            User: The added user
        """
        discord_id = str(discord_id)

        users = self._data["users"]

        if discord_id not in users:
            users[discord_id] = {
                "puuid": puuid,
                "region": region,
                "recent_matches": []
            }

        return User(discord_id, users[discord_id])
    
    def remove_member(self, discord_id: int) -> bool:
        """
        Removes a member from the guild

        *Note: Save your changes you made with `save()` from `TrackManager`*

        Args:
            discord_id (int): the member you want to remove

        Returns:
            bool: True if it got removed, otherwise False
        """

        discord_id = str(discord_id)
        users = self._data["users"]

        if discord_id in users:
            del User[discord_id]
            return True

        return False
    
    def get_all_members(self) -> list:
        """
        get a list of all the member in the guild

        *Note: Save your changes you made with `save()` from `TrackManager`*

        Returns:
            list: The list of members in the guild
        """
        all_users = []
        for discord_id, data in self._data["users"].items():
            user_object = User(discord_id, data)
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

    def _load(self) -> dict | None:
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
    

    def get_guild(self, guild_id_int: int) -> Guild | None:
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

        return Guild(guild_id_int, guild_map[guild_id_str])
    
    def add_guild(self, guid_id: int) -> Guild:
        """
        Adds a new guild to the json and returns the guild you added

        *Note: Save your changes you made with `save()`*

        Args:
            guid_id (int): the guild id you want to add

        Returns:
            Guild: the added guild or already existing guild
        """
        guid_id = str(guid_id)

        guild_map = self._data["guilds"]

        if guid_id not in guild_map:
            guild_map[guid_id] = {
                "users": {
                }
            }
        
        return Guild(guid_id, guild_map[guid_id])
    
    def remove_guild(self, guild_id: int) -> bool:
        """
        Removes a guild from the json

        *Note: Save your changes you made with `save()`*

        Args:
            guild_id (int): the id you want to remove

        Returns:
            bool: True if the guild was deleted, otherwise False
        """

        guild_map = self._data["guilds"]

        if guild_id in guild_map:
            del guild_map[guild_id]
            return True
        
        return False

    def save(self):
        """
        Saves the changes you made in json file
        """
        with open(self._filepath, 'w') as File:
            json.dump(self._data, File, indent=4)
        print("Track.json has been saved")