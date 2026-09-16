from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from shablbot.models.user import User

if TYPE_CHECKING:
    from shablbot.components.chat import Chat
    from shablbot.models.shablbot import VkBotMessageEventModel


@dataclass(frozen=True)
class HandlerContext:
    """Контекст обработки входящего сообщения."""

    chat: Chat
    user: User
    message_text: str

    @classmethod
    def from_event(
        cls,
        chat: Chat,
        event: VkBotMessageEventModel,
        admin_id: int,
    ) -> HandlerContext:
        return cls(
            chat=chat,
            user=User.from_event(event, admin_id),
            message_text=event.message.text,
        )

    @property
    def processed_message(self) -> str:
        return self.message_text.lower()

    @property
    def from_id(self) -> int:
        return self.user.user_id

    @property
    def admin_id(self) -> int:
        return self.user.admin_id

    @property
    def is_admin(self) -> bool:
        return self.user.is_admin

    @property
    def reply_chat_id(self) -> str:
        return self.chat.chat_id
