from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ResponceHandler(BaseModel):
    send_to_chat_id: str

    message: Optional[str]
    keyboard_code: Optional[str] = None
    error: Optional[str] = None

    is_matches_found: bool = False

    class Config:
        arbitrary_types_allowed = True
