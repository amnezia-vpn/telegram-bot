from django.db import models

from server.apps.core.logic.vault import get_vault_client
from server.settings.components.vault import VAULT_MOUNT_POINT, VAULT_SECRETS_PATH


class TimestampMixin(models.Model):
    """Abstract model to automatically managing timestamps."""

    create_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    class Meta:
        abstract = True


class Key(TimestampMixin):
    id = models.PositiveBigIntegerField(
        verbose_name="WireGuard Key ID",
        unique=True,
        db_index=True,
        primary_key=True,
    )
    associated_ip = models.GenericIPAddressField(
        verbose_name="Associated IP",
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"Key <{self.id}>"

    def inquire_actual_wireguard_key(self):
        """Inquire actual WireGuard key from Vault."""
        try:

            client = get_vault_client()
            response = client.secrets.kv.v2.read_secret(
                f"{VAULT_SECRETS_PATH}/{self.id}", VAULT_MOUNT_POINT
            )
            return response["data"]["data"]["private"]
        except KeyError:
            return None

    class Meta:
        db_table = "key"
        verbose_name = "Key"
        verbose_name_plural = "Keys"


class User(TimestampMixin):
    id = models.PositiveBigIntegerField(
        verbose_name="User ID", unique=True, db_index=True, primary_key=True
    )
    username = models.CharField(
        verbose_name="Username",
        null=False,
        blank=False,
        max_length=255,
    )
    key = models.OneToOneField(
        Key,
        on_delete=models.CASCADE,
        verbose_name="Key",
        null=True,
        blank=False,
        related_name="user",
    )

    class Meta:
        db_table = "tg_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"User <{self.id}>"

    def assign_key(self):
        key = Key.objects.filter(user__isnull=True).first()

        if not key:
            return False

        self.key = key
        self.save()

        return True

    def get_actual_wireguard_config(self):
        """Get an actual WireGuard key from Vault server."""
        return self.key.inquire_actual_wireguard_key()
