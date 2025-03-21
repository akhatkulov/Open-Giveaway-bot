from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.db.alchemy import get_info
from data.config import ADMIN


class IsBotAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_is = get_info(cid=int(message.from_user.id), type_data="whois")
        print("Handler is admin", message.from_user.id, user_is)
        return user_is == "admin" or int(message.from_user.id) == ADMIN
