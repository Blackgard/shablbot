#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Создан .env — заполните TOKEN, BOT_CHAT_ID, ADMIN_ID и API-ключи."
  exit 1
fi

mkdir -p data logs

if command -v docker &>/dev/null; then
  docker compose build
  docker compose up -d
  echo "Бот Ходор запущен. Health: http://localhost:3010/"
  docker compose logs -f --tail=50
else
  echo "Docker не найден. Используйте: ./install-systemd.sh"
  exit 1
fi
