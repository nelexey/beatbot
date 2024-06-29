import asyncio
import os


async def create_user_dir(dirname: str) -> str:
    relative_path = os.path.join("data", str(dirname))

    absolute_path = os.path.abspath(relative_path)

    os.makedirs(absolute_path, exist_ok=True)

    return absolute_path
