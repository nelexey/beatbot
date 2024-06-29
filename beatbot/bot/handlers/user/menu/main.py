from aiogram import Router
from typing import Tuple

from .menu import menu_router
from .balance import balance_router
from .free_options import free_options_router

def register_menu_handlers(main_router: Router) -> Tuple[Router, ...]:
    routers = (
        menu_router,
        balance_router,
        free_options_router
    )

    return routers
