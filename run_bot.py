from settings import SETTINGS
from components.handler_message import handler_message
from components.init_bot import init_components

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
        print(err_init)
        exit()

    del state_init, err_init # чистка лишних переменных

    print("------- Бот запущен / Bot is runing -------")
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:	
                handler_message(
                    event.obj,          # Весь обьект класса event (вся информация об полученном сообщении)
                    event.obj.peer_id,  # id чата откуда было полученно сообщение
                    botAPI              # API для работы с действиями бота
                )    
    except ConnectionError as err:
        print("Произошел разрыв соединения с сервером, лог об ошибке ниже:")
        print(err)

if __name__ == "__main__":
    import sys

    run_server(sys.argv) 