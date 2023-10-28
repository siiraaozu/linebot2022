"""
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)

import os

"""
from flask import request, abort
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import integratedSQL as sql #独自関数
import handle_msg
import datetime

from init_src import *

import psycopg2


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
    event_id = event.webhook_event_id
    userMes = event.message.text
    timestamp_dt = datetime.datetime.fromtimestamp(int(event.timestamp)/1000)

    try:           
        reply_mes = handle_msg.handle_message_core(event_id, userMes, timestamp_dt)
        if not(reply_mes):
            return 0
    except psycopg2.OperationalError:
        reply_mes = "エラー\nherokuの資格情報を確認してください。"
    except:
        reply_mes = "エラー\nログを確認してください。"
    finally:
        try:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_mes))
        except LineBotApiError:
            #tugiha invalid token指定したい
            line_bot_api.push_message(
            YOUR_USER_ID,
            TextSendMessage(text=reply_mes))
        except:
            reply_mes = "エラー\nログを確認してください。"
            line_bot_api.push_message(
            YOUR_USER_ID,
            TextSendMessage(text=reply_mes))

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
