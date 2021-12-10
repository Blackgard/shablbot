
import loguru
from shablbot.models.shablbot import VkBotMessageEventModel


class User:
    def __init__(self, vk_event: VkBotMessageEventModel, logger: loguru.logger):
        self.logger = logger
        self.logger.debug(vk_event)
