import unittest
from datetime import time
from pathlib import Path
from unittest.mock import MagicMock

from shablbot.components.chat import Chat
from shablbot.components.handlers.command import CommandHandler
from shablbot.core.authorization import AuthorizationService
from shablbot.core.message_matcher import MessageMatcher
from shablbot.models.command import CommandSettingsMethods
from shablbot.models.handler_context import HandlerContext
from shablbot.models.user import User
from shablbot.settings import SettingsModel
from shablbot.settings.settings_model import ChatSettingsBody, ChatSettingsBodyTimeWork, TimeWorkEnum


class MessageMatcherTests(unittest.TestCase):
    def test_normal_matches_single_word(self):
        self.assertTrue(
            MessageMatcher.matches("help", "need help please", CommandSettingsMethods.NORMAL)
        )
        self.assertFalse(
            MessageMatcher.matches("help", "helpful friend", CommandSettingsMethods.NORMAL)
        )

    def test_normal_matches_phrase(self):
        self.assertTrue(
            MessageMatcher.matches("выкл бот", "пожалуйста выкл бот", CommandSettingsMethods.NORMAL)
        )

    def test_regular_matches_regex(self):
        self.assertTrue(
            MessageMatcher.matches(r"бот\w*", "мой ботик тут", CommandSettingsMethods.REGULAR)
        )


class AuthorizationTests(unittest.TestCase):
    def test_private_commands_require_admin(self):
        admin_context = HandlerContext(
            chat=MagicMock(chat_id="1"),
            user=User(user_id=100, admin_id=100, peer_id=1),
            message_text="test",
        )
        user_context = HandlerContext(
            chat=MagicMock(chat_id="1"),
            user=User(user_id=200, admin_id=100, peer_id=1),
            message_text="test",
        )

        self.assertTrue(AuthorizationService.can_execute_private_command(admin_context))
        self.assertFalse(AuthorizationService.can_execute_private_command(user_context))


class ChatScheduleTests(unittest.TestCase):
    def test_custom_time_range(self):
        chat_settings = ChatSettingsBody(
            enabled=True,
            time_work=ChatSettingsBodyTimeWork(
                type=TimeWorkEnum.CUSTOM,
                time_zone="UTC",
                time_from="09:00",
                time_to="18:00",
            ),
        )

        self.assertTrue(
            Chat._is_time_in_range(time(10, 0), time(9, 0), time(18, 0))
        )
        self.assertFalse(
            Chat._is_time_in_range(time(20, 0), time(9, 0), time(18, 0))
        )


class SettingsModelSourceTests(unittest.TestCase):
    def test_init_settings_imports_package_model(self):
        settings_path = (
            Path(__file__).resolve().parents[1]
            / "shablbot"
            / "init"
            / "settings"
            / "settings.py"
        )
        settings_source = settings_path.read_text(encoding="utf-8")

        self.assertIn("from shablbot.settings import SettingsModel", settings_source)
        self.assertNotIn("settings_model.py", settings_source)


class CommandHandlerTests(unittest.TestCase):
    def test_private_command_ignored_for_non_admin(self):
        command = MagicMock()
        command.command_type = "private"
        command.get_templates.return_value = ["secret"]
        command.command_settings.method = CommandSettingsMethods.NORMAL

        commands = MagicMock()
        commands.get_commands.return_value = {
            "public": {},
            "private": {"secret_cmd": command},
        }

        handler = CommandHandler(
            settings=MagicMock(ADMIN_ID=1),
            commands=commands,
            chats=MagicMock(),
            logger=MagicMock(),
        )

        context = HandlerContext(
            chat=MagicMock(chat_id="2"),
            user=User(user_id=999, admin_id=1, peer_id=2),
            message_text="secret",
        )

        self.assertFalse(handler.check_message(context))


if __name__ == "__main__":
    unittest.main()
