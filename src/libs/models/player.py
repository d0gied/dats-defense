from pydantic import BaseModel, Field

class Player(BaseModel):
    enemy_block_kills: int = Field(..., alias="enemyBlockKills", examples=[1])
    game_ended_at: str = Field(..., alias="gameEndedAt", examples=["2021-10-10T10:00:00Z"])
    gold: int = Field(..., examples=[1])
    name: str = Field(..., examples=["BDSM"])
    points: int = Field(..., examples=[1])
    zombie_kills: int = Field(..., alias="zombieKills", examples=[1])
