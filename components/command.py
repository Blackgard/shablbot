from settings import *
from components.cache import CACHE
import re

def check_on_comm_bot(message, user_id, group_id):

    bot_on = CACHE.included.get(group_id)

    for type_com, com in CONST.command[0].items():
        for name_com, templates in com.items():
            for template in templates['templates']:
                if re.search(template, message):                    
                    if type_com == "public":
                        return parse_public_com(name_com, group_id)

                    if type_com == "private":
                        return parse_private_com(name_com, user_id)

    return None, None


def parse_public_com(name_com, group_id):
    if name_com == CONST.list_all_com[0]: # включить бота
        CACHE.included[group_id] = True
        print(f"В группе #{group_id}, бот вкл.")

    if name_com == CONST.list_all_com[1]: # выключить бота
        CACHE.included[group_id] = False
        print(f"В группе #{group_id}, бот выкл.")

    if name_com == CONST.list_all_com[2]: # покажи стат группы
        answer = ""
        for type_phrases, count in CACHE.counter_word[group_id].most_common():
            answer += f"Сообщение с редкостью {type_phrases} встречалась {count} раз \n"
        print(f"Группа #{group_id}, запросила статистику по словам.")
        return group_id, answer


def parse_private_com(name_com, user_id=CONST.admin_id):
    if name_com == CONST.list_all_com[3]: # покажи всю стат
        print(f"Администратор id{user_id}, запросил всю статистику по словам.")
        return CONST.admin_id, f"{CACHE.counter_word}"