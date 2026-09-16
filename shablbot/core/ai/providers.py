from __future__ import annotations

from typing import Any, Dict, List

import requests

from shablbot.settings.settings_model import AISettings


class AIProviderError(Exception):
    """Ошибка при обращении к AI-провайдеру."""


class OpenAICompatibleProvider:
    """Клиент для OpenAI-совместимых API (OpenRouter, Polza.ai)."""

    def __init__(self, settings: AISettings) -> None:
        self.settings = settings

    def complete(self, messages: List[Dict[str, str]]) -> str:
        if not self.settings.is_configured:
            raise AIProviderError(
                "AI не настроен. Проверьте AI_ENABLED, AI_PROVIDER, API-ключ и AI_MODEL в .env."
            )

        payload = {
            "model": self.settings.model,
            "messages": messages,
            "temperature": self.settings.temperature,
            "max_tokens": self.settings.max_tokens,
        }

        headers = {
            "Authorization": f"Bearer {self.settings.api_key}",
            "Content-Type": "application/json",
        }

        if self.settings.provider == "openrouter":
            if self.settings.http_referer:
                headers["HTTP-Referer"] = self.settings.http_referer
            if self.settings.site_title:
                headers["X-OpenRouter-Title"] = self.settings.site_title

        url = f"{self.settings.base_url.rstrip('/')}/chat/completions"

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.settings.timeout,
            )
        except requests.RequestException as error:
            raise AIProviderError(
                f"Не удалось связаться с {self.settings.provider}: {error}"
            ) from error

        if response.status_code >= 400:
            raise AIProviderError(
                self._format_api_error(response.status_code, response.text)
            )

        return self._extract_content(response.json())

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
