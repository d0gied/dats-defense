FROM python:3.12-slim as builder

ARG SERVICE_PATH

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install poetry

COPY $SERVICE_PATH/pyproject.toml $SERVICE_PATH/poetry.lock ./
RUN poetry exåport -f requirements.txt --output requirements.txt --without=local
RUN poetry export -f requirements.txt --output requirements-local.txt --only=local

FROM python:3.12-slim as runtime

WORKDIR /app

COPY --from=builder /app/requirements.txt ./
COPY --from=builder /app/requirements-local.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/$SERVICE_PATH
WORKDIR /app/$SERVICE_PATH

COPY ./libs /app/libs
RUN pip install --no-cache-dir -r requirements-local.txt

COPY $SERVICE_PATH /app/$SERVICE_PATH

RUN chmod +x ntrypoint.sh
CMD ["bash", "entrypoint.sh"]
