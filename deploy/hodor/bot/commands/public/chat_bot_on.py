from shablbot.components.chat import Chat

def command(processed_chat: Chat) -> None:
    processed_chat.turn_on()

command_settings = {
    "code": "bot_on",
    "name": "Включить бота",
    "templates": ["вкл бот", "бот вкл"],
    "answer": "Теперь бот читает сообщения в чате",
    "description": "Команда для включения бота в чате (Внутри чата)",
    "method": "normal",
    "need": ["processed_chat",],
    "entry_point": command
}
