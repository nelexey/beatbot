import asyncio
import logging

from generator.web import init_web_server
from generator.misc import settings


async def launch():
    web_server_task = asyncio.create_task(init_web_server(settings.web_config))
    # This is a simple way of keeping the server running forever.
    try:
        while True:
            await asyncio.sleep(3600)  # Wait for one hour before checking again
    except KeyboardInterrupt:
        web_server_task.cancel()
        try:
            await web_server_task
        except asyncio.CancelledError:
            pass
