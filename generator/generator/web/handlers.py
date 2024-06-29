from aiohttp import web
import asyncio
import traceback

from generator.web.requests.Service import option_done_req
from generator.beats.BeatsRouter import BeatsRouter
from generator.options.OptionsRouter import OptionsRouter


class RouterFactory:
    @staticmethod
    def create_router(operation_type):
        if operation_type == 'beat':
            return BeatsRouter()
        elif operation_type == 'option':
            return OptionsRouter()
        else:
            raise ValueError("Invalid operation_type parameter")


async def process_option(result, data, option_name):
    if result is not None:
        await option_done_req(option_name, data['chat_id'], result)


async def handle_request(operation_type, data):
    router = RouterFactory.create_router(operation_type)

    if operation_type == 'beat':
        # Запускаем асинхронно и сразу возвращаем результат
        asyncio.create_task(router.handle_request(data))
        return "Request is being processed"
    elif operation_type == 'option':
        # Запускаем асинхронно, но ждем результата
        handle_request_task = asyncio.create_task(router.handle_request(data))
        result = await handle_request_task

        # Запускаем process_option асинхронно
        asyncio.create_task(process_option(result, data, data['option_name']))

        return result
    else:
        raise ValueError("Invalid operation_type")


async def handle_new_query(request):
    try:
        data = await request.json()
    except Exception:
        return web.Response(text="Invalid JSON data provided", status=400)

    operation_type = data.get('operation_type')

    if operation_type is None:
        return web.Response(text="Missing operation_type parameter", status=400)

    try:
        result = await handle_request(operation_type, data)

        return web.Response(text=str(result), status=200)
    except ValueError as ve:
        return web.Response(text=str(ve), status=400)
    except Exception as e:
        traceback.print_exc()
        return web.Response(text="Error processing request", status=500)


async def handle_main_page(request):
    try:
        return web.Response(text='OK')
    except Exception as e:
        traceback.print_exc()
        return web.Response(text="Error processing request", status=500)