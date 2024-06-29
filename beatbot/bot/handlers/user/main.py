from aiogram import Router
from typing import Tuple

from .menu.main import register_menu_handlers
from .free_options.main import register_free_options_handlers
from .commands import commands_router


def register_user_handlers(main_router: Router) -> Tuple[Router, ...]:
    routers = (
        commands_router,
        *register_menu_handlers(main_router),
        *register_free_options_handlers(main_router)
    )

    return routers
