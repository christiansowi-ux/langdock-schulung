#!/usr/bin/env bash
# Arbeitshefte auf den Quint-VPS bringen: public/ neu bauen lassen (python _quellen/build.py --web), dann
#   bash ops/deploy.sh
# Laedt den Ordner (ohne node_modules) in EINER SSH-Verbindung hoch und baut den Container neu.
set -euo pipefail
cd "$(dirname "$0")/.."
SERVER="${SERVER:-root@212.227.85.113}"
KEY="${KEY:-$HOME/.ssh/id_ed25519}"
STACK=/opt/stacks/langdock-hefte
URL="${URL:-https://quint-games.de/hefte}"

test -f public/manifest.json || { echo "public/manifest.json fehlt – erst: python ../_quellen/build.py --web"; exit 1; }
test -f .env || { echo ".env fehlt (DOZENT_PASSWORT, COOKIE_SECRET) – siehe README"; exit 1; }

tar --exclude=node_modules --exclude=ops --exclude='*.log' -czf - Dockerfile docker-compose.yml package.json server.mjs public .env \
  $(test -f package-lock.json && echo package-lock.json) \
| ssh -i "$KEY" -o BatchMode=yes "$SERVER" "set -e; mkdir -p $STACK/data; cd $STACK; rm -rf public; tar -xzf -; chown root:root .env; chmod 600 .env; chown 1000:1000 data; docker compose up -d --build; docker image prune -f >/dev/null"

echo "Warte auf den Container ..."
for i in $(seq 1 30); do
  if curl -fsS "$URL/healthz" >/dev/null 2>&1; then echo "OK: $URL/"; exit 0; fi
  sleep 2
done
echo "Healthcheck nicht erreichbar: $URL/healthz"; exit 1
