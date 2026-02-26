from pydantic import BaseModel, Field

# User Creation
class NewPlayerData(BaseModel):
    player_name: str = Field(title="Player Name", description="The name of the player", min_length=3, max_length=100)