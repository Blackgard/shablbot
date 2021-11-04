from typing import Dict, List

from pydantic import BaseModel

from shablbot.models.phrases import PhraseBodyWord


class FoundPhrasesByGroups(BaseModel):
    len: int
    phrases: Dict[str, List[PhraseBodyWord]]
