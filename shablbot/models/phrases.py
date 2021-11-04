from typing import Dict, List, Optional

from pydantic import BaseModel


class PhraseBodyWordAnswerWithProbability(BaseModel):
    common: List[str]
    uncommon: Optional[List[str]]
    rare: Optional[List[str]]
    legendary: Optional[List[str]]


class PhraseBodyWord(BaseModel):
    templates: List[str]
    answer: PhraseBodyWordAnswerWithProbability
    keyboard: Optional[str] = None


class PhraseBody(BaseModel):
    group: str
    words: Dict[str, PhraseBodyWord]
