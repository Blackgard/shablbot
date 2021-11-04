"""
Файл с настройками бота, регулировка данного файла позволяет создать своего уникального бота.
"""
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from .settings_model import SettingsModel

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# Токен хранится в виде строки (генерируется в паблике).
# Пример: r"1234566789908798689764867293876243987" (str)
TOKEN = os.getenv("TOKEN")

# Id паблика бота хранится в виде числа.
# Пример: 123456789 (int)
BOT_CHAT_ID = os.getenv("BOT_CHAT_ID")

# Шаблоны слов, на который бот должен всегда давать какой-либо ответ.
# Лучше всего сюда поставить имя бота.
DEFAULT_REACTION_TEMPLATES = (r"бот",)

# Шаблон слова или пробела, с помощью которого будет происходить соединение с другими шаблонами.
# По умолчанию пробел.
JOIN_SYMBOL_TEMPLATE = r"\s.*?"

# Id администаратора бота.
# Пример: 123456789 (int)
ADMIN_ID = os.getenv("ADMIN_ID")

# Значение времени работы бота, которое устанавливается по умолчанию для всех чатов.
# (Не указанных в settings_chat)
DEFAULT_TIME_WORK = "ALL"

# Временная зона бота, в рамках которой он будет работать по умолчанию.
# Список доступных временных зон:
#   [1] https://gist.github.com/JellyWX/913dfc8b63d45192ad6cb54c829324ee
DEFAULT_TIME_ZONE = "Asia/Tomsk"

# Режим отладки включен если True, и отключен если False.
DEBUG_MODE = True

# Размер буфера кеша бота. По умолчанию - 128. / Времено отключено
# DEFAULT_SIZE_CACHE = 128

# Папка для модулей бота
MODULES_FOLDER = "modules"

# Модули дополнения функциональной возможности бота.
# Имеется возможность разрабатывать индивидуальные модули , выполненные в определенном формате.
# (Смотрите пример модуля "flip_and_roll.py")
ACTIVE_MODULES = ["games.flip_and_roll"]

# Папка для клавиатур бота
KEYBOARDS_FOLDER = BASE_DIR.joinpath("keyboards")

# Список клавиатур доступных для бота
KEYBOARDS = {
    "default": "default.json",
    "clear": "clear.json",
}

# Показывать ли клавиатуру в беседах и группах
IS_SHOW_KEYBOARD_TO_CHAT = False

# Папка для команд бота
COMMANDS_FOLDER = "commands"

# Список команд
# Публичные команды доступны всем пользователям, приватные - только администратору.
ACTIVE_COMMANDS = {
    "public": ["chat_bot_off", "chat_bot_on", "chat_show_statistics"],
    "private": ["show_id_active_chats"]
}

# Папка для фраз бота
PHRASES_FOLDER = BASE_DIR.joinpath("phrases")

# Исключенные фразы для ответа
EXCLUDED_PHRASES = []

# Варианты времени работы бота с учетом временной зоны.
TYPE_TIME_WORK = {
    "ALL": DEFAULT_TIME_ZONE,
    "CUSTOM": DEFAULT_TIME_ZONE,
    "NIGHT_MSK": "Europe/Moscow",
    "DAY_MSK": "Europe/Moscow",
}

# Настройки времени работы конкретного чата
CHAT_SETTINGS = {
    123456789: {
        "enabled": True,
        "time_work": {
            "type": "ALL",
            "time_zone": TYPE_TIME_WORK.get("ALL"),
            "time_from": "00:00",  # Optional
            "time_to": "23:59",  # Optional
        },
    },
    123456780: {
        "enabled": True,
        "time_work": {
            "type": "ALL",
            "time_zone": TYPE_TIME_WORK.get("ALL"),
            "time_from": "00:00",  # Optional
            "time_to": "23:59",  # Optional
        },
    },
}

# Шанс выпадения ответа бота для каждого из типов редкости
DEFAULT_PROBABILITY = {
    "common": 0.5,
    "uncommon": 0.25,
    "rare": 0.05,
    "legendary": 0.005,
}

# Настройки для логгера бота, конфиг настраивается исходя из конфига loguru:
#   [2] https://github.com/Delgan/loguru
LOGGER_CONFIG = {
    "handlers": [
        dict(
            sink=sys.stderr,
            colorize=True,
            format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{level}</level> | {message}"
        ),
        dict(
            sink=open("main.log", mode="w", encoding="UTF-8"),
            format="{time} | {level} | {name}:{function}:{line} | {message}"
        )
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

    PHRASES_FOLDER=PHRASES_FOLDER,
    EXCLUDED_PHRASES=EXCLUDED_PHRASES,

    MODULES_FOLDER=MODULES_FOLDER,
    ACTIVE_MODULES=ACTIVE_MODULES,

    COMMANDS_FOLDER=COMMANDS_FOLDER,
    ACTIVE_COMMANDS=ACTIVE_COMMANDS,

    KEYBOARDS_FOLDER=KEYBOARDS_FOLDER,
    KEYBOARDS=KEYBOARDS,
    IS_SHOW_KEYBOARD_TO_CHAT=IS_SHOW_KEYBOARD_TO_CHAT,

)
