import os
import aiofiles
import asyncio


async def delete_files_and_directory(directory_path):
    try:
        files = os.listdir(directory_path)
        await asyncio.gather(*(aiofiles.os.remove(os.path.join(directory_path, file)) for file in files))
        await aiofiles.os.rmdir(directory_path)
        print(f"Deleted directory: {directory_path}")
    except Exception as e:
        print(f"Failed to delete directory: {directory_path}. Error: {e}")

# Usage:
# asyncio.run(delete_files_and_directory("/path/to/your/directory"))
