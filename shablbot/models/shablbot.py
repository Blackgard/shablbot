from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Message(BaseModel):
    date: int
    from_id: int
    id: int
    out: int
    peer_id: int
    text: str
    conversation_message_id: int
    fwd_messages: List
    important: bool
    random_id: int
    attachments: List
    is_hidden: bool


class ClientInfo(BaseModel):
    button_actions: List[str]
    keyboard: bool
    inline_keyboard: bool
    carousel: bool
    lang_id: int


class VkBotMessageEventModel(BaseModel):
    message: Message
    client_info: ClientInfo
