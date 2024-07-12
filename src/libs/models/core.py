from pydantic import BaseModel, Field


class Coordinate(BaseModel):
    x: int = Field(..., examples=[1])
    y: int = Field(..., examples=[1])


class AttackCommand(BaseModel):
    blockId: str = Field(
        ..., alias="block_id", examples=["f47ac10b-58cc-0372-8562-0e02b2c3d479"]
    )
    target: Coordinate = Field(..., examples=[{"x": 1, "y": 1}])


class BuildCommand(Coordinate):
    pass


class CommandPayload(BaseModel):
    attack: list[AttackCommand] = Field(
        ...,
        examples=[
            {
                "blockId": "f47ac10b-58cc-0372-8562-0e02b2c3d479",
                "target": {"x": 1, "y": 1},
            }
        ],
    )
    build: list[BuildCommand] = Field(..., examples=[{"x": 1, "y": 1}])
    moveBase: Coordinate = Field(..., alias="move_base", examples=[{"x": 1, "y": 1}])


class Response(BaseModel): ...


class ErrorResponse(Response):
    errCode: int = Field(..., alias="err_code", examples=[22])
    error: str = Field(..., examples=["description of the error"])


class CommandResponse(Response):
    acceptedCommands: CommandPayload = Field(
        ...,
        alias="accepted_commands",
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
    errors: list[str] = Field(..., examples=["coordinate at {0 0} is already occupied"])
