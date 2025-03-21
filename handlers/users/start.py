import json
from asyncio import sleep
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.fsm.context import FSMContext
from loader import bot
from utils.db.alchemy import (
    create_user,
    get_info,
    change_info,
    get_info_gw,
    change_info_gw,
)
from keyboards.inline.phonenumber import send_number
from states.test import UserState
from helper_utils.join_checker_part import join
from keyboards.inline.home_button import home_button

router = Router()


@router.message(CommandStart())
async def do_start(message: types.Message, state: FSMContext):
    create_user(cid=message.chat.id)

    if message.text and len(message.text.split()) > 1:
        giveaway_id = int(message.text.split()[1])  # Giveaway ID'ни олиш
        print("giveaway_id",giveaway_id)
        change_info(cid=message.chat.id, type_data="cache", value=giveaway_id)
        
        owner_id = get_info_gw(id=int(giveaway_id), x_type="gwo")
        owner_channels = get_info(cid=owner_id, type_data="channels")
        
        print("CC--CC", owner_id, owner_channels)
        
        if await join(user_id=message.chat.id, c_channels=owner_channels):
            if get_info(cid=message.chat.id, type_data="phonenumber") == "null":
                await message.answer(
                    "📱 Телефон рақамингизни киритинг", reply_markup=send_number()
                )
                await state.set_state(UserState.send_number)
            else:
                if get_info_gw(id=int(giveaway_id),x_type="status")=="open":
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=f"Сиз #{giveaway_id} гивевейда қатнашмоқдасиз! Тугаш вақти: {get_info_gw(id=int(giveaway_id), x_type='period')}. Ютсангиз хабар берамиз!",
                    )
                    change_info(cid=message.chat.id, type_data="add_gws", value=giveaway_id)
                    change_info_gw(
                        id=int(giveaway_id), x_type="add_user", value=message.chat.id
                    )
                else:
                    await bot.send_message(chat_id=message.chat.id,text=f"#{giveaway_id} Гивеаwай яукланди, {get_info_gw(id=int(giveaway_id),x_type='winner')} ютди!")
 
                change_info(cid=message.chat.id, type_data="cache", value="none")
    else:
        if await join(user_id=message.chat.id):
            if get_info(cid=message.chat.id, type_data="phonenumber") == "null":
                await message.answer(
                    "📱 Телефон рақамингизни киритинг", reply_markup=send_number()
                )
                await state.set_state(UserState.send_number)
            else:
                await message.answer(
                    "✋ Хуш келибсиз!\nБизнинг бот сизга канал ёки чатда ўйин ўтказишда ёрдам беради.\nЯнги совға яратишга тайёрмисиз?",
                    reply_markup=home_button,
                )
    await sleep(0.3)