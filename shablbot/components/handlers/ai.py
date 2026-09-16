from __future__ import annotations

import loguru

from shablbot.components.command import Commands
from shablbot.components.handlers.base import BaseMessageHandler
from shablbot.components.handlers.message import MessageHandler
from shablbot.core.ai import AIChatService, AIProviderError
from shablbot.models.event_handler import ResponseHandler
from shablbot.models.handler_context import HandlerContext
from shablbot.settings.settings_model import SettingsModel


class AIHandler(BaseMessageHandler):
    """Обработчик standalone-режима: нейросеть отвечает на естественные сообщения."""

    def __init__(
        self,
        settings: SettingsModel,
        commands: Commands,
        message_handler: MessageHandler,
        logger: loguru.logger,
    ) -> None:
        self.settings = settings
        self.commands = commands
        self.message_handler = message_handler
        self.logger = logger
        self._service: AIChatService | None = None

    def _get_service(self) -> AIChatService:
        if self._service is None:
            self._service = AIChatService(self.settings.AI_SETTINGS)
        return self._service

    def check_message(self, context: HandlerContext) -> bool:
        if not self.settings.AI_SETTINGS.is_standalone:
            return False
        return self.message_handler.check_message(context)

    def handling(self, context: HandlerContext) -> ResponseHandler:
        try:
            message = self._get_service().ask_standalone(context, self.commands)
            return ResponseHandler(
                send_to_chat_id=context.reply_chat_id,
                message=message,
                is_matches_found=True,
            )
        except AIProviderError as error:
            return ResponseHandler(
                send_to_chat_id=context.reply_chat_id,
                message=f"Ошибка AI: {error}",
                is_matches_found=True,
            )
        except Exception as error:
            self.logger.error(f"Standalone AI error: {error}")
            return ResponseHandler(
                send_to_chat_id=context.reply_chat_id,
                message="Не удалось получить ответ нейросети.",
                is_matches_found=True,
            )
