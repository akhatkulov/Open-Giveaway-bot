from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def send_number():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return markup
