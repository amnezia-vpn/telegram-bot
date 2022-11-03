#! /bin/sh
set +x

poetry run ./manage.py migrate && \
poetry run ./manage.py collectstatic --noinput && \
poetry run ./manage.py set_webhook && \
gunicorn --workers=2 --env=DJANGO_SETTINGS_MODULE=server.settings server.wsgi :"${BOT_LISTEN_PORT}"
