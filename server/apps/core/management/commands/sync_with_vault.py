import collections

from django.core.management.base import BaseCommand

from server.apps.core.logic.vault import get_vault_client
from server.apps.core.models import Key
from server.settings.components.vault import VAULT_MOUNT_POINT, VAULT_SECRETS_PATH
from server.settings.components.wireguard import WIREGUARD_IP_NETWORK


def get_unassociated_ips():
    """Get unassociated IPs."""
    associated_ips = Key.objects.filter(associated_ip__isnull=False).values_list(
        "associated_ip", flat=True
    )
    # Exclude 10.112.0.0
    ip_network = list(WIREGUARD_IP_NETWORK)[1:]
    return collections.deque(
        sorted([ip for ip in ip_network if str(ip) not in associated_ips])
    )


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = get_vault_client()
        ips = get_unassociated_ips()

        secrets = client.secrets.kv.v2.list_secrets(
            VAULT_SECRETS_PATH, VAULT_MOUNT_POINT
        )
        filenames = secrets["data"]["keys"]

        for filename in sorted(filenames, key=int):
            # Get first unassociated IP
            ip = ips.popleft()

            try:
                Key.objects.get(id=filename)
            except Key.DoesNotExist:
                Key.objects.create(
                    id=filename,
                    associated_ip=str(ip),
                )
