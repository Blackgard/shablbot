# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from enum import Enum
from pydantic import BaseModel


# TIME WORK MODELS


class TimeWorkEnum(str, Enum):
    ALL = "ALL"
    CUSTOM = "CUSTOM"
    NIGHT_MSK = "NIGHT_MSK"
    DAY_MSK = "DAY_MSK"


# CHAT SETTING MODELS


class ChatSettingsBodyTimeWork(BaseModel):
    type: TimeWorkEnum
    time_zone: str
    time_from: Optional[str]
    time_to: Optional[str]

class ChatSettingsBody(BaseModel):
    enabled: bool
    time_work: ChatSettingsBodyTimeWork


# COMMAND MODELS


class Commands(BaseModel):
    public: List[str]
    private: List[str]


# PROHABILITY MODELS


class ProbabilityValue(BaseModel):
    common: float = 0.5
    uncommon: float = 0.25
    rare: float = 0.05
    legendary: float = 0.005


# LOGGER CONFIG MODELS


class LoggerConfigHandlers(BaseModel):
    sink: Any
    format: Optional[Any]
    enqueue: Optional[bool]
    serialize: Optional[bool]
    colorize: Optional[bool]

class LoggerConfigLevel(BaseModel):
    name: str
    no: Optional[int]
    icon: Optional[str]
    color: Optional[str]

class LoggerConfig(BaseModel):
    handlers: Optional[List[LoggerConfigHandlers]]
    levels: Optional[List[LoggerConfigLevel]]
    extra: Optional[Dict[str, str]]
    patcher: Optional[Any]
    activation: Optional[List[Tuple[str, bool]]]


# SETTINGS MODELS


class SettingsModel(BaseModel):
    TOKEN: str
    ADMIN_ID: int
    BOT_CHAT_ID: int
    DEBUG_MODE: bool = False
    LOGGER_CONFIG: LoggerConfig

    JOIN_SYMBOL_TEMPLATE: str

    DEFAULT_REACTION_TEMPLATES: List[str]
    DEFAULT_TIME_WORK: TimeWorkEnum = "ALL"
    DEFAULT_TIME_ZONE: str = "Asia/Tomsk"
    #DEFAULT_SIZE_CACHE: int = 128
    DEFAULT_PROBABILITY: ProbabilityValue

    PHRASES_FOLDER: Path
    EXCLUDED_PHRASES: List[str]

    MODULES_FOLDER: str
    ACTIVE_MODULES: List[str]

    TYPE_TIME_WORK: Dict[str, str]
    CHAT_SETTINGS: Dict[str, ChatSettingsBody]

    COMMANDS_FOLDER: str
    ACTIVE_COMMANDS: Commands

    KEYBOARDS_FOLDER: Path
    KEYBOARDS: Dict[str, str]

    IS_SHOW_KEYBOARD_TO_CHAT: bool
