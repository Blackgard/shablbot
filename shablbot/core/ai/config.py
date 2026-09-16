import os
from typing import Any, Dict

from shablbot.settings.settings_model import AISettings

PROVIDER_PRESETS: Dict[str, Dict[str, Any]] = {
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key_env": "OPENROUTER_API_KEY",
        "http_referer_env": "OPENROUTER_HTTP_REFERER",
        "site_title_env": "OPENROUTER_SITE_TITLE",
    },
    "polza": {
        "base_url": "https://polza.ai/api/v1",
        "api_key_env": "POLZA_API_KEY",
    },
}


def build_ai_settings_from_env() -> AISettings:
    """Собрать AISettings из переменных окружения."""
    provider = os.getenv("AI_PROVIDER", "openrouter").strip().lower()
    preset = PROVIDER_PRESETS.get(provider)

    if preset is None:
        raise ValueError(
            f"Неизвестный AI_PROVIDER='{provider}'. "
            f"Допустимые значения: {', '.join(PROVIDER_PRESETS)}"
        )

    return AISettings(
        enabled=os.getenv("AI_ENABLED", "false").strip().lower() == "true",
        provider=provider,
        model=os.getenv("AI_MODEL", "openai/gpt-4o-mini"),
        api_key=os.getenv(preset["api_key_env"], ""),
        base_url=preset["base_url"],
        system_prompt=os.getenv(
            "AI_SYSTEM_PROMPT",
            "Ты дружелюбный ассистент VK-бота. Отвечай кратко и по-русски.",
        ),
        max_tokens=int(os.getenv("AI_MAX_TOKENS", "1024")),
        temperature=float(os.getenv("AI_TEMPERATURE", "0.7")),
        history_limit=int(os.getenv("AI_HISTORY_LIMIT", "10")),
        timeout=float(os.getenv("AI_TIMEOUT", "60")),
        http_referer=os.getenv(preset.get("http_referer_env", ""), None) or None,
        site_title=os.getenv(preset.get("site_title_env", ""), "ShablBot") or "ShablBot",
    )
