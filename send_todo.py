"""
from flask import Flask

from linebot import (
    LineBotApi
)

from linebot.models import (
    TextSendMessage,
)
"""


import requests
import covert_todo
import send_schedule

from init_src import *

def makeMes_todo():
    response = requests.get('https://dl.dropboxusercontent.com/s/9tq9l020fl5y4j8/todolist.txt')
    txt = response.text
    mes = ""
    txt = txt.splitlines()

    now, today= get_nowToday()

    #メッセージ作成
    for todo in txt:
        todo_n = covert_todo.covert_todo(todo)
        print(todo_n)
        #優先度(A)かつ(期日5日以内　or 期日無し)
        if todo_n["priority"] == "A":
            if todo_n["due"] == None:
                left = "期日なし"
                mes += (todo_n["task"] + " (" + left + ")\n")
            elif (todo_n["due"] - today).days <=5:
                td = todo_n["due"] - today #なぜ時差ない？(前ver)
                left = "あと" + str(td.days) + "日"
                mes += (todo_n["task"] + " (" + left + ")\n")
    
    if mes != "":
        mes = "現在のタスク(todolist.txt, 重要度A)をお届けします♪\n" + mes
        mes = mes[:-1]#最後の改行をとる
    return mes

def timeSend_todo():
    mes = makeMes_todo()
    send_schedule.line_send(mes)



# for debug
if __name__ == "__main__":
    timeSend_todo()
