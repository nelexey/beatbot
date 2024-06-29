from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable

from bot.database.methods.get import get_user


class UserDataMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:

        if isinstance(event, Message):
            chat_id = event.chat.id
            answer = event.answer
        # elif isinstance(event, CallbackQuery):
        else:
            chat_id = event.message.chat.id
            answer = event.message.answer

        user = get_user(chat_id)
        data["user"] = user

        # Проверяем, находится ли пользователь в процессе обработки
        if not user:
            result = None
            await answer('Зарегестрируйтесь! /start')
        else:
            result = await handler(event, data)

        return result
