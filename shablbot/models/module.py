from typing import Dict, List
from types import FunctionType

from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, field_validator


class ModuleSettingsFucntions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    description: str
    entry_point: FunctionType


class ModuleSettings(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    version: str
    author: str
    date_created: date
    entry_point: FunctionType
    func: Dict[str, ModuleSettingsFucntions]
    templates: Dict[str, List[str]]

    @field_validator("date_created", mode="before")
    @classmethod
    def parse_date_created(cls, value):
        if isinstance(value, date):
            return value
        return datetime.strptime(value, "%d.%m.%Y").date()
