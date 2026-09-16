from typing import Dict, List, Optional

from pydantic import BaseModel


class PhraseBodyWordAnswerWithProbability(BaseModel):
    common: List[str]
    uncommon: Optional[List[str]] = None
    rare: Optional[List[str]] = None
    legendary: Optional[List[str]] = None


class PhraseBodyWord(BaseModel):
    templates: List[str]
    answer: PhraseBodyWordAnswerWithProbability
    keyboard: Optional[str] = None


class PhraseBody(BaseModel):
    group: str
    words: Dict[str, PhraseBodyWord]
