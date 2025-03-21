from aiogram import BaseMiddleware, types
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from loader import bot
from utils.db.alchemy import create_user, change_info, is_there, get_info


class BlockChecking(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any],
    ) -> Any:
        try:
            if event.text == "/start" and (not is_there(cid=event.from_user.id)):
                create_user(cid=event.from_user.id, cache=event.text.split()[1])
            elif (len(event.text.split()) == 2) and ("/start" in event.text):
                print(is_there(cid=event.from_user.id), "--[status]--")
                if is_there(cid=event.from_user.id):
                    change_info(
                        cid=event.from_user.id,
                        type_data="cache",
                        value=event.text.split()[1],
                    )
                else:
                    create_user(cid=event.from_user.id, cache=event.text.split()[1])

        except Exception as e:
            print(e)
            pass

        if get_info(cid=event.from_user.id, type_data="status") == "blocked":
            await event.answer(
                text="Qoidalarni buzganingiz uchun siz bloklangansiz!!! Bog'lanish: @Akhatkulov",
            )
            return

        return await handler(event, data)


class BlockCheckingCall(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: types.CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:

        if get_info(cid=event.from_user.id, type_data="status") == "blocked":
            await event.answer(
                text="Qoidalarni buzganingiz uchun siz bloklangansiz!!! Bog'lanish: @Akhatkulov",
            )
            return

        return await handler(event, data)
