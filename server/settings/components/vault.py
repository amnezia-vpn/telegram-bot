from server.settings.components import config

VAULT_ADDR = config("VAULT_ADDR")
VAULT_TOKEN = config("VAULT_TOKEN")
VAULT_NAMESPACE = config("VAULT_NAMESPACE", default=None)