from pydantic import BaseModel, Field
from .cell import Cell


class Zombie(Cell):
    direction: str = Field(..., examples=["up"])
    id: str = Field(..., examples=["f47ac10b-58cc-0372-8562-0e02b2c3d479"])
    speed: int = Field(..., examples=[1])
    type: str = Field(..., examples=["normal"])
    wait_turns: int = Field(..., alias="waitTurns", examples=[1])


class ZPot(Cell):
    type: str = Field(..., examples=["default"])
