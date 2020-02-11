import datetime as dt
import logging

from collections import Counter

from functools import lru_cache
from .decorators import freezeargs

from settings import SETTINGS
class CACHE:
    """
    Класс реализующий функционал кэширования данных необходимых для работы бота
    """

    _settings_chat = {}
    _counter_word = {}
        
    @classmethod
    def set_settings_chat(cls, id_chat, settings):
        try:
            cls._settings_chat[id_chat] = settings
            return True
        except:
            return False
        
    @classmethod    
    def get_settings_chat(cls, id_chat=None):
        if id_chat:
            return cls._settings_chat.get(id_chat)
        else:
            return cls._settings_chat
    
    @classmethod
    def set_counter_word(cls, id_chat, word):
        cls._counter_word[id_chat] += Counter([word])
        
    @classmethod    
    def init_counter_word(cls, id_chat):
        cls._counter_word[id_chat] = Counter()
        
    @classmethod    
    def get_counter_word(cls, id_chat=None):
        print(cls._counter_word)
        if id_chat:
            return cls._counter_word.get(id_chat)
        else:
            return cls._counter_word
        
from components.chat_settings import get_settings_chat

@freezeargs
@lru_cache(maxsize=SETTINGS.def_size_cache,typed=False)
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

    find_chat = CACHE.get_settings_chat(chat_id)
    try:
        if find_chat is None:
            
            if settings:
                CACHE.set_settings_chat(
                    chat_id, 
                    settings
                )
            else:    
                CACHE.set_settings_chat(
                    chat_id, 
                    get_settings_chat(chat_id)
                ) 
                
            CACHE.init_counter_word(chat_id)

            if SETTINGS.debug:
                logging.debug(f"Была сохранена группа id{chat_id}")
    except:
        return False
    return True

#@lru_cache(maxsize=SETTINGS.def_size_cache,typed=False)
def add_single_value_counter_chat(chat_id, type_word):
    try:
        CACHE.set_counter_word(chat_id, type_word)
        return True
    except:
        logging.error(f"Не удалось добавить уникальное слово для id{chat_id}.")
        return False