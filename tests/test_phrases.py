import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from shablbot.components.phrases import Phrase
from shablbot.models.phrases import PhraseBody


class PhraseBodyModelTests(unittest.TestCase):
    def test_partial_answer_tiers_default_to_none(self):
        body = PhraseBody(
            group="прощание",
            words={
                "пока": {
                    "templates": ["пока"],
                    "answer": {"common": ["Ходор..."]},
                }
            },
        )
        self.assertEqual(body.words["пока"].answer.common, ["Ходор..."])
        self.assertIsNone(body.words["пока"].answer.rare)

    def test_hodor_bye_phrase_file_loads(self):
        phrase_path = (
            Path(__file__).resolve().parents[1]
            / "deploy/hodor/bot/phrases/bye.json"
        )
        data = json.loads(phrase_path.read_text(encoding="utf-8"))
        body = PhraseBody(**data)
        self.assertIn("пока", body.words)


class PhraseMatchingTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.phrase_path = Path(self.temp_dir.name) / "hello.json"
        self.phrase_path.write_text(
            json.dumps(
                {
                    "group": "приветствие",
                    "words": {
                        "привет": {
                            "templates": ["привет"],
                            "answer": {"common": ["Ходор!"]},
                        }
                    },
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        self.phrase = Phrase(self.phrase_path, MagicMock())

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_matches_without_prefix_in_private_chat(self):
        matches = self.phrase.find_match_with_message("привет")
        self.assertEqual(len(matches), 1)

    def test_accepts_prefix_keyword_argument(self):
        matches = self.phrase.find_match_with_message(
            "ходор привет",
            prefix=r"ходор\s.*?",
        )
        self.assertEqual(len(matches), 1)

    def test_requires_prefix_in_group_chat(self):
        no_prefix = self.phrase.find_match_with_message(
            "привет",
            prefix=r"ходор\s.*?",
        )
        self.assertEqual(no_prefix, [])


if __name__ == "__main__":
    unittest.main()
