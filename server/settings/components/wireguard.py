from ipaddress import IPv4Network

from server.settings.components import config

WIREGUARD_PSK = config("WIREGUARD_PSK")
WIREGUARD_SERVER_IP = config("WIREGUARD_SERVER_IP", cast=str)
WIREGUARD_SERVER_PORT = config("WIREGUARD_SERVER_PORT", cast=int)
WIREGUARD_SERVER_PUB_KEY = config("WIREGUARD_SERVER_PUB_KEY")
WIREGUARD_IP_NETWORK = config(
    "WIREGUARD_IP_NETWORK", cast=IPv4Network, default=IPv4Network("10.112.0.0/16")
)
