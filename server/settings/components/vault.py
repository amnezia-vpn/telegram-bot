from server.settings.components import config

VAULT_URL = config("VAULT_URL")
VAULT_TOKEN = config("VAULT_TOKEN")
VAULT_NAMESPACE = config("VAULT_NAMESPACE", default=None)
