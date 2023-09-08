#LINEの入力からDB対応の文字列に変換
#trans 引数:[種類(int),スケジュール配列[日時(datetime),内容(str)]]
#outputSche:配列または文字列
'''
マッチ条件
1.予定登録
構文:[day schedule],[day time schedule]
day:{yyyy-mm-dd(ex.2021-1-12),yyyy/mm/dd,mm-dd(ex.7-3,12-03), mm/dd, dd(ex. 4),[曜日](ex.水,~~今週水~~,来週金),今日,明日,明後日}

3.予定削除
構文:[削除],[削除 day]

4.確認
構文:[はい　いいえ]
→直前の履歴を確認してreceive.pyに送信
'''

#分類方法:区切って、最初のコマンドで判断。「予定」「削除」は#1,#3,その他は#2

import re #正規表現を使う際は、こちらが必要になります。
import datetime
import integratedSQL as sql #独自関数

from init_src import get_nowToday

#transDate:transに使う
#input="予定"
DISP_SCHEDULE = 1
REGIST_SCHEDULE = 2
EXEC_DELETE = 3
CONFIRM_DELETE = 4
ERROR = 9
INTERRUPT = 10


class Command:
    def __init__(self, mesType, content_schedule):
        if mesType == REGIST_SCHEDULE:
            self.mesType = mesType
            self.schedule = content_schedule
            self.content = ""
            self.date_del = ""
        elif mesType == CONFIRM_DELETE:
            self.mesType = mesType
            self.date_del = content_schedule
            self.schedule = ""
            self.content = ""


class Schedule:
    def __init__(self, datatime, event):
        self.mesType 

#　グローバル変数(ファイル内)
[now, today] = get_nowToday()

# ローカル関数

#---trans_date群(transd_xx)---
def transd_kanji2day(date_str):
    key_DayofWeek = r"[月火水木金土日]"
    list_DayofWeek = ["月","火","水","木","金","土","日"]

    if "今日" in date_str:
        new_date_str = today.strftime('%Y/%m/%d') + date_str[2:]
    
    elif "明日" in date_str:
        tomorrow = today + datetime.timedelta(days=1)
        new_date_str = tomorrow.strftime('%Y/%m/%d') + date_str[2:]

    elif "明後日" in date_str:
        DayAfterTomorrow = today + datetime.timedelta(days=2)
        new_date_str = DayAfterTomorrow.strftime('%Y/%m/%d') + date_str[3:]

    elif re.search(key_DayofWeek, date_str): #曜日が含まれるか？
        offset_week = 0
        new_date_str = date_str
        
        if "来週" in date_str: #先頭に来週があるか？？　今週廃止
            offset_week = 7
            new_date_str = new_date_str[2:]
        
        #new_date_str="水　18 予定"
        for i, dow in enumerate(list_DayofWeek):
            if dow == new_date_str[0]:
                offset = i - today.weekday()
                date = today + datetime.timedelta(days=offset+offset_week)
                date_str = date.strftime('%Y/%m/%d')
        
        new_date_str = date_str + new_date_str[1:]
    else:
        new_date_str = date_str
    
    return new_date_str


#区切り4つ→4つ目以降は捨てる
def transd_splitDate(date_str):
    str_split = r"[/-]"
    splited_date_strs = re.split(str_split,date_str)

    if len(splited_date_strs) == 3:
        year_str = splited_date_strs[0]
        month_str = splited_date_strs[1]
        day_str = splited_date_strs[2]
        
    elif len(splited_date_strs) == 2:
        year_str = ""
        month_str = splited_date_strs[0]
        day_str = splited_date_strs[1]

    elif len(splited_date_strs) == 1:
        year_str = ""
        month_str = ""
        day_str = splited_date_strs[0]
    else:
        year_str = ""
        month_str = ""
        day_str = ""
        
    return year_str, month_str, day_str


def transd_compYear():
    year_str  = str(today.year)
    return year_str

def transd_compMonth():
    month_str  = str(today.month)
    return month_str

def trans_date(date_str):
    new_date_str = transd_kanji2day(date_str)
    
    year_str, month_str, day_str = transd_splitDate(new_date_str)

    if year_str == "":
        year_str = transd_compYear()

    if month_str == "":
        month_str = transd_compMonth()
    
    return year_str, month_str, day_str



#時の処理
def trans_time(time_str):
    if "半" in time_str:
        new_time_str = time_str.replace("時半","30")
    elif "時" in time_str:
        new_time_str = time_str.replace("時","")
    elif ":" in time_str:
        new_time_str = time_str.replace(":","")
    else:
        new_time_str = time_str

    if len(new_time_str) == 1:
        new_time_str = "0" + new_time_str + "00"
    elif len(new_time_str) == 2:
        new_time_str =       new_time_str + "00"
    elif len(new_time_str) == 3:
        new_time_str = "0" + new_time_str
    elif len(new_time_str) == 4:
        pass

    hour = new_time_str[:2]
    min = new_time_str[2:]

    return hour, min

def checkFormat_date(year_str, month_str, day_str):
    OKFlag = True
    if year_str.isdigit() == False:
        OKFlag = False
    elif month_str.isdigit() == False:
        OKFlag = False
    elif int(month_str) <= 0 or int(month_str) >= 13:
        OKFlag = False
    elif day_str.isdigit() == False:
        OKFlag = False
    elif int(day_str) <= 0 or int(day_str) >= 32:
        OKFlag = False
    return OKFlag

