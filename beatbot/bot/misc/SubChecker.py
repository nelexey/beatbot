from aiogram import Bot, types
from .parameters import CHANNELS


class SubChecker:
    bot = None
    channels = CHANNELS

    @classmethod
    def set_bot(cls, bot: Bot):
        cls.bot = bot

    @classmethod
    async def is_member(cls, user_id: int) -> bool:
        for channel in cls.channels:
            try:
                member = await cls.bot.get_chat_member(channel, user_id)
                print(member)
                status = member.status in ['member', 'administrator', 'creator']
                if not status:
                    return False
            except Exception as e:
                print(f"Error in channel {channel}: {e}")
                return False
        return True
