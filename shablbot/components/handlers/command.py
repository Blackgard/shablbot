import loguru

from shablbot.components.chat import Chats
from shablbot.components.command import Commands
from shablbot.components.handlers.base import BaseMessageHandler
from shablbot.core.authorization import AuthorizationService
from shablbot.core.message_matcher import MessageMatcher
from shablbot.models.event_handler import ResponseHandler
from shablbot.models.handler_context import HandlerContext
from shablbot.settings.settings_model import SettingsModel


class CommandHandler(BaseMessageHandler):
    """Обработчик команд от администратора и пользователей."""

    def __init__(
        self,
        settings: SettingsModel,
        commands: Commands,
        chats: Chats,
        logger: loguru.logger,
    ) -> None:
        self.logger = logger
        self.settings = settings
        self.chats = chats
        self.commands = commands

    def _iter_accessible_commands(self, context: HandlerContext):
        commands_dict = self.commands.get_commands()

        for _, command in commands_dict["public"].items():
            yield command

        if AuthorizationService.can_execute_private_command(context):
            for _, command in commands_dict["private"].items():
                yield command

    def check_message(self, context: HandlerContext) -> bool:
        for command in self._iter_accessible_commands(context):
            if MessageMatcher.matches_any(
                command.get_templates(),
                context.processed_message,
                command.command_settings.method,
            ):
                return True

        return False

    def handling(self, context: HandlerContext) -> ResponseHandler:
        for command in self._iter_accessible_commands(context):
            if not MessageMatcher.matches_any(
                command.get_templates(),
                context.processed_message,
                command.command_settings.method,
            ):
                continue

            message_to_reply = command.execute_command(
                processed_chat=context.chat,
                chats=self.chats,
                commands=self.commands,
            )

            send_chat_id = (
                self.settings.ADMIN_ID
                if command.command_type == "private"
                else context.reply_chat_id
            )

            return ResponseHandler(
                send_to_chat_id=send_chat_id,
                message=message_to_reply,
                is_matches_found=True,
            )

        return ResponseHandler(
            send_to_chat_id=context.reply_chat_id,
            message=None,
            error="Is not found matches!",
            is_matches_found=False,
        )
