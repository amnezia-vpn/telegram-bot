from telebot import TeleBot

from server.apps.core.logic.messages import (
    BOT_ERROR_ON_GETTING_CONFIG_MESSAGE,
    BOT_EXHAUSTED_UNASIGNED_KEYS_MESSAGE,
    BOT_NEW_USER_HELLO_MESSAGE,
    BOT_USER_ALREADY_EXISTS_MESSAGE,
    BOT_WIREGUARD_CONFIG_GENERATED_MESSAGE,
)
from server.apps.core.models import Key, User
from server.settings.components.telegram import TELEGRAM_BOT_TOKEN

bot = TeleBot(TELEGRAM_BOT_TOKEN)


# TODO: Decouple this function to different commands
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
            # If there are no free keys,
            # we can't generate a config for the user.
            return bot.send_message(
                chat_id,
                BOT_EXHAUSTED_UNASIGNED_KEYS_MESSAGE,
            )

        user.assign_key()
        bot.send_message(chat_id, BOT_NEW_USER_HELLO_MESSAGE)
        bot.send_message(
            chat_id,
            BOT_WIREGUARD_CONFIG_GENERATED_MESSAGE,
            parse_mode="Markdown",
        )
        bot.send_document(
            chat_id,
            document=user.get_wireguard_config_file(),
            visible_file_name="wg10.conf",
        )
    else:
        try:
            bot.send_message(
                chat_id,
                BOT_USER_ALREADY_EXISTS_MESSAGE,
                parse_mode="Markdown",
            )
            bot.send_document(
                chat_id,
                document=user.get_wireguard_config_file(),
                visible_file_name="wg10.conf",
            )
        except ValueError:
            bot.send_message(chat_id, BOT_ERROR_ON_GETTING_CONFIG_MESSAGE)
