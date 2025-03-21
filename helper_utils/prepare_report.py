import json

def prepare_report(join_gw, add_gw):
    res = "Сиз қилган Giveawayлар🏆:\n\n"
    
    for x in add_gw:
        res += f"🆔:{x.id}\n📅:{x.period}\n👥:{len(json.loads(x.users))}\n❓:{x.status}\n🏆:{x.winner}\n\n"
    
    res += "Сиз қатнашган Giveawayлар🏆:\n\n"
    
    for x in join_gw:
        print(x.users)
        res += f"🆔:{x.id}\n📅:{x.period}\n👥:{len(json.loads(x.users))}\n❓:{x.status}\n🏆:{x.winner}\n\n"
    
    return res
