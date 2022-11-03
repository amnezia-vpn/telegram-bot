FROM python:3.10-slim-bullseye
RUN pip install poetry==1.2.2
WORKDIR /bot
COPY . .
RUN chmod 755 docker/dev/bot.entrypoint.sh
RUN poetry install
ENTRYPOINT docker/dev/bot.entrypoint.sh

ENV BOT_LISTEN_ADDR=0.0.0.0
ENV BOT_LISTEN_PORT=8000
