from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shablbot.components.chat import Chat
    from shablbot.models.shablbot import VkBotMessageEventModel


@dataclass(frozen=True)
class HandlerContext:
    """Контекст обработки входящего сообщения."""

    chat: Chat
    message_text: str
    from_id: int
    admin_id: int

    @classmethod
    def from_event(
        cls,
        chat: Chat,
        event: VkBotMessageEventModel,
        admin_id: int,
    ) -> HandlerContext:
        return cls(
            chat=chat,
            message_text=event.message.text,
            from_id=event.message.from_id,
            admin_id=admin_id,
        )

    @property
    def processed_message(self) -> str:
        return self.message_text.lower()

    @property
    def is_admin(self) -> bool:
        return self.from_id == self.admin_id

    @property
    def reply_chat_id(self) -> str:
        return self.chat.chat_id
