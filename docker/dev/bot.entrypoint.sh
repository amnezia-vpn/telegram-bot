#! /bin/sh
set +x

poetry run ./manage.py migrate && \
poetry run ./manage.py set_webhook && \
exec poetry run python manage.py runserver "${BOT_LISTEN_ADDR}:${BOT_LISTEN_PORT}"
