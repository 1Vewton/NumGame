from pydantic import BaseModel, Field

# User Creation
class NewPlayerData(BaseModel):
    player_name: str = Field(title="Player Name",
                             description="The name of the player",
                             min_length=3,
                             max_length=100)

# User Login
class LoginPlayerData(BaseModel):
    player_name: str = Field(title="Player Name",
                             description="The name of the player",
                             min_length=3,
                             max_length=100)

# User Info Query
class PlayerData(BaseModel):
    player_name: str = Field(title="Player Name",
                             description="The name of the player",
                             min_length=3,
                             max_length=100)
    palyer_id: str = Field(title="Player ID",
                           description="The ID of the player",
                           min_length=3,
                           max_length=100)