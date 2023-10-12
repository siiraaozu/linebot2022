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

import integratedSQL as sql #独自関数
import handle_msg


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

        reply_mes = handle_msg.handle_msg2reply(userMes)
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_mes))

    except psycopg2.OperationalError:
        reply_mes = "エラー\nherokuの資格情報を確認してください。"
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_mes))
    except:
        reply_mes = "エラー\nログを確認してください。"
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_mes))




if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
