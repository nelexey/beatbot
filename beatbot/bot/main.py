from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
import asyncio
import logging

from bot.misc import settings
from bot.misc import SubChecker
from bot.filters import register_all_filters
from bot.handlers import register_all_handlers
from bot.database.models import register_models
from bot.web.server import init_web_server
from bot.webhooks import create_all_webhooks

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode='HTML'))

# Подключение главного роутера
main_router = Router()
dp.include_router(main_router)


async def __on_start_up(dp: Dispatcher,
                        router: Router,
                        bot: Bot) -> None:
    """
    Функция запуска, регистрирующая фильтры, обработчики и модели
    """
    register_all_filters(dp)
    register_all_handlers(router)
    register_models()
    SubChecker.set_bot(bot)

    web_server_task = asyncio.create_task(init_web_server(settings.web_config, bot))
    await asyncio.sleep(0.1)

    # create_all_webhooks()


async def start_bot():
    """
    Запуск бота с использованием токена из переменных окружения
    """
    await __on_start_up(dp, main_router, bot)
    await dp.start_polling(bot)
