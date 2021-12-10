from __future__ import annotations

from typing import Optional, Dict, List, Any
from types import ModuleType

import loguru

from importlib.machinery import ModuleSpec
from importlib.util import find_spec, module_from_spec

from shablbot.components.chat import Chat

from shablbot.settings.settings_model import SettingsModel
from shablbot.models.command import CommandSettings

from shablbot.core.color import ColorText
from shablbot.core.utils import render_state


class Command:
    def __init__(
        self,
        command_name: str,
        command_type: str,
        commands_folder: str,
        logger: loguru.logger,
        is_system_command: bool = False,
        command_settings: Optional[CommandSettings] = None
    ) -> None:
        self.command_name = command_name
        self.command_type = command_type
        self.commands_folder = commands_folder

        self.logger = logger

        self.command_fullname = None
        self.command_settings: Optional[CommandSettings] = command_settings if is_system_command else None

        self.command_path = f"{self.commands_folder}.{self.command_type}.{self.command_name}"
        self.is_loaded = True if is_system_command else self.load_module()

        if not self.is_loaded and not is_system_command:
            self.logger.warning(f"Комманда {self.command_name} не был подключена!")

    def __get_module_spec(self,command_path: str) -> Optional[ModuleSpec]:
        """Getcommand spec for pathcommand.

        Args:
           command_path (str): path to findcommands

        Returns:
            Optional[ModuleSpec]: Specification for acommand, used for loading.
        """
        command_spec = find_spec(command_path)
        return command_spec

    def __import_module_from_spec(self, command_spec:ModuleSpec ) -> Optional[ModuleType]:
        """Importcommand from spec

        Args:
           command_spec (ModuleSpec): Specification for acommand, used for loading.

        Returns:
            Optional[ModuleType]:command type with settingscommand
        """
        command = module_from_spec(command_spec)
        command_spec.loader.exec_module(command)
        return command

    def __pre_execute_command(self, *args, **kwrags) -> Dict[str, Any]:
        """ Pre process run command

        Returns:
            Dict[str, Any]: kwargs to command entry point
        """
        return {arg: kwrags.get(arg) for arg in self.command_settings.need if arg in kwrags.keys()}

    def load_module(self) -> bool:
        "Loadcommand from info."

        command_spec = self.__get_module_spec(self.command_path)
        if not command_spec: return False

        command = self.__import_module_from_spec(command_spec)
        if not command: return False

        self.command_fullname = command_spec.name
        self.command_settings = CommandSettings(**command.command_settings)

        return True

    def get_templates(self) -> List[str]:
        """ Get templates command

        Returns:
            List[str]: Templates list
        """
        return self.command_settings.templates

    def get_answer(self, result: str) -> str:
        """ Get answer command.

        Args:
            result (str): Payload.Resilt entry point.

        Returns:
            str: answer to chat
        """
        if r"{=result}" in self.command_settings.answer:
            return result
        return self.command_settings.answer

    def execute_command(self, *args, **kwargs) -> str:
        """ Run command

        Returns:
            str: answer message
        """
        return self.get_answer(
            self.command_settings.entry_point(**self.__pre_execute_command(*args, **kwargs))
        )

    def __str__(self):
        is_active_str = f'{ColorText.OKGREEN}включен{ColorText.ENDC}' if self.is_loaded else f'{ColorText.FAIL}выключен{ColorText.ENDC}'
        return "{0} - {1}".format(self.command_name, is_active_str)

class Commands:
    """ Commands class for work with command """
    def __init__(self, settings: SettingsModel, logger: loguru.logger):
        self.settings = settings
        self.logger = logger

        self.commands_folder = self.settings.COMMANDS_FOLDER

        self.private_command = {
            path_command : Command(path_command, "private", self.commands_folder, self.logger)
            for path_command in self.settings.ACTIVE_COMMANDS.private
        }

        self.public_command = {
            path_command: Command(path_command, "public", self.commands_folder, self.logger)
            for path_command in self.settings.ACTIVE_COMMANDS.public
        }

        self.public_command['help'] = self.__create_help()

    def __get_help(self, processed_chat: Chat) -> str:
        """Get help text on string

        Args:
            processed_chat (Chat): Chat processed. Need for check Admin ID.

        Returns:
            str: Help list format string
        """
        command_format_public = "- {0} - \n| Описание | {1} \n| Шаблоны | {2}"
        command_format_private = "- {0} ({1}) - \n| Описание | {2} \n| Шаблоны | {3}"

        help_commands = "\n\n".join([
            command_format_public.format(
                command.command_settings.name,
                command.command_settings.description,
                ", ".join(command.command_settings.templates)
            )
            for _, command in self.public_command.items()
            if command.is_loaded
        ])

        if processed_chat.chat_id == self.settings.ADMIN_ID:
            help_commands += "\n\n"
            help_commands += "\n\n".join([
                command_format_private.format(
                    command.command_settings.name,
                    command.command_type,
                    command.command_settings.description,
                    ", ".join(command.command_settings.templates)
                )
                for _, command in self.private_command.items()
                if command.is_loaded
            ])

        return help_commands

    def __create_help(self) -> Command:
        """ Create nelp command and return this.

        Returns:
            Command: Help command
        """
        return Command(
            command_name="help",
            command_type="public",
            commands_folder=self.commands_folder,
            logger=self.logger,
            is_system_command=True,
            command_settings=CommandSettings(
                code="help",
                name="Список команд",
                answer="{=result}",
                description="Выводит список доступных команд",
                templates=["help", "помощь"],
                method="normal",
                need=["processed_chat"],
                entry_point=self.__get_help
            )
        )

    def get_command(self, command_name: str, command_type: Optional[str] = None) -> Optional[Command]:
        """ Get command by name and optional type

        Args:
            command_name (str): Command name
            command_type (Optional[str], optional): Command type (private/public). Defaults to None.

        Returns:
            Optional[Command]: Command or Optional
        """
        if command_type == "private": return self.private_command.get(command_name, None)
        elif command_type == "public": return self.public_command.get(command_name, None)
        return self.private_command.get(command_name, None) or self.public_command.get(command_name, None)

    def get_commands(self) -> Dict[str, Dict[str, Command]]:
        """ Get all comands

        Returns:
            Dict[str, Optional[Command]]: Dict with private/public command
        """
        return { "private": self.private_command, "public": self.public_command }

    def render_state(self):
        render_state(self.__class__.__name__, { **self.public_command, **self.private_command })

    def get_main_data_object(self):
        return { **self.public_command, **self.private_command }
