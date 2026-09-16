from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from shablbot.models.shablbot import VkBotMessageEventModel


class User(BaseModel):
    """Модель пользователя VK, инициировавшего событие."""

    model_config = ConfigDict(frozen=True)

    user_id: int
    admin_id: int
    peer_id: int
    message_id: int | None = None

    @classmethod
    def from_event(
        cls,
        event: VkBotMessageEventModel,
        admin_id: int,
    ) -> User:
        return cls(
            user_id=event.message.from_id,
            admin_id=admin_id,
            peer_id=event.message.peer_id,
            message_id=event.message.id,
        )

    @property
    def is_admin(self) -> bool:
        return self.user_id == self.admin_id

    @property
    def is_personal_chat(self) -> bool:
        return str(self.peer_id).startswith("1")

    @property
    def is_group_chat(self) -> bool:
        return str(self.peer_id).startswith("2")
