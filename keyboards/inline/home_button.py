from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

home_button_list = [
    [
        InlineKeyboardButton(text="Giveaway яратиш🎁", callback_data="add_giveaway"),
        InlineKeyboardButton(text="Giveawayларим 🗒", callback_data="list_giveaway"),
    ],
    [
        InlineKeyboardButton(text="Каналларим 📢", callback_data="mychannels"),
        InlineKeyboardButton(text="Техник ёрдам ⁉️", callback_data="support"),
    ],
    # [InlineKeyboardButton(text="Ҳомийлик 💰", callback_data="donate")],
]

home_button = InlineKeyboardMarkup(inline_keyboard=home_button_list)
