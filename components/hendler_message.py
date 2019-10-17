import re
from settings import *
from components.cache import *
from components.time_work import check_work_time
from components.command import check_on_comm_bot

def write_msg(answer, chat_id, bot):
    """
    Функция для написания ответа на сообщения пользователя.

    :param (str) answer  - ответ бота на полученное сообщение
    :param (int) chat_id - id группы в которое необходимо отправить сообщение
    :param (object) bot  - обьект позволяющий обрашатся от имени бота к VkApi
    """

    from components.public_functions import get_random_id

    bot.messages.send(
        peer_id     = int(chat_id),
        message     = str(answer),
        random_id   = get_random_id()
    )
    print(f"Было отправленно сообщение: {answer} - группа: {chat_id}")


def choice_of_answer(found_matches):
    answer = CONST.def_templ
    for key, _ in found_matches[1:]:
        answer = key.replace(CONST.def_templ + CONST.join_templ, "") 
    return templ_and_respons[answer]


def find_matches(text):
    """
    Поиск в тексте слов из шаблонов находящихся в "CONST.all_templ" для ответа.\n
    Возращает кортеж из пары  ( шаблон : найденное слово )
    """
    find              = {}
    default_tmp       = CONST.def_templ
    join_tmp          = CONST.join_templ

    find[default_tmp] = re.findall(default_tmp, text)

    if not find[default_tmp]:
        return None

    for _, value in CONST.all_templ.items():
        for _, template in value.items():
            find[default_tmp + join_tmp + template] = re.findall(default_tmp + join_tmp + template, text) 

    return [(k,v[0]) for k,v in find.items() if v != []]


def choise_answer(list_answer, group_id, botAPI):
    """
    Функция выбора варианта ответа из предложенного списка, чем ближе список к концу, тем реже встречаются данные ответы.
    ---
    :param (str)    list_answer - все доступные варинаты ответа на найденые овпадения в шаблонах;
    :param (int)    group_id    - обьект VkApi храняший в себе все данные о принятом сообщении;
    :param (object) botAPI      - обьект позволяющий обрашатся от имени бота к VkApi.
    """
    import random

    prohabilities   = CONST.prohabilities
    actial_proha    = { k:v for k,v in prohabilities.items() if list_answer.get(k)}
    type_answer     = random.choices([*actial_proha.keys()], weights=[*actial_proha.values()])[0]
    answer          = random.choice(list_answer[type_answer])

    add_single_value(group_id, type_answer)

    write_msg(
        answer=answer, 
        chat_id=group_id, 
        bot=botAPI
    )


def handler(eventObj, group_id, botAPI):
    """
    Функция для обработки полученного от сервера сообщения.
    ----

    :param (object) eventObj    - обьект VkApi храняший в себе все данные о принятом сообщении;
    :param (int)    group_id    - Группа или человек от которого сервер уловил сообщение;
    :param (object) botAPI      - обьект позволяющий обрашатся от имени бота к VkApi. 
    """

    message = eventObj.text.lower()
    save_group_to_cache(group_id)

    user_id, answer_com = check_on_comm_bot(
        message=message, 
        user_id=eventObj.from_id, 
        group_id=group_id,
    ) 

    on_time = check_work_time(group_id)

    if bool(answer_com) and on_time :
        write_msg(answer_com, user_id, botAPI)
    else:
        if CACHE.included[group_id] and bool(on_time):    
            found_matches = find_matches(message)
            print(found_matches)

            if bool(found_matches):
                list_answer = choice_of_answer(found_matches)
                choise_answer(
                    list_answer, 
                    eventObj.peer_id, 
                    botAPI
                )