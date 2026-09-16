import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from shablbot.components.chat import Chat
from shablbot.components.handlers.message import MessageHandler
from shablbot.components.phrases import Phrases
from shablbot.models.handler_context import HandlerContext
from shablbot.models.user import User
from shablbot.settings.settings_model import (
    ChatSettingsBody,
    ChatSettingsBodyTimeWork,
    ProbabilityValue,
    TimeWorkEnum,
)


def _build_settings(phrases_folder: Path) -> MagicMock:
    settings = MagicMock()
    settings.PHRASES_FOLDER = phrases_folder
    settings.EXCLUDED_PHRASES = []
    settings.DEFAULT_REACTION_TEMPLATES = (r"ходор", r"hodor", r"бот")
    settings.JOIN_SYMBOL_TEMPLATE = r"\s.*?"
    settings.DEFAULT_PROBABILITY = ProbabilityValue()
    return settings


def _write_phrase(path: Path, group: str, templates: list[str], answers: list[str]) -> None:
    path.write_text(
        json.dumps(
            {
                "group": group,
                "words": {
                    "main": {
                        "templates": templates,
                        "answer": {"common": answers},
                    }
                },
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


class MessageHandlerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.phrases_folder = Path(self.temp_dir.name)
        _write_phrase(
            self.phrases_folder / "_default.json",
            "default",
            ["ходор", "hodor", "бот"],
            ["Ходор"],
        )
        _write_phrase(
            self.phrases_folder / "hello.json",
            "приветствие",
            ["привет"],
            ["Ходор!"],
        )

        self.settings = _build_settings(self.phrases_folder)
        self.logger = MagicMock()
        self.phrases = Phrases(self.settings, self.logger)
        self.handler = MessageHandler(self.settings, self.phrases, self.logger)

    def tearDown(self):
        self.temp_dir.cleanup()

    def _context(self, chat_id: str, message: str) -> HandlerContext:
        chat = Chat(
            chat_id=chat_id,
            chat_settings=ChatSettingsBody(
                enabled=True,
                time_work=ChatSettingsBodyTimeWork(
                    type=TimeWorkEnum.ALL,
                    time_zone="UTC",
                ),
            ),
            default_time_work=TimeWorkEnum.ALL,
            default_time_zone="UTC",
            _info=None,
        )
        return HandlerContext(
            chat=chat,
            user=User(user_id=1, admin_id=1, peer_id=int(chat_id)),
            message_text=message,
        )

    def test_private_message_matches_greeting(self):
        context = self._context("153950322", "Привет")
        self.assertTrue(self.handler.check_message(context))

    def test_private_message_handles_reply(self):
        context = self._context("153950322", "Привет")
        response = self.handler.handling(context)
        self.assertTrue(response.is_matches_found)
        self.assertIn(response.message, ["Ходор!", "Ходор"])

    def test_group_chat_requires_bot_prefix(self):
        context = self._context("2000000001", "привет")
        self.assertFalse(self.handler.check_message(context))

    def test_group_chat_matches_with_prefix(self):
        context = self._context("2000000001", "ходор привет")
        self.assertTrue(self.handler.check_message(context))


if __name__ == "__main__":
    unittest.main()
