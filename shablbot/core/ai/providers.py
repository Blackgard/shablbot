from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

import requests

from shablbot.settings.settings_model import AIProviderConfig


class AIProviderName(str, Enum):
    OPENROUTER = "openrouter"
    POLZA = "polza"


class AIProviderError(Exception):
    """Ошибка при обращении к AI-провайдеру."""


class OpenAICompatibleProvider:
    """Клиент для OpenAI-совместимых API (OpenRouter, Polza.ai)."""

    def __init__(
        self,
        name: AIProviderName,
        config: AIProviderConfig,
        timeout: float,
    ) -> None:
        self.name = name
        self.config = config
        self.timeout = timeout

    @property
    def is_configured(self) -> bool:
        return self.config.enabled and bool(self.config.api_key.strip())

    def complete(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
    ) -> str:
        if not self.is_configured:
            raise AIProviderError(
                f"Провайдер {self.name.value} не настроен. Укажите API-ключ и enabled=true."
            )

        payload = {
            "model": model or self.config.default_model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        if self.name == AIProviderName.OPENROUTER:
            if self.config.http_referer:
                headers["HTTP-Referer"] = self.config.http_referer
            if self.config.site_title:
                headers["X-OpenRouter-Title"] = self.config.site_title

        url = f"{self.config.base_url.rstrip('/')}/chat/completions"

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as error:
            raise AIProviderError(
                f"Не удалось связаться с {self.name.value}: {error}"
            ) from error

        if response.status_code >= 400:
            raise AIProviderError(
                self._format_api_error(response.status_code, response.text)
            )

        data = response.json()
        return self._extract_content(data)

    @staticmethod
    def _extract_content(data: Dict[str, Any]) -> str:
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as error:
            raise AIProviderError("Провайдер вернул неожиданный формат ответа.") from error

        if not content:
            raise AIProviderError("Провайдер вернул пустой ответ.")

        return str(content).strip()

    @staticmethod
    def _format_api_error(status_code: int, body: str) -> str:
        short_body = body[:300].strip() if body else "без описания"
        return f"Ошибка API ({status_code}): {short_body}"
