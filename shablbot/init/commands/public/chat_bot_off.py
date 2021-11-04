from shablbot.components.chat import Chat

def command(processed_chat: Chat) -> None:
    processed_chat.turn_off()

command_settings = {
    "code": "bot_off",
    "name": "Выключить бота",
    "templates": ["выкл бот", "бот выкл"],
    "answer": "Теперь бот не читает сообщения в чате",
    "description": "Команда для выключения бота в чате (Внутри чата)",
    "method": "normal",
    "need": ["processed_chat",],
    "entry_point": command
}
