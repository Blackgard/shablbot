# -*- coding: utf-8 -*-

from typing import List

import os
import sys
import shutil
import argparse

from pathlib import Path
from importlib import import_module


from shablbot.shablbot import ShablBot, SettingsModel

from shablbot.core.exceptions import SettingNotExists
from shablbot.core.color import ColorText


class ManageShablbot:
    " CLI Shablbot manager "

    def __init__(self, argv: List[str]):
        self.work_forder: Path = Path(sys.path[0])
        self.manage_file: Path = self.work_forder.joinpath(os.path.basename(argv[0]))

        self.__shablbot_folder: Path = Path(__file__).parent.parent
        self.__init_folder: Path = Path(__file__).parent.parent.joinpath("init")

        self.parser = self.__create_parser()
        self.namespace = self.parser.parse_args(argv[1:])

    def __create_parser(self) -> argparse.ArgumentParser:
        """ Create argument parser object with command.

        Returns:
            argparse.ArgumentParser: Argument parser
        """
        parser = argparse.ArgumentParser(
            prog="python manage.py ",
            description="🤖 Бот написанный на Python для социальной сети Вконтакте, работающий через VkBotLongPull",
            epilog="(c) Alex Drachenin",
        )
        parser.add_argument(
            "-r",
            "--run-bot",
            action="store_const",
            const=True,
            help="Запустить сервер для работы бота",
        )
        parser.add_argument(
            "-i",
            "--init",
            action="store_const",
            const=True,
            help='Инициировать каталоги для работы бота [ "commands", "keyboards", "modules", "phrases", "settings", "manager.py" ]',
        )
        parser.add_argument(
            "-c",
            "--check-bot",
            action="store_const",
            const=True,
            help="Проверить работоспособность бота без запуска сервера"
        )

        return parser

    def __get_settings(self) -> SettingsModel:
        """ Get setting from work folder. If not found, raise error.

        Raises:
            ModuleNotFoundError: File settings.py not found.
            SettingNotExists: settings.py not have SETTING variable.

        Returns:
            SettingsModel: Setting model shablbot.
        """
        try:
            settings_mod = import_module('settings.settings')
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                f"{ColorText.FAIL}Setting not import{ColorText.ENDC}. You need create settings folder and settings.py file.\n"
                f"Use command {ColorText.ENDC}{ColorText.WARNING}'python manage.py --init_settings .'{ColorText.ENDC} for init settings folder."
            )

        if not settings_mod.SETTINGS:
            raise SettingNotExists(
                "In settings.py not found SETTINGS variable!"
            )

        return settings_mod.SETTINGS

    def start_bot(self):
        """ CLI START BOT
            --------

            Run bot server and lister longpoll.

            Read more about the structure: https://github.com/Blackgard/shablbot
        """
        bot_settings = self.__get_settings()
        bot = ShablBot(bot_settings)
        bot.listen()

    def init(self):
        """ CLI INIT
            --------

            Create modules for work shablbot.

            List modules:
            - commands (folder);
            - keyboards (folder);
            - modules (folder);
            - phrases (folder);
            - settings (folder);
            - manager.py (file);

            Read more about the structure: https://github.com/Blackgard/shablbot
        """
        list_existing_folders = [catalog for catalog in self.work_forder.iterdir() if catalog.is_dir()]
        list_init_folders = [catalog for catalog in self.__init_folder.iterdir() if catalog.is_dir()]

        for init_catalog in list_init_folders:
            if init_catalog.name in ["__pycache__"]: continue

            is_found = any([catalog for catalog in list_existing_folders if catalog.name == init_catalog.name])

            if is_found:
                print(
                    f"{ColorText.FAIL}Каталог '{init_catalog.name}' уже создан!"
                    f" Либо удалите старый, либо поменяйте название.{ColorText.ENDC}"
                )
                continue

            shutil.copytree(init_catalog, self.work_forder.joinpath(init_catalog.name), ignore=shutil.ignore_patterns('*.pyc', 'tmp*'))
            print(f"{ColorText.OKGREEN}Каталог '{init_catalog.name}' инициирован!{ColorText.ENDC}")

        is_exists_manager = self.work_forder.joinpath("manager.py").exists()

        if is_exists_manager:
            print(f"{ColorText.FAIL}Файл manager.py уже создан!{ColorText.ENDC}")
            return

        if not self.__shablbot_folder.joinpath("__main__.py").exists():
            raise FileNotFoundError(
                f"{ColorText.FAIL}File '__main__.py' not found in shablbot folder!{ColorText.ENDC}"
                " Reinstall shablbot for create this file."
            )

        new_manager_file: Path = shutil.copy2(
            self.__shablbot_folder.joinpath("__main__.py"),
            self.work_forder
        )

        try:
            Path(new_manager_file).rename("manager.py")
        except FileExistsError:
            print(f"{ColorText.FAIL}Файл manager.py уже создан!{ColorText.ENDC}")
            return

        print(f"{ColorText.OKGREEN}Файл manager.py инициирован!{ColorText.ENDC}")

    def check_bot(self):
        """ CLI CHECK BOT
            --------

            Shows which components the bot downloaded and which could not.

            Read more about the structure: https://github.com/Blackgard/shablbot
        """
        bot_settings = self.__get_settings()
        ShablBot(bot_settings, check_all_components = True)

    def execute_command(self):
        """ Up command """
        if self.namespace.run_bot:
            self.start_bot()
        elif self.namespace.init:
            self.init()
        elif self.namespace.check_bot:
            self.check_bot()
        else:
            self.parser.print_help()


def manager_command(argv):
    """ Manager command. Processes commands passed in line. """
    manager = ManageShablbot(argv)
    manager.execute_command()
