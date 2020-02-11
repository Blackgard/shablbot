# -*- coding: utf-8 -*-

from settings import SETTINGS
from components.handler_message import handler_message
from components.init_bot import init_components
import logs.log_settings 
import logging


def run_server(*args):
    """
    Точка начала работы бота, здесь находится прослушка от VKBotLongPoll.
    При получении сообщения оно попадает в обработчик handler_message.
    """

    import vk_api as api
    from   vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
    
    bot_session = api.VkApi(token=SETTINGS.token)
    botAPI      = bot_session.get_api()
    longpoll    = VkBotLongPoll(bot_session, SETTINGS.bot_chat_id)
  
    state_init, err_init = init_components()

    if not state_init:          
        logging.warning(err_init)
    
    logging.info("------- Бот запущен / Bot is runing -------")
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:	
                handler_message(
                    event.obj,          # Весь объект класса event (вся информация об полученном сообщении)
                    event.obj.peer_id,  # Id чата откуда было получено сообщение
                    botAPI              # API для работы с действиями бота
                )    
    except ConnectionError as err:
        logging.error("Произошел разрыв соединения с сервером.\n" + err)

if __name__ == "__main__":
    import sys

    run_server(sys.argv) 