
import loguru

from shablbot.models.shablbot import VkBotMessageEventModel

from shablbot.components.phrases import Phrases
from shablbot.components.command import Commands
from shablbot.components.chat import Chat, Chats
from shablbot.components.module import Modules

from shablbot.models.event_handler import ResponceHandler

from shablbot.components.handlers.modules import ModuleHandler
from shablbot.components.handlers.message import MessageHandler
from shablbot.components.handlers.command import CommandHandler

from shablbot.settings.settings_model import SettingsModel


class EventHandler:
    """Event processing module from VkAPi. Receives a message, parses and returns a response based on
    the contents of the message received"""

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
        self.command_handler = CommandHandler(self.settings, self.commands, self.chats, self.logger)
        self.message_handler = MessageHandler(self.settings, self.phrases, self.logger)

    def process_chat_event(
        self, chat: Chat, event: VkBotMessageEventModel
    ) -> ResponceHandler:
        """Process chat event for message command/module/common_message.

        Args:
            chat (Chat): Chat object
            event (VkBotMessageEventModel): Vk event

        Returns:
            [ResponceHandler]: message answer object
        """

        if self.__is_command_event(event):
            return self.command_handler.handling(event.message.text, chat)
        elif self.__is_module_event(event) and chat.chat_settings.enabled:
            return self.module_handler.handling(event.message.text, chat)
        elif chat.chat_settings.enabled:
            return self.message_handler.handling(event.message.text, chat)

        return ResponceHandler(send_to_chat_id=chat.chat_id, error="Not found matches", is_matches_found=False)

    def __is_command_event(self, event: VkBotMessageEventModel) -> bool:
        "Check message for command"
        return self.command_handler.check_message(event.message.text)

    def __is_module_event(self, event: VkBotMessageEventModel) -> bool:
        "Check message for module template"
        return self.module_handler.check_message(event.message.text)
