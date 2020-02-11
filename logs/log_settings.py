# -*- coding: utf-8 -*-
import coloredlogs, logging
from datetime import datetime as dt
from settings import SETTINGS

root_logger= logging.getLogger()
date = dt.now().strftime("%d_%m_%Y_%H_%M")

if SETTINGS.debug:
    root_logger.setLevel(logging.DEBUG) 
    handler = logging.FileHandler(f'logs/debug_logs/debug_{date}.log', 'w', 'utf-8') 
    coloredlogs.install(level='DEBUG')
else:
    root_logger.setLevel(logging.INFO) 
    handler = logging.FileHandler(f'logs/prod_logs/prod_{date}.log', 'w', 'utf-8') 
    coloredlogs.install(level='INFO')
    
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')) 
root_logger.addHandler(handler)
logging.basicConfig()