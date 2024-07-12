from pydantic import BaseModel, Field
from .cell import Cell
from .core import Coordinate


class Block(Cell):
    attack: int = Field(..., examples=[1])
    health: int = Field(..., examples=[1])
    is_head: bool = Field(..., alias="isHead", examples=[True])
    last_attack: Coordinate = Field(
        ..., alias="lastAttack", examples=[Coordinate(x=1, y=1)]
    )


class Base(Block):
    id: str = Field(..., examples=["f47ac10b-58cc-0372-8562-0e02b2c3d479"])
    range: int = Field(..., examples=[1])


class EnemyBase(Block):
    name: str = Field(..., examples=["BDSM"])
