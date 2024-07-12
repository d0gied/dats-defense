from pydantic import BaseModel, Field

class Cell(BaseModel):
    x: int = Field(examples=[1])
    y: int = Field(examples=[1])
