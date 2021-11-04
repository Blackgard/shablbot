from typing import Dict, List
from types import FunctionType

from datetime import datetime, date
from pydantic import BaseModel, validator


class ModuleSettingsFucntions(BaseModel):
    name: str
    description: str
    entry_point: FunctionType

    class Config:
        arbitrary_types_allowed = True


class ModuleSettings(BaseModel):
    name: str
    version: str
    author: str
    date_created: date
    entry_point: FunctionType
    func: Dict[str, ModuleSettingsFucntions]
    templates: Dict[str, List[str]]

    @validator("date_created", pre=True)
    def parse_date_created(cls, value):
        return datetime.strptime(value, "%d.%m.%Y").date()

    class Config:
        arbitrary_types_allowed = True
