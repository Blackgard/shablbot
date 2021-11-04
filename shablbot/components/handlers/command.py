from typing import Optional

import re
import loguru

from shablbot.components.chat import Chat, Chats
from shablbot.components.command import Commands

from shablbot.models.event_handler import ResponceHandler
from shablbot.settings.settings_model import SettingsModel


class CommandHandler:
    """MessageHandler is a handler for command messages from admin/users"""

    def __init__(
        self, settings: SettingsModel, commands: Commands, chats: Chats, logger: loguru.logger
    ) -> None:
        self.logger = logger
        self.settings = settings

        self.chats = chats
        self.commands = commands

    def check_message(self, message: str) -> bool:
        """Check message from chat to command

        Args:
            message (str): The message that was sent to the chat

        Returns:
            bool: is founded
        """
        processed_message = message.lower()
        commands_dict = self.commands.get_commands()

        for command_type in commands_dict:
            for _, command_settings in commands_dict[command_type].items():
                for find_message_template in command_settings.get_templates():
                    found_command = re.findall(find_message_template, processed_message)
                    if found_command:
                        return True

        return False

    def handling(self, message: str, chat: Chat) -> ResponceHandler:
        """Handler for command messages from all chat users

        Args:
            message (str): The message that was sent to the chat
            chat (Chat): Chat object

        Returns:
            answer (str): Answer shablbot for message
        """
        processed_message = message.lower()
        message_to_reply = None
        type_command = None

        commands_dict = self.commands.get_commands()

        for commands_type in commands_dict:
            for _, command in commands_dict[commands_type].items():
                for find_message_template in command.get_templates():
                    found_command = re.findall(find_message_template, processed_message)
                    if not found_command:
                        continue

                    message_to_reply = command.execute_command(
                        processed_chat=chat,
                        chats=self.chats,
                        commands=self.commands,
                    )
                    type_command = command.command_type
                    break

        send_chat_id = self.settings.ADMIN_ID if type_command == "private" else chat.chat_id

        if not message_to_reply:
            return ResponceHandler(
                send_to_chat_id=send_chat_id,
                message=None,
                error="Is not found matches!",
                is_matches_found=False
            )

        return ResponceHandler(
            send_to_chat_id=send_chat_id,
            message=message_to_reply,
            is_matches_found=True
        )