def checkFormat_time(hour_str, min_str):
    OKFlag = True
    if hour_str.isdigit() == False:
        OKFlag = False
    elif int(hour_str) <= -1 or int(hour_str) >= 25:
        OKFlag = False
    elif min_str.isdigit() == False:
        OKFlag = False
    elif int(min_str) <= -1 or int(min_str) >= 60:
        OKFlag = False
    return OKFlag


def split_schedule(schedule_str):
    new_schedule_strs = re.split(" |　",schedule_str)
    return new_schedule_strs

def transf_registSchedule(schedule_str):
    #split
    new_schedule_strs = split_schedule(schedule_str)

    if len(new_schedule_strs) == 2:
        date = new_schedule_strs[0]
        time = "0830"
        scheduleCont = new_schedule_strs[1]
    elif len(new_schedule_strs) == 3:
        date = new_schedule_strs[0]
        time = new_schedule_strs[1]
        scheduleCont = new_schedule_strs[2]
    else:
        date = ""
        time = ""
        scheduleCont = ""

    year, month, day = trans_date(date)
    hour, min = trans_time(time)
    
    if checkFormat_date(year, month, day) and checkFormat_time(hour, min):
        dateTime = datetime.datetime(int(year), int(month), int(day), int(hour), int(min))
        new_schedule = [dateTime, scheduleCont]
        mesType = REGIST_SCHEDULE
    else:
        mesType = ERROR
        new_schedule = ""

    return mesType, new_schedule


#形式チェックはしない
def transf_delete(schedule_str):
    new_schedule_strs = split_schedule(schedule_str)
    if len(new_schedule_strs) == 1:
        new_schedule = ""
        mesType = CONFIRM_DELETE
    else:
        year, month, day = trans_date(new_schedule_strs[1])
        if checkFormat_date(year, month, day):
            dateTime = datetime.date(int(year), int(month), int(day))
            new_schedule = [dateTime, ""]
            mesType =  CONFIRM_DELETE
        else:
            new_schedule = ""
            mesType =  ERROR
    #つづき
    return mesType, new_schedule

def transf_dispSchedule(schedule_str):
    new_schedule_strs = split_schedule(schedule_str)
    if len(new_schedule_strs) == 1:
        mesType = DISP_SCHEDULE
        new_schedule = ""
    elif len(new_schedule_strs) == 2 \
        and (new_schedule_strs[1] == "全て" \
        or new_schedule_strs[1] == "すべて"):
        mesType = DISP_SCHEDULE
        new_schedule = "all"
    else:
        mesType = ERROR
        new_schedule =""  

    return mesType, new_schedule
 
def transf_execute(schedule_str):
    mesType = EXEC_DELETE
    new_schedule = ""
    return mesType, new_schedule

def transf_interrupt(schedule_str):
    mesType = INTERRUPT
    new_schedule = ""
    return mesType, new_schedule

def trans_func(mestype_tmp, schedule_str):
    func_dict = {
    "disp_schedule" : transf_dispSchedule,
    "regist_schedule_etc" : transf_registSchedule,
    "execute" : transf_execute,
    "delete" : transf_delete,
    "inrerrupt" : transf_interrupt
    }

    return func_dict[mestype_tmp](schedule_str)



#lookup
def classify_mesType(schedule_str):
    #new_schedule_strs = split_schedule(schedule_str)
    if schedule_str[:2] == "削除": #今の所すべて削除
        mestype_tmp = "delete"
    elif schedule_str[:2] == "はい": 
        mestype_tmp = "execute"
    elif schedule_str[:3] == "いいえ": 
        mestype_tmp = "inrerrupt"
    elif schedule_str[:2] == "予定":
        mestype_tmp = "disp_schedule"
    else:
        mestype_tmp = "regist_schedule_etc"
    return mestype_tmp



#main
def trans(schedule_str):
    mestype_tmp = classify_mesType(schedule_str)
    mesType, new_schedule = trans_func(mestype_tmp, schedule_str)

    output = [mesType, new_schedule]
    print("ind.{}".format(mesType))

    return output


def new_trans(schedule_str):
    if schedule_str[:2] == "削除": #今の所すべて削除
        mesType, new_schedule= transf_delete(schedule_str)
        
    elif schedule_str[:2] == "はい": 
        mesType = EXEC_DELETE
        new_schedule = ""

    elif schedule_str[:3] == "いいえ": 
        mesType = INTERRUPT
        new_schedule = ""

    elif schedule_str[:2] == "予定":
        new_schedule_strs = split_schedule(schedule_str)
        if len(new_schedule_strs) == 1:
            mesType = DISP_SCHEDULE
            new_schedule = ""
        elif len(new_schedule_strs) == 2 \
            and (new_schedule_strs[1] == "全て" \
            or new_schedule_strs[1] == "すべて"):
            mesType = DISP_SCHEDULE
            new_schedule = "all"
        else:
            mesType = ERROR
            new_schedule =""  
    else:
        mesType, new_schedule = transf_registSchedule(schedule_str)

        output = [mesType, new_schedule]
        print("ind.{}".format(mesType))

        return output



#デバッグ用
if __name__=='__main__':
    date_str="あ"
    print(trans(date_str))




sche=["2019-06-05", "18:00", "バイト"]

""
