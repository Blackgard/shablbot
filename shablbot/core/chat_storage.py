from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any
from pydantic import ValidationError

from shablbot.settings.settings_model import ChatSettingsBody


class ChatSettingsStorage:
    """JSON-хранилище настроек чатов."""

    def __init__(self, path: Path, logger: Any) -> None:
        self.path = path
        self.logger = logger

    def load(self) -> Dict[str, ChatSettingsBody]:
        if not self.path.exists():
            return {}

        try:
            raw_data = json.loads(self.path.read_text(encoding="utf-8"))
            return {
                str(chat_id): ChatSettingsBody.model_validate(settings)
                for chat_id, settings in raw_data.items()
            }
        except (OSError, json.JSONDecodeError, ValidationError, TypeError) as error:
            self.logger.error(
                f"Не удалось загрузить настройки чатов из '{self.path}': {error}"
            )
            return {}

    def save(self, chats: Dict[str, ChatSettingsBody]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            chat_id: settings.model_dump(mode="json")
            for chat_id, settings in chats.items()
        }
        self.path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
