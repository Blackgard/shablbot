from typing import Optional

import random
import loguru

from shablbot.components.handlers.base import BaseMessageHandler
from shablbot.components.phrases import Phrases
from shablbot.components.handlers.models.message_models import FoundPhrasesByGroups
from shablbot.models.event_handler import ResponseHandler
from shablbot.models.handler_context import HandlerContext
from shablbot.models.phrases import PhraseBodyWord, PhraseBodyWordAnswerWithProbability
from shablbot.settings.settings_model import SettingsModel


class MessageHandler(BaseMessageHandler):
    """Обработчик обычных сообщений, если они не являются командой или модулем."""

    def __init__(
        self,
        settings: SettingsModel,
        phrases: Phrases,
        logger: loguru.logger,
    ) -> None:
        self.logger = logger
        self.settings = settings
        self.phrases = phrases

    def choice_of_answer_probability(
        self, found_matches: FoundPhrasesByGroups
    ) -> Optional[PhraseBodyWord]:
        if found_matches.len > 1:
            found_matches.phrases = {
                key: value
                for key, value in found_matches.phrases.items()
                if key != "default"
            }
        elif found_matches.len == 1:
            return found_matches.phrases.get(
                list(found_matches.phrases.keys())[0], []
            )[0]

        for _, phase_list in found_matches.phrases.items():
            return phase_list[0]

        return None

    def find_matches_to_message(
        self, context: HandlerContext
    ) -> FoundPhrasesByGroups:
        processed_message = context.processed_message
        chat = context.chat
        default_templates = self.settings.DEFAULT_REACTION_TEMPLATES
        join_tmp = self.settings.JOIN_SYMBOL_TEMPLATE

        matched_phrase = {}

        if chat.is_person:
            matched_phrase["default"] = [
                self.phrases.get_default_phrase().words["main"]
            ]

        for phrase in self.phrases.get_phrases():
            if chat.is_person and phrase.group == "default":
                continue

            prefix = ""
            if chat.is_chat:
                prefix = [f"{def_tem}{join_tmp}" for def_tem in default_templates]

            matched_phrase[phrase.group] = phrase.find_match_with_message(
                processed_message, prefix=prefix
            )

        matched_phrase = {key: value for key, value in matched_phrase.items() if value}

        return FoundPhrasesByGroups(
            len=len(matched_phrase.keys()),
            phrases=matched_phrase,
        )

    def get_message_to_reply(
        self, probability: PhraseBodyWordAnswerWithProbability
    ) -> str:
        default_probabilities = self.settings.DEFAULT_PROBABILITY.model_dump()
        dict_probabilities = probability.model_dump(exclude_none=True)
        weights_probabilities = [
            prob
            for name, prob in default_probabilities.items()
            if dict_probabilities.get(name)
        ]

        probability_type: str = random.choices(
            [*dict_probabilities.keys()], weights=weights_probabilities
        )[0]

        return random.choice(probability.model_dump()[probability_type])

    def check_message(self, context: HandlerContext) -> bool:
        return bool(self.find_matches_to_message(context).phrases)

    def handling(self, context: HandlerContext) -> ResponseHandler:
        found_matches = self.find_matches_to_message(context)
        if not found_matches.phrases:
            return ResponseHandler(
                send_to_chat_id=context.reply_chat_id,
                message=None,
                error="Not found matches.",
                is_matches_found=False,
            )

        phrase_body = self.choice_of_answer_probability(found_matches)
        if not phrase_body:
            return ResponseHandler(
                send_to_chat_id=context.reply_chat_id,
                message=None,
                error=f'No response found for the phrase "{context.message_text}".',
                is_matches_found=False,
            )

        return ResponseHandler(
            send_to_chat_id=context.reply_chat_id,
            message=self.get_message_to_reply(phrase_body.answer),
            keyboard_code=phrase_body.keyboard,
            is_matches_found=True,
        )
