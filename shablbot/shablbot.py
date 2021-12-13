"""
ShablBot - is easy bot for your project.
"""

from typing import Optional, Union

import random
import loguru
import requests

import vk_api
from vk_api.vk_api import VkApiMethod
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll, VkBotMessageEvent

from shablbot.components.chat import Chat, Chats
from shablbot.components.module import Modules
from shablbot.components.command import Commands
from shablbot.components.keyboard import Keyboards
from shablbot.components.event_handler import EventHandler
from shablbot.components.phrases import Phrases

from shablbot.models.event_handler import ResponceHandler
from shablbot.models.shablbot import VkBotMessageEventModel

from shablbot.settings.settings_model import SettingsModel

from shablbot.core.utils import render_state_all_components
from shablbot.core.exceptions import VkBotLonngpollNotExists


class ShablBot:
    """ShablBot is a lightweight and easy-to-configure bot that can cover most of the basic tasks when creating a bot.

    Args:
        settings (SettingsModel): Settings bot. Check folder "/settings"
    """

    def __init__(self, settings: SettingsModel, check_all_components: bool = False):
        self.settings: SettingsModel = settings
        self.logger: loguru.Logger = loguru.logger

        if self.settings.LOGGER_CONFIG:
            self.logger.configure(**self.settings.LOGGER_CONFIG.dict(exclude_none=True))

        self._bot_session: vk_api.VkApi = vk_api.VkApi(token=settings.TOKEN)
        self.botAPI: VkApiMethod = self._bot_session.get_api()
        self.bot_longpoll = self.__get_bot_longpoll()

        if self.bot_longpoll is None:
            raise VkBotLonngpollNotExists(
                "Vk botlongpoll not imported. Check your token."
            )

        self.debug: bool = settings.DEBUG_MODE

        self.phrases: Phrases = Phrases(self.settings, self.logger)
        self.commands: Commands = Commands(self.settings, self.logger)
        self.modules: Modules = Modules(self.settings, self.logger)
        self.chats: Chats = Chats(self.settings, self.botAPI, self.logger)
        self.keyboards: Keyboards = Keyboards(self.settings, self.logger)

        self.__handler_event = EventHandler(
            settings=self.settings,
            commands=self.commands,
            chats=self.chats,
            modules=self.modules,
            phrases=self.phrases,
            logger=self.logger,
        )

        if check_all_components:
            render_state_all_components([
                self.phrases,
                self.commands,
                self.modules,
                self.chats,
                self.keyboards
            ])

    def __get_bot_longpoll(self) -> Optional[VkBotLongPoll]:
        """Get bot longpoll

        Returns:
            VkBotLongPoll: VkBotLongPoll object
        """
        try:
            return VkBotLongPoll(self._bot_session, self.settings.BOT_CHAT_ID)
        except requests.exceptions.ConnectionError as error:
            self.logger.error(f"VkBotLongPoll not create. Error: {error}")

    def __get_event_object(self, event: VkBotMessageEvent) -> Union[VkBotMessageEventModel, bool]:
        """ Get a model of a VK object by data type

        Args:
            event (VkBotMessageEvent): Object VkApi that stores all the data about the message received by the server

        Returns:
            Union[VkBotMessageEventModel, bool]: Pydantic model with data or nothing
        """
        allowed_events = {
            VkBotEventType.MESSAGE_REPLY: lambda _: False,
            VkBotEventType.MESSAGE_NEW: VkBotMessageEventModel.parse_obj,
            # ... and more event type
        }
        return allowed_events.get(event.type, lambda _: False)(event.object)

    def __process_event(self, event: VkBotMessageEvent) -> bool:
        """Function for process get message from vk chat

        Args:
            event (VkBotMessageEvent): Object VkApi that stores all the data about the message received by the server

        Returns:
            is_processed (bool): Is processed event or not
        """
        event_object = self.__get_event_object(event)
        if not event_object: return

        chat_work: Chat = self.chats.get_chat(
            event_object.message.peer_id,
            add_is_not_exist=True
        )
        if not chat_work.is_premitted_work():
            return False

        responceHandler = self.__handler_event.process_chat_event(
            chat_work, event_object
        )

        if not responceHandler.is_matches_found:
            return False

        return self.write_message_to_chat(responceHandler, chat_work)

    def listen(self) -> None:
        """Start listen chat messages"""

        loguru.logger.info("------- Бот запущен / Bot is runing -------")
        for event in self.bot_longpoll.listen():
            self.__process_event(event)
        loguru.logger.info("------- Бот выключен / Bot is close -------")

    def write_message_to_chat(
        self, responceHandler: ResponceHandler, chat: Chat
    ) -> bool:
        try:
            keyboard = self.keyboards.get_clear_keyboard().get_keyboard_json()

            if responceHandler.keyboard_code:
                keyboard = self.keyboards.get_keyboard(
                    responceHandler.keyboard_code
                ).get_keyboard_json()

            if not self.settings.IS_SHOW_KEYBOARD_TO_CHAT and chat.is_chat:
                keyboard = self.keyboards.get_clear_keyboard().get_keyboard_json()

            self.botAPI.messages.send(
                peer_id=int(responceHandler.send_to_chat_id),
                message=str(responceHandler.message),
                random_id=random.getrandbits(31) * random.choice([-1, 1]),
                keyboard=keyboard,
            )

            if self.debug:
                self.logger.debug(
                    f"Было отправлено сообщение: '{responceHandler.message}' (id беседы: {chat.chat_id})"
                )

            return True
        except Exception as e:
            self.logger.error(e)
            self.logger.error(
                f"При отправке сообщения произошла ошибка. (ID{chat.chat_id}) | {responceHandler.message}"
            )

        return False
