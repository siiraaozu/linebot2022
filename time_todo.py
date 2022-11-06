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
import requests
import trans_todo as trans

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



def main():
    response = requests.get('https://dl.dropboxusercontent.com/s/9tq9l020fl5y4j8/todolist.txt')
    txt = response.text
    mes = ""
    txt = txt.splitlines()

    #メッセージ作成
    for todo in txt:
        todo_n = trans.trans_todo(todo)
        print(todo_n)
        #優先度(A)かつ(期日5日以内　or 期日無し)
        if todo_n["priority"] == "A":
            if todo_n["due"] == None:
                left = "期日なし"
                mes += (todo_n["task"] + " (" + left + ")\n")
            elif (todo_n["due"] - today).days <=5:
                td=todo_n["due"]-datetime.date.today()
                left = "あと" + str(td.days) + "日"
                mes += (todo_n["task"] + " (" + left + ")\n")

    #タスクがあるとき
    if mes != "":
        mes = "現在のタスク(todolist.txt, 重要度A)をお届けします♪\n" + mes
        mes = mes[:-1]#最後の改行をとる
        line_bot_api.push_message(
        YOUR_USER_ID,
        TextSendMessage(text=mes))



if __name__ == "__main__":
    main()
