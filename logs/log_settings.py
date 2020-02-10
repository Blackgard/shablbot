# -*- coding: utf-8 -*-

import coloredlogs, logging
from settings import SETTINGS


root_logger= logging.getLogger()
if SETTINGS.debug:
    
    root_logger.setLevel(logging.DEBUG) 
    handler = logging.FileHandler('logs/debug.log', 'w', 'utf-8') 
    coloredlogs.install(level='DEBUG')
else:
    root_logger.setLevel(logging.INFO) 
    handler = logging.FileHandler('logs/production.log', 'w', 'utf-8') 
    root_logger.addHandler(handler)
    coloredlogs.install(level='INFO')
    
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')) 
root_logger.addHandler(handler)
logging.basicConfig()