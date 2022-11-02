UNREGISTERED_USER_MESSAGE = """
Привет! Это бот Amnezia VPN.

Сейчас мы сгенерируем для вас ключ WireGuard и привяжем его к вашему Telegram аккаунту.
"""

KEY_GENERATED_MESSAGE = """
Скопируй его и вставь в настройки WireGuard на своем устройстве.

Вот ваш ключ:

`{key}`
"""

REGISTERED_USER_MESSAGE = """
Вы уже зарегистрированы в системе.

Ваш WireGuard ключ:

`{key}`
"""

EXHAUSTED_FREE_KEYS_MESSAGE = """
К сожалению, мы не можем сгенерировать для вас ключ, так как все ключи уже заняты.

Свяжитесь с нами для получения дополнительных ключей: @amnezia_vpn
"""
