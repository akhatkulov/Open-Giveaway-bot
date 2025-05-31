from loader import bot

async def get_channel_info(channels):
    channel_list = []
    for channel_id in channels:
        chat = await bot.get_chat(channel_id)
        if chat.username:
            channel_list.append(f"@{chat.username}")
        else:
            channel_list.append(chat.title)
    return "\n".join(channel_list) if channel_list else "[МАВЖУД ЭМАС]"