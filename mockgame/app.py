from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/play/zombidef/command")
def command(payload: dict):
    return JSONResponse(
        content={
            "acceptedCommands": {
                "attack": [
                    {
                        "blockId": "f47ac10b-58cc-0372-8562-0e02b2c3d479",
                        "target": {"x": 1, "y": 1},
                    }
                ],
                "build": [{"x": 1, "y": 1}],
                "moveBase": {"x": 1, "y": 1},
            },
            "errors": ["coordinate at {0 0} is already occupied"],
        },
        status_code=200,
    )


@app.put("/play/zombidef/participate")
def participate():
    return JSONResponse({"startsInSec": 300}, status_code=200)


@app.get("/play/zombidef/units")
def units():
    return JSONResponse(
        {
            "base": [
                {
                    "attack": 10,
                    "health": 100,
                    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                    "isHead": True,
                    "lastAttack": {"x": 1, "y": 1},
                    "range": 5,
                    "x": 1,
                    "y": 1,
                }
            ],
            "enemyBlocks": [
                {
                    "attack": 10,
                    "health": 100,
                    "isHead": True,
                    "lastAttack": {"x": 1, "y": 1},
                    "name": "player-test",
                    "x": 1,
                    "y": 1,
                }
            ],
            "player": {
                "enemyBlockKills": 100,
                "gameEndedAt": "2021-10-10T10:00:00Z",
                "gold": 100,
                "name": "player-test",
                "points": 100,
                "zombieKills": 100,
            },
            "realmName": "map1",
            "turn": 1,
            "turnEndsInMs": 1000,
            "zombies": [
                {
                    "attack": 10,
                    "direction": "up",
                    "health": 100,
                    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                    "speed": 10,
                    "type": "normal",
                    "waitTurns": 1,
                    "x": 1,
                    "y": 1,
                }
            ],
        },
        status_code=200,
    )


@app.get("/play/zombidef/world")
def world():
    return JSONResponse(
        {"realmName": "map1", "zpots": [{"x": 1, "y": 1, "type": "default"}]},
        status_code=200,
    )


@app.get("/rounds/zombidef")
def zombidef():
    return JSONResponse(
        {
            "gameName": "defense",
            "now": "2021-01-01T00:00:00Z",
            "rounds": [
                {
                    "duration": 60,
                    "endAt": "2021-01-01T00:00:00Z",
                    "name": "Round 1",
                    "repeat": 1,
                    "startAt": "2021-01-01T00:00:00Z",
                    "status": "active",
                }
            ],
        },
        status_code=200,
    )
