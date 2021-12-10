from typing import Optional, Dict, Any

import loguru

from datetime import timezone, datetime as dt

from vk_api.vk_api import VkApiMethod

from shablbot.models.chat import VkInfo
from shablbot.settings.settings_model import (
    SettingsModel,
    TimeWorkEnum,
    ChatSettingsBody,
)

from shablbot.core.color import ColorText
from shablbot.core.utils import render_state


class Chat:
    """The model describing the chat in VK"""

    def __init__(
        self,
        chat_id: str,
        chat_settings: Optional[ChatSettingsBody],
        default_time_work: TimeWorkEnum,
        default_time_zone: str,
        _info: Optional[Dict[str, Any]]
    ) -> None:
        self.chat_id = chat_id
        self.chat_settings = chat_settings
        self.default_time_zone = default_time_zone
        self.default_time_work = default_time_work
        self.chat_title = None

        self.info = VkInfo(**_info)

        if self.info.chat_settings:
            self.chat_title = self.info.chat_settings.title

        self.is_chat = True if str(self.chat_id)[0] == "2" else False
        self.is_person = True if str(self.chat_id)[0] == "1" else False

        if self.chat_settings is None:
            self.chat_settings = self.create_default_settings()

        self.vk_chat_info = None

    def __str__(self):
        return (self.chat_id, self.chat_settings)

    def is_premitted_work(self) -> bool:
        action = {
            TimeWorkEnum.ALL: lambda time, settings: True,
            TimeWorkEnum.CUSTOM: self.check_chat_time_work,
            TimeWorkEnum.NIGHT_MSK: self.check_chat_time_work,
            TimeWorkEnum.DAY_MSK: self.check_chat_time_work,
            "default": lambda time, settings: False,
        }

        chat_time_work = self.chat_settings.time_work.type
        return action.get(chat_time_work)(chat_time_work, self.chat_settings)

    def check_chat_time_work(trigger_name: str, chat_settings: ChatSettingsBody) -> bool:
        if trigger_name == "CUSTOM":  # CUSTOM
            time_zone = dt.now(timezone(chat_settings.time_work))
            time_from = chat_settings.time_from
            time_to = chat_settings.time_to

            if time_from <= time_zone.time() <= time_to:
                return True
            return False

        elif trigger_name == "NIGHT_MSK":  #
            t_msk_NGT = [0, 8]

            time_zone = dt.now(timezone(chat_settings.time_zone))
            time_from = t_msk_NGT[0]
            time_to = t_msk_NGT[1]

            if time_from <= time_zone.time() <= time_to:
                return True
            return False

        elif trigger_name == "DAY_MSK":  # DAY_MSK
            t_msk_DAY = [9, 22]

            time_zone = dt.now(timezone(chat_settings.time_zone))
            time_from = t_msk_DAY[0]
            time_to = t_msk_DAY[1]

            if time_from <= time_zone.time() <= time_to:
                return True
            return False

        return False

    def create_default_settings(self) -> ChatSettingsBody:
        """ """
        new_chat_settings = ChatSettingsBody(
            enabled=True,
            time_work={
                "type": self.default_time_work,
                "time_zone": self.default_time_zone,
                "time_from": "00:00",
                "time_to": "23:59",
            },
        )
        return new_chat_settings

    def turn_off(self) -> None:
        "Disable bot chat"
        self.chat_settings.enabled = False

    def turn_on(self) -> None:
        "Disable bot chat"
        self.chat_settings.enabled = True

    def show_statistics(self) -> str:
        return ""

    def __str__(self):
        is_active_str = f'{ColorText.OKGREEN}включен{ColorText.ENDC}' if self.chat_settings.enabled else f'{ColorText.FAIL}выключен{ColorText.ENDC}'
        return "{0} - {1}".format(self.chat_id, is_active_str)

class Chats:
    """Chats class for work with chat class"""

    def __init__(self, settings: SettingsModel, botAPI: VkApiMethod, logger: loguru.logger,):
        self.settings = settings
        self.logger = logger

        self.__botAPI = botAPI

        self.chats: Dict[str, Chat] = {
            chat_id: self.create_chat(chat_id, settings)
            for chat_id, settings in self.settings.CHAT_SETTINGS.items()
        }

    def create_chat(
        self, chat_id: str, chat_settings: Optional[ChatSettingsBody]
    ) -> Chat:
        """Create new chat object

        Args:
            chat_id (str): Chat id
            chat_settings (Optional[ChatSettingsBody]): Chat settings

        Returns:
            Chat: Chat object
        """
        return Chat(
            chat_id=chat_id,
            chat_settings=chat_settings,
            default_time_work=self.settings.DEFAULT_TIME_WORK,
            default_time_zone=self.settings.DEFAULT_TIME_ZONE,
            _info=self.__get_info_chat(chat_id)
        )

    def __get_info_chat(self, chat_id: str) -> Optional[Dict[str, Any]]:
        return self.__botAPI.messages.getConversationsById(peer_ids=chat_id).get('items', [None])[0]


    def get_chat(self, chat_id: str, add_is_not_exist=False) -> Optional[Chat]:
        """Get chat object by id.

        Args:
            chat_id (str): chat id how need get
            add_is_not_exist (bool): Create new chat if this value is True

        Returns:
            Optional[Chat]: Chat object or None
        """
        chat = self.chats.get(chat_id, None)
        if add_is_not_exist and chat is None:
            chat = self.chats[chat_id] = self.create_chat(chat_id, None)
        return chat

    def render_state(self):
        render_state(self.__class__.__name__, self.chats)

    def get_main_data_object(self):
        return self.chats
