from loader import bot


async def bot_is_admin(kanal_id):
    try:
        chat_member = await bot.get_chat_member(
            chat_id=kanal_id, user_id=(await bot.me()).id
        )
        return chat_member.status in ["administrator", "creator"]
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return False
    finally:
        await bot.session.close()
