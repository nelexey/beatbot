from aiofiles.os import remove


async def delete_file(file_path):
    # Delete the file at the specified file path
    try:
        await remove(file_path)
    except:
        ...
