from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class ResponseHandler(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    send_to_chat_id: str

    message: Optional[str] = None
    keyboard_code: Optional[str] = None
    error: Optional[str] = None

    is_matches_found: bool = False


# Обратная совместимость со старым именем.
ResponceHandler = ResponseHandler
