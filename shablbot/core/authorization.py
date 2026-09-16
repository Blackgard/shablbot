from shablbot.models.handler_context import HandlerContext


class AuthorizationService:
    """Проверка прав на выполнение приватных команд."""

    @staticmethod
    def can_execute_private_command(context: HandlerContext) -> bool:
        return context.is_admin
