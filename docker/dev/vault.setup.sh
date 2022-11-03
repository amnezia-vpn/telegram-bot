#! /bin/sh

set -eux

export VAULT_ADDR='http://localhost:8200/'
export VAULT_TOKEN="$VAULT_DEV_ROOT_TOKEN_ID"

sleep 3

vault secrets enable -path=vpn -version=2 kv
cat << 'EOF' | vault policy write vpn-keys-ro -
# vpn-keys-ro
#
# Allow Read-only access to client VPN private keys
#
path "vpn/*" {
  capabilities = ["read", "list"]
}
EOF
vault token create -id="$VAULT_DEV_APP_TOKEN_ID" -period=786h -orphan -renewable -policy=vpn-keys-ro

for I in `seq $VAULT_WG_KEYS_COUNT` ; do
    vault kv put -mount=vpn "keys/$I" private="$(wg genkey)"
done

touch /tmp/configured
