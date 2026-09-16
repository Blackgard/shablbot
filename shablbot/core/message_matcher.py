import re
from typing import Union

from shablbot.models.command import CommandSettingsMethods


class MessageMatcher:
    """Сопоставление шаблонов с текстом сообщения."""

    @staticmethod
    def matches(
        template: str,
        message: str,
        method: Union[CommandSettingsMethods, str] = CommandSettingsMethods.NORMAL,
    ) -> bool:
        processed_message = message.lower()
        method_value = (
            method.value if isinstance(method, CommandSettingsMethods) else method
        )

        if method_value == CommandSettingsMethods.REGULAR.value:
            return bool(re.search(template, processed_message))

        template = template.lower().strip()
        if " " in template:
            return template in processed_message

        return template in processed_message.split()

    @staticmethod
    def matches_any(
        templates: list[str],
        message: str,
        method: Union[CommandSettingsMethods, str] = CommandSettingsMethods.REGULAR,
    ) -> bool:
        return any(
            MessageMatcher.matches(template, message, method) for template in templates
        )
