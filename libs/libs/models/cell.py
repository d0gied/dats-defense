from pydantic import BaseModel, Field


class Coordinate(BaseModel):
    x: int = Field(..., examples=[1])
    y: int = Field(..., examples=[1])


class Cell(BaseModel):
    x: int = Field(examples=[1])
    y: int = Field(examples=[1])

    def get_coordinate(self) -> Coordinate:
        return Coordinate(x=self.x, y=self.y)
