from pydantic import BaseModel, Field

class Coordinate(BaseModel):
  x: int = Field(..., examples=[1])
  y: int = Field(..., examples=[1])

class AttackCommand(BaseModel):
  block_id: str = Field(..., alias="blockId", examples=["f47ac10b-58cc-0372-8562-0e02b2c3d479"])
  target: Coordinate = Field(..., examples=[{"x": 1, "y": 1}])

class BuildCommand(Coordinate):
  pass

class CommandPayload(BaseModel):
  attack: list[AttackCommand] = Field(..., examples=[{"blockId": "f47ac10b-58cc-0372-8562-0e02b2c3d479", "target": {"x": 1, "y": 1}}])
  build: list[BuildCommand] = Field(..., examples=[{"x": 1, "y": 1}])
  move_base: Coordinate = Field(..., alias="moveBase", examples=[{"x": 1, "y": 1}])

class CommandResponse(BaseModel): ...

class CommandError(CommandResponse):
  err_code: int = Field(..., alias="errCode", examples=[22])
  error: str = Field(..., examples=["description of the error"])

class CommandSuccess(CommandResponse):
  accepted_commands: CommandPayload = Field(..., alias="acceptedCommands", examples=[{"attack": [{"blockId": "f47ac10b-58cc-0372-8562-0e02b2c3d479", "target": {"x": 1, "y": 1}}], "build": [{"x": 1, "y": 1}], "moveBase": {"x": 1, "y": 1}}])
  errors: list[str] = Field(..., examples=["coordinate at {0 0} is already occupied"])
