import hvac
from django.core.management.base import BaseCommand

from server.apps.core.models import Key  # noqa
from server.settings.components.vault import VAULT_TOKEN, VAULT_ADDR


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = hvac.Client(
            url=VAULT_ADDR,
            token=VAULT_TOKEN,
        )
        authenticated = client.is_authenticated()

        if authenticated:
            print("Vault is authenticated")
