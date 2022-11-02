## Amnezia Bot

Amnezia Bot is a bot that allows you to generate WireGuard keys to use Amnezia VPN.

## Prerequisites

You will need:

- `python3.10` (see `pyproject.toml` for full version)
- `postgresql` with version `13` or higher
- [`poetry`](https://github.com/python-poetry/poetry) with version `1.2.2` or higher

When developing locally, we are recommending to use:

- [`editorconfig`](http://editorconfig.org/) plugin (**required**)
- [`ngrok`](https://ngrok.com/download) with version `3.1.0`.


## Getting started

First of all, you have to create `.env` file and fill in all the secrets and environment variables (see `.env.template`).

- Use [@BotFather](https://t.me/BotFather) to obtain `TELEGRAM_BOT_TOKEN`.
- Use `ngrok` to expose your local server through `HTTPS` to fill in (`TELEGRAM_WEBHOOK_URI`).

Next, you have to install all the dependencies:

```bash
poetry install
```

Then you have to create database and run migrations:

```bash
poetry run python manage.py migrate
```

Now you can set webhook and run the bot:

```bash
poetry run python manage.py set_webhook
poetry run python manage.py runserver
```
