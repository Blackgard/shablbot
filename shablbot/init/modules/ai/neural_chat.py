import re
from typing import Optional

from shablbot.core.ai import AIChatService, AIProviderError
from shablbot.models.handler_context import HandlerContext

_SERVICE: Optional[AIChatService] = None


def _get_service() -> AIChatService:
    global _SERVICE
    if _SERVICE is None:
        from settings.settings import SETTINGS

        _SERVICE = AIChatService(SETTINGS.AI_SETTINGS)
    return _SERVICE


def _extract_prompt(context: HandlerContext, patterns: list[str]) -> str:
    message = context.message_text.strip()
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""


def activate_module(func_name: str, context: HandlerContext = None) -> str:
    """Входная точка модуля нейросетей."""
    if context is None:
        return "Модуль нейросетей требует контекст сообщения."

    patterns = settings["templates"].get(func_name, [])
    prompt = _extract_prompt(context, patterns)

    if not prompt:
        return (
            "Напишите вопрос после команды.\n"
            "Примеры:\n"
            "• ии Привет!\n"
            "• openrouter Объясни квантовую физику\n"
            "• polza Напиши стих про кота"
        )

    try:
        service = _get_service()

        if func_name == "openrouter":
            return service.ask("openrouter", context.from_id, prompt)
        if func_name == "polza":
            return service.ask("polza", context.from_id, prompt)
        if func_name == "ask":
            return service.ask_default(context.from_id, prompt)

        return "Неизвестная команда нейросети."
    except AIProviderError as error:
        return f"Ошибка AI: {error}"
    except Exception as error:
        return f"Не удалось получить ответ нейросети: {error}"


settings = {
    "name": "Neural chat",
    "version": "1.0.0",
    "author": "ShablBot",
    "date_created": "16.09.2026",
    "entry_point": activate_module,
    "func": {
        "ask": {
            "name": "ask",
            "description": "Запрос к провайдеру по умолчанию",
            "entry_point": activate_module,
        },
        "openrouter": {
            "name": "openrouter",
            "description": "Запрос через OpenRouter",
            "entry_point": activate_module,
        },
        "polza": {
            "name": "polza",
            "description": "Запрос через Polza.ai",
            "entry_point": activate_module,
        },
    },
    "templates": {
        "ask": [r"(?i)^(?:ии|ai|gpt)\s+(.+)$"],
        "openrouter": [r"(?i)^(?:openrouter|ор)\s+(.+)$"],
        "polza": [r"(?i)^(?:polza|польза)\s+(.+)$"],
    },
}
