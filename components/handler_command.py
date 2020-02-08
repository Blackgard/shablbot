from settings import SETTINGS
from components.cache import CACHE

def parse_message_com(message, user_id, chat_id, botAPI):
    """
    Проверка полученного сервервером сообщение на наличие команд.

    `:param: (str) message`  - обрабатываемое сообщение\n
    `:param: (int) user_id`  - id пользователя отправившего сообщение\n
    `:param: (int) chat_id` - id группы из которой поступило сообщение

    Если совпадения найдены, возвращает `первым параметром id группы или пользователя`, 
    которому необходимо вернуть ответ, а `вторым параметром сам ответ`.

    ```python
    parse_message_com("Выкл бота", 159233229, 200000000, vk_api)
    ==> [200000000, "Бот был включен"]
    ```

    Если совпадения не были найденный, возвращает два значения типа None.

    ```
    parse_message_com("", 159233229, 200000000, vk_api)
    ==> [None, None]
    ```
    """
    import re
    message       = message.lower()
    dict_commands = SETTINGS.command.items()
    
    for type_com, commands in dict_commands:
        for name_com, templates in commands.items():
            for template in templates:             

                if re.search(template, message):                    
                    if type_com == "public":
                        return execute_public_com(
                            name_com=name_com, 
                            chat_id=chat_id 
                        )

                    if type_com == "private" and user_id == SETTINGS.admin_id:
                        return execute_private_com(
                            command=message,
                            name_com=name_com,
                            chat_id=chat_id, 
                            bot=botAPI
                        )
    
    return None, None

def execute_public_com(name_com, chat_id, admin_id=SETTINGS.admin_id):
    """
    Обрабатывает команды доступные всем пользователям имеющим доступ к 
    паблику или беседе, в которой бот находится.
    """

    if name_com == SETTINGS.list_all_com[0][0]: # включить бота
        CACHE.settings_chat[chat_id]["included"] = True
        print(f"В группе #{chat_id}, бот вкл.")

        return chat_id, "Бот был включен"

    elif name_com == SETTINGS.list_all_com[1][0]: # выключить бота
        CACHE.settings_chat[chat_id]["included"] = False
        print(f"В группе #{chat_id}, бот выкл.")

        return chat_id, "Бот был выключен"

    elif name_com == SETTINGS.list_all_com[2][0]: # покажи стат группы
        answer_stat_chat = ""
        for type_phrases, count in CACHE.counter_word[chat_id].most_common():
            answer_stat_chat += f"Сообщение с редкостью {type_phrases} встречалась {count} раз \n"
        print(f"Группа #{chat_id}, запросила статистику по словам.")

        if not bool(answer_stat_chat):
            answer_stat_chat = "Не было найдено совпадений, напишите что-нибудь"

        return chat_id, answer_stat_chat

    answer_error = "Ошибка, команда не была найдена"
    if SETTINGS.debug:
        print(answer_error)
    return admin_id, answer_error

def execute_private_com(command, name_com, bot, chat_id, admin_id=SETTINGS.admin_id):
    """
    Обрабатывает команды доступные только администратору бота.
    """
    if name_com == SETTINGS.list_all_com[3][0]: # Помощь
        answer_com_help = ""
        for com, description in SETTINGS.list_all_com:
            if com == SETTINGS.list_all_com[3][0]:
                continue
            answer_com_help += f"  {com} - {description}.\n\n"

        return admin_id, answer_com_help.title()

    elif name_com == SETTINGS.list_all_com[4][0]: # покажи всю стат
        answer_com_stat = CACHE.counter_word
        print(f"Администратор id{admin_id}, запросил всю статистику по словам.")
        
        return admin_id, answer_com_stat

    elif name_com == SETTINGS.list_all_com[5][0]: # сменить время работы группы {id_chats}

        import re
        from components.chat_settings import get_settings_chat, modify_settings_chat

        answer_swap_time_work = ""
        error_message =  "Время работы группы не было изменено. Проверьте правильность введенных данных."
        try:
            args_command  = command.split()
            params_command = [ "CUSTOM" ]

            for arg in args_command:
                if arg.isdigit() or re.search(":", arg):
                    params_command.append(arg)

            modify_chat_id = int(params_command[1])

            new_settings_chat = get_settings_chat(
                type_time=params_command[0],
                chat_id=modify_chat_id,            
                t_from=params_command[2],
                t_to=params_command[3]
            )
        except:
            answer_swap_time_work = error_message
            return admin_id, answer_swap_time_work
        
        err_on_swap = modify_settings_chat(
            modify_chat_id, 
            new_settings_chat
        )

        if err_on_swap:
            answer_swap_time_work = f"Время работы группы {modify_chat_id} было успешно сменено."
        else:
            answer_swap_time_work = error_message

        return admin_id, answer_swap_time_work

    elif name_com == SETTINGS.list_all_com[6][0]: # покажи id групп
        answer_show_grops = ""
        
        info_chats = bot.messages.getConversationsById(
            peer_ids=[*(CACHE.settings_chat.keys())],
            extended=1,
            fields=["title"],
            chat_id=SETTINGS.bot_chat_id
        )
        
        for chat in info_chats["items"]:
            chat_id = chat["peer"]["id"]
            if chat_id >= 2000000000:
                answer_show_grops += f"{chat['chat_settings']['title']} - {chat_id}\n"

        if not answer_show_grops:
            answer_show_grops = "Бот еще не сохранил ни одну группу"

        return admin_id, answer_show_grops
    
    else:
        answer_error = "Ошибка, команда не была найдена"

        if SETTINGS.debug:
            print(answer_error)

        return admin_id, answer_error