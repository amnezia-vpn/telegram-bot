import subprocess
import ipaddress
import io
import os
import json
import time

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update,
                      ReplyKeyboardMarkup, KeyboardButton)
from telegram.ext import Updater, CommandHandler, CallbackContext


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WIREGUARD_MAX_ALLOWED_IP = ipaddress.ip_address('10.63.255.254')

servers = {}
data_keys = {}


def get_new_ip():
    previous_ip_str = ""
    # read
    with open('last_ip.conf', 'r') as file:
        previous_ip_str = file.read().replace('\n', '')

    current_ip = ipaddress.ip_address(previous_ip_str) + 1
    if current_ip > WIREGUARD_MAX_ALLOWED_IP:
        raise ValueError('The limit of allowed IPs has been exceeded.')

    # save peers to conf
    f = open("last_ip.conf", "w")
    f.write(str(current_ip))
    f.close()

    return str(current_ip)



FINAL_CONFIG = """
[Interface]
Address = {dedicated_ip}/32
DNS = 1.1.1.1, 1.0.0.1
PrivateKey = {private_key}

[Peer]
PublicKey = {server_pub_key}
PresharedKey = {preshared_key}
AllowedIPs = {vpn_networks}
Endpoint = {server_ip}:{server_port}
PersistentKeepalive = 25
""".strip()

def gen_user_config(dedicated_ip, private_key, server_pub_key, preshared_key, server_ip, server_port):
    return FINAL_CONFIG.format(
                dedicated_ip=dedicated_ip,
                private_key=private_key,
                server_pub_key=server_pub_key,
                preshared_key=preshared_key,
                server_ip=server_ip,
                server_port=server_port
            )

def get_config_for_user(user_id):
    with open('db2.json', 'r') as db_file:
        data = json.load(db_file)

        user_id_str = "id" + str(user_id)
        if user_id_str in data:
            return data[user_id_str]
    return


def add_user_to_database(user_name, user_id, dedicated_ip, private_key):
    with open('db2.json', 'r') as db2:
        data = json.load(db2)
        with open('db2.json', 'w') as db2:
            user_cfg = {}
            user_cfg["n"] = user_name
            user_cfg["i"] = dedicated_ip
            user_cfg["c"] = private_key
            user_cfg["s"] = "s3"
            user_cfg["t"] = round(time.time())

            data["id" + str(user_id)] = user_cfg
            json.dump(data, db2, indent = 1)

def is_subscribed(context, chat_id, user_id):
    # dont forget add bot to target chat as admin to have access to members list
    try:
        user = context.bot.getChatMember(chat_id, user_id)

        if user["status"] in ["administrator", "creator", "member"]:
            return True
        else:
            return False
    except:
        return False

def start(update: Update, context: CallbackContext) -> None:

    user_id = update.effective_user.id
    user_name = str(update.effective_user.username)
    user_json_config = get_config_for_user(user_id)

    if is_subscribed(context, "@amnezia_vpn_news_ru", user_id):
        update.message.reply_text(f"Отлично, вы подписаны на канал @amnezia_vpn_news_ru\n C 05.08.2022 доступ к VPN включен только для подписчиков.")
    else:
        update.message.reply_text(f"Для использования бесплатного AmneziaVPN необходимо быть подписанным на наш новостной канал @amnezia_vpn_news_ru\n\nЭтот канал используется только для оповещения о новостях AmneziaVPN, рекламы не будет. После того, как подпишитесь - запустите бота заново, он выдаст конфиг для подключния и инструкцию.")
        return

    """
    reply_keyboard = InlineKeyboardMarkup(
           inline_keyboard=[
               [InlineKeyboardButton('Request new server', callback_data='renew')],
           ],
       )
    update.message.reply_text(text="Request new server", reply_markup=reply_keyboard)
    """

    if user_json_config is not None:
        print ("Existing user: " + str(user_id) + " : " + str(user_name))
        update.message.reply_text(f"Вот ваш конфиг:")

        serv_name = user_json_config["s"]

        serv = servers[serv_name]
        server_ip = serv["ip"]
        server_port = serv["port"]
        psk_key = serv["psk_key"]
        server_public_key = serv["public_key"]

        dedicated_ip=user_json_config["i"]
        user_private_key=user_json_config["c"]

        user_wg_config = gen_user_config(dedicated_ip, user_private_key, server_public_key, psk_key, server_ip, server_port)

        context.bot.sendDocument(
            document=io.StringIO(user_wg_config),
            chat_id=update.message.chat_id,
            filename='wg10.conf',
        )

        update.message.reply_text(f"""Для использования конфига необходимо установить WireGuard VPN клиент, и загрузить в него этот конфиг.
		На присланном файле конфига нажимаете "Сохранить в загрузки", далее запускаете программу WireGuard, нажимаете иконку добавить (иконка "+"), выбираете файл wg10.conf (он сохранится в загрузки в папку Telegram), и всё готово, включаете, и можно работать!
		Ссылка на инсталляторы для всех устройств тут ->
        https://www.wireguard.com/install/
        """)
    else:
        print ("New user: " + str(user_id) + " : " + str(user_name))
        update.message.reply_text("Запускаем процесс генерации конфига...")

        serv = servers["s3"]
        server_ip = serv["ip"]
        server_port = serv["port"]
        psk_key = serv["psk_key"]
        server_public_key = serv["public_key"]


        dedicated_ip = get_new_ip()
        user_private_key=data_keys[dedicated_ip]


        new_user_config = gen_user_config(dedicated_ip, user_private_key, server_public_key, psk_key, server_ip, server_port)

        add_user_to_database(user_name, user_id, dedicated_ip, user_private_key)
        update.message.reply_text(f"Мы сгенерировали для вас конфиг, {user_name}:")
        context.bot.sendDocument(
            document=io.StringIO(new_user_config),
            chat_id=update.message.chat_id,
            filename='wg10.conf',
        )
		
        update.message.reply_text("Внимание! Не делитесь с конфигом ни с кем, он работает только для одного пользователя! Вы можете загрузить этот конфиг на несколько своих устройств, но одновременно работать сможет только одно. Активация VPN профиля на сервере может занять до 5 минут после генерации ключей.")

        update.message.reply_text(f"""Для использования конфига необходимо установить WireGuard VPN клиент, и загрузить в него этот конфиг.
		На присланном файле конфига нажимаете "Сохранить в загрузки", далее запускаете программу WireGuard, нажимаете иконку добавить (иконка "+"), выбираете файл wg10.conf, (он сохранится в загрузки в папку Telegram), и всё готово, включаете, и можно работать!
		Ссылка на инсталляторы для всех устройств тут ->
        https://www.wireguard.com/install/
        """)

        update.message.reply_text(f"""Список доступных через этот VPN сервисов:
        Instagram, Facebook, Twitter, LinkedIn, Meduza и другие СМИ
        """)

def main() -> None:

    global servers
    global data_keys

    # read servers json
    with open('servers.json', 'r') as db_servers:
        servers = json.load(db_servers)

    # read servers json
    with open('keys.json', 'r') as db_keys:
         data_keys = json.load(db_keys)

    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
