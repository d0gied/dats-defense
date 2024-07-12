from pydantic import BaseModel, Field

class Cell(BaseModel):
    x: int = Field(example=1)
    y: int = Field(example=1)
