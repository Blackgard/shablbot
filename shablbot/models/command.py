from types import FunctionType, MethodType
from typing import List, Union

from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator


class CommandSettingsNeed(str, Enum):
    PROCESSED_CHAT = "processed_chat"
    CHATS = "chats"
    COMMANDS = "commands"


class CommandSettingsMethods(str, Enum):
    NORMAL = "normal"
    REGULAR = "regular"


class CommandSettings(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    code: str
    name: str

    answer: str
    description: str
    templates: List[str]

    method: CommandSettingsMethods
    need: List[CommandSettingsNeed]

    entry_point: Union[FunctionType, MethodType]

    @field_validator("code", mode="before")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        return value.lower() if isinstance(value, str) else value
