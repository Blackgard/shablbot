# -*- coding: utf-8 -*-

from typing import List, Optional

from pydantic import BaseModel


class VkInfoPeer(BaseModel):
    id: int
    type: str
    local_id: int


class VkInfoCanWrite(BaseModel):
    allowed: bool


class VkInfoChatSettingsAcl(BaseModel):
    can_change_info: bool
    can_change_invite_link: bool
    can_change_pin: bool
    can_invite: bool
    can_promote_users: bool
    can_see_invite_link: bool
    can_moderate: bool
    can_copy_chat: bool
    can_call: bool
    can_use_mass_mentions: bool
    can_change_style: bool


class VkInfoChatSettings(BaseModel):
    owner_id: int
    title: str
    state: str
    acl: VkInfoChatSettingsAcl
    members_count: int
    admin_ids: List[int]
    active_ids: List[int]
    is_group_channel: bool
    is_service: bool


class VkInfo(BaseModel):
    peer: VkInfoPeer
    last_message_id: int
    in_read: int
    out_read: int
    last_conversation_message_id: int
    is_marked_unread: bool
    important: bool
    can_write: VkInfoCanWrite
    chat_settings: Optional[VkInfoChatSettings]
