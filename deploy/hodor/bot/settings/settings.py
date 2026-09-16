"""
Настройки бота Ходор (Игра престолов).
Секреты — только в .env, остальное уже настроено.
"""
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from shablbot.settings import SettingsModel
from shablbot.core.ai import build_ai_settings_from_env

# .env лежит в deploy/hodor/.env
load_dotenv(Path(__file__).resolve().parents[2] / ".env")
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

TOKEN = os.getenv("TOKEN")
BOT_CHAT_ID = os.getenv("BOT_CHAT_ID")
ADMIN_ID = os.getenv("ADMIN_ID")

# Имя бота в беседах — обращение к Ходору
DEFAULT_REACTION_TEMPLATES = (r"ходор", r"hodor", r"бот")

JOIN_SYMBOL_TEMPLATE = r"\s.*?"

DEFAULT_TIME_WORK = "ALL"
DEFAULT_TIME_ZONE = "Europe/Moscow"
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

MODULES_FOLDER = "modules"
ACTIVE_MODULES = []

KEYBOARDS_FOLDER = BASE_DIR.joinpath("keyboards")
KEYBOARDS = {
    "default": "default.json",
    "clear": "clear.json",
}
IS_SHOW_KEYBOARD_TO_CHAT = False

COMMANDS_FOLDER = "commands"
ACTIVE_COMMANDS = {
    "public": ["chat_bot_off", "chat_bot_on", "chat_show_statistics"],
    "private": ["show_id_active_chats"],
}

PHRASES_FOLDER = BASE_DIR.joinpath("phrases")
EXCLUDED_PHRASES = []

TYPE_TIME_WORK = {
    "ALL": DEFAULT_TIME_ZONE,
    "CUSTOM": DEFAULT_TIME_ZONE,
    "NIGHT_MSK": "Europe/Moscow",
    "DAY_MSK": "Europe/Moscow",
}

CHAT_SETTINGS_FILE = BASE_DIR.joinpath("data", "chat_settings.json")
CHAT_SETTINGS_PERSIST = True
CHAT_SETTINGS = {}

AI_SETTINGS = build_ai_settings_from_env()

DEFAULT_PROBABILITY = {
    "common": 0.7,
    "uncommon": 0.2,
    "rare": 0.08,
    "legendary": 0.02,
}

LOGGER_CONFIG = {
    "handlers": [
        dict(
            sink="stderr",
            colorize=True,
            format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{level}</level> | {message}",
        ),
        dict(
            sink=str(BASE_DIR.joinpath("logs", "hodor.log")),
            format="{time} | {level} | {name}:{function}:{line} | {message}",
        ),
    ],
}

SETTINGS = SettingsModel(
    TOKEN=TOKEN,
    ADMIN_ID=ADMIN_ID,
    BOT_CHAT_ID=BOT_CHAT_ID,
    DEBUG_MODE=DEBUG_MODE,
    LOGGER_CONFIG=LOGGER_CONFIG,
    JOIN_SYMBOL_TEMPLATE=JOIN_SYMBOL_TEMPLATE,
    TYPE_TIME_WORK=TYPE_TIME_WORK,
    DEFAULT_REACTION_TEMPLATES=DEFAULT_REACTION_TEMPLATES,
    DEFAULT_TIME_WORK=DEFAULT_TIME_WORK,
    DEFAULT_TIME_ZONE=DEFAULT_TIME_ZONE,
    DEFAULT_PROBABILITY=DEFAULT_PROBABILITY,
    CHAT_SETTINGS=CHAT_SETTINGS,
    CHAT_SETTINGS_FILE=CHAT_SETTINGS_FILE,
    CHAT_SETTINGS_PERSIST=CHAT_SETTINGS_PERSIST,
    PHRASES_FOLDER=PHRASES_FOLDER,
    EXCLUDED_PHRASES=EXCLUDED_PHRASES,
    MODULES_FOLDER=MODULES_FOLDER,
    ACTIVE_MODULES=ACTIVE_MODULES,
    COMMANDS_FOLDER=COMMANDS_FOLDER,
    ACTIVE_COMMANDS=ACTIVE_COMMANDS,
    KEYBOARDS_FOLDER=KEYBOARDS_FOLDER,
    KEYBOARDS=KEYBOARDS,
    IS_SHOW_KEYBOARD_TO_CHAT=IS_SHOW_KEYBOARD_TO_CHAT,
    AI_SETTINGS=AI_SETTINGS,
)
