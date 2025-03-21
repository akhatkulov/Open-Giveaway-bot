import logging

from aiogram import Bot

from utils.db.alchemy import get_admins
from data.config import ADMIN


async def on_startup_notify(bot: Bot):
    admins_list = get_admins()
    admins_list.append(ADMIN)
    print(admins_list)
    for admin in admins_list:
        try:
            bot_properties = await bot.me()
            message = [
                "<b>Bot ishga tushdi.</b>\n",
                f"<b>Bot ID:</b> {bot_properties.id}",
                f"<b>Bot Username:</b> {bot_properties.username}",
            ]
            print("---", admin)
            await bot.send_message(admin, "\n".join(message))
        except Exception as err:
            logging.exception(err)
