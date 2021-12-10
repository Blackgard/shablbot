from typing import Optional, Dict, Any

import os
import json
import loguru
from pathlib import Path

from shablbot.settings.settings_model import SettingsModel

from shablbot.core.color import ColorText
from shablbot.core.utils import render_state


class Keyboard:
    """Keyboard model"""

    def __init__(self, keyboard_code: str, keyboard_name: str, folder: Path):
        self.keyboard_code = keyboard_code
        self.keyboard_name = keyboard_name
        self.folder = folder

        self.path_to_keyboard = os.path.join(self.folder, self.keyboard_name)
        self.keyboard = self.get_keyboard_from_json()

        self.is_loaded = True if self.keyboard else False


    def get_keyboard_json(self) -> Optional[str]:
        """Get active keyboard

        Returns:
            Optional[Dict[str, Any]]: keyboard json
        """
        return json.dumps(self.keyboard)

    def get_keyboard_from_json(self) -> Optional[Dict[str, Any]]:
        """ Get keyboard json in dict from file.

        Returns:
            Optional[Dict[str, Any]]: json keyboard or None
        """
        if not self.path_to_keyboard: return None

        with open(self.path_to_keyboard, encoding="utf-8") as json_keyboard:
            return json.loads(json_keyboard.read())

    def __str__(self):
        is_active_str = f'{ColorText.OKGREEN}включен{ColorText.ENDC}' if self.is_loaded else f'{ColorText.FAIL}выключен{ColorText.ENDC}'
        return "{0} - {1}".format(self.keyboard_code, is_active_str)



class Keyboards:
    """Keyboard class for work with keybord"""

    def __init__(self, settings: SettingsModel, logger: loguru.logger):
        self.settings = settings
        self.logger = logger

        self.folder = self.settings.KEYBOARDS_FOLDER
        self.keyboards: Dict[str, Keyboard] = {
            code: Keyboard(code, path, self.folder)
            for code, path in self.settings.KEYBOARDS.items()
        }

    def get_default_keyboard(self) -> Keyboard:
        return self.keyboards.get("default", None)

    def get_clear_keyboard(self) -> Keyboard:
        return self.keyboards.get("clear", None)

    def get_keyboard(self, code: str) -> Optional[Keyboard]:
        """Get keyboard from code

        Args:
            code (str): keyboarde code from settings.py

        Returns:
            Optional[Keyboard]: Keyboard or None
        """
        return self.keyboards.get(code, None)

    def render_state(self):
        render_state(self.__class__.__name__, self.keyboards)

    def get_main_data_object(self):
        return self.keyboards
