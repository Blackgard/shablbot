from settings import SETTINGS
from components.cache import CACHE
import logging
import json

def parse_message_com(message, user_id, chat_id, botAPI):
    """
    Проверка полученного сервером сообщения на наличие команд.

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
        sett_chat = CACHE.get_settings_chat(chat_id)
        sett_chat['included'] = True
        
        CACHE.set_settings_chat(chat_id,  sett_chat)
        logging.info(f"id{chat_id} - бот был включен.")

        return chat_id, "Бот был включен"

    elif name_com == SETTINGS.list_all_com[1][0]: # выключить бота
        sett_chat = CACHE.get_settings_chat(chat_id)
        sett_chat['included'] = False
        
        CACHE.set_settings_chat(chat_id,  sett_chat)
        logging.info(f"id{chat_id} - бот был выключен.")

        return chat_id, "Бот был выключен"

    elif name_com == SETTINGS.list_all_com[2][0]: # покажи стат группы
        answer_stat_chat = ""
        for type_phrases, count in CACHE.get_counter_word(chat_id).most_common():
            answer_stat_chat += f"Сообщение с редкостью {type_phrases} встречалась {count} раз \n"
        logging.info(f"id{chat_id} - запросила статистику по словам.")

        if not bool(answer_stat_chat):
            answer_stat_chat = "Не было найдено совпадений, напишите что-нибудь"

        return chat_id, answer_stat_chat

    answer_error = "Ошибка, команда не была найдена"
    if SETTINGS.debug:
        logging.warning(answer_error)
    
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
            answer_com_help += f"{com} - {description}.\n\n"

        return admin_id, answer_com_help.capitalize()

    elif name_com == SETTINGS.list_all_com[4][0]: # покажи всю стат
        counter_word_all = CACHE.get_counter_word()
        counter_array = []
        
        for id_group, counter in counter_word_all.items():
             counter_array.append( {id_group : dict(counter)} )   
        
        answer_com_stat = json.dumps(counter_array, indent=4, sort_keys=True)
        logging.info(f"Админ id{admin_id} - запросил всю статистику по словам.")
        
        return admin_id, answer_com_stat

    elif name_com == SETTINGS.list_all_com[5][0]: # сменить время работы группы {id_chats}

        import re
        
        from components.chat_settings import get_settings_chat, modify_settings_chat

        answer_swap_time_work = ""
        error_message =  """
        Время работы группы не было изменено. Проверьте правильность введенных данных.
        Шаблон : сменить время 123456789 c 00:00 по 8:00
        """
        try:
            args_command  = command.split()
            params_command = [ ("CUSTOM", SETTINGS.time_zone) ]

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
        except Exception as err:
            answer_swap_time_work = error_message
            if SETTINGS.debug:
                logging.debug(f"handler_command.execute_private_com:\n\tparams_command -> {params_command},\n\terror -> {err}")
            return admin_id, answer_swap_time_work
        
        if SETTINGS.debug:
                logging.debug(f"handler_command.execute_private_com:\n\tparams_command -> {params_command},\n\tnew_settings_chat -> {new_settings_chat}")
        
        isModify = modify_settings_chat(
            modify_chat_id, 
            new_settings_chat
        )

        if isModify:
            answer_swap_time_work = f"Время работы группы @[id{modify_chat_id}|{modify_chat_id}] было успешно сменено."
            logging.info(f"id{chat_id} сменил время работы группы id{modify_chat_id} [с {new_settings_chat['from'].strftime('%H:%M')} по {new_settings_chat['to'].strftime('%H:%M')}]")
        else:
            answer_swap_time_work = error_message
        
        return admin_id, answer_swap_time_work

    elif name_com == SETTINGS.list_all_com[6][0]: # покажи id групп
        answer_show_grops = ""
        
        info_chats = bot.messages.getConversationsById(
            peer_ids=[*(CACHE.get_settings_chat().keys())],
            extended=1,
            fields=["title"],
            chat_id=SETTINGS.bot_chat_id
        )
        
        for number_chat in range(info_chats["count"]):
            chat_info = info_chats['items'][number_chat]
            prof_info = info_chats['profiles'][number_chat]
            
            chat_id = chat_info["peer"]["id"]
            isUser  = chat_info["peer"]['type'] == 'user'
            
            if isUser:
                answer_show_grops += f"[user] {prof_info['first_name']} {prof_info['last_name']} - @[id{prof_info['id']}|{prof_info['id']}]\n"
            else:
                answer_show_grops += f"[chat] { chat_info['chat_settings']['title']} - @[id{chat_id}|{chat_id}]\n"

        if not answer_show_grops:
            answer_show_grops = "Бот еще не сохранил ни одну группу"
            if SETTINGS.debug:
                logging.debug(info_chats)

        return admin_id, answer_show_grops
    
    
    answer_error = "Ошибка, команда не была найдена"

    if SETTINGS.debug:
        logging.warning(answer_error)

    return admin_id, answer_error