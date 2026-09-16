import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from shablbot.components.chat import Chat
from shablbot.core.chat_storage import ChatSettingsStorage
from shablbot.settings.settings_model import (
    ChatSettingsBody,
    ChatSettingsBodyTimeWork,
    TimeWorkEnum,
)


class ChatSettingsStorageTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.temp_dir.name) / "chat_settings.json"
        self.storage = ChatSettingsStorage(self.storage_path, MagicMock())

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load_roundtrip(self):
        settings = ChatSettingsBody(
            enabled=False,
            time_work=ChatSettingsBodyTimeWork(
                type=TimeWorkEnum.ALL,
                time_zone="UTC",
                time_from="00:00",
                time_to="23:59",
            ),
        )

        self.storage.save({"123": settings})
        loaded = self.storage.load()

        self.assertIn("123", loaded)
        self.assertFalse(loaded["123"].enabled)

    def test_load_missing_file_returns_empty_dict(self):
        self.assertEqual(self.storage.load(), {})


class ChatPersistenceCallbackTests(unittest.TestCase):
    def test_turn_off_triggers_persistence_callback(self):
        callback = MagicMock()
        chat = Chat(
            chat_id="123",
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
            on_settings_changed=callback,
        )

        chat.turn_off()

        callback.assert_called_once_with(chat)
        self.assertFalse(chat.chat_settings.enabled)


if __name__ == "__main__":
    unittest.main()
