from pydantic import BaseModel, Field, validator
from .cell import Cell, Coordinate


class Block(Cell):
    attack: int = Field(..., examples=[1])
    health: int = Field(..., examples=[1])
    is_head: bool = Field(False, alias="isHead", examples=[True])
    last_attack: Coordinate | None = Field(None, alias="lastAttack", examples=[Coordinate(x=1, y=1)])

class Base(Block):
    id: str = Field(..., examples=["f47ac10b-58cc-0372-8562-0e02b2c3d479"])
    range: int = Field(..., examples=[1])


class EnemyBase(Block):
    name: str = Field("unknown", examples=["BDSM"])
