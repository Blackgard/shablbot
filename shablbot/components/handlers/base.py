from abc import ABC, abstractmethod

from shablbot.models.event_handler import ResponseHandler
from shablbot.models.handler_context import HandlerContext


class BaseMessageHandler(ABC):
    """Базовый интерфейс обработчиков входящих сообщений."""

    @abstractmethod
    def check_message(self, context: HandlerContext) -> bool:
        """Проверить, может ли обработчик обработать сообщение."""

    @abstractmethod
    def handling(self, context: HandlerContext) -> ResponseHandler:
        """Обработать сообщение и вернуть ответ."""
