# dats-defense
Big Data Small Memory

## Requirements

- Python 3.12

## Setup

.env file
```bash
# .env
TEAM_TOKEN=
```

```bash
poetry install
```

## Run

```bash
poetry run python src/main.py
```

```bash
poetry run python src/main.py --command-test
```

```bash
# /mockgame
poetry run uvicorn app:app
```
