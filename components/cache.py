from collections import Counter
import datetime as dt
from settings import CONST
from components.public_functions import setTime

class CACHE:
    time_work_group = {} 
    counter_word    = {}
    included        = {}

def set_time_work_delta(group_id, type_time = None, t_from = None, t_to = None):
    if not t_from and not t_to and not type_time:
        try:
            for _group_id, time_work in CONST.time_work_group.items():
                if _group_id == group_id:
                    type_time = time_work["type"]
                    break
            
            if type_time == None or type_time == CONST.def_time_work:
                return {
                    "type" : CONST.def_time_work
                }

            t_from  = setTime(CONST.time_work_group[group_id]["from"])
            t_to    = setTime(CONST.time_work_group[group_id]["to"])
        except EnvironmentError as err:
            print(err)

        return  {
            "type"  : type_time,
            "from"  : t_from,
            "to"    : t_to,
        }


def save_group_to_cache(group_id):
    """
    Функция задает начальные правила для работы бота с новой группой.
    ---
    Настройка правил производится с помощью дописания в данный блок новых модификаций.

    :param (int) group_id - уникальный идентификатор группы, для которой задаются правила (peer_id в vkApi).
    """
    find_group = CACHE.included.get(group_id)

    if find_group is None:
        CACHE.included[group_id]        = True
        CACHE.counter_word[group_id]    = Counter()
        CACHE.time_work_group[group_id] = set_time_work_delta(group_id)
        print(f"Была сохранена группа #{group_id}")

def add_single_value(group_id, type_answer):
    CACHE.counter_word[group_id] += Counter([type_answer])
