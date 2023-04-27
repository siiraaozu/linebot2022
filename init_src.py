from flask import Flask

from linebot import (
    LineBotApi, WebhookHandler
)

import os
import datetime

#定数
LINE_RECEIVE = 0
LINE_SEND = 1

idx_TOKEN = 0
idx_SECRET = 1
idx_USERID = 2

try:
    YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
    YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
    YOUR_USER_ID = os.environ["YOUR_USER_ID"]
except KeyError:
    print("[DEBUG]")
    YOUR_CHANNEL_ACCESS_TOKEN = "RZNtaBkl4+E9IrrKQM1jDkC0ge5LQ/q6llRIC4IjbSfFncZcnw9ZajmsPomDJkm6VwTzsUQCbIDyujcm5d9qKBCxDKpNk3MVSlS8sWxWPULsxTzqSfUnzpfIInnxx/CLPqeDOAkmhwL1bhnrihqCwQdB04t89/1O/w1cDnyilFU="
    YOUR_USER_ID="Uf7ae85768045d752c0cded101ea24c34"

#関数
def init_flask(mode):
    app = Flask(__name__)

    line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)

    if mode == 0:
        handler = WebhookHandler(YOUR_CHANNEL_SECRET)
        return app, line_bot_api, handler
    else:
        return line_bot_api

def get_nowToday():
    now = datetime.datetime.today() \
        + datetime.timedelta(hours=9) #時差
    today = now.date()

    return now, today

def get_tomorrow():
    now = datetime.datetime.today() \
        + datetime.timedelta(hours=9) #時差
    nowplus24 = now +  datetime.timedelta(hours=24)#今日→明日
    tomorrow = nowplus24.date()
    return tomorrow