from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import trans #独自関数
import integratedSQL as sql #独自関数
import datetime

app = Flask(__name__)

#LINE Access Token
#os.environ["環境変数名"]
#YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_ACCESS_TOKEN = "RZNtaBkl4+E9IrrKQM1jDkC0ge5LQ/q6llRIC4IjbSfFncZcnw9ZajmsPomDJkm6VwTzsUQCbIDyujcm5d9qKBCxDKpNk3MVSlS8sWxWPULsxTzqSfUnzpfIInnxx/CLPqeDOAkmhwL1bhnrihqCwQdB04t89/1O/w1cDnyilFU="


#LINE User ID
#YOUR_USER_ID = os.environ["YOUR_USER_ID"]
YOUR_USER_ID="Uf7ae85768045d752c0cded101ea24c34"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
#handler = WebhookHandler(YOUR_CHANNEL_SECRET)

def zero(str_):
    if str_ == "0":
        return "00"
    else:
        return str_

def main():
    now = datetime.datetime.today() + datetime.timedelta(hours=9) #時差
    today = now.date()
    print("today:{}".format(today))
    schedules=sql.select(["date",today])
    print("schedule:{}".format(schedules))
    if schedules:#から出ない
        mes = "おはようございます🌞\n今日は"
        for _sche in schedules:
            mesTime=str(_sche[1].hour)+":"+zero(str(_sche[1].minute))
            mes += (mesTime + "に" +_sche[2]+"\n")
        mes += "があります！"
        line_bot_api.push_message(
        YOUR_USER_ID,
        TextSendMessage(text=mes))
    else:
        pass

        """
        mes="おはようございます🌞\n今日の予定はありません。"
        line_bot_api.push_message(
        YOUR_USER_ID,
        TextSendMessage(text=mes))
        """

    



if __name__ == "__main__":
    main()
