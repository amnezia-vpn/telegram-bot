import subprocess
import ipaddress
import io
import os
import json
import time

from subprocess import Popen, PIPE, STDOUT

WIREGUARD_MAX_ALLOWED_IP = ipaddress.ip_address('10.8.63.254')


def execute_amnezia_command(subcommand: str) -> str:
    return subprocess.check_output([
        "docker", "exec", "amnezia-wireguard", "bash", "-c", subcommand
    ]).decode('utf-8').replace("\n","")


def execute_host_command(subcommand: str) -> str:
    return subprocess.check_output([subcommand]).decode('utf-8').replace("\n","")

def restart_wireguard():
    execute_amnezia_command('wg syncconf wg0 <(wg-quick strip /opt/amnezia/wireguard/wg0.conf)')


NEW_PEER = """

[Peer]
PublicKey = {public_key}
PresharedKey = {preshared_key}
AllowedIPs = {dedicated_ip}
"""


def start() -> None:

    preshared_key = execute_amnezia_command("cat /opt/amnezia/wireguard/wireguard_psk.key")
    server_pub_key = execute_amnezia_command('cat /opt/amnezia/wireguard/wireguard_server_public_key.key')

    peers_to_conf = ""

    # save peers to conf
    f = open("keys.json", "w")
    f.write("{}")
    f.close()

    with open('keys.json', 'w') as db_keys:
        data_keys = {}

        current_ip = ipaddress.ip_address('10.8.1.2')

        while current_ip < WIREGUARD_MAX_ALLOWED_IP :
            current_ip += 1

            private_key = subprocess.check_output(["wg", "genkey"]).decode('utf-8').replace("\n","")

            p = Popen(["wg", "pubkey"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
            public_key = p.communicate(input=private_key.encode())[0].decode('utf-8').replace("\n","")


            peers_to_conf += NEW_PEER.format(
            public_key=public_key,
            preshared_key=preshared_key,
            dedicated_ip=str(current_ip) + "/32",
            )

            data_keys[str(current_ip)] = private_key


        json.dump(data_keys, db_keys, indent = 1)



    # save peers to conf
    f = open("wg_clients.conf", "w")
    f.write(peers_to_conf)
    f.close()

def main() -> None:
    start()


if __name__ == '__main__':
    main()
