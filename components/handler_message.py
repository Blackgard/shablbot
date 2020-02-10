import sys

from settings         import SETTINGS
from components.cache import (  
    add_single_value_counter_chat, 
    save_chat_to_cache, 
    CACHE
)

from components.time_work       import check_work_time
from components.handler_command import parse_message_com
from components.handler_modules import parse_message_module

def get_random_id():
    import random

    return random.getrandbits(31) * random.choice([-1, 1])

def write_msg(answer, chat_id, botAPI):
    """
    Функция для отправки ответа бота на сообщения пользователя

    Параметры
    ---
    ```
    str    : answer   - ответ бота на полученное сообщение
    int    : chat_id  - id группы в которое необходимо отправить сообщение
    object : botAPI   - обьект позволяющий обращаться от имени бота к VkApi.
    ```

    Примеры
    ---
    Функция не возвращает значения, но оповещает в лог `[print()]` о результате отправки сообщения
    ```

    write_msg("Answer", 123456789, botAPI)
    ==> None 
    Сообщение было отправленно

    write_msg("Answer", None, None)
    ==> None
    При отправке сообщения произошла ошибка
    ```
    """
    try:
        botAPI.messages.send(
            peer_id     = int(chat_id),
            message     = str(answer),
            random_id   = get_random_id()
        )
    except:
        print("При отправке сообщения произошла ошибка")
    
    if SETTINGS.debug:
        print(f"Было отправленно сообщение: '{answer}' (id беседы: {chat_id})")


def choice_of_answer(found_matches):
    """
    Функция для выбора на какой из найденных шаблонных фраз ответить боту, 
    приоритет отдается последнему элементу массива `found_matches`.

    Параметры
    ---
    ```
    list : found_matches   - массив содержащий котреж из регулярного выражения 
    и текста найденного по этому выражению
    ```

    Примеры
    ---

    ```
    choice_of_answer([ 
        ("t.xt"  ," text"  ),
        ("s.mpl.", "simple")
    ])
    ==> {
        "common" : [
                "Simple text it"s nice"
            ],

        "uncommon" : [
                "I like simple text"
            ],
    }
    
    choice_of_answer("")
    ==> None
    ```
    """

    word_answer = ""
    for index_temp in found_matches:
        for def_templ in SETTINGS.def_templ:
            word_answer = index_temp[0].replace(def_templ + SETTINGS.join_templ, "") 

    if word_answer:
        return SETTINGS.templ_and_respons.get(word_answer)
    return None

def find_matches(message):
    """
    Поиск в тексте слов из шаблонов находящихся в "SETTINGS.all_templ" для ответа.

    Параметры
    ---
    ```
    str : message - сообщение полученое ботом
    ```

    Логика работы
    ---
    Функция принимает на вход сообщение полученное ботом, а на выходе выдает
    список с найденными совпадениями в виде кортежа:\n
        ("регулярное выражение","найденный текст")
    ```

    find_matches("simple text")
    ==> [ 
        ("t.xt"  , "text"  )
        ("s.mpl.", "simple")
    ]
    
    find_matches("")
    ==> None
    ```
    """
    import re

    message      = message.lower()
    find         = []
    default_tmps = SETTINGS.def_templ
    join_tmp     = SETTINGS.join_templ

    for def_tmp in default_tmps:
        find_def = re.findall(def_tmp, message)
        if bool(find_def):
            find.append( (def_tmp, find_def[0]) )

    for _, value in SETTINGS.all_templ.items():
        for _, template in value.items():
            for def_tmp in default_tmps:
                find_templ = def_tmp + join_tmp + template
                find_match = re.findall(find_templ, message)

                if bool(find_match):
                    find.append( (find_templ, find_match[0]) )

    if bool(find):
        return find
    else:
        return None


def choise_answer(list_answer, chat_id, botAPI):
    """
    Функция выбора варианта ответа из представленного в первом параметре списка.\n
    Чем ближе список к концу, тем реже встречаются данные ответы.

    Параметры
    ---
    ```
    dict   : list_answer - все доступные варинаты ответа на найденые совпадения с ключивыми словами
    int    : chat_id     - группа или человек от которого сервер получил сообщение
    object : botAPI      - обьект позволяющий обращаться от имени бота к VkApi.
    ```
    """
    import random
    
    prohabilities   = SETTINGS.prohabilities
    actial_proha    = { 
        name_proh : value_proh 
        for name_proh, value_proh 
        in prohabilities.items() 
        if list_answer.get(name_proh)
    }
    type_answer     = random.choices(
        [*actial_proha.keys()], 
        weights=[*actial_proha.values()]
    )[0]
    answer          = random.choice(
        list_answer[type_answer]
    )

    add_single_value_counter_chat(chat_id, type_answer)

    write_msg(
        answer=answer, 
        chat_id=chat_id, 
        botAPI=botAPI
    )

def check_on_com_and_module(message, eventObj, botAPI):
    user_id_com, answer_com = parse_message_com(
        message=message, 
        user_id=eventObj.from_id, 
        chat_id=eventObj.peer_id,
        botAPI=botAPI
    ) 

    user_id_module, answer_module = parse_message_module(
        message=message, 
        user_id=eventObj.from_id, 
        chat_id=eventObj.peer_id,
        botAPI=botAPI
    )

    if bool(answer_com):
        return user_id_com, answer_com
    elif bool(answer_module):
        return user_id_module, answer_module
    return None, None

def handler_message(eventObj, chat_id, botAPI):
    """
    Функция для обработки полученного от сервера сообщения.

    Параметры
    ----------
    ```
    dict   : eventObj - обьект VkApi хранящий в себе все данные о принятом сервером сообщении
    int    : chat_id  - группа или человек от которого сервер получил сообщение
    object : botAPI   - обьект позволяющий обращаться от имени бота к VkApi
    ```
    """
    
    message     = eventObj.text.lower()
    save_chat_to_cache(chat_id)
    on_time     = check_work_time(chat_id)

    chat_id_com_or_mod, answer_com_or_module = check_on_com_and_module(
        message=message,
        eventObj=eventObj,
        botAPI=botAPI
    )
    
    if answer_com_or_module is not None:
        write_msg(
            answer  = answer_com_or_module, 
            chat_id = chat_id_com_or_mod, 
            botAPI  = botAPI
        )
    elif CACHE.get_settings_chat(chat_id)["included"] and on_time is not False:
        found_matches = find_matches(message)

        if SETTINGS.debug:
            print(f"Найденные совпадения: {found_matches}")

        if found_matches is not None:                
            answers = choice_of_answer(found_matches)
            
            if answers is not None:
                choise_answer(
                    answers, 
                    eventObj.peer_id, 
                    botAPI
                )