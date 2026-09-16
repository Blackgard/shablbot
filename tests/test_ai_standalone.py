import unittest
from unittest.mock import MagicMock, patch

from shablbot.components.handlers.ai import AIHandler
from shablbot.core.ai.actions import parse_ai_action_response
from shablbot.models.handler_context import HandlerContext
from shablbot.models.user import User
from shablbot.settings.settings_model import AISettings


class ParseAIActionTests(unittest.TestCase):
    def test_parse_json_response(self):
        action, reply = parse_ai_action_response(
            '{"action": "bot_off", "reply": "Бот выключен"}'
        )
        self.assertEqual(action, "bot_off")
        self.assertEqual(reply, "Бот выключен")

    def test_parse_plain_text_fallback(self):
        action, reply = parse_ai_action_response("Просто ответ без JSON")
        self.assertEqual(action, "none")
        self.assertEqual(reply, "Просто ответ без JSON")


class AIHandlerTests(unittest.TestCase):
    def test_check_message_only_in_standalone_mode(self):
        settings = MagicMock()
        settings.AI_SETTINGS = AISettings(
            enabled=True,
            mode="module",
            api_key="key",
            base_url="https://openrouter.ai/api/v1",
        )

        message_handler = MagicMock()
        message_handler.check_message.return_value = True

        handler = AIHandler(settings, MagicMock(), message_handler, MagicMock())
        context = HandlerContext(
            chat=MagicMock(),
            user=User(user_id=1, admin_id=1, peer_id=1),
            message_text="привет бот",
        )

        self.assertFalse(handler.check_message(context))

    def test_standalone_delegates_activation_to_message_handler(self):
        settings = MagicMock()
        settings.AI_SETTINGS = AISettings(
            enabled=True,
            mode="standalone",
            api_key="key",
            base_url="https://openrouter.ai/api/v1",
        )

        message_handler = MagicMock()
        message_handler.check_message.return_value = True

        handler = AIHandler(settings, MagicMock(), message_handler, MagicMock())
        context = HandlerContext(
            chat=MagicMock(),
            user=User(user_id=1, admin_id=1, peer_id=1),
            message_text="выключи бота",
        )

        self.assertTrue(handler.check_message(context))


if __name__ == "__main__":
    unittest.main()
