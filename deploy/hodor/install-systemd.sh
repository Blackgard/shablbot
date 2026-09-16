#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INSTALL_DIR="${INSTALL_DIR:-/opt/shablbot-hodor}"
SERVICE_USER="${SERVICE_USER:-$USER}"

if [[ ! -f "$SCRIPT_DIR/.env" ]]; then
  cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
  echo "Заполните $SCRIPT_DIR/.env и запустите скрипт снова."
  exit 1
fi

sudo mkdir -p "$INSTALL_DIR"
sudo rsync -a --delete \
  "$REPO_ROOT/shablbot" \
  "$REPO_ROOT/setup.py" \
  "$REPO_ROOT/pyproject.toml" \
  "$REPO_ROOT/requirements.txt" \
  "$SCRIPT_DIR/" \
  "$INSTALL_DIR/"

sudo cp "$SCRIPT_DIR/.env" "$INSTALL_DIR/.env"
sudo mkdir -p "$INSTALL_DIR/data" "$INSTALL_DIR/logs"

sudo python3 -m venv "$INSTALL_DIR/venv"
sudo "$INSTALL_DIR/venv/bin/pip" install -U pip
sudo "$INSTALL_DIR/venv/bin/pip" install -e "$INSTALL_DIR" -r "$INSTALL_DIR/requirements.txt"

sudo tee /etc/systemd/system/shablbot-hodor.service >/dev/null <<EOF
[Unit]
Description=ShablBot Hodor VK Bot
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$INSTALL_DIR
EnvironmentFile=$INSTALL_DIR/.env
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/run.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now shablbot-hodor
echo "Сервис shablbot-hodor запущен. Проверка: curl http://127.0.0.1:3010/"
