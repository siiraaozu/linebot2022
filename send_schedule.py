
#initに必要なもの以外は入れない
from linebot.models import (
    TextSendMessage,
)

from init_src import *

import integratedSQL as sql #独自関数


#date:today or tomorrow
#mes[MES_BEGIN,MES_END]
#MES_BEGIN="おはようございます🌞\n今日は"
#MES_END="があります！"
def makeMes_schedule(date, MES_BEGIN, MES_END):
    schedules = sql.select(["date",date])
    print("schedule:{}".format(schedules))

    if schedules:
        mes = MES_BEGIN
        for _sche in schedules:
            mesTime=str(_sche[1].hour)+":"+zero(str(_sche[1].minute))
            mes += (mesTime + "に" +_sche[2]+"\n")
        mes += MES_END
        return mes
    else:
        return ""

def line_send(mes):
    line_bot_api = init_flask(LINE_SEND)
    if len(mes) > 0:
        line_bot_api.push_message(
            YOUR_USER_ID,
            TextSendMessage(text=mes))

def main():
    now, today= get_nowToday()
    print("today:{}".format(today))

    mes = makeMes_schedule(today \
                        ,MES_BEGIN = "おはようございます🌞\n今日は" \
                        , MES_END="があります！")
    
    line_send(mes)

#うえとおなじ
def timeSend_schedule():
    now, today= get_nowToday()
    print("today:{}".format(today))

    mes = makeMes_schedule(today \
                        ,MES_BEGIN = "おはようございます🌞\n今日は" \
                        , MES_END = "があります！")
    
    line_send(mes)

def timeSend_scheduleNight():
    tomorrow = get_tomorrow()
    print("tomorrow:{}".format(tomorrow))

    mes = makeMes_schedule(tomorrow \
                        ,MES_BEGIN = "明日は" \
                        , MES_END=  "があります。\n忘れないでくださいね。") 
    line_send(mes)


#デバッグ陽
if __name__ == "__main__":
   timeSend_scheduleNight()
