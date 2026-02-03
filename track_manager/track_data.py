import json
import os

FILE = "track_manager/track.json"

class User:
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
    def __init__(self, guild_id: str, guild_data: dict):
        self._id = guild_id
        self._data = guild_data

    def get_member(self, discord_id: str) -> User | None:


        users = self._data["users"]

        if discord_id in users:
            return User(discord_id, users[discord_id])
        return None
    
    def add_member(self, discord_id: str, puuid: str, region: str) -> User:
        users = self._data["users"]

        if discord_id not in users:
            users[discord_id] = {
                "puuid": puuid,
                "region": region,
                "recent_matches": []
            }

        return User(discord_id, users[discord_id])
    
    def remove_member(self, discord_id: str) -> bool:
        users = self._data["users"]

        if discord_id in users:
            del User[discord_id]
            return True

        return False
    
    def get_all_members(self):
        all_users = []
        for discord_id, data in self._data["users"].items():
            user_object = User(discord_id, data)
            all_users.append(user_object)
        return all_users
    

class TrackManager:
    def __init__(self):
        self._filepath = FILE
        self._data = self._load()

    def _load(self) -> tuple[dict, bool]:
        """
        Loads the content of the json file.

        Returns:
            tuple: `(dict, bool)` The json itself and a boolean that represents if there are any problems with opening or not.
        """

        # check if the file exists
        if not os.path.exists(self._filepath):
            print(f"ERROR: could not find the following path: {self._filepath}")
            return {"guilds": {}}
        
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
            return {"guilds": {}}
    

    def get_guild(self, guild_id: int) -> Guild | None:
        guild_id = str(guild_id)

        if "guilds" not in self._data:
            self._data["guilds"] = {}

        guild_map = self._data["guilds"]

        if guild_id not in guild_map:
            return None

        return Guild(guild_id, guild_map[guild_id])
    
    def add_guild(self, guid_id: int):
        guid_id = str(guid_id)

        guild_map = self._data["guilds"]

        if guid_id not in guild_map:
            guild_map[guid_id] = {
                "users": {
                }
            }
        
        return Guild(guid_id, guild_map[guid_id])

    def save(self):
        with open(self._filepath, 'w') as File:
            json.dump(self._data, File, indent=4)
        print("Track.json has been saved")