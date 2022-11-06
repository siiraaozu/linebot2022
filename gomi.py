#伝言を張る

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
#import trans #独自関数
#import integratedSQL as sql #独自関数
import datetime

now = datetime.datetime.today() + datetime.timedelta(hours=9) #時差
today = now.date()

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

def mes_garbage(weekday):
    mes = ""
    mes_1st = "🏠ゴミ出し情報🏠\n今日は"
    mes_half = ["【不燃ゴミ】と【プラ】", "【可燃ゴミ】", "【PET】", "【紙布缶】または【ビン】", "【可燃ごみ】", "", ""]
    mes_2nd = "のゴミ出しの日です！\n"
    mes3_add = ["第2水曜日は【粗大ごみ】の日です。何か捨てるものはありませんか？", 
                "冷凍庫の生ごみの処理は大丈夫ですか？",
                "明日は【紙布缶/ビン】の回収日です。紙布缶はまとめるのが大変なので、早めに準備しましょう！",
                "冷凍庫の生ごみの処理は大丈夫ですか？",
                "",
                ""]

    if weekday < 5:
        mes = mes_1st + mes_half[weekday] + mes_2nd + mes3_add[weekday]
        print(mes)
    return mes


def main():
    weekday = today.weekday()
    mes = mes_garbage(weekday)

    #タスクがあるとき
    if mes != "":
        line_bot_api.push_message(
        YOUR_USER_ID,
        TextSendMessage(text=mes))



if __name__ == "__main__":
    main()


