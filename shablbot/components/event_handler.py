
import loguru

from shablbot.models.shablbot import VkBotMessageEventModel

from shablbot.components.phrases import Phrases
from shablbot.components.command import Commands
from shablbot.components.chat import Chat, Chats
from shablbot.components.module import Modules

from shablbot.models.event_handler import ResponseHandler
from shablbot.models.handler_context import HandlerContext

from shablbot.components.handlers.modules import ModuleHandler
from shablbot.components.handlers.message import MessageHandler
from shablbot.components.handlers.command import CommandHandler

from shablbot.settings.settings_model import SettingsModel


class EventHandler:
    """Обработка событий VkAPI: парсинг сообщения и выбор подходящего обработчика."""

    def __init__(
        self,
        settings: SettingsModel,
        commands: Commands,
        chats: Chats,
        modules: Modules,
        phrases: Phrases,
        logger: loguru.logger,
    ):
        self.settings = settings
        self.logger = logger

        self.chats = chats
        self.phrases = phrases
        self.modules = modules
        self.commands = commands

        self.module_handler = ModuleHandler(self.settings, self.modules, self.logger)
        self.command_handler = CommandHandler(
            self.settings, self.commands, self.chats, self.logger
        )
        self.message_handler = MessageHandler(self.settings, self.phrases, self.logger)

    def _build_context(
        self, chat: Chat, event: VkBotMessageEventModel
    ) -> HandlerContext:
        return HandlerContext.from_event(chat, event, self.settings.ADMIN_ID)

    def process_chat_event(
        self, chat: Chat, event: VkBotMessageEventModel
    ) -> ResponseHandler:
        context = self._build_context(chat, event)

        if self.command_handler.check_message(context):
            return self.command_handler.handling(context)

        if chat.chat_settings.enabled and self.module_handler.check_message(context):
            return self.module_handler.handling(context)

        if chat.chat_settings.enabled:
            return self.message_handler.handling(context)

        return ResponseHandler(
            send_to_chat_id=context.reply_chat_id,
            error="Not found matches",
            is_matches_found=False,
        )
