#!/usr/bin/env python3
"""Запуск VK-бота Ходор и health-check на порту HEALTH_PORT (для nginx)."""

import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

BOT_DIR = Path(__file__).resolve().parent / "bot"
sys.path.insert(0, str(BOT_DIR))


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps(
            {
                "status": "ok",
                "character": "hodor",
                "service": "shablbot-hodor",
            },
            ensure_ascii=False,
        ).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def start_health_server() -> None:
    port = int(os.getenv("HEALTH_PORT", "3010"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Health-check: http://0.0.0.0:{port}/")
    server.serve_forever()


def start_bot() -> None:
    from settings.settings import SETTINGS
    from shablbot import ShablBot

    bot = ShablBot(SETTINGS)
    bot.listen()


def main() -> None:
    os.chdir(BOT_DIR)
    threading.Thread(target=start_health_server, daemon=True).start()
    start_bot()


if __name__ == "__main__":
    main()
