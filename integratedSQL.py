# -*- coding: utf-8 -*-
import psycopg2
import datetime #for debug

#linebotから情報が送られる
sche=["2019-7-30", "6:00", "面談"]


def sqlproc(func): ##SQL処理
    def wrapper(*args, **kwargs):
        dsn = "dbname=linebot_xjgh port=5432 host=dpg-cdcj0s82i3msb94cqrcg-a.oregon-postgres.render.com user=satoshi password=ZqnpwBDLryspgqj4piqddWBdoqh92BWW"
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        #print('--start--')
        ans=func(cur,*args, **kwargs)
        #print('--end--')
        conn.commit()
        cur.close()
        conn.close()
        return ans #戻り値が在るばあいは返す

    return wrapper

@sqlproc
def add(_cur,_sche): #予定の追加 _sche:要素2のりすと[日時,予定]
    _cur.execute("INSERT INTO schedule values(%s, %s, %s);",(_sche[0].date(), _sche[0].time(), _sche[1]))

@sqlproc
def delete(_cur,_date): #date:'2019-07-30'
    _cur.execute("DELETE FROM schedule WHERE date=%s;",(_date,))

@sqlproc
def delete0(_cur,_num): #date:'2019-07-30'
    _cur.execute("DELETE FROM schedule;")

@sqlproc
def disp(_cur,_num): #_numにはてきとうな数字
    _cur.execute("select * from schedule order by date, time;")
    rows = _cur.fetchall()
    return rows

@sqlproc
def select(_cur, _value): #_value[0]:type,_value[1]:value
    com = "select * from schedule where "+_value[0]+"=\'"+str(_value[1])+"\';"
    _cur.execute(com)
    rows = _cur.fetchall()
    return rows

#送信履歴の登録
@sqlproc
def save_send(_cur, _text):
     _cur.execute("INSERT INTO send_log values(%s, %s);",(datetime.datetime.now(), _text))

#送信履歴確認 最新の履歴
@sqlproc
def ref_log(_cur,_num):
    _cur.execute("select * from send_log order by datetime;")
    rows = _cur.fetchall()
    return rows[-2] #はい、いいえの送信後なのでひとつ前

"""
@sqlproc
def sort(_cur, _num):
     _cur.execute("SELECT * from schedule order by date, time;")
"""

@sqlproc
def update():
    pass


"""デバック用"""
@sqlproc
def disp_tableName(_cur,_num):
    _cur.execute("select schemaname, tablename, tableowner from pg_tables where tableowner = 'satoshi';")
    rows = _cur.fetchall()
    return rows

@sqlproc
def disp_tableContent(_cur, table_name, order):
    _cur.execute("select * from " + table_name + " order by " + order + ";")
    rows = _cur.fetchall()
    return rows


@sqlproc
def delete_log(_cur,_num): #date:'2019-07-30'
    _cur.execute("DELETE FROM send_log;")



if __name__=="__main__":
    #today = datetime.date.today()
    #schedules=select(["date",today])
    #d=["date", today]
    #print(schedules)
    #print(ref_log(0))
    print(delete0(0))
    #print(disp_tableContent("schedule", "date, time"))
    #delete_log(0)
    #print(disp_tableContent("send_log", "datetime"))
    #save_send("www")