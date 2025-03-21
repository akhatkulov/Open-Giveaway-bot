from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

manage_channel_buttons = [
    [InlineKeyboardButton(text="Qo'shish➕", callback_data="add_channel_gwo")],
    [InlineKeyboardButton(text="Olib tashlash ➖", callback_data="rm_channel_gwo")],
]

manage_channel = InlineKeyboardMarkup(inline_keyboard=manage_channel_buttons)
