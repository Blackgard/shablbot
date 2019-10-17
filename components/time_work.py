from settings import *
from components.cache import CACHE
import datetime as dt

def check_work_time(group_id):
    _type = CACHE.time_work_group.get(group_id)["type"]

    if _type == CONST.type_time_work[0]: # ALL
        return True
    
    if _type == CONST.type_time_work[1]: # NIGHT_MSK
        time_msk_ng  = dt.datetime.now(dt.timezone(dt.timedelta(hours=3)))
        time_from    = CACHE.time_work_group.get(group_id)['from']
        time_to      = CACHE.time_work_group.get(group_id)['to']

        if time_msk_ng.time() >= time_from and time_msk_ng.time() <= time_to:
            return True
        else:
            return False