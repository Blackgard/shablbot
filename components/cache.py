import datetime as dt
from collections import Counter

from settings import SETTINGS
class CACHE:
    """
    Класс реализующий функционал кэширования данных необходимых для работы бота
    """
    settings_chat  = {} 
    counter_word    = {}

from components.chat_settings import get_settings_chat

def save_chat_to_cache(chat_id, settings = None):
    """
    Функция задает начальные правила для работы бота с новой группой

    Параметры
    ---
    ```
    int  : chat_id  - уникальный идентификатор группы, для которой задаются правила
    dict : settings - настройки бота полученные из get_settings_chat (Не обязательный параметр) 
    ```
    """

    find_chat = CACHE.settings_chat.get(chat_id)
    try:
        if find_chat is None:
            if settings:
                CACHE.settings_chat[chat_id] = settings
            else:    
                CACHE.settings_chat[chat_id] = get_settings_chat(chat_id) 
            CACHE.counter_word[chat_id]    = Counter()

            if SETTINGS.debug:
                print(f"Была сохранена группа #{chat_id}")
    except:
        return False
    return True

def add_single_value_counter_chat(chat_id, type_word):
    try:
        CACHE.counter_word[chat_id] += Counter([type_word])
        return True
    except:
        return False