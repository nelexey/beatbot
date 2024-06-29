from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable

from bot.database.methods.get import get_user, get_user_credits
from bot.database.methods.update import refill_credits_if_needed, delete_sub_if_expired


class UserSubMiddleware(BaseMiddleware):
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
        user_credits = get_user_credits(chat_id)

        data["user"] = user
        data["user_credits"] = user_credits

        result = None

        if user:
            refill_credits_if_needed(chat_id)

            if delete_sub_if_expired(chat_id):
                await answer('Ваша подписка закончилась, для вас снова действуют лимиты')

            if data['user_credits'].options > 0 or data['user'].has_sub:
                result = await handler(event, data)
            else:
                await answer('Ваш лимит по бесплатным опциям на сегодня исчерпан.')

        return result
