from typing import Optional, List
from typing_extensions import Literal
from pydantic import BaseModel, Field, conlist, validator
from .block import Base, EnemyBase
from .player import Player
from .zombie import Zombie, ZPot
from .cell import Coordinate
from datetime import datetime, timedelta
from enum import Enum

class AttackCommand(BaseModel):
    block_id: str = Field(
        ..., alias="blockId", examples=["f47ac10b-58cc-0372-8562-0e02b2c3d479"]
    )
    target: Coordinate = Field(..., examples=[{"x": 1, "y": 1}])


class BuildCommand(Coordinate):
    pass


class CommandPayload(BaseModel):
    attack: list[AttackCommand] | None = Field(
        ...,
        examples=[
            {
                "blockId": "f47ac10b-58cc-0372-8562-0e02b2c3d479",
                "target": {"x": 1, "y": 1},
            }
        ],
    )
    build: list[BuildCommand] | None = Field(..., examples=[{"x": 1, "y": 1}])
    move_base: Coordinate | None = Field(
        ..., alias="moveBase", examples=[{"x": 1, "y": 1}]
    )


class Response(BaseModel):
    class Config:
        extra = "allow"


class ErrorResponse(Response):
    err_code: int = Field(..., alias="errCode", examples=[22])
    error: str = Field(..., examples=["description of the error"])


class CommandResponse(Response):
    accepted_commands: CommandPayload = Field(
        ...,
        alias="acceptedCommands",
        examples=[
            {
                "attack": [
                    {
                        "blockId": "f47ac10b-58cc-0372-8562-0e02b2c3d479",
                        "target": {"x": 1, "y": 1},
                    }
                ],
                "build": [{"x": 1, "y": 1}],
                "moveBase": {"x": 1, "y": 1},
            }
        ],
    )
    errors: list[str] | None = Field(
        ..., examples=["coordinate at {0 0} is already occupied"]
    )


class ParticipateResponse(Response):
    starts_in_sec: int = Field(..., alias="startsInSec", examples=[300])


class UnitsRepsonse(Response):
    base: list[Base] = Field(...)
    enemy_blocks: list[EnemyBase] = Field(default_factory=list, alias="enemyBlocks")
    player: Player = Field(...)
    realm_name: str = Field(..., alias="realmName", examples=["map1"])
    turn: int = Field(..., examples=[1])
    turn_ends_in_ms: int = Field(..., alias="turnEndsInMs", examples=[1000])
    zombies: list[Zombie] = Field(default_factory=list)

    @validator("base", "enemy_blocks", "zombies", pre=True, always=True)
    def base_val(cls, v):
        return v or []

class WorldResponse(Response):
    zpots: list[ZPot] = Field(...)

class Round(BaseModel):
    duration: int = Field(..., examples=[60])
    end_at: datetime = Field(..., alias="endAt", examples=["2021-10-10T10:00:00Z"])
    name: str = Field(..., examples=["round1"])
    repeat: Optional[int] = Field(None, examples=[1])
    start_at: datetime = Field(..., alias="startAt", examples=["2021-10-10T10:00:00Z"])
    status: Literal["active", "not started", "ended"] = Field(..., examples=["active"])

    def starts_in(self) -> timedelta:
        return self.start_at - datetime.now().astimezone()

    def ends_in(self):
        return self.end_at - datetime.now().astimezone()

class RoundsResponse(BaseModel):
    game_name: str = Field(..., alias="gameName", examples=["defense"])
    now: datetime = Field(..., examples=["2021-10-10T10:00:00Z"])
    rounds: list[Round] = Field(...)
