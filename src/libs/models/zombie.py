from pydantic import BaseModel, Field
from .cell import Cell

class Zoombie(Cell):
    attack: int = Field(..., examples=[1])
    direction: str = Field(..., examples=["up"])
    health: int = Field(..., examples=[1])
    id: str = Field(..., examples=["f47ac10b-58cc-0372-8562-0e02b2c3d479"])
    speed: int = Field(..., examples=[1])
    type: str = Field(..., examples=["normal"])
    wait_turns: int = Field(..., alias="waitTurns", examples=[1])

class ZPots(Cell):
    type: str = Field(..., examples=["default"])
