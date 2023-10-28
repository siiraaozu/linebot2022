#todo.txt の解釈
import re #正規表現を使う際は、こちらが必要になります。
import datetime


#改行は除く
def covert_todo(todo):
    todo=todo.split()
    priority = r"\([A-Z]\)"
    ymd = r"^(\d{4})-(\d{2})-(\d{2})$"
    data={}

    if todo[0] == "x":
        data["done"] = True
        todo.pop(0)
    else:
        data["done"] = False

    if re.fullmatch(priority, todo[0]):
        data["priority"] = todo[0][1]
        todo.pop(0)
    else:
        data["priority"] = None
    
    if data["done"] == True:
        data["day_finish"] = datetime.datetime.strptime(todo[0], '%Y-%m-%d').date()
        todo.pop(0)
    else:
        data["day_finish"] = None

    if re.fullmatch(ymd, todo[0]):
        data["day_add"] = datetime.datetime.strptime(todo[0], '%Y-%m-%d').date()
        todo.pop(0)
    else:
         data["day_add"] = None
    
    data["task"] = todo[0]
    todo.pop(0)

    data["due"] = None
    if todo:
        if re.match("due:", todo[0]):
            data["due"] = datetime.datetime.strptime(todo[0][4:], '%Y-%m-%d').date()

    #re.fullmatch(priority, todo)

    return data

