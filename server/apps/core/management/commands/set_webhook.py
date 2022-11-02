from django.core.management.base import BaseCommand

from server.apps.core.bot import bot
from server.settings.components.telegram import TELEGRAM_WEBHOOK_URI


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot.remove_webhook()
        bot.set_webhook(f"{TELEGRAM_WEBHOOK_URI}/bot/")
