from server.apps.core.messages import (
    EXHAUSTED_FREE_KEYS_MESSAGE,
    KEY_GENERATED_MESSAGE,
    REGISTERED_USER_MESSAGE,
    UNREGISTERED_USER_MESSAGE,
)
from server.apps.core.models import Key, User
from server.settings.components.telegram import TELEGRAM_BOT_TOKEN
from telebot import TeleBot

bot = TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start_message(message):
    chat_id = message.chat.id
    username = message.chat.username

    user, created = User.objects.get_or_create(
        id=chat_id,
        username=username,
    )

    if created:
        keys = Key.objects.filter(user__isnull=True).exists()
        if not keys:
            return bot.send_message(
                chat_id,
                EXHAUSTED_FREE_KEYS_MESSAGE,
            )

        user.assign_key()
        bot.send_message(chat_id, UNREGISTERED_USER_MESSAGE)
        return bot.send_message(
            chat_id,
            KEY_GENERATED_MESSAGE.format(
                key=user.get_actual_wireguard_key(),
            ),
            parse_mode="Markdown",
        )
    bot.send_message(
        chat_id,
        REGISTERED_USER_MESSAGE.format(
            key=user.get_actual_wireguard_key(),
        ),
        parse_mode="Markdown",
    )
