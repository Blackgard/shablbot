from typing import Optional

import random
import loguru

from shablbot.components.chat import Chat
from shablbot.components.phrases import Phrases
from shablbot.models.event_handler import ResponceHandler

from shablbot.models.phrases import PhraseBodyWord, PhraseBodyWordAnswerWithProbability
from shablbot.components.handlers.models.message_models import FoundPhrasesByGroups
from shablbot.settings.settings_model import SettingsModel


class MessageHandler:
    """MessageHandler is a handler for normal messages from users, if the bot has not
    defined messages as "command" or "modular"."""

    def __init__(self, settings: SettingsModel, phrases: Phrases, logger: loguru.logger) -> None:
        self.logger = logger
        self.settings = settings
        self.phrases = phrases

    def choice_of_answer_probability(
        self, found_matches: FoundPhrasesByGroups
    ) -> Optional[PhraseBodyWord]:
        """Choosing an answer option based on found matches of response templates

        Args:
        ---
            found_matches (List[MatchedPhases]): Priority word matches found in the message

        Returns:
        ---
            answers_list (Probability): answers list with probability
        """

        phrase_body = None

        if found_matches.len > 1:
            found_matches.phrases = { k:v for k,v in found_matches.phrases.items() if k != "default" }
        elif found_matches.len == 1:
            return found_matches.phrases.get(list(found_matches.phrases.keys())[0], [])[0]

        for _, phase_list in found_matches.phrases.items():
            return phase_list[0]

        return phrase_body

    def find_matches_to_message(self, message: str, chat: Chat) -> FoundPhrasesByGroups:
        """Search in the text for words from templates located in "SETTINGS.DEFAULT_REACTION_TEMPLATES" for the answer.

        Args:
        ---
            message (str): The message that was sent to the chat
            chat (Chat): Object in which the bot processes the message

        Returns:
        ---
            matched_phrase (FoundPhrasesByGroups): Found phrases grouped by groups
        """

        processed_message: str = message.lower()
        default_templates = self.settings.DEFAULT_REACTION_TEMPLATES
        join_tmp = self.settings.JOIN_SYMBOL_TEMPLATE

        matched_phrase = {}

        if chat.is_person:
            matched_phrase['default'] = [self.phrases.get_default_phrase().words["main"]]

        for phrase in self.phrases.get_phrases():
            if chat.is_person and phrase.group == "default": continue

            preffix = ""
            if chat.is_chat:
                preffix = [f"{def_tem}{join_tmp}" for def_tem in default_templates]

            matched_phrase[phrase.group] = phrase.find_match_with_message(processed_message, preffix=preffix)

        # clear empty item
        matched_phrase = {k:v for k,v in matched_phrase.items() if v}

        return FoundPhrasesByGroups(
            len=len(matched_phrase.keys()),
            phrases=matched_phrase
        )

    def get_message_to_reply(self, probability: PhraseBodyWordAnswerWithProbability) -> str:
        """The function returns the response of the bot for the chat, to receive the response,
        you need to send a block with the list of responses grouped by probabilities

        Args:
            probability (Probability): Model of answers grouped by probabilities

        Returns:
            answer (str): Answer message to chat
        """
        default_probabilities = self.settings.DEFAULT_PROBABILITY.dict()
        dict_probabilities = probability.dict(exclude_none=True)
        weights_probabilities = [
            prob
            for name, prob in default_probabilities.items()
            if dict_probabilities.get(name)
        ]

        probability_type: str = random.choices(
            [*dict_probabilities.keys()], weights=weights_probabilities
        )[0]

        return random.choice(probability.dict()[probability_type])

    def handling(self, message: str, chat: Chat) -> ResponceHandler:
        """Handler for regular messages from all chat users

        Args:
            message (str): The message that was sent to the chat
            chat (Chat): Chat object

        Returns:
            answer (str): Answer shablbot for message
        """
        found_matches = self.find_matches_to_message(message, chat)
        if not found_matches.phrases:
            return ResponceHandler(send_to_chat_id=chat.chat_id, message=None, error=f"Not found matches.")

        phrase_body = self.choice_of_answer_probability(found_matches)
        if not phrase_body:
            return ResponceHandler(
                send_to_chat_id=chat.chat_id,
                message=None,
                error=f'No response found for the phrase "{message}".'
            )

        return ResponceHandler(
            send_to_chat_id=chat.chat_id,
            message=self.get_message_to_reply(phrase_body.answer),
            keyboard_code=phrase_body.keyboard,
            is_matches_found=True,
        )
