import requests

UNBLOCK_IPS_LIST_URL = 'https://raw.githubusercontent.com/amnezia-vpn/unblock-lists-ru/master/to_ru.csv'

response = requests.get(UNBLOCK_IPS_LIST_URL)
rows = response.content.decode('utf-8')

with open('allowed-ips.txt', 'w') as f:
    f.write(rows)
