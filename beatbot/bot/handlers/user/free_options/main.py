from aiogram import Router
from typing import Tuple

from bot.middlewares import UserDataMiddleware, UserSubMiddleware
from .speed_up import speed_up_router
from .slow_down import slow_down_router
from .bassboost import bassboost_router
from .find_key import find_key_router
from .find_tempo import find_tempo_router
from .normalize_sound import normalize_sound_router
from .midi_to_wav import midi_to_wav_router
from .remove_vocal import remove_vocal_router
from .rhymes import rhymes_router


def register_free_options_handlers(main_router: Router) -> Tuple[Router, ...]:
    routers = (
        speed_up_router,
        slow_down_router,
        bassboost_router,
        find_key_router,
        find_tempo_router,
        normalize_sound_router,
        midi_to_wav_router,
        remove_vocal_router,
        rhymes_router
    )

    for router in routers:
        router.callback_query.outer_middleware(UserDataMiddleware())
        router.callback_query.middleware(UserSubMiddleware())
        router.message.outer_middleware(UserDataMiddleware())
        router.message.middleware(UserSubMiddleware())

    return routers
