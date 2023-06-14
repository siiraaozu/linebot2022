#LINEの入力からDB対応の文字列に変換
#trans 引数:[種類(int),スケジュール配列[日時(datetime),内容(str)]]
#種類
#0:なし
#1:予定表示
#2:予定登録
#3:予定削除
#4:予定変更
#9:エラー
#outputSche:配列または文字列
'''
マッチ条件
1.予定登録
構文:[day schedule],[day time schedule]
day:{yyyy-mm-dd(ex.2021-1-12),yyyy/mm/dd,mm-dd(ex.7-3,12-03), mm/dd, dd(ex. 4),[曜日](ex.水,今週水,来週金),今日,明日,明後日}

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


#transDate:transに使う
#input="予定"
def transDate(date0):
    monthDatekey=r"[/-]"
    DWkey = r"[月火水木金土日]"
    DWs = ["月","火","水","木","金","土","日"]
    weekkey = r"[今来]+[週]" #今週or 来週

    now = datetime.datetime.today() + datetime.timedelta(hours=9) #時差
    today = now.date()

    monthDate = re.split(monthDatekey,date0) #月日の区切りを探せ
    week = ""
    #区切りがなければ(else)　ex 30,来週土 →日付 or 文字と認識
    if  len(monthDate) == 3: #区切りあり ３つ（年があるばあい）
        month = int(monthDate[1])
        day = int(monthDate[2])
        year  = int(monthDate[0])
        return [year, month, day]
    elif len(monthDate) == 2: #区切りあり ２つ
        month = int(monthDate[0])
        day = int(monthDate[1])
        year  = today.year
        return [year, month, day]
    elif len(monthDate) == 1: #区切りなし　１つ
        try: #dayが数字 ex 30
            day = int(monthDate[0])
        except (ValueError): # 文字列
            days = monthDate[0] #days:dayの文字列
            if days == "今日":
                scheday = today
            elif days == "明日":
                scheday = today + datetime.timedelta(days=1)
            elif days == "明後日":
                scheday = today + datetime.timedelta(days=2)
            else:
                if re.match(weekkey, days): #先頭に今週来週があるか？？　ex 来週月
                    week = days[:2]
                    DW = days[2]
                else: #曜日 ex 水
                    if re.match(DWkey, days):#先頭に曜日があるか？？
                        DW = days[0]
                    else: #例外
                        return [-1, -1, -1]
                #曜日変換 schedayに落とし込む
                for i,_DW in enumerate(DWs):
                    if _DW == DW:
                        offset = i - today.weekday()
                        scheday = today + datetime.timedelta(days=offset)

                if week == "来週": #来週は7+
                    #print("sssssssdssssssss")
                    scheday = scheday + datetime.timedelta(weeks=1)
                    print(scheday)

            #年月日schedayを分解・格納
            month = scheday.month
            day = scheday.day
            year = scheday.year
        else:
            month = today.month #情報が日だけなので今月
            year  = today.year
            #日が文字列修了
        return [year, month, day]
    else: #例外
        return [-1,-1,-1]
    #月日の区切り1つ修了

#時の処理
def transTime(stime): #stime:文字列
    timeType = [r"\d\d\d\d",r"\d\d\d",r"\d\d:\d\d",r"\d:\d\d",r"\d\d時半",r"\d時半",r"\d時",r"\d",r"\d\d時",r"\d\d"] #0630,630,6:30.
    if re.fullmatch(timeType[0], stime):
        hour = stime[:2]
        min = stime[2:]
    elif re.fullmatch(timeType[1], stime):
        hour = stime[0]
        min = stime[1:]
    elif re.fullmatch(timeType[2], stime):
        hour = stime[:2]
        min = stime[3:]
    elif re.fullmatch(timeType[3], stime):
        hour = stime[0]
        min = stime[2:]
    elif re.fullmatch(timeType[4], stime):
        hour=stime[:2]
        min = 30
    elif re.fullmatch(timeType[5], stime):
        hour=stime[0]
        min = 30
    elif re.fullmatch(timeType[6], stime) or re.fullmatch(timeType[7], stime):
        hour=stime[0]
        min = 0
    elif re.fullmatch(timeType[8], stime) or re.fullmatch(timeType[9], stime):
        hour=stime[:2]
        min = 0
    else:
        print("エラー:時刻の記述が不正です")
        hour = 100
        min = 100

    hour = int(hour)
    min = int(min)
    return [hour,min]


def trans_del(input):
    if input[0] == "削除": #今の所すべて削除
            if len(input) == 1: #「予定」のみ　オプションなし
                return [3,""]
            elif len(input) == 2: #オプション（日付）
                [year, month, day] = transDate(input[1])
                if year == -1:
                    print("エラー:月日の記述が不正です")
                    return [9,""]
                else:
                    #index = 3
                    outputSche = datetime.date(year,month,day)
                    return [3, outputSche]
            else:
                print("エラー:引数が3つ以上です")
                return [9,""]
def trans(_input):
    #number="[0-9]" #数字集合　\dでも可
    input2=re.split(" |　",_input) #半角or全角スペースでくぎる
    print("inputdata:{}".format(input2))

    #scheday：予定日のdate型
    #日　,　時　予定
    if input2[0] == "予定":
        index = 1 #予定
        if len(input2) == 1: #「予定」のみ　オプションなし
            outputSche = ""
        elif len(input2) == 2:
            if input2[1] == "全て":
                outputSche = "all"
        else:
            return [9,""]

    elif input2[0] == "削除": #今の所すべて削除
        [index, outputSche] = trans_del(input2)
        if index == 3:
            index = 4


    elif input2[0] == "はい": #確認
        pre_mes = sql.ref_log(0)
        #注:premes :"時刻"＋メッセージ
        print("pre_mes:"+str(pre_mes))
        pm_split=re.split(" |　",pre_mes[1]) #分割

        [index, outputSche] = trans_del(pm_split)

    elif input2[0] == "いいえ":
        index = 10
        outputSche = ""
        

    else:
        #予定登録
        #---日([０]、第一コマンド)の処理---

        if len(input2) == 3 or len(input2) == 2:#再掲:予定登録の構文:[day schedule],[day time schedule]
            [year, month, day] = transDate(input2[0])
            if year == -1:
                print("エラー:月日の記述が不正です")
                return [9,""]
            else:
                index = 2
            #予定修了

            #時の処理
            if len(input2) == 3: #要素が全てある
                [hour, min] = transTime(input2[1])
                if hour == 100:
                    print("エラー:時刻の記述が不正です")
                    return [9,""]
                #ivenntoの処理
                event = input2[2]

            elif len(input2) == 2: #要素２つ　(日時、内容)
                hour = 8
                min = 30
                event = input2[1]
            outputDatetime = datetime.datetime(year,month,day,hour,min)
            outputSche = [outputDatetime, event]
        else: #予定登録　引数例外
            print("エラー:引数が1つか4つ以上です")
            return [9,""]

        #予定登録終わり

    output = [index, outputSche]
    print("ind.{}".format(index))
    return output

#datetime型を日本語に変換

#デバッグ用
if __name__=='__main__':
    inpu="5/10 19 クリーニング"
    print(trans(inpu))
#print(output)
#print(trans(input))





sche=["2019-06-05", "18:00", "バイト"]

""
