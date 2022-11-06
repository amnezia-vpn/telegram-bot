FROM python:3.10-slim-bullseye

ENV PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.2.2 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on


RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /bot
COPY pyproject.toml poetry.lock* .

# No need to create a virtualenv, the env is isolated anyway
RUN poetry config virtualenvs.create false  \
    && poetry install --no-interaction --no-ansi

COPY . .

ENTRYPOINT docker/dev/bot.entrypoint.sh

ENV BOT_LISTEN_ADDR=0.0.0.0
ENV BOT_LISTEN_PORT=8000
