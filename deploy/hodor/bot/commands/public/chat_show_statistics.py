from shablbot.components.chat import Chat

def command(processed_chat: Chat) -> str:
    return processed_chat.show_statistics()

command_settings = {
    "code": "show_statictics",
    "name": "Показать статистику группы",
    "templates": ["покажи статус групп", "показать стат групп "],
    "answer": r"{=result}",
    "description": "Команда показывает какое количество ответов разного уровня редкости выпало в чате",
    "method": "normal",
    "need": ["processed_chat",],
    "entry_point": command
}
