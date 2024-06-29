from aiogram import Router
from typing import Tuple

from .platinum.parameters import platinum_router
from .beatfusion.parameters import beatfusion_router
from .full_version import full_version_router


def register_generation_handlers(main_router: Router) -> Tuple[Router, ...]:
    routers = (
        platinum_router,
        beatfusion_router,
        full_version_router
    )

    return routers
