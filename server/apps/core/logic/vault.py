import hvac

from server.settings.components.vault import VAULT_ADDR, VAULT_TOKEN


def get_vault_client():
    client = hvac.Client(
        url=VAULT_ADDR,
        token=VAULT_TOKEN,
    )
    authenticated = client.is_authenticated()

    if authenticated:
        return client

    raise ConnectionError("Vault is not authenticated.")
