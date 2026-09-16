from shablbot.components.chat import Chats

def command(chats: Chats) -> None:
    state_chat_on = "Включен (on)"
    state_chat_off = "Выключен (off)"
    str_format = "{0} ({1}) | Состояние: {2}"

    answer = "\n\n".join([
        str_format.format(
            chat.chat_title,
            chat.chat_id,
            state_chat_on if chat.chat_settings.enabled else state_chat_off
        )
        for chat in chats.chats.values()
    ])
    return answer

command_settings = {
    "code": "show_id_active_chats",
    "name": "Показать id всех активных чатов",
    "templates": [
        "покажи id групп",
        "покажи id чатов",
        "покажи id бесед",
        "показать id групп",
        "показать id чатов",
        "показать id бесед",
    ],
    "answer": r"{=result}",
    "description": "Команда отображает id чатов, в которых бот был активен",
    "method": "normal",
    "need": ["chats",],
    "entry_point": command
}
