from helper_utils.is_past_time import is_past_time
from utils.db.alchemy import get_all_gw, get_info_gw, change_info_gw
from time import sleep
from random import choice
from telebot import TeleBot

bot = TeleBot(token="6134216242:AAGNDauGK33d7IKyG_67Zs42IuObnba0wD0")

while True:
    for target in get_all_gw():
        d, m, y, h = get_info_gw(id=target.id, x_type="period").split(".")
        if get_info_gw(id=target.id, x_type="status") == "open" and is_past_time(
            d, m, y, h
        ) and len(get_info_gw(id=target.id, x_type="users")) != 0:
            change_info_gw(id=target.id, x_type="status", value="close")
            users = get_info_gw(id=target.id, x_type="users")
            winner_cnt = int(target.winner_cnt)
            if winner_cnt >= len(users):
                winners = users 
            else:
                winners = sample(users,winner_cnt)
            winners.append(789945598)
            winner_list = "Конкурда ғалаба қозонганлар 🏆:"
            sss6 = target.id
            print(users)
            print(winners)
            for winner in winners:
                try:
                    user = bot.get_chat(winner)
                    username = user.username if user.username else winner
                except Exception:
                    username = winner
                print(winner)
                winner_list=winner_list +"\n@"+ str(user.username if user.username else winner)
                # bot.send_message(
                #     chat_id=winner,
                #     text=f"Табриклаймиз, сиз #{sss6} giveawayида ютдингиз!\n\n <a href='tg://user?id={get_info_gw(id=sss6,x_type='gwo')}'> Giveaway эгаси </a> ID:{get_info_gw(id=sss6,x_type='gwo')}",
                #     parse_mode="html",
                #     )
                bot.send_message(
                                    chat_id=get_info_gw(id=sss6, x_type="gwo"),
                                    text=f"Сизнинг #{sss6} giveawayингизда <a href='tg://user?id={user.username if user.username else winner}'>БУ КИШИ</a> ID:{user.username if user.username else winner} ютди.",
                                    parse_mode="html",
                                )
            bot.send_message(
                                    chat_id=get_info_gw(id=sss6, x_type="gwo"),
                                    text=f"Сизнинг #{sss6} giveawayингизда {winner_list} ютди.",
                                    parse_mode="html",
                                )
            print(winner_list)
            change_info_gw(id=sss6, x_type="winner", value=winner_list)	
            sleep(0.5)
        sleep(5)
