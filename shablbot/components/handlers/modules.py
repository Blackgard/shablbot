from typing import List, Optional, Tuple

import loguru

from shablbot.components.handlers.base import BaseMessageHandler
from shablbot.components.module import Module, Modules
from shablbot.core.message_matcher import MessageMatcher
from shablbot.models.event_handler import ResponseHandler
from shablbot.models.handler_context import HandlerContext
from shablbot.settings.settings_model import SettingsModel


class ModuleHandler(BaseMessageHandler):
    """Обработчик пользовательских модулей."""

    def __init__(
        self,
        settings: SettingsModel,
        modules: Modules,
        logger: loguru.logger,
    ) -> None:
        self.logger = logger
        self.settings = settings
        self.modules = modules

    def check_message(self, context: HandlerContext) -> bool:
        return self.find_matches_to_message(context.processed_message) is not None

    def activate_func(self, module: Module, func_name: str) -> Optional[str]:
        return module.module_settings.entry_point(func_name)

    def find_matches_to_message(
        self, message: str
    ) -> Optional[Tuple[str, Module]]:
        processed_message = message.lower()
        for _, module in self.modules.get_modules():
            if not module.is_loaded:
                continue

            for func_name, reg_list in module.module_settings.templates.items():
                if MessageMatcher.matches_any(reg_list, processed_message):
                    return func_name, module

        return None

    def handling(self, context: HandlerContext) -> ResponseHandler:
        match = self.find_matches_to_message(context.processed_message)
        if not match:
            return ResponseHandler(
                send_to_chat_id=context.reply_chat_id,
                message=None,
                error="Not found matches.",
                is_matches_found=False,
            )

        func_name, module = match
        return ResponseHandler(
            send_to_chat_id=context.reply_chat_id,
            message=self.activate_func(module, func_name),
            is_matches_found=True,
        )
