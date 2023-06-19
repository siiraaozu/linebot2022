"""
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)

import os

"""
from flask import request, abort
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import new_trans #独自関数
import integratedSQL as sql #独自関数
import datetime


from init_src import *

import psycopg2
"""
app = Flask(__name__)

#LINE Access Token
#os.environ["環境変数名"]
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
#LINE Channel Secret
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

now = datetime.datetime.today() + datetime.timedelta(hours=9) #時差
today = now.date()
"""

app, line_bot_api, handler = init_flask(LINE_RECEIVE)
now, today= get_nowToday()



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    # ここでLINEからのメッセージを受け取るらしいm→違うっぽい
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# Messageを送る
# メッセージが来た時の反応らしい
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        userMes = event.message.text
        print("mes:{}".format(userMes))

        #送信テキストの保存
        sql.save_send(userMes)
        [mesType,schedule] = new_trans.new_trans(userMes) 
        print("type:{}".format(mesType))
        if mesType == 1: #予定表示
            schedules = sql.disp(0)
            mes = "" #メッセージの準備
            if schedules: #空でない
                #print("today:{}".format(today))
                #print("all:{}".format(con_all))
                for _sche in schedules:
                    #デフォルトは、今日以降の予定を表示
                    con_all = (schedule == "all")

                    con_nf = _sche[0] >= today #今日以降 nf:now and future
                    con_u1m = _sche[0] <= today + datetime.timedelta(days=31)#今日から一ヶ月以内
                    if con_all or (not con_all and con_nf and con_u1m): #allとデフォルトを両方表現
                        print(_sche[0], _sche[1], _sche[2])
                        mesDate = str(_sche[0].year)  + " "+ str(_sche[0].month) + "/" + str(_sche[0].day)
                        mes += (mesDate + "　")
                        mesTime = str(_sche[1].hour) + ":" + zero(str(_sche[1].minute))
                        mes += (mesTime + "　" + _sche[2]+"\n")
                mes = mes[:-1]#最後の改行をとる
            else:
                mes="一ヶ月以内の予定はありません。"

        elif mesType == 2: #予定登録
            print("type1:{}".format(type(schedule[0])))
            #予定登録SQL実行
            sql.add(schedule) 
            mes = str(schedule[0].month) + "月" + str(schedule[0].day) +"日の"
            mes += str(schedule[0].hour) + ":" + zero(str(schedule[0].minute)) + "に"
            mes +=  schedule[1] + "ですね！\n予定を登録しました！\n予定を表示するには「予定」と入力してください♪"

        elif mesType == 3: #予定削除(実行)
            #「削除　日付」→削除確認→はい→削除 いいえ→何もしない
            mes = ""
            if schedule == "":
                sql.delete0(0)
            else:
                sql.delete(schedule[1])
                mes = str(schedule[1].month) + "月" + str(schedule[1].day) +"日の"
            mes += "予定を削除しました！"

        elif mesType == 4: #予定削除(確認)
            if schedule == "":
                mes = "予定を【すべて】削除しますか？\n削除する場合は「はい」\n 削除しない場合は「いいえ」を入力するか、別のコマンドを入力してください。"
            else:
                mes = "予定を削除しますか？\n削除する場合は「はい」\n 削除しない場合は「いいえ」を入力するか、別のコマンドを入力してください。"

        elif mesType == 9:
            mes = "コマンドが間違っているみたいです…\nもう一度入力してください。"

        elif mesType == 10:
            mes = "処理を取り消しました。"

        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=mes))

    except psycopg2.OperationalError:
        mes = "エラー\nherokuの資格情報を確認してください。"
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=mes))
    except:
        mes = "エラー\nログを確認してください。"
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=mes))




if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
