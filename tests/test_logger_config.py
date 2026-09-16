import sys
import unittest

from shablbot.core.utils import normalize_logger_config
from shablbot.settings.settings_model import LoggerConfig


class LoggerConfigTests(unittest.TestCase):
    def test_string_stderr_sink(self):
        config = LoggerConfig(
            handlers=[{"sink": "stderr", "format": "test"}]
        ).model_dump(exclude_none=True)
        normalized = normalize_logger_config(config)
        self.assertIs(normalized["handlers"][0]["sink"], sys.stderr)

    def test_serialization_iterator_fallback(self):
        broken = LoggerConfig(
            handlers=[{"sink": sys.stderr, "format": "test"}]
        ).model_dump(exclude_none=True)
        self.assertEqual(
            type(broken["handlers"][0]["sink"]).__name__,
            "SerializationIterator",
        )
        normalized = normalize_logger_config(broken)
        self.assertIs(normalized["handlers"][0]["sink"], sys.stderr)


if __name__ == "__main__":
    unittest.main()
