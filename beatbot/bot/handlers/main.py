from aiogram import Router

from bot.handlers.admin import register_admin_handlers
from bot.handlers.user import register_user_handlers
from bot.handlers.other import other_router
from bot.handlers.user.generation.main import register_generation_handlers


def register_all_handlers(main_router: Router) -> None:
    routers = (
        *register_user_handlers(main_router),
        *register_admin_handlers(main_router),
        *register_generation_handlers(main_router),
        other_router,
    )

    main_router.include_routers(*routers)
