from __future__ import annotations

from collections import defaultdict, deque
from typing import Deque, Dict, List, Literal

from shablbot.core.ai.providers import (
    AIProviderError,
    AIProviderName,
    OpenAICompatibleProvider,
)
from shablbot.settings.settings_model import AISettings, AIProviderConfig


ProviderName = Literal["openrouter", "polza"]


class AIChatService:
    """Сервис диалога с нейросетями через OpenRouter и Polza.ai."""

    def __init__(self, settings: AISettings) -> None:
        self.settings = settings
        self._history: Dict[str, Deque[Dict[str, str]]] = defaultdict(deque)
        self._providers = {
            AIProviderName.OPENROUTER: OpenAICompatibleProvider(
                AIProviderName.OPENROUTER,
                settings.openrouter,
                settings.timeout,
            ),
            AIProviderName.POLZA: OpenAICompatibleProvider(
                AIProviderName.POLZA,
                settings.polza,
                settings.timeout,
            ),
        }

    def is_enabled(self) -> bool:
        return self.settings.enabled and any(
            provider.is_configured for provider in self._providers.values()
        )

    def ask(
        self,
        provider_name: ProviderName,
        user_id: int,
        prompt: str,
        model: str | None = None,
    ) -> str:
        if not self.settings.enabled:
            raise AIProviderError("AI-модуль отключён в настройках (AI_SETTINGS.enabled=false).")

        provider = self._get_provider(provider_name)
        history_key = self._history_key(user_id, provider_name)
        messages = self._build_messages(provider.config, history_key, prompt)
        answer = provider.complete(messages, model=model)
        self._remember_exchange(history_key, prompt, answer)
        return self._truncate_for_vk(answer)

    def ask_default(self, user_id: int, prompt: str, model: str | None = None) -> str:
        return self.ask(self.settings.default_provider, user_id, prompt, model=model)

    def _get_provider(self, provider_name: ProviderName) -> OpenAICompatibleProvider:
        try:
            provider_key = AIProviderName(provider_name)
        except ValueError as error:
            raise AIProviderError(f"Неизвестный провайдер: {provider_name}") from error

        return self._providers[provider_key]

    @staticmethod
    def _history_key(user_id: int, provider_name: str) -> str:
        return f"{user_id}:{provider_name}"

    def _build_messages(
        self,
        provider_config: AIProviderConfig,
        history_key: str,
        prompt: str,
    ) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": provider_config.system_prompt}
        ]
        messages.extend(self._history[history_key])
        messages.append({"role": "user", "content": prompt})
        return messages

    def _remember_exchange(self, history_key: str, prompt: str, answer: str) -> None:
        if self.settings.history_limit <= 0:
            return

        history = self._history[history_key]
        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": answer})

        while len(history) > self.settings.history_limit * 2:
            history.popleft()

    @staticmethod
    def _truncate_for_vk(text: str, limit: int = 4000) -> str:
        if len(text) <= limit:
            return text
        return text[: limit - 1] + "…"
