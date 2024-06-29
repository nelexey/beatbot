import asyncio

from generator import launch

if __name__ == '__main__':
    try:
        asyncio.run(launch())
    except KeyboardInterrupt:
        print('Force exit')
