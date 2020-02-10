from components.time_work import _getTime

def get_settings_chat(chat_id, type_time = None, t_from = None, t_to = None, included = None):
    """
    Функция формирования настроек работы бота с беседой (ВК)

    Параметры
    ---
    ```
    int : chat_id   - id беседы для которого необходимо собрать настройки
    str : type_time - время работы беседы по часовому признаку (смотреть settings.py - type_time_work)
    str : t_from    - время работы беседы с какого-то конкретного временного значения
    str : t_to      - время работы беседы по какое-то конкретное временное значение
    str : included  - состояние включенности бота в беседе
    ```

    Логика работы
    ---
    Функция принимает на вход параметры необходимые для настройки бота. 
    Если в данную функцию подать id чата, который не указан в settings.py (settings_chat),
    то для данного чата функция вернет значения из стандартных переменных указанных в settings.py:
        `type_time - (def_time_work, time_zone)`,
        `included  - True`

    ```

    get_settings_chat(123456789)
    ==> {
        "type_time" : ("ALL", "Asia/Tomsk"),
        "included"  : True
    }

    ```
    Если в данную функцию подать id чата, который указанн в settings.py (settings_chat),
    то для данного чата функция вернет значения указанные в переменной settings_chat.

    ```
    :settings.py:
        settings_chat = {
            123456780 : {
                "type_time" : ("NIGHT_MSK", "Europe/Moscow"),
                "included"  : True
            }
        }
    :end_file:

    get_settings_chat(123456780)
    ==> {
        "type_time" : ("NIGHT_MSK", "Europe/Moscow"),
        "included"  : True
    }

    ```
    Если для функции указать дополнительные переменные, то вместо стандартных или указанных в settings_chat,
    будут заданны указанные значения.
    ```
    get_settings_chat(123456780, "CUSTOM", "12:00", "00:00")
    ==> {
        "type_time" : ("CUSTOM", "Asia/Tomsk" <-- (time_zone)),
        "from"      : datetime(hour=12, minute=0),
        "to"        : datetime(hour=0, minute=0),
        "included"  : True
    }

    get_settings_chat(123456780, "CUSTOM", "00:00", "23:59", False)
    ==> {
        "type_time" : ("CUSTOM", "Asia/Tomsk" <-- (time_zone)),
        "from"      : datetime(hour=0, minute=0),
        "to"        : datetime(hour=23, minute=59),
        "included"  : False
    }
    ```
    """
    from settings import SETTINGS

    chat_id     = int(chat_id)

    for set_chat_id, settings_chat in SETTINGS.settings_chat.items():

        if set_chat_id == chat_id: 
            # Нашли id беседы в settings, теперь производим считывание настроек
            
            if type_time is None:       
                settings_time = settings_chat["time_type"]  
                type_time     = settings_time[0]                  
            else: 
                settings_time = (type_time[0].upper(), type_time[1])
                type_time     = type_time[0].upper() 
                

            if included is None:
                included = settings_chat["included"]   
                
            if type_time == "CUSTOM" and t_from is None and t_to is None:
                t_from  = settings_chat["from"]
                t_to    = settings_chat["to"]
            
            break
    
    if type_time == None:
        return {
            "time_type" : (SETTINGS.def_time_work, SETTINGS.time_zone),
            "included"  : True            
        }

    elif type_time == "CUSTOM":
        t_from  = _getTime(t_from)
        t_to    = _getTime(t_to)

        return  {
            "time_type" : settings_time,
            "from"      : t_from,
            "to"        : t_to,
            "included"  : included
        }
        
    return {
        "time_type"     : settings_time,
        "included"      : included
    }

def modify_settings_chat(chat_id, settings):
    """
    Функция позволяет изменять настройки работы бота с конкретной группой

    Параметры
    ---
    ```
    int  : chat_id  - уникальный идентификатор группы, для которой задаются правила
    dict : settings - настройки бота полученные из get_settings_chat
    ```
    Логика работы
    ---
    Функция возвращает параметр типа bool. `True` - если изменения настроек произошло успешно,
    `False` - если не успешно
    ```

    modify_settings_chat(123456789, {
        "time_type" : "ALL",
        "included"  : True
    })
    ==> True

    modify_settings_chat(123456789, None)  
    ==> False

    modify_settings_chat(123456789, {})
    ==> False
    ```
    """
    from components.cache import CACHE
    
    try:
        if settings:
            CACHE.set_settings_chat(chat_id, settings)
            return True
        else:
            return False
    except:
        return False