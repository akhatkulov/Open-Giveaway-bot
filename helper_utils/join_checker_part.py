from loader import bot
from utils.db.alchemy import get_channel, create_user, change_info, is_there
from keyboards.inline.buttons import join_buttons
from data.config import ADMIN


async def join(user_id, c_channels=[]):
    try:
        channels = get_channel()
        channels = [*channels, *c_channels]
        x_channels = []
        for channel in channels:
            status = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if status.status == "left":
                x_channels.append(await bot.export_chat_invite_link(chat_id=channel))

        if x_channels:
            await bot.send_message(
                chat_id=user_id,
                text="Iltimos, barcha kanallarga obuna bo'ling!",
                reply_markup=join_buttons(x_channels),
            )
            return False
        else:
            return True
    except Exception as e:
        print(e)
        await bot.send_message(
            ADMIN, f"Kanalga bot admin qilinmagan yoki xato: {str(e)}"
        )
        return True
