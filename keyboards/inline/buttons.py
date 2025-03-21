from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_keyboard = [
    [
        InlineKeyboardButton(text="✅ Ҳа", callback_data="yes"),
        InlineKeyboardButton(text="❌ Йўқ", callback_data="no"),
    ]
]
are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

adm_buttons_list = [
    [InlineKeyboardButton(text="📊 Статистика", callback_data="stat")],
    [InlineKeyboardButton(text="📬 Хабар юбориш", callback_data="send")],
    [InlineKeyboardButton(text="⚙️ Каналларни созлаш", callback_data="channels")],
    [
        InlineKeyboardButton(
            text="➕ Админларни бошқариш", callback_data="sitting_admins"
        )
    ],
]

admin_buttons = InlineKeyboardMarkup(inline_keyboard=adm_buttons_list)

channel_control_buttons_list = [
    [InlineKeyboardButton(text="➕ Канал қўшиш", callback_data="channel_add")],
    [InlineKeyboardButton(text="➖ Канални олиб ташлаш", callback_data="channel_del")],
]

channel_control = InlineKeyboardMarkup(inline_keyboard=channel_control_buttons_list)


def join_buttons(l):
    button_base = []

    for i, j in enumerate(l):
        button_base.append([InlineKeyboardButton(text=f"〽️ {i+1}-канал", url=j)])

    button_base.append(
        [InlineKeyboardButton(text="✔️ Текшириш", callback_data="check_join")]
    )
    res = InlineKeyboardMarkup(inline_keyboard=button_base)

    return res
