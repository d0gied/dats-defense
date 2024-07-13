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
                    "x": 187,
                    "y": 517,
                    "attack": 40,
                    "health": 75,
                    "isHead": True,
                    "lastAttack": None,
                    "id": "0190abe9-2042-7e79-9b0a-6a24bb133d95",
                    "range": 8
                },
                {
                    "x": 188,
                    "y": 517,
                    "attack": 10,
                    "health": 7,
                    "isHead": False,
                    "lastAttack": None,
                    "id": "0190abe9-2042-7e7d-94e5-d797d710de91",
                    "range": 5
                }
            ],
            "enemy_blocks": [
                {
                    "x": 198,
                    "y": 507,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": None,
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 519,
                    "attack": 10,
                    "health": 81,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 523
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 520,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 523
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 518,
                    "attack": 10,
                    "health": 81,
                    "isHead": False,
                    "lastAttack": {
                        "x": 196,
                        "y": 519
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 510,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 193,
                    "y": 507,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 523,
                    "attack": 10,
                    "health": 26,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 523
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 510,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 518,
                    "attack": 10,
                    "health": 81,
                    "isHead": False,
                    "lastAttack": {
                        "x": 196,
                        "y": 519
                    },
                    "name": "unknown"
                },
                {
                    "x": 194,
                    "y": 508,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 508,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 522,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 523
                    },
                    "name": "unknown"
                },
                {
                    "x": 195,
                    "y": 508,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 196,
                    "y": 509,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 513,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 516,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 196,
                        "y": 519
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 515,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 196,
                        "y": 519
                    },
                    "name": "unknown"
                },
                {
                    "x": 192,
                    "y": 507,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 515,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 192,
                        "y": 515
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 511,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 522,
                    "attack": 10,
                    "health": 32,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 523
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 516,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 196,
                        "y": 519
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 507,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 196,
                    "y": 507,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 192,
                    "y": 508,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 521,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 523
                    },
                    "name": "unknown"
                },
                {
                    "x": 192,
                    "y": 509,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": None,
                    "name": "unknown"
                },
                {
                    "x": 195,
                    "y": 507,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 523,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 523
                    },
                    "name": "unknown"
                },
                {
                    "x": 196,
                    "y": 508,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 512,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 509,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 193,
                    "y": 508,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 509,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 513,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 512,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 508,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 521,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 523
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 517,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 196,
                        "y": 519
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 520,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 523
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 517,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 196,
                        "y": 519
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 514,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 511,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 194,
                    "y": 507,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                },
                {
                    "x": 198,
                    "y": 519,
                    "attack": 10,
                    "health": 81,
                    "isHead": False,
                    "lastAttack": {
                        "x": 196,
                        "y": 519
                    },
                    "name": "unknown"
                },
                {
                    "x": 197,
                    "y": 514,
                    "attack": 10,
                    "health": 100,
                    "isHead": False,
                    "lastAttack": {
                        "x": 194,
                        "y": 511
                    },
                    "name": "unknown"
                }
            ],
            "player": {
                "enemyBlockKills": 0,
                "gameEndedAt": None,
                "gold": 10,
                "name": "Big Data Small Memory",
                "points": 0,
                "zombieKills": 0
            },
            "realmName": "test-day2-15",
            "turn": 86,
            "turnEndsInMs": 1069,
            "zombies": [
                {
                    "x": 182,
                    "y": 523,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "01c4c7b5-1972-44d4-a901-fdbccf6353c6",
                    "speed": 1,
                    "type": "liner",
                    "waitTurns": 1
                },
                {
                    "x": 182,
                    "y": 523,
                    "attack": 43,
                    "direction": "right",
                    "health": 19,
                    "id": "eb9eb763-f5e7-4f5d-b442-1a6c058c327e",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 179,
                    "y": 519,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "a544f518-5301-414c-b349-86a544663451",
                    "speed": 1,
                    "type": "bomber",
                    "waitTurns": 1
                },
                {
                    "x": 187,
                    "y": 518,
                    "attack": 999999,
                    "direction": "up",
                    "health": 17,
                    "id": "aef1b7e7-7108-449d-b609-87f882677d13",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 2
                },
                {
                    "x": 179,
                    "y": 513,
                    "attack": 25,
                    "direction": "right",
                    "health": 13,
                    "id": "045e7a80-54cd-4754-bc46-6cbc6e1d874d",
                    "speed": 3,
                    "type": "chaos_knight",
                    "waitTurns": 1
                },
                {
                    "x": 193,
                    "y": 524,
                    "attack": 999999,
                    "direction": "up",
                    "health": 19,
                    "id": "c5372ce9-17e8-4a6f-995e-e14d205b4392",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 2
                },
                {
                    "x": 178,
                    "y": 524,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "46635343-513a-41c1-81d6-1b1947b6a2b9",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 181,
                    "y": 524,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "3f4a35e5-ae05-4fd5-bfd1-77ffcc028eae",
                    "speed": 1,
                    "type": "liner",
                    "waitTurns": 1
                },
                {
                    "x": 194,
                    "y": 512,
                    "attack": 43,
                    "direction": "left",
                    "health": 19,
                    "id": "71878b5e-7caf-41b5-9a44-561115bd9979",
                    "speed": 3,
                    "type": "chaos_knight",
                    "waitTurns": 1
                },
                {
                    "x": 189,
                    "y": 517,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "a73d02b9-ea13-4409-b6f6-83803f1fee26",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 177,
                    "y": 518,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "d7ecd747-ba09-46f2-b626-bbf85ac3f860",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 190,
                    "y": 522,
                    "attack": 37,
                    "direction": "right",
                    "health": 17,
                    "id": "72dfc820-cc6d-47d5-b8de-13f6bcc3c6a0",
                    "speed": 1,
                    "type": "liner",
                    "waitTurns": 1
                },
                {
                    "x": 179,
                    "y": 515,
                    "attack": 999999,
                    "direction": "left",
                    "health": 19,
                    "id": "c60a0604-0659-4d8e-a288-d0bc14729edc",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 1
                },
                {
                    "x": 185,
                    "y": 517,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "fb8c016d-2d8b-4025-98b7-c0697818cb21",
                    "speed": 1,
                    "type": "bomber",
                    "waitTurns": 1
                },
                {
                    "x": 181,
                    "y": 519,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "0b9c11df-c6d8-4c5c-b531-f23e328ee1da",
                    "speed": 1,
                    "type": "bomber",
                    "waitTurns": 1
                },
                {
                    "x": 191,
                    "y": 516,
                    "attack": 999999,
                    "direction": "up",
                    "health": 17,
                    "id": "4268ce1c-ffaf-416d-a0e2-5dbc1cfd6ff2",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 2
                },
                {
                    "x": 191,
                    "y": 516,
                    "attack": 37,
                    "direction": "right",
                    "health": 17,
                    "id": "8cfe95e0-e8aa-4683-b1d6-f02d296fbc94",
                    "speed": 1,
                    "type": "bomber",
                    "waitTurns": 1
                },
                {
                    "x": 185,
                    "y": 508,
                    "attack": 37,
                    "direction": "up",
                    "health": 17,
                    "id": "edb63072-0f7f-48e6-9afa-b07b7e865af4",
                    "speed": 1,
                    "type": "liner",
                    "waitTurns": 1
                },
                {
                    "x": 186,
                    "y": 512,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "fbb36b1e-6cd0-4440-9676-935c6bce3984",
                    "speed": 2,
                    "type": "fast",
                    "waitTurns": 1
                },
                {
                    "x": 190,
                    "y": 513,
                    "attack": 37,
                    "direction": "up",
                    "health": 17,
                    "id": "40c9c239-42e5-4da5-86d5-fb343d6f9b5d",
                    "speed": 1,
                    "type": "bomber",
                    "waitTurns": 1
                },
                {
                    "x": 192,
                    "y": 524,
                    "attack": 999999,
                    "direction": "up",
                    "health": 19,
                    "id": "642fe2f0-074e-4a37-b5cd-59a8815aa255",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 2
                },
                {
                    "x": 177,
                    "y": 524,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "e2dc3304-d25c-4986-9f5a-af3538dcffca",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 182,
                    "y": 513,
                    "attack": 37,
                    "direction": "up",
                    "health": 17,
                    "id": "244e7420-29c5-4d43-bbb0-69cc387434df",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 178,
                    "y": 511,
                    "attack": 999999,
                    "direction": "up",
                    "health": 15,
                    "id": "76078b50-31e9-47ef-845d-d1fc23e704e4",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 1
                },
                {
                    "x": 190,
                    "y": 514,
                    "attack": 37,
                    "direction": "right",
                    "health": 17,
                    "id": "7f1e6104-ec66-4a98-94f5-340f0a3a78a3",
                    "speed": 1,
                    "type": "bomber",
                    "waitTurns": 1
                },
                {
                    "x": 190,
                    "y": 516,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "1398d2cd-33d5-4e20-97e5-281c90d9ce2c",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 178,
                    "y": 516,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "90f09c98-78dc-4607-9c92-27a2866286f8",
                    "speed": 1,
                    "type": "liner",
                    "waitTurns": 1
                },
                {
                    "x": 178,
                    "y": 516,
                    "attack": 999999,
                    "direction": "up",
                    "health": 17,
                    "id": "82e1471d-e505-497f-bc3b-37acc19a51ab",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 1
                },
                {
                    "x": 185,
                    "y": 519,
                    "attack": 43,
                    "direction": "right",
                    "health": 19,
                    "id": "72edea7a-b4db-4c9f-9002-b31b85348092",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 179,
                    "y": 520,
                    "attack": 37,
                    "direction": "right",
                    "health": 17,
                    "id": "e35f7ef5-1ffe-4358-abe4-baa685281e6e",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 179,
                    "y": 512,
                    "attack": 37,
                    "direction": "up",
                    "health": 17,
                    "id": "bb68dd68-6851-4a05-9cf3-726dcfcf93d7",
                    "speed": 1,
                    "type": "liner",
                    "waitTurns": 1
                },
                {
                    "x": 188,
                    "y": 514,
                    "attack": 43,
                    "direction": "right",
                    "health": 19,
                    "id": "f5aadb6f-a844-4c8f-861f-950f2bde998e",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 196,
                    "y": 524,
                    "attack": 999999,
                    "direction": "up",
                    "health": 19,
                    "id": "4cce3162-9501-4df9-b357-e095bee35329",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 2
                },
                {
                    "x": 183,
                    "y": 520,
                    "attack": 999999,
                    "direction": "right",
                    "health": 19,
                    "id": "aaf46e20-a54e-4859-9145-2f957374d516",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 1
                },
                {
                    "x": 182,
                    "y": 516,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "07aba49f-3c17-4281-9ac3-cceaa8ae2792",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 190,
                    "y": 521,
                    "attack": 37,
                    "direction": "right",
                    "health": 17,
                    "id": "cf1986b1-0b5d-4f3c-b414-6c6397efc620",
                    "speed": 1,
                    "type": "liner",
                    "waitTurns": 1
                },
                {
                    "x": 177,
                    "y": 511,
                    "attack": 37,
                    "direction": "right",
                    "health": 17,
                    "id": "b6c14b99-7f92-4a73-afea-140ece36e590",
                    "speed": 1,
                    "type": "bomber",
                    "waitTurns": 1
                },
                {
                    "x": 177,
                    "y": 511,
                    "attack": 43,
                    "direction": "left",
                    "health": 19,
                    "id": "c9c37f23-4d5c-4d97-b0c5-650a293bfa81",
                    "speed": 1,
                    "type": "bomber",
                    "waitTurns": 1
                },
                {
                    "x": 188,
                    "y": 522,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "f13a406a-832a-4a7e-9eb8-e5d9fed55c30",
                    "speed": 1,
                    "type": "bomber",
                    "waitTurns": 1
                },
                {
                    "x": 190,
                    "y": 519,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "a5c0b001-0b8e-4503-bdf1-c40e26288787",
                    "speed": 1,
                    "type": "liner",
                    "waitTurns": 1
                },
                {
                    "x": 185,
                    "y": 522,
                    "attack": 999999,
                    "direction": "up",
                    "health": 19,
                    "id": "f0e26291-c143-43eb-80ad-eaaad1bbe5b9",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 2
                },
                {
                    "x": 183,
                    "y": 516,
                    "attack": 43,
                    "direction": "right",
                    "health": 19,
                    "id": "cdb2a3a4-7a44-49d7-99a7-905a3482f13a",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 189,
                    "y": 516,
                    "attack": 31,
                    "direction": "up",
                    "health": 5,
                    "id": "d10002d9-bace-4d08-a66a-8ca1133776c2",
                    "speed": 3,
                    "type": "chaos_knight",
                    "waitTurns": 1
                },
                {
                    "x": 189,
                    "y": 516,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "3988dd5e-22ba-4059-aa64-400b79d8aaec",
                    "speed": 1,
                    "type": "liner",
                    "waitTurns": 1
                },
                {
                    "x": 183,
                    "y": 510,
                    "attack": 43,
                    "direction": "left",
                    "health": 19,
                    "id": "a0315498-908f-4edc-8ae8-de31ef1561bd",
                    "speed": 3,
                    "type": "chaos_knight",
                    "waitTurns": 1
                },
                {
                    "x": 178,
                    "y": 519,
                    "attack": 999999,
                    "direction": "up",
                    "health": 17,
                    "id": "1a4039dc-521b-448f-a1c2-63d01403685e",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 2
                },
                {
                    "x": 178,
                    "y": 519,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "26da5408-3db4-44a0-abc2-ff1eaa9f277a",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 178,
                    "y": 519,
                    "attack": 999999,
                    "direction": "left",
                    "health": 19,
                    "id": "bc9f4175-21ea-4315-966c-796df8811633",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 2
                },
                {
                    "x": 190,
                    "y": 523,
                    "attack": 999999,
                    "direction": "up",
                    "health": 19,
                    "id": "6a78dae3-628d-48db-a74d-1ddf47c46f93",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 1
                },
                {
                    "x": 181,
                    "y": 510,
                    "attack": 43,
                    "direction": "right",
                    "health": 19,
                    "id": "e3241cd1-678b-495f-aef4-3a3b5d810e4c",
                    "speed": 2,
                    "type": "fast",
                    "waitTurns": 1
                },
                {
                    "x": 185,
                    "y": 510,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "752b3c84-c8ae-45f8-bc7f-21a1db2e78f5",
                    "speed": 3,
                    "type": "chaos_knight",
                    "waitTurns": 1
                },
                {
                    "x": 184,
                    "y": 511,
                    "attack": 999999,
                    "direction": "right",
                    "health": 19,
                    "id": "8e4eb59b-cf39-4862-ad6d-278a513a9339",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 1
                },
                {
                    "x": 184,
                    "y": 513,
                    "attack": 999999,
                    "direction": "up",
                    "health": 15,
                    "id": "ef7dad35-6825-43cc-b023-b621ae17b503",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 1
                },
                {
                    "x": 192,
                    "y": 515,
                    "attack": 999999,
                    "direction": "right",
                    "health": 5,
                    "id": "13bd8f47-2eff-480d-8820-63db4634f90b",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 1
                },
                {
                    "x": 182,
                    "y": 510,
                    "attack": 999999,
                    "direction": "right",
                    "health": 19,
                    "id": "4c209943-bcf3-4218-9b09-e26d4efe3e73",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 1
                },
                {
                    "x": 182,
                    "y": 524,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "0ef28a6f-2d1d-47bc-94cf-b4836b6db8d9",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 179,
                    "y": 524,
                    "attack": 999999,
                    "direction": "right",
                    "health": 15,
                    "id": "c6fe739b-e84e-4f78-af87-710c4af6e4a6",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 1
                },
                {
                    "x": 179,
                    "y": 524,
                    "attack": 999999,
                    "direction": "left",
                    "health": 19,
                    "id": "2ab461fe-46cf-414d-afb4-f01c0b2a1aed",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 2
                },
                {
                    "x": 196,
                    "y": 513,
                    "attack": 999999,
                    "direction": "right",
                    "health": 19,
                    "id": "40be4c2f-3e36-460e-9e76-1f6bb3da0b6a",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 2
                },
                {
                    "x": 182,
                    "y": 522,
                    "attack": 999999,
                    "direction": "up",
                    "health": 19,
                    "id": "ebf1b1a4-ff23-4684-8e57-b8e3ad568f4a",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 2
                },
                {
                    "x": 182,
                    "y": 522,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "d0a1ca14-8820-4df1-824a-a7b0a1947f93",
                    "speed": 1,
                    "type": "liner",
                    "waitTurns": 1
                },
                {
                    "x": 186,
                    "y": 519,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "a90e91d6-1d76-4688-8876-b1bac8e3ca46",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 187,
                    "y": 519,
                    "attack": 43,
                    "direction": "right",
                    "health": 19,
                    "id": "95f363b7-3e21-4e5a-9cd6-3956da45728e",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 187,
                    "y": 519,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "d80b6d73-7a12-4f5d-b21e-3a3410d2298e",
                    "speed": 1,
                    "type": "bomber",
                    "waitTurns": 1
                },
                {
                    "x": 187,
                    "y": 522,
                    "attack": 43,
                    "direction": "right",
                    "health": 19,
                    "id": "31302ae4-ac4b-46c7-8340-8a98df0faceb",
                    "speed": 2,
                    "type": "fast",
                    "waitTurns": 1
                },
                {
                    "x": 182,
                    "y": 517,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "74fde8c9-e4b5-4171-aada-15c7f7920515",
                    "speed": 1,
                    "type": "bomber",
                    "waitTurns": 1
                },
                {
                    "x": 183,
                    "y": 517,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "a0ce20f5-881b-41a6-85a6-03694f14e658",
                    "speed": 1,
                    "type": "bomber",
                    "waitTurns": 1
                },
                {
                    "x": 185,
                    "y": 524,
                    "attack": 43,
                    "direction": "right",
                    "health": 19,
                    "id": "9f48ed15-78f8-4d64-a32d-e5f6ce1ca47f",
                    "speed": 1,
                    "type": "normal",
                    "waitTurns": 1
                },
                {
                    "x": 185,
                    "y": 524,
                    "attack": 43,
                    "direction": "up",
                    "health": 19,
                    "id": "138ce5fa-b8fe-4285-8969-3e5714812c25",
                    "speed": 1,
                    "type": "bomber",
                    "waitTurns": 1
                },
                {
                    "x": 194,
                    "y": 519,
                    "attack": 999999,
                    "direction": "left",
                    "health": 19,
                    "id": "37441fa0-7b98-4180-bf46-6eeea0b30b15",
                    "speed": 1,
                    "type": "juggernaut",
                    "waitTurns": 2
                },
                {
                    "x": 189,
                    "y": 513,
                    "attack": 37,
                    "direction": "up",
                    "health": 17,
                    "id": "6a9b6074-6385-4e87-b024-181ad29cb332",
                    "speed": 1,
                    "type": "bomber",
                    "waitTurns": 1
                }
            ]
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
