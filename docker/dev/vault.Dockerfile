FROM vault:1.11.0

RUN apk update && apk add wireguard-tools
RUN apk add --no-cache wireguard-tools
COPY ./docker/dev/vault.setup.sh /usr/local/bin/setup.sh
RUN chmod 755 /usr/local/bin/setup.sh
RUN sed -i '/exec "\$@"/d' /usr/local/bin/docker-entrypoint.sh && \
    echo 'nohup /usr/local/bin/setup.sh &' >> /usr/local/bin/docker-entrypoint.sh && \
    echo 'exec "$@"' >> /usr/local/bin/docker-entrypoint.sh

ENV VAULT_WG_KEYS_COUNT=10
ENV VAULT_DEV_APP_TOKEN_ID=mysecretvaultbottoken
