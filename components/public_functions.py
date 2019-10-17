import random
import datetime as dt

def get_random_id():
    return random.getrandbits(31) * random.choice([-1, 1])

def setTime(time):
    return dt.datetime(2009, 12, 1, time, 0).time()