
import new_convert #独自関数
from new_convert import Schedule, Command
import integratedSQL as sql #独自関数
import datetime


from init_src import *

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

#app, line_bot_api, handler = init_flask(LINE_RECEIVE)
now, today= get_nowToday()

def check_isDupicateEvent(event_id):
    event_sameid = sql.select("send_log", "event_id", event_id)
    if event_sameid:
        return True
    else:
        return False

def checkSave_mesEvent(event_id, userMes, timestamp_dt):
    if check_isDupicateEvent(event_id):
        print("Dupicate message. (id:{})".format(event_id))
        return False
    else:
        #送信テキストの保存
        sql.save_send(timestamp_dt, userMes, event_id)
        print("id:{} mes:{}".format(event_id, userMes))
        return True

# handle_msg2reply サブ関数
def handle_dispSchedule(new_cmd):
    schedules = sql.disp(0)
    reply_mes = "" #メッセージの準備
    if schedules: #空でない
        for _sche in schedules:
            #デフォルトは、今日以降の予定を表示
            con_all = (new_cmd.content == "all")
            con_nf = _sche[0] >= today #今日以降 nf:now and future
            con_u1m = _sche[0] <= today + datetime.timedelta(days=31)#今日から一ヶ月以内
            if con_all or (not con_all and con_nf and con_u1m): #allとデフォルトを両方表現
                print(_sche[COL_SCHEDULE_DATE], _sche[COL_SCHEDULE_TIME], _sche[COL_SCHEDULE_EVENT])
                mesDate = str(_sche[COL_SCHEDULE_DATE].year)  + " "+ str(_sche[COL_SCHEDULE_DATE].month) + "/" + str(_sche[COL_SCHEDULE_DATE].day)
                reply_mes += (mesDate + "　")
                mesTime = str(_sche[COL_SCHEDULE_TIME].hour) + ":" + zero(str(_sche[COL_SCHEDULE_TIME].minute))
                reply_mes += (mesTime + "　" + _sche[COL_SCHEDULE_EVENT]+"\n")        
        if reply_mes:
                reply_mes = reply_mes[:-1]#最後の改行をとる
        else:
            reply_mes= "一ヶ月以内の予定はありません。"
    else:
        reply_mes="予定はありません。"
    return reply_mes

def handle_registSchedule(new_cmd):
    schedule = new_cmd.content
    sql.add(schedule) 
    reply_mes = str(schedule.datetime.month) + "月" + str(schedule.datetime.day) +"日の"
    reply_mes += str(schedule.datetime.hour) + ":" + zero(str(schedule.datetime.minute)) + "に"
    reply_mes +=  schedule.event + "ですね！\n予定を登録しました！\n予定を表示するには「予定」と入力してください♪"
    return reply_mes

def handle_execute(new_cmd):
    prev_userMes = sql.ref_log(2)[COL_SENDLOG_MES_TXT]
    #[prev_mesType, prev_schedule] = new_convert.convert(prev_userMes) 
    prev_newcmd = new_convert.convert(prev_userMes) 
    prev_schedule = prev_newcmd.content
    if prev_newcmd.mesType == "confirm_delete":
        reply_mes = ""
        if type(prev_schedule.datetime) is datetime.date:
            sql.delete(prev_schedule.datetime.strftime('%Y-%m-%d'))
            reply_mes = str(prev_schedule.datetime.month) + "月" + str(prev_schedule.datetime.day) +"日の"
        else:
            sql.delete0(0)
        reply_mes += "予定を削除しました！"
    else:
        reply_mes = "無効なコマンドです…。"
    return reply_mes

def handle_confirmDelete(new_cmd):
    if type(new_cmd.content) != Schedule:
        reply_mes = "予定を【すべて】削除しますか？\n削除する場合は「はい」\n 削除しない場合は「いいえ」を入力するか、別のコマンドを入力してください。"
    else:
        reply_mes = "予定を削除しますか？\n削除する場合は「はい」\n 削除しない場合は「いいえ」を入力するか、別のコマンドを入力してください。"
    return reply_mes

def handle_error(new_cmd):
    reply_mes = "コマンドが間違っているみたいです…\nもう一度入力してください。"
    return reply_mes

def handle_abort(new_cmd):
    reply_mes = "処理を取り消しました。"
    return reply_mes


def handle_msg2reply(userMes):
    new_cmd = new_convert.convert(userMes) 
    print("type:{}".format(new_cmd.mesType))

    func_dict = {
    "display_schedule" : handle_dispSchedule,
    "regist_schedule" : handle_registSchedule,
    "execute" : handle_execute,
    "confirm_delete" : handle_confirmDelete,
    "error" : handle_error,
    "abort" : handle_abort
    }

    return func_dict[new_cmd.mesType](new_cmd)

def handle_message_core(event_id, userMes, timestamp_dt):
    chk  = checkSave_mesEvent(event_id, userMes, timestamp_dt)
    if chk:
        reply_mes = handle_msg2reply(userMes)
    else:
        reply_mes = ""
    return reply_mes

#デバッグ用
if __name__=='__main__':
    event_id = "01HCPE0ZGASC38J25Q9PN368GFWWD"
    userMes="いいえ"
    timestamp_dt = datetime.datetime.now()
    print(handle_message_core(event_id, userMes, timestamp_dt))
    