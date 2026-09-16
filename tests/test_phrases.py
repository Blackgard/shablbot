import json
from pathlib import Path

from shablbot.models.phrases import PhraseBody


def test_phrase_body_allows_partial_answer_tiers():
    body = PhraseBody(
        group="прощание",
        words={
            "пока": {
                "templates": ["пока"],
                "answer": {"common": ["Ходор..."]},
            }
        },
    )
    assert body.words["пока"].answer.common == ["Ходор..."]
    assert body.words["пока"].answer.rare is None


def test_hodor_bye_phrase_file_loads():
    phrase_path = Path(__file__).resolve().parents[1] / "deploy/hodor/bot/phrases/bye.json"
    data = json.loads(phrase_path.read_text(encoding="utf-8"))
    body = PhraseBody(**data)
    assert "пока" in body.words
