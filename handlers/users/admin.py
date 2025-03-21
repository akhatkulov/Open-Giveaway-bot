import logging
import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from loader import bot
from keyboards.inline.buttons import admin_buttons, channel_control
from states.test import AdminState
from filters.admin import IsBotAdminFilter
from utils.db.alchemy import (
    user_count,
    get_all_user,
    get_channel,
    put_channel,
    get_channel_with_id,
    delete_channel,
    get_admins,
    change_info,
    manage_admin,
)
from data.config import ADMIN

router = Router()


@router.message(Command("admin"), IsBotAdminFilter())
async def admin_panel(msg: types.Message):
    await bot.send_message(
        chat_id=msg.chat.id,
        text="Салом, Админ! Хуш келибсиз.",
        reply_markup=admin_buttons,
    )


@router.message(Command("list_admins"), IsBotAdminFilter())
async def get_admins_list(msg: types.Message):
    if int(msg.chat.id) == ADMIN:
        l_o_a = get_admins()
        print(l_o_a)
        await bot.send_message(
            chat_id=msg.chat.id, text=f"Админлар рўйхати:\n\n{l_o_a}"
        )


@router.message(Command("add_admin"), IsBotAdminFilter())
async def add_admin(msg: types.Message):
    if int(msg.chat.id) == ADMIN:
        try:
            target_cid = msg.text.split()[1]
            print(target_cid)
            manage_admin(cid=int(target_cid), action="add")
            await bot.send_message(chat_id=msg.chat.id, text=f"✅ Бажарилди.")
        except Exception as e:
            await bot.send_message(chat_id=ADMIN, text=f"❌ Хатолик: {e}")
    else:
        await bot.send_message(chat_id=msg.chat.id, text="⛔ Сизда бундай имконият йўқ!")


@router.message(Command("del_admin"), IsBotAdminFilter())
async def del_admin(msg: types.Message):
    if int(msg.chat.id) == ADMIN:
        try:
            target_cid = msg.text.split()[1]
            manage_admin(cid=int(target_cid), action="rm")
            await bot.send_message(chat_id=msg.chat.id, text=f"✅ Админ ўчирилди.")
        except Exception as e:
            await bot.send_message(chat_id=ADMIN, text=f"❌ Хатолик: {e}")
    else:
        await bot.send_message(chat_id=msg.chat.id, text="⛔ Сизда бундай имконият йўқ!")


@router.callback_query(F.data == "stat")
async def show_stat(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id, text=f"👥 Фойдаланувчилар сони: {user_count()}"
    )


@router.callback_query(F.data == "send")
async def ask_ad_content(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="📢 Юбормоқчи бўлган хабарингизни юборинг. Бекор қилиш учун /admin!",
    )
    await state.set_state(AdminState.ask_ad_content)


@router.callback_query(F.data == "channels")
async def show_channels(call: types.CallbackQuery):
    r = get_channel_with_id()
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=f"📡 Каналлар рўйхати:\n{r}",
        reply_markup=channel_control,
    )


@router.callback_query(F.data == "channel_add")
async def ask_channel_add(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="🔗 @ белгисиз канал манзилини юборинг. Бекор қилиш учун /admin!",
    )
    await state.set_state(AdminState.Add_Channel)


@router.callback_query(F.data == "channel_del")
async def ask_channel_del(call: types.CallbackQuery, state: FSMContext):
    res_text = f"{get_channel_with_id()}\n\n❌ Ўчирмоқчи бўлган канали ID рақамини юборинг. Бекор қилиш учун /admin!"
    await bot.send_message(chat_id=call.message.chat.id, text=res_text)
    await state.set_state(AdminState.Delete_Channel)


@router.callback_query(F.data == "sitting_admins", IsBotAdminFilter())
async def admin_settings(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=f"⚙️ Бу функциядан фақат {ADMIN} фойдаланиши мумкин!\n\n"
             "/list_admins - Админлар рўйхатини кўриш\n"
             "/add_admin [CID] - Админ қўшиш\n"
             "/del_admin [CID] - Админни ўчириш",
    )


@router.message(AdminState.ask_ad_content, IsBotAdminFilter())
async def send_ad_to_users(message: types.Message, state: FSMContext):
    if message.text not in ["/admin", "/start"]:
        users = get_all_user()
        count = 0
        for user in users:
            try:
                await message.send_copy(chat_id=user)
                count += 1
                await asyncio.sleep(0.033)
            except Exception as error:
                logging.info(f"Хабар юборилмади: {user}. Хатолик: {error}")
        await message.answer(
            text=f"📢 Реклама {count} та фойдаланувчига юборилди."
        )
    await state.clear()


@router.message(AdminState.Add_Channel, IsBotAdminFilter())
async def add_channel_process(message: types.Message, state: FSMContext):
    if message.text not in ["/admin", "/start"]:
        try:
            put_channel(channel=message.text)
            await bot.send_message(
                chat_id=message.chat.id,
                text=f"📡 @{message.text} мажбурий каналлар рўйхатига қўшилди ✅",
            )
        except Exception as error:
            logging.info(f"Канални қўшишда хатолик: {error}")
    await state.clear()


@router.message(AdminState.Delete_Channel, IsBotAdminFilter())
async def delete_channel_process(message: types.Message, state: FSMContext):
    if message.text not in ["/admin", "/start"]:
        try:
            x = int(message.text)
            if delete_channel(ch_id=x):
                await bot.send_message(
                    chat_id=message.chat.id, text="❌ Канал ўчирилди."
                )
            else:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="⚠️ Хатолик! ID'ни тўғри киритдингизми?",
                )
        except Exception as error:
            logging.info(f"Канални ўчиришда хатолик: {error}")

    await state.clear()
