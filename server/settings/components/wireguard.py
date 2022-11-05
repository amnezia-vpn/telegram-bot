from ipaddress import IPv4Network

from server.settings.components import config

WIREGUARD_IP_NETWORK = IPv4Network("10.112.0.0/16")

WIREGUARD_PSK = config("WIREGUARD_PSK")
WIREGUARD_SERVER_PUB_KEY = config("WIREGUARD_SERVER_PUB_KEY")
