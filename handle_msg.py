from flask import request, abort

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import new_trans #独自関数
import integratedSQL as sql #独自関数
import datetime


from init_src import *

import psycopg2

app, line_bot_api, handler = init_flask(LINE_RECEIVE)
now, today= get_nowToday()


def handle_msg2reply(userMes):
    #リトライ重複チェック
    prev_userMes_beforesave = sql.ref_log(1)[1]
    if userMes != prev_userMes_beforesave:
        #送信テキストの保存
        sql.save_send(userMes)
        [mesType,schedule] = new_trans.trans(userMes) 
        print("type:{}".format(mesType))
        if mesType == 1: #予定表示
            schedules = sql.disp(0)
            reply_mes = "" #メッセージの準備
            if schedules: #空でない
                for _sche in schedules:
                    #デフォルトは、今日以降の予定を表示
                    con_all = (schedule == "all")
                    con_nf = _sche[0] >= today #今日以降 nf:now and future
                    con_u1m = _sche[0] <= today + datetime.timedelta(days=31)#今日から一ヶ月以内
                    if con_all or (not con_all and con_nf and con_u1m): #allとデフォルトを両方表現
                        print(_sche[0], _sche[1], _sche[2])
                        mesDate = str(_sche[0].year)  + " "+ str(_sche[0].month) + "/" + str(_sche[0].day)
                        reply_mes += (mesDate + "　")
                        mesTime = str(_sche[1].hour) + ":" + zero(str(_sche[1].minute))
                        reply_mes += (mesTime + "　" + _sche[2]+"\n")        
                if reply_mes:
                        reply_mes = reply_mes[:-1]#最後の改行をとる
                else:
                    reply_mes= "一ヶ月以内の予定はありません。"
            else:
                reply_mes="予定はありません。"

        elif mesType == 2: #予定登録
            print("type1:{}".format(type(schedule[0])))
            #予定登録SQL実行
            sql.add(schedule) 
            reply_mes = str(schedule[0].month) + "月" + str(schedule[0].day) +"日の"
            reply_mes += str(schedule[0].hour) + ":" + zero(str(schedule[0].minute)) + "に"
            reply_mes +=  schedule[1] + "ですね！\n予定を登録しました！\n予定を表示するには「予定」と入力してください♪"

        elif mesType == 3: #予定削除(実行)
            #「削除　日付」→削除確認→はい→削除 いいえ→何もしない
            #send logの2番目に新しいデータを見る

            prev_userMes = sql.ref_log(2)[1]
            [prev_mesType, prev_schedule] = new_trans.trans(prev_userMes) 
            if prev_mesType == 4:
                reply_mes = ""
                if type(prev_schedule[0]) is datetime.date:
                    sql.delete(prev_schedule[0].strftime('%Y-%m-%d'))
                    reply_mes = str(prev_schedule[0].month) + "月" + str(prev_schedule[0].day) +"日の"
                else:
                    sql.delete0(0)
                reply_mes += "予定を削除しました！"
            else:
                reply_mes = "無効なコマンドです…。"

        elif mesType == 4: #予定削除(確認)
            if schedule == "":
                reply_mes = "予定を【すべて】削除しますか？\n削除する場合は「はい」\n 削除しない場合は「いいえ」を入力するか、別のコマンドを入力してください。"
            else:
                reply_mes = "予定を削除しますか？\n削除する場合は「はい」\n 削除しない場合は「いいえ」を入力するか、別のコマンドを入力してください。"

        elif mesType == 9:
            reply_mes = "コマンドが間違っているみたいです…\nもう一度入力してください。"

        elif mesType == 10:
            reply_mes = "処理を取り消しました。"
    else: 
        reply_mes = "⚠メッセージが重複しています！\n送信のリトライを行った可能性があります。"
    return reply_mes