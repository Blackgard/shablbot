from __future__ import annotations

from collections import defaultdict, deque
from typing import Deque, Dict, List

from shablbot.core.ai.actions import execute_bot_action, parse_ai_action_response
from shablbot.core.ai.prompts import build_standalone_system_prompt
from shablbot.core.ai.providers import AIProviderError, OpenAICompatibleProvider
from shablbot.components.command import Commands
from shablbot.models.handler_context import HandlerContext
from shablbot.settings.settings_model import AISettings


class AIChatService:
    """Сервис диалога с нейросетью через выбранный в .env провайдер."""

    def __init__(self, settings: AISettings) -> None:
        self.settings = settings
        self._provider = OpenAICompatibleProvider(settings)
        self._history: Dict[str, Deque[Dict[str, str]]] = defaultdict(deque)

    def is_enabled(self) -> bool:
        return self.settings.is_configured

    def ask(self, user_id: int, prompt: str) -> str:
        if not self.settings.enabled:
            raise AIProviderError("AI отключён. Установите AI_ENABLED=true в .env.")

        history_key = str(user_id)
        messages = self._build_messages(
            history_key, prompt, self.settings.system_prompt
        )
        answer = self._provider.complete(messages)
        self._remember_exchange(history_key, prompt, answer)
        return self._truncate_for_vk(answer)

    def ask_standalone(
        self,
        context: HandlerContext,
        commands: Commands,
    ) -> str:
        if not self.settings.is_standalone:
            raise AIProviderError("Standalone-режим AI не включён (AI_MODE=standalone).")

        history_key = str(context.from_id)
        system_prompt = build_standalone_system_prompt(self.settings.system_prompt)
        messages = self._build_messages(
            history_key, context.message_text, system_prompt
        )
        raw_answer = self._provider.complete(messages)
        action, reply = parse_ai_action_response(raw_answer)

        action_reply = execute_bot_action(action, context, commands)
        final_reply = action_reply if action_reply is not None else reply

        self._remember_exchange(history_key, context.message_text, final_reply)
        return self._truncate_for_vk(final_reply)

    def _build_messages(
        self,
        history_key: str,
        prompt: str,
        system_prompt: str,
    ) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt}
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
