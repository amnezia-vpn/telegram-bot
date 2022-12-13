#! /bin/sh
set +x

echo 'fetch_allowed_ips' && poetry run python ./fetch_allowed_ips.py && \
echo 'migrate' && poetry run ./manage.py migrate && \
echo 'collectstatistic' && poetry run ./manage.py collectstatic --noinput && \
echo 'set_webhook' && poetry run ./manage.py set_webhook && \
echo 'start app server' && gunicorn --workers=2 --env=DJANGO_SETTINGS_MODULE=server.settings --bind "${BOT_LISTEN_ADDR}:${BOT_LISTEN_PORT}" server.wsgi
