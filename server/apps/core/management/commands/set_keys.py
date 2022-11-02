from django.core.management.base import BaseCommand

from server.apps.core.models import Key  # noqa


class Command(BaseCommand):
    def handle(self, *args, **options):
        raise NotImplementedError
