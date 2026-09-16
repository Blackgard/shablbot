from __future__ import annotations

from pathlib import Path
from typing import Optional, Dict, Any, Callable

import loguru

from datetime import datetime as dt, time
from zoneinfo import ZoneInfo

from vk_api.vk_api import VkApiMethod

from shablbot.core.chat_storage import ChatSettingsStorage
from shablbot.models.chat import VkInfo
from shablbot.settings.settings_model import (
    SettingsModel,
    TimeWorkEnum,
    ChatSettingsBody,
    ChatSettingsBodyTimeWork,
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
        _info: Optional[Dict[str, Any]],
        on_settings_changed: Optional[Callable[["Chat"], None]] = None,
    ) -> None:
        self.chat_id = chat_id
        self.chat_settings = chat_settings
        self.default_time_zone = default_time_zone
        self.default_time_work = default_time_work
        self.chat_title = None
        self._on_settings_changed = on_settings_changed

        self.info = VkInfo.model_validate(_info) if _info else None

        if self.info and self.info.chat_settings:
            self.chat_title = self.info.chat_settings.title

        self.is_chat = str(self.chat_id).startswith("2")
        self.is_person = str(self.chat_id).startswith("1")

        if self.chat_settings is None:
            self.chat_settings = self.create_default_settings()

        self.vk_chat_info = None

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

    @staticmethod
    def _parse_clock(value: str) -> time:
        hours, minutes = value.split(":")
        return time(hour=int(hours), minute=int(minutes))

    @staticmethod
    def _is_time_in_range(current: time, time_from: time, time_to: time) -> bool:
        if time_from <= time_to:
            return time_from <= current <= time_to
        return current >= time_from or current <= time_to

    @staticmethod
    def check_chat_time_work(trigger_name: str, chat_settings: ChatSettingsBody) -> bool:
        time_work = chat_settings.time_work
        current_time = dt.now(ZoneInfo(time_work.time_zone)).time()

        if trigger_name == TimeWorkEnum.CUSTOM:
            time_from = Chat._parse_clock(time_work.time_from)
            time_to = Chat._parse_clock(time_work.time_to)
            return Chat._is_time_in_range(current_time, time_from, time_to)

        if trigger_name == TimeWorkEnum.NIGHT_MSK:
            return Chat._is_time_in_range(current_time, time(0, 0), time(8, 0))

        if trigger_name == TimeWorkEnum.DAY_MSK:
            return Chat._is_time_in_range(current_time, time(9, 0), time(22, 0))

        return False

    def create_default_settings(self) -> ChatSettingsBody:
        new_chat_settings = ChatSettingsBody(
            enabled=True,
            time_work=ChatSettingsBodyTimeWork(
                type=self.default_time_work,
                time_zone=self.default_time_zone,
                time_from="00:00",
                time_to="23:59",
            ),
        )
        return new_chat_settings

    def _notify_settings_changed(self) -> None:
        if self._on_settings_changed:
            self._on_settings_changed(self)

    def turn_off(self) -> None:
        self.chat_settings.enabled = False
        self._notify_settings_changed()

    def turn_on(self) -> None:
        self.chat_settings.enabled = True
        self._notify_settings_changed()

    def show_statistics(self) -> str:
        return ""

    def __str__(self):
        is_active_str = (
            f"{ColorText.OKGREEN}включен{ColorText.ENDC}"
            if self.chat_settings.enabled
            else f"{ColorText.FAIL}выключен{ColorText.ENDC}"
        )
        return "{0} - {1}".format(self.chat_id, is_active_str)


class Chats:
    """Chats class for work with chat class"""

    def __init__(
        self,
        settings: SettingsModel,
        botAPI: VkApiMethod,
        logger: loguru.Logger,
    ):
        self.settings = settings
        self.logger = logger
        self.__botAPI = botAPI

        self._storage = ChatSettingsStorage(
            self._resolve_storage_path(),
            self.logger,
        )
        self.chats: Dict[str, Chat] = {
            chat_id: self.create_chat(chat_id, chat_settings)
            for chat_id, chat_settings in self._load_chat_settings().items()
        }

    def _resolve_storage_path(self) -> Path:
        if self.settings.CHAT_SETTINGS_FILE:
            return Path(self.settings.CHAT_SETTINGS_FILE)
        return Path("data") / "chat_settings.json"

    def _load_chat_settings(self) -> Dict[str, ChatSettingsBody]:
        settings_map = dict(self.settings.CHAT_SETTINGS)
        if self.settings.CHAT_SETTINGS_PERSIST:
            settings_map.update(self._storage.load())
        return settings_map

    def _persist_chat_settings(self, _chat: Chat) -> None:
        if not self.settings.CHAT_SETTINGS_PERSIST:
            return

        self._storage.save(
            {chat_id: chat.chat_settings for chat_id, chat in self.chats.items()}
        )

    def create_chat(
        self, chat_id: str, chat_settings: Optional[ChatSettingsBody]
    ) -> Chat:
        return Chat(
            chat_id=chat_id,
            chat_settings=chat_settings,
            default_time_work=self.settings.DEFAULT_TIME_WORK,
            default_time_zone=self.settings.DEFAULT_TIME_ZONE,
            _info=self.__get_info_chat(chat_id),
            on_settings_changed=self._persist_chat_settings,
        )

    def __get_info_chat(self, chat_id: str) -> Optional[Dict[str, Any]]:
        return self.__botAPI.messages.getConversationsById(peer_ids=chat_id).get(
            "items", [None]
        )[0]

    def get_chat(self, chat_id: str, add_is_not_exist=False) -> Optional[Chat]:
        chat_id = str(chat_id)
        chat = self.chats.get(chat_id)
        if add_is_not_exist and chat is None:
            chat = self.create_chat(chat_id, None)
            self.chats[chat_id] = chat
            self._persist_chat_settings(chat)
        return chat

    def render_state(self):
        render_state(self.__class__.__name__, self.chats)

    def get_main_data_object(self):
        return self.chats
