import typing as t

from server.settings.components import BASE_DIR
from server.settings.components.wireguard import (
    WIREGUARD_IP_NETWORK,
    WIREGUARD_PSK,
    WIREGUARD_SERVER_IP,
    WIREGUARD_SERVER_PORT,
    WIREGUARD_SERVER_PUB_KEY,
)

__all__ = ["create_wireguard_config"]

WIREGUARD_CONFIG_TEMPLATE: t.Final[
    str
] = """
[Interface]
Address = {associated_ip}
DNS = 1.1.1.1, 1.0.0.1
PrivateKey = {private_key}

[Peer]
PublicKey = {server_pub_key}
PresharedKey = {preshared_key}
AllowedIPs = {allowed_ips},
Endpoint = {wireguard_server_ip}:{wireguard_server_port}
PersistentKeepalive = 25
"""


def create_wireguard_config(associated_ip: str, private_key: str) -> str:
    with open(BASE_DIR.joinpath('allowed-ips.txt'), "r") as f:
        allowed_ips = [ip.strip() for ip in f.readlines()]
        allowed_ips.insert(0, str(WIREGUARD_IP_NETWORK))
        allowed_ips = ", ".join(allowed_ips)

        return WIREGUARD_CONFIG_TEMPLATE.format(
            associated_ip=associated_ip,
            private_key=private_key,
            server_pub_key=WIREGUARD_SERVER_PUB_KEY,
            preshared_key=WIREGUARD_PSK,
            allowed_ips=allowed_ips,
            wireguard_server_ip=WIREGUARD_SERVER_IP,
            wireguard_server_port=WIREGUARD_SERVER_PORT,
        ).strip()
