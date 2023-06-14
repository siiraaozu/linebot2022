
#initに必要なもの以外は入れない
from linebot.models import (
    TextSendMessage,
)

from init_src import *
from common import zero

import integratedSQL as sql #独自関数

import time_schedule

def main():
    now = datetime.datetime.today() + datetime.timedelta(hours=9) #時差
    tomorrow = get_tomorrow(now)
    print("tomorrow:{}".format(tomorrow))

    schedules=sql.select(["date",tomorrow])
    print("schedule:{}".format(schedules))

    if schedules:
        mes = "明日は"
        for _sche in schedules:
            mesTime=str(_sche[1].hour)+":"+zero(str(_sche[1].minute))
            mes += (mesTime + "に" +_sche[2]+"\n")
        mes += "があります。\n忘れないでくださいね。"
        line_bot_api.push_message(
        YOUR_USER_ID,
        TextSendMessage(text=mes))
    else:
        pass
        #mes="おはようございます🌞\n今日の予定はありません。"




if __name__ == "__main__":
    time_schedule.time_scheduleNight()
