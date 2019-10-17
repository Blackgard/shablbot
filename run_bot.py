from settings import *
from components.hendler_message import handler

def run_server():
    """
    Точка начала работы бота, здесь находится прослушка от VKBotLongPoll
    и находится точка входа в обработчик полученного сообщения от сервера.
    """

    import vk_api as api
    from   vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
    

    bot_session = api.VkApi(token=CONST.token)
    botAPI      = bot_session.get_api()
    longpoll    = VkBotLongPoll(bot_session, CONST.bot_group_id)

    print("------- Бот запущен / Bot is runing -------")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:	
            handler(
                event.obj,          # Весь обьект класса event (вся информация об полученном сообщении)
                event.obj.peer_id,  # id группы откуда пришло сообщение
                botAPI              # API для работы с действиями бота
            )    

if __name__ == "__main__":
    run_server() 