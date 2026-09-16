# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Literal

from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator


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
    time_from: Optional[str] = None
    time_to: Optional[str] = None


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
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sink: Any
    format: Optional[Any] = None
    enqueue: Optional[bool] = None
    serialize: Optional[bool] = None
    colorize: Optional[bool] = None


class LoggerConfigLevel(BaseModel):
    name: str
    no: Optional[int] = None
    icon: Optional[str] = None
    color: Optional[str] = None


class LoggerConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    handlers: Optional[List[LoggerConfigHandlers]] = None
    levels: Optional[List[LoggerConfigLevel]] = None
    extra: Optional[Dict[str, str]] = None
    patcher: Optional[Any] = None
    activation: Optional[List[Tuple[str, bool]]] = None


# AI MODELS


class AISettings(BaseModel):
    """Активный AI-провайдер и модель (настраиваются через .env)."""

    enabled: bool = False
    mode: Literal["module", "standalone"] = "module"
    provider: Literal["openrouter", "polza"] = "openrouter"
    model: str = "openai/gpt-4o-mini"
    api_key: str = ""
    base_url: str
    system_prompt: str = (
        "Ты дружелюбный ассистент VK-бота. Отвечай кратко, понятно и по-русски."
    )
    max_tokens: int = 1024
    temperature: float = 0.7
    history_limit: int = 10
    timeout: float = 60.0
    http_referer: Optional[str] = None
    site_title: Optional[str] = "ShablBot"

    @property
    def is_configured(self) -> bool:
        return self.enabled and bool(self.api_key.strip()) and bool(self.base_url.strip())

    @property
    def is_standalone(self) -> bool:
        return self.is_configured and self.mode == "standalone"


# SETTINGS MODELS


class SettingsModel(BaseModel):
    TOKEN: str
    ADMIN_ID: int
    BOT_CHAT_ID: int
    DEBUG_MODE: bool = False
    LOGGER_CONFIG: LoggerConfig

    JOIN_SYMBOL_TEMPLATE: str

    DEFAULT_REACTION_TEMPLATES: List[str]
    DEFAULT_TIME_WORK: TimeWorkEnum = TimeWorkEnum.ALL
    DEFAULT_TIME_ZONE: str = "Asia/Tomsk"
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

    CHAT_SETTINGS_FILE: Optional[Path] = None
    CHAT_SETTINGS_PERSIST: bool = True

    AI_SETTINGS: AISettings = Field(
        default_factory=lambda: AISettings(
            enabled=False,
            api_key="",
            base_url="https://openrouter.ai/api/v1",
        )
    )

    @field_validator("ADMIN_ID", "BOT_CHAT_ID", mode="before")
    @classmethod
    def parse_required_int(cls, value):
        if value in (None, ""):
            raise ValueError("value is required")
        return int(value)

    @field_validator("CHAT_SETTINGS", mode="before")
    @classmethod
    def normalize_chat_settings_keys(cls, value):
        if not value:
            return value
        return {str(chat_id): settings for chat_id, settings in value.items()}
