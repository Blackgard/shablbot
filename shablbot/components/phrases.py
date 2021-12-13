from __future__ import annotations
from typing import Optional, Dict, List, Union

import re
import os
import json
import loguru

from shablbot.models.phrases import PhraseBody, PhraseBodyWord
from shablbot.settings.settings_model import SettingsModel

from shablbot.core.color import ColorText
from shablbot.core.utils import render_state


class Phrase:
    def __init__(self, phrase_path_file: str, logger: loguru.logger) -> None:
        self.logger = logger
        self.phrase_path_file = phrase_path_file

        self.__phrase_body = self.__load_phrase_from_file()

        if self.__phrase_body:
            self.group = self.__phrase_body.group
            self.words = self.__phrase_body.words

        self.is_loaded = True if isinstance(self.__phrase_body, PhraseBody) else False

        if not self.is_loaded:
            self.logger.warning(f"Фраза {self.phrase_path_file} не была загружена!")

    def __load_phrase_from_file(self) -> Optional[PhraseBody]:
        try:
            with open(self.phrase_path_file, mode='r', encoding="UTF-8") as file:
                phrase_body = json.load(file)
                if isinstance(phrase_body, Dict):
                    return PhraseBody(**phrase_body)
                return None
        except OSError as err:
            self.logger.error(f"Could not load phrase file -> '{self.phrase_path_file}' |\n err -> {err}")
        return None

    def __findall(self, message, word_body, processed_message, matched_list) -> None:
        """ Find all match for message from chat

        Args:
            message ([type]): expected message
            word_body ([type]): processed word
            processed_message ([type]): processed_message
            matched_list ([type]): list matched with words
        """
        if re.findall(message, processed_message):
            matched_list.append(word_body)

    def find_match_with_message(self, processed_message: str, preffix: Union[str, List[str]] = "") -> List[PhraseBodyWord]:
        """Find a match with a message.

        Args:
            processed_message (str): string fo find template.
            preffix (str, List[str], optional): Prefixx to phrase. Defaults to "".

        Returns:
            List[PhraseBodyWord]: List mached phrases.
        """

        matched_list = []
        preffix_list = [preffix] if isinstance(preffix, str) else preffix

        for _, word_body in self.words.items():
            for template in word_body.templates:
                if not preffix_list:
                    for _preffix in preffix_list:
                        self.__findall(
                            f"{_preffix}{template}",
                            word_body,
                            processed_message,
                            matched_list
                        )
                else:
                    self.__findall(template, word_body, processed_message, matched_list)

        return matched_list

    def __str__(self):
        is_active_str = f'{ColorText.OKGREEN}включен{ColorText.ENDC}' if self.is_loaded else f'{ColorText.FAIL}выключен{ColorText.ENDC}'
        return "{0} - {1}".format(self.group, is_active_str)


class Phrases:
    """ Phrases class for work with phrase """
    def __init__(self, settings: SettingsModel, logger: loguru.logger, exclude_empty: bool = False):
        self.settings = settings
        self.logger = logger

        self.phrases_folder = self.settings.PHRASES_FOLDER

        self.phrases = [
            Phrase(self.phrases_folder.joinpath(phrase_file), self.logger)
            for phrase_file in os.listdir(self.phrases_folder)
            if phrase_file not in self.settings.EXCLUDED_PHRASES
            and phrase_file.split(".")[-1] == "json"
        ]

        if exclude_empty:
            self.phrases = [ phrase for phrase in self.phrases if phrase.is_loaded ]

    def get_phrases(self) -> List[Phrase]:
        """ Get list with phrases bot

        Returns:
            List[Phrase]: list with phrases
        """
        return self.phrases

    def get_default_phrase(self) -> Phrase:
        return [phrase for phrase in self.phrases if phrase.group == "default"][0]

    def render_state(self):
        """ Render state module to console tree """
        render_state(self.__class__.__name__, self.phrases)

    def get_main_data_object(self) -> List[Phrase]:
        """ Get main data object is system function. Need for work render main state shablbot.

        Returns:
            List[Phrase]: list phrases
        """
        return self.phrases
