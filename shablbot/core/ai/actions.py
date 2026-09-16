import json
import re
from typing import Optional, Tuple

from shablbot.components.chat import Chat
from shablbot.components.command import Commands
from shablbot.models.handler_context import HandlerContext

ALLOWED_ACTIONS = {"none", "bot_off", "bot_on", "help"}


def parse_ai_action_response(text: str) -> Tuple[str, str]:
    """Разобрать JSON-ответ нейросети на action и reply."""
    text = text.strip()

    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return _normalize_action_data(data)
    except json.JSONDecodeError:
        pass

    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(0))
            if isinstance(data, dict):
                return _normalize_action_data(data)
        except json.JSONDecodeError:
            pass

    return "none", text


def _normalize_action_data(data: dict) -> Tuple[str, str]:
    action = str(data.get("action", "none")).strip().lower()
    reply = str(data.get("reply", "")).strip()

    if action not in ALLOWED_ACTIONS:
        action = "none"

    if not reply:
        reply = "Готово."

    return action, reply


def execute_bot_action(
    action: str,
    context: HandlerContext,
    commands: Commands,
) -> Optional[str]:
    """Выполнить действие бота. Возвращает текст ответа или None (использовать reply от AI)."""
    chat: Chat = context.chat

    if action == "bot_off":
        chat.turn_off()
        return None

    if action == "bot_on":
        chat.turn_on()
        return None

    if action == "help":
        help_command = commands.public_command.get("help")
        if help_command and help_command.is_loaded:
            return help_command.execute_command(processed_chat=chat)
        return "Справка по командам недоступна."

    return None
