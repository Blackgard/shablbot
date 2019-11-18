from datetime import datetime as dt
from pytz import timezone

from settings import SETTINGS
from components.cache import CACHE

def _getTime(time):
    hour, minute = time.split(':')
    return dt(2009, 12, 1, int(hour), int(minute)).time()

def check_work_time(chat_id):
    # TODO: ПЕРЕДЕЛАТЬ ДАННЫЙ БЛОК 
    chat_time_type = CACHE.settings_chat.get(chat_id)["time_type"]

    if chat_time_type[0] == SETTINGS.type_time_work[0][0]: # ALL
        return True
    
    elif chat_time_type[0] == SETTINGS.type_time_work[1][0]: #CUSTOM 
        time_zone = dt.now(timezone(CACHE.settings_chat[chat_id]['time_type'][1]))
        time_from = CACHE.settings_chat[chat_id]['from']
        time_to   = CACHE.settings_chat[chat_id]['to']

        if time_from <= time_zone.time() <= time_to:
            return True
        return False
    
    elif chat_time_type[0] == SETTINGS.type_time_work[2][0]: # NIGHT_MSK
        t_msk_NGT = [0, 8]

        time_msk_ng  = dt.now(timezone(SETTINGS.type_time_work[2][1]))
        time_from    = t_msk_NGT[0]
        time_to      = t_msk_NGT[1]

        if time_from <= time_msk_ng.time() <= time_to:
            return True       
        return False
        

    elif chat_time_type[0] == SETTINGS.type_time_work[3][0]: #DAY_MSK
        t_msk_DAY = [9, 22]
        
        time_msk_day  = dt.now(timezone(SETTINGS.type_time_work[3][1]))
        time_from    = t_msk_NGT[0]
        time_to      = t_msk_NGT[1]

        if time_from <= time_msk_day.time() <= time_to:
            return True
        return False       

    else:
        return False