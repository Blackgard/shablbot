from typing import List, Optional, Tuple

import re
import loguru

from shablbot.components.chat import Chat
from shablbot.components.module import Module, Modules
from shablbot.models.event_handler import ResponceHandler

from shablbot.settings.settings_model import (
    SettingsModel as DefaultSettingsModel,
)


class ModuleHandler:
    """ModulesHandler description of the module for the bot"""

    def __init__(
        self, settings: DefaultSettingsModel, modules: Modules, logger: loguru.logger
    ) -> None:
        self.logger = logger
        self.settings = settings

        self.modules = modules

    def check_message(self, message: str) -> bool:
        """Check message from chat to module templates

        Args:
            message (str): The message that was sent to the chat

        Returns:
            bool: is founded
        """
        processed_message = message.lower()

        for _, module in self.modules.get_modules():
            if not module.is_loaded:
                continue

            for _, reg_list in module.module_settings.templates.items():
                find_match = any(
                    [re.findall(reg, processed_message) for reg in reg_list]
                )
                if find_match:
                    return True
        return False

    def activate_func(self, module: Module, func_name: str) -> Optional[str]:
        """Activate module for response

        Args:
            func_name (str): The function to be called

        Returns:
            Optional[str]: answer message
        """
        return module.module_settings.entry_point(func_name)

    def find_matches_to_message(
        self, message: str
    ) -> Tuple[Optional[str], Optional[Module]]:
        """Find matches with the message.

        Args:
            message (str):  The message that was sent to the chat

        Returns:
            first (Optional[str]): name function
            second (Optional[str]): module
        """
        processed_message = message.lower()
        for _, module in self.modules.get_modules():
            if not module.is_loaded:
                continue
            for func_name, reg_list in module.module_settings.templates.items():
                for reg in reg_list:
                    find_match = re.findall(reg, processed_message)
                    if find_match:
                        return (func_name, module)

        return (None, None)

    def handling(self, message: str, chat: Chat) -> ResponceHandler:
        """Handler for regular messages from all chat users

        Args:
            message (str): The message that was sent to the chat
            chat (Chat): Chat object

        Returns:
            answer (str): Answer shablbot for message
        """
        func_name, module = self.find_matches_to_message(message)
        if not func_name and not module:
            return ResponceHandler(
                send_to_chat_id=chat.chat_id,
                message=None,
                error="Not found matches."
            )

        return ResponceHandler(
            send_to_chat_id=chat.chat_id,
            message=self.activate_func(module, func_name),
            is_matches_found=True
        )
