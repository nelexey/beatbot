from aiohttp import web
from aiogram import Bot


async def handle_payment(request, bot: Bot):
    data = await request.json()

    print(data)
    return web.Response()
