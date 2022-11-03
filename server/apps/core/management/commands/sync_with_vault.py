import hvac
from django.core.management.base import BaseCommand

from server.apps.core.models import Key  # noqa
from server.settings.components.vault import VAULT_NAMESPACE, VAULT_TOKEN, VAULT_URL


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = hvac.Client(
            url=VAULT_URL,
            token=VAULT_TOKEN,
            namespace=VAULT_NAMESPACE,
        )
        authenticated = client.is_authenticated()

        if authenticated:
            print("Vault is authenticated")
