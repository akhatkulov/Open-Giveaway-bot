from helper_utils.is_past_time import is_past_time
from utils.db.alchemy import get_all_gw, get_info_gw, change_info_gw
from time import sleep
from random import choice
from telebot import TeleBot

bot = TeleBot(token="6134216242:AAGNDauGK33d7IKyG_67Zs42IuObnba0wD0")

while True:
    for target in get_all_gw():
        print(
            target.id,
            get_info_gw(id=target.id, x_type="period"),
            get_info_gw(id=target.id, x_type="users"),
            get_info_gw(id=target.id, x_type="status"),
        )
    for target in get_all_gw():
        print(
            target.id,
            get_info_gw(id=target.id, x_type="period"),
            get_info_gw(id=target.id, x_type="users"),
            get_info_gw(id=target.id, x_type="status"),
        )
        d, m, y, h = get_info_gw(id=target.id, x_type="period").split(".")
        if get_info_gw(id=target.id, x_type="status") == "open" and is_past_time(
            d, m, y, h
        ) and len(get_info_gw(id=target.id, x_type="users")) != 0:
            change_info_gw(id=target.id, x_type="status", value="close")
            users = get_info_gw(id=target.id, x_type="users")
            winner = choice(users)
            bot.send_message(
                chat_id=winner,
                text=f"Табриклаймиз, сиз #{target.id} giveawayида ютдингиз!\n\n <a href='tg://user?id={get_info_gw(id=target.id,x_type='gwo')}'> Giveaway эгаси </a> ID:{get_info_gw(id=target.id,x_type='gwo')}",
                parse_mode="html",
            )
            bot.send_message(
                chat_id=get_info_gw(id=target.id, x_type="gwo"),
                text=f"Сизнинг #{target.id} giveawayингизда <a href='tg://user?id={winner}'>БУ КИШИ</a> ID:{winner} ютди.",
                parse_mode="html",
            )
            change_info_gw(id=target.id, x_type="winner", value=winner)
        sleep(5)
