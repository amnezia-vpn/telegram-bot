from django.core.management.base import BaseCommand, CommandError

from server.settings.components.vault import VAULT_ADDR, VAULT_TOKEN

from hvac.adapters import RawAdapter
from hvac.api.auth_methods import Token

class Command(BaseCommand):
    def handle(self, *args, **options):
        adapter = RawAdapter(
                base_uri=VAULT_ADDR,
                token=VAULT_TOKEN,
        )
        token = Token(adapter)

        try:
            resp = token.renew_self()
        except Exception as e:
            raise CommandError(str(e))

        self.stdout.write(self.style.SUCCESS('Token successfully renewed'))
