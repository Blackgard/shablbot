"""
Shablbot exception and warning classes
"""


class SettingNotExists(Exception):
    """ The settings were imported, but the setting variable was not found """
    pass


class VkBotLonngpollNotExists(Exception):
    """ Vk longpoll was not imported """
    pass
