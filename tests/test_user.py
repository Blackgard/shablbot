import unittest

from shablbot.models.shablbot import ClientInfo, Message, VkBotMessageEventModel
from shablbot.models.user import User


def _build_event(from_id: int, peer_id: int = 1) -> VkBotMessageEventModel:
    return VkBotMessageEventModel(
        message=Message(
            date=1,
            from_id=from_id,
            id=10,
            out=0,
            peer_id=peer_id,
            text="hello",
            conversation_message_id=1,
            fwd_messages=[],
            important=False,
            random_id=0,
            attachments=[],
            is_hidden=False,
        ),
        client_info=ClientInfo(
            button_actions=[],
            keyboard=False,
            inline_keyboard=False,
            carousel=False,
            lang_id=0,
        ),
    )


class UserModelTests(unittest.TestCase):
    def test_from_event(self):
        user = User.from_event(_build_event(from_id=42, peer_id=100), admin_id=1)

        self.assertEqual(user.user_id, 42)
        self.assertEqual(user.peer_id, 100)
        self.assertEqual(user.message_id, 10)

    def test_is_admin(self):
        admin = User.from_event(_build_event(from_id=1), admin_id=1)
        regular = User.from_event(_build_event(from_id=2), admin_id=1)

        self.assertTrue(admin.is_admin)
        self.assertFalse(regular.is_admin)

    def test_chat_type_flags(self):
        personal = User.from_event(_build_event(from_id=1, peer_id=123), admin_id=1)
        group = User.from_event(_build_event(from_id=1, peer_id=2000000001), admin_id=1)

        self.assertTrue(personal.is_personal_chat)
        self.assertFalse(personal.is_group_chat)
        self.assertTrue(group.is_group_chat)


if __name__ == "__main__":
    unittest.main()
