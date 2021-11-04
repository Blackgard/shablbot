from types import FunctionType, MethodType
from typing import List, Union

from enum import Enum

from pydantic import BaseModel, constr


class CommandSettingsNeed(str, Enum):
    PROCESSED_CHAT = "processed_chat"
    CHATS = "chats"
    COMMANDS = "commands"


class CommandSettingsMethods(str, Enum):
    NORMAL = "normal"
    REGULAR = "regular"


class CommandSettings(BaseModel):
    code: constr(to_lower=True)
    name: str

    answer: str
    description: str
    templates: List[str]

    method: CommandSettingsMethods
    need: List[CommandSettingsNeed]

    entry_point: Union[FunctionType, MethodType]

    class Config:
        arbitrary_types_allowed = True
