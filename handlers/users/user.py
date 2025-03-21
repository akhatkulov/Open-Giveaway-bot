import json
from asyncio import sleep
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.test import UserState, PanelState
from utils.db.alchemy import (
    change_info,
    get_info,
    add_channel_gwo,
    delete_channel_gwo,
    create_giveaway,
    change_info_gw,
    get_info_gw,
    get_own_gws
)
from loader import bot
from keyboards.inline.phonenumber import send_number
from keyboards.inline.home_button import home_button
from keyboards.inline.manage_channels import manage_channel
from helper_utils.id_filter import is_id
from helper_utils.bot_is_admin import bot_is_admin
from helper_utils.is_time import is_time_check
from helper_utils.prepare_report import prepare_report
from data.config import BOT_USERNAME
from helper_utils.join_checker_part import join

router = Router()


@router.callback_query(F.data == "check_join")
async def check_join_cb_answer(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(
        chat_id=call.message.chat.id, message_id=call.message.message_id
    )
    
    if await join(user_id=call.message.chat.id):
        if get_info(cid=call.message.chat.id, type_data="phonenumber") == "null":
            await call.message.answer(
                "📱Телефон рақамингизни киритинг", reply_markup=send_number()
            )
            await state.set_state(UserState.send_number)
        else:
            user_cache = get_info(cid=call.message.chat.id, type_data="cache")
            owner_id = get_info_gw(id=int(user_cache), x_type="gwo")
            owner_channels = get_info(cid=owner_id, type_data="channels")
        
            print("CC--CC", owner_id, owner_channels)
        
            if await join(user_id=call.message.chat.id, c_channels=owner_channels):
                if user_cache != "none":
                    if get_info_gw(id=int(user_cache),x_type="status")=="open":
                        await bot.send_message(
                            chat_id=call.message.chat.id,
                            text=f"Сиз #{user_cache} гивевейда қатнашмоқдасиз! Тугаш вақти: {get_info_gw(id=int(user_cache), x_type='period')}. Ютсангиз хабар берамиз!",
                        )
                        change_info(cid=call.message.chat.id, type_data="add_gws", value=user_cache)
                        change_info_gw(
                            id=int(user_cache), x_type="add_user", value=call.message.chat.id
                        )
                    else:
                        await bot.send_message(chat_id=call.message.chat.id,text=f"#{user_cache} Гивеаwай яукланди, {get_info_gw(id=int(user_cache),x_type='winner')} ютди!")
                    change_info(cid=call.message.chat.id, type_data="cache", value="none")
                else:
                    await bot.send_message(
                        chat_id=call.message.chat.id,
                        text="✅Тасдиқланди, фойдаланишингиз мумкин.",
                    )
        await sleep(0.3)


@router.message(UserState.send_number)
async def send_ad_to_users(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    change_info(cid=message.chat.id, type_data="phonenumber", value=str(contact))
    
    user_cache = get_info(cid=message.chat.id, type_data="cache")
    owner_id = get_info_gw(id=int(user_cache), x_type="gwo")
    owner_channels = get_info(cid=owner_id, type_data="channels")
        
    print("CC--CC", owner_id, owner_channels)
    await state.clear()

    if await join(user_id=message.chat.id, c_channels=owner_channels):
        if user_cache != "none":
            await bot.send_message(
                chat_id=message.chat.id,
                text=f"Сиз #{user_cache} гивевейда қатнашмоқдасиз! Тугаш вақти: {get_info_gw(id=int(user_cache), x_type='period')}. Ютсангиз хабар берамиз!",
            )
            change_info(cid=message.chat.id, type_data="add_gws", value=user_cache)
            change_info_gw(id=int(user_cache), x_type="add_user", value=message.chat.id)
            change_info(cid=message.chat.id, type_data="cache", value="none")
        else:
            await message.answer(
                "✋ Хуш келибсиз!\nБизнинг бот сизга канал ёки чатда ўйин ўтказишда ёрдам беради.\nЯнги совға яратишга тайёрмисиз?",
                reply_markup=home_button,
            )
    await sleep(0.3)


@router.callback_query(F.data == "mychannels")
async def gwo_channels(call: types.CallbackQuery):
    channels = get_info(cid=call.message.chat.id, type_data="channels")
    if len(channels) != 0:
        channel_list = "\n".join(channels)
    else:
        channel_list = "[МАВЖУД ЭМАС]"
    res = f"Сизнинг каналларингиз:\n {channel_list}"
    await bot.send_message(
        chat_id=call.message.chat.id, text=res, reply_markup=manage_channel
    )
    await sleep(0.3)


@router.callback_query(F.data == "add_channel_gwo")
async def add_gwo_channel(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(
        chat_id=call.message.chat.id, message_id=call.message.message_id
    )
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Қўшмоқчи бўлган каналиңиздан постни forward қилиб юборинг",
    )
    await state.set_state(PanelState.add_channel)
    await sleep(0.3)

@router.callback_query(F.data == "rm_channel_gwo")
async def rm_channel_gwo(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(
        chat_id=call.message.chat.id, message_id=call.message.message_id
    )
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Ўчирмоқчи бўлган каналиңиздан постни forward қилиб юборинг",
    )
    await state.set_state(PanelState.delete_channel)
    await sleep(0.3)


@router.message(PanelState.delete_channel)
async def rm_channel_gwo_state(msg: types.Message, state: FSMContext):
    if msg.forward_from_chat and msg.forward_from_chat.type == "channel":
        delete_channel_gwo(gwo=msg.chat.id, value=str(msg.forward_from_chat.id))
        await bot.send_message(chat_id=msg.chat.id, text="Бажарилди")
        await state.clear()
    else:
        await bot.send_message(
            chat_id=msg.chat.id,
            text="Хато!!! Қайтадан уриниб кўринг, жараённи бекор қилиш учун эса <b>/start</b> буйруғидан фойдаланинг!",
        )
    await sleep(0.3)

@router.message(PanelState.add_channel)
async def add_channel_gwo_state(msg: types.Message, state: FSMContext):
    if msg.forward_from_chat and msg.forward_from_chat.type == "channel":
        if await bot_is_admin(msg.forward_from_chat.id):
            add_channel_gwo(gwo=msg.chat.id, value=str(msg.forward_from_chat.id))
            await bot.send_message(chat_id=msg.chat.id, text="Бажарилди")
            await state.clear()
        else:
            await bot.send_message(
                chat_id=msg.chat.id,
                text="❌ Бот каналга админ қилинмаган ёки канал мавжуд эмас (ID хато)! Қайтадан уриниб кўринг, жараённи бекор қилиш учун /start буйруғидан фойдаланинг!",
            )
    else:
        await bot.send_message(
            chat_id=msg.chat.id,
            text="❌ Хато!!! Қайтадан уриниб кўринг, жараённи бекор қилиш учун /start буйруғидан фойдаланинг!",
        )
    await sleep(0.3)


@router.callback_query(F.data == "add_giveaway")
async def add_giveaway(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Конкурс тугаш вақтини киритинг. Масалан: <code>11.05.2008.13:00</code> , жараённи бекор қилиш учун /start буйруғини беринг.",
        parse_mode="HTML"
    )
    await state.set_state(PanelState.ask_giweaway_period)
    await sleep(0.3)

@router.message(PanelState.ask_giweaway_period)
async def add_giveaway_state(msg: types.Message, state: FSMContext):
    if is_time_check(time=msg.text):
        x_id = create_giveaway(gwo=msg.chat.id, period=msg.text)
        await bot.send_message(
            chat_id=msg.chat.id,
            text=f"Конкурс яратилди: https://t.me/{BOT_USERNAME}?start={x_id}",
        )
    else:
        await bot.send_message(
            chat_id=msg.chat.id,
            text="❌ Хато!!! Қайтадан уриниб кўринг, жараённи бекор қилиш учун /start буйруғидан фойдаланинг!",
        )
    await sleep(0.3)

@router.callback_query(F.data == "list_giveaway")
async def list_giveaway(call: types.CallbackQuery):
    if await join(user_id=call.message.chat.id):
        join_gw = get_info(cid=call.message.chat.id,type_data="gws")
        add_gw = get_own_gws(gwo=call.message.chat.id)
        
        join_gw=[get_info_gw(id=int(y), x_type="object") for y in join_gw]
        
        res = prepare_report(join_gw=join_gw,add_gw=add_gw)
        print(res)
        await bot.send_message(chat_id=call.message.chat.id,text=res)
        await sleep(0.3)

@router.callback_query(F.data == "support")
async def support(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="⚙️ Ботда муаммолар кузатилса дастурчига мурожаат қилинг.\n🧑‍💻",
    )
    await sleep(0.3)
