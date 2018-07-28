import socket
import threading
from connMysql import mysqlOperaction
from connectRedis import connectRedis
import random

format = "&$&"
userID = ""

userCK = {}
def taskclassification(ck, recvdata):
    try:
        paramater = recvdata.split(format)[1]
        print(paramater)
        print(recvdata)
        if paramater == "login":
            login(ck, recvdata)
        elif paramater == "logup":
            logup(ck, recvdata)
        elif paramater == "searchfriend":
            searchfriend(ck, recvdata)
        elif paramater == "connectfriend":
            connectfriend(ck, recvdata)
        elif paramater == "addfriend":
            if searchfriend(ck, recvdata) != False:
                addfriend(ck, recvdata)
                friendlist(ck, userID)
        elif paramater == "delfriend":
            if searchfriend(ck, recvdata) != False:
                delfriend(ck, recvdata)
                friendlist(ck, userID)
        elif paramater == "logout":
            logout(ck, recvdata)
            return True
        else:
            return 0
    except Exception as e:
        exit(0)


def login(ck, recvdata):
       global userCK
       userID = recvdata.split(format)[2]
       userPass = recvdata.split(format)[3]
       if checkuser(userID,userPass) == True:
           print("successful")
           senddata(ck, "&$&login&$&" + userID + "&$&successful!!&$&")
           friendlist(ck, userID)
           onlinelist(ck, userID)
           modifyIP(ck, userID)
           savesocket(ck, userID)
           userCK[userID] = ck
       else:
           print("failure")
           senddata(ck, "&$&login&$&" + userID + "&$&failed&$&")
           return True
def logup(ck, recvdata):
    print("log up start ")
    nickName = recvdata.split("&$&")[2]
    passWord = recvdata.split("&$&")[3]
    gender = recvdata.split("&$&")[4]
    phoneNumber = recvdata.split("&$&")[5]
    address = recvdata.split("&$&")[6]
    redisInsert = connectRedis("westos")
    userID = str(random.randint(1000,1000000))
    print(userID)
    adduser(ck, userID, nickName,passWord,gender,phoneNumber,address)
    redisInsert.set(userID,passWord)
    messages = "&$&logup&$&" + userID + "&$&"
    senddata(ck, messages)

def adduser(ck, userID, userName, userpass, userGender, phoneNumber,address):
    usersocket = str(ck).split("raddr=('")[1].replace(")>","").replace("', ",":")
    conneMysql = mysqlOperaction("localhost", "root", "westos", "userInfo")
    conneMysql.connect()
    sqlDetail = str(
        'INSERT INTO user_detail(user_ID, user_gender,user_phone,user_address) '
        'values(' + '"' + userID + '"' + ", " + '"' + userGender  + '"' + ", " + '"' + phoneNumber + '"' + "," + '"' + address + '"' + ");")
    print(sqlDetail)
    sqlLog = str(
        'INSERT INTO user_log(user_ID, user_name,user_passwd,user_log_ip) '
        'values(' + '"' + userID + '"' + ',' + '"' + userName + '"' + "," + '"' + userpass + '"' + "," + '"' + usersocket + '"' + ");")
    print(sqlLog)
    createUserSql = "CREATE TABLE IF NOT EXISTS " + "schat" + userID +"(user_list INT PRIMARY KEY);"
    print(createUserSql)
    result = conneMysql.insert(sqlDetail)
    print(result)
    conneMysql.insert(sqlLog)
    conneMysql.create(createUserSql)
def checkuser(userID,userpasswd):
    redissearch = connectRedis("westos")
    conneMysql = mysqlOperaction("localhost", "root", "westos", "userInfo")
    conneMysql.connect()
    sqlsearch = "SELECT user_passwd FROM user_log WHERE user_ID = " + userID + ";"
    print(sqlsearch)

    redisresult = str(redissearch.get(userID))
    mysqlresult = str(conneMysql.getOne(sqlsearch)).replace("',)","").replace("('","")
    if redisresult == userpasswd or mysqlresult == userpasswd:
        return True
    else:
        return False
def addfriend(ck, recvdata):
    user_table = "schat" + str(recvdata).split("&$&")[2]
    userID = str(recvdata).split("&$&")[2]
    print(user_table)
    friend_ID = str(recvdata).split("&$&")[3]
    sql_exist = "SELECT user_list FROM " + user_table + " WHERE user_list = " + "'" + friend_ID + "';"
    sql_insert = "INSERT INTO " +  user_table + "(user_list) values('" + friend_ID + "');"
    conneMysql = mysqlOperaction("localhost", "root", "westos", "userInfo")
    conneMysql.connect()
    result = str(conneMysql.getOne(sql_exist))
    result = result.replace("(","").replace(")","").replace(",","")
    if result == friend_ID:
        senddata(ck, "&$&addfriend&$&" + userID + "&$&" + friend_ID + "&$&user exist in list&$&")
        friendlist(ck, userID)
    elif result == "None":
        conneMysql.insert(sql_insert)
        senddata(ck, "&$&addfriend&$&" + userID + "&$&" + friend_ID + "&$&successful&$&")
        friendlist(ck, userID)

def delfriend(ck, recvdata):
    userID = str(recvdata).split("&$&")[2]
    user_table = "schat" + str(recvdata).split("&$&")[2]
    friend_ID = str(recvdata).split("&$&")[3]
    sql_exist = "SELECT user_list FROM " + user_table + " WHERE user_list = " + "'" + friend_ID + "';"
    sql_delete = "DELETE FROM " + user_table + " WHERE user_list = " + friend_ID + ";"
    print(sql_delete)
    conneMysql = mysqlOperaction("localhost", "root", "westos", "userInfo")
    conneMysql.connect()
    result = str(conneMysql.getOne(sql_exist)).replace("(","").replace(")","").replace(",","")
    print(result)
    if result == "None":
        senddata("&$&delfriend&$&" + userID + "&$&" + friend_ID + "&$&delete error&$&")
    else:
        conneMysql.delete(sql_delete)
        senddata(ck, "&$&delfriend&$&" + userID + "&$&" + friend_ID + "&$&successful&$&")
    friendlist(ck, userID)

def searchfriend(ck, recvdata):
    conneMysql = mysqlOperaction("localhost", "root", "westos", "userInfo")
    conneMysql.connect()
    sqlDetail = str("SELECT user_name FROM user_log WHERE user_ID = " + recvdata.split("&$&")[3])
    print(sqlDetail)
    user_name = str(conneMysql.getOne(sqlDetail))
    if user_name == "None":
        user_name = "No such user"
        user_name = "&$&searchfriend&$&" + userID + "&$&" + user_name + "&$&"
        senddata(ck, str(user_name))
        return False
    else:
        user_name = user_name.replace(",)","").replace("'",'').replace("(","")
        user_name = "&$&searchfriend&$&" + userID + "&$&" + user_name + "&$&"
        senddata(ck, str(user_name))
        return True

def senddata(ck, messages):
    ck.send(messages.encode("utf-8"))

def connectfriend(ck, recvdata):
    friendID = recvdata.split("&$&")[3]
    friendck = userCK[friendID]
    print(type(friendck))
    friendck.send(recvdata.encode("utf-8"))


def savesocket(ck, userID):
    connect = connectRedis("westos")
    IPsocket = userID + "IP"
    connect.set(IPsocket,ck)

def modifyIP(ck, userID):
    print("ck is %s" %(ck))
    usersocket = str(ck).split("raddr=('")[1].replace(")>","").replace("', ",":")
    print(usersocket)
    modifyIPsql = "UPDATE user_log SET user_log_ip = " + '"' + usersocket + '"' + " WHERE user_ID = " + "'" + userID + "';"
    conneMysql = mysqlOperaction("localhost", "root", "westos", "userInfo")
    print(modifyIPsql)
    conneMysql.update(modifyIPsql)

def friendlist(ck, userID):
    sql = 'SELECT user_list FROM ' + "schat" + userID + ';'
    conneMysql = mysqlOperaction("localhost", "root", "westos", "userInfo")
    sqlSelectName = "SELECT user_name FROM user_log  WHERE user_ID = "
    # print(sql)
    friendList = conneMysql.getAll(sql)
    result = str(friendList).replace(",", "", ).replace(")", " ").replace("(", "", -1)
    print(result)
    messages = "&$&friendlist&$&" + userID + "&$&"
    for user_ID in result.split("  "):
        print(user_ID)
        sqlSelect = sqlSelectName + "'" + user_ID + "';"
        user_name = conneMysql.getOne(sqlSelect)
        user_name = str(user_name).split("',")[0].replace("('", "", -1)
        messages += str(user_ID) + "&$&" + user_name + "&$&"
    senddata(ck, messages)

def onlinelist(ck, userID):
    sql = 'SELECT user_list FROM ' + "schat" + userID +  ' join user_log on ' "schat" + userID +'.user_list = user_log.user_ID AND user_log.user_log_ip <> "0.0.0.0:00000";'
    conneMysql = mysqlOperaction("localhost", "root", "westos", "userInfo")
    sqlSelectName = "SELECT user_name FROM user_log  WHERE user_ID = "
    # print(sql)
    friendList = conneMysql.getAll(sql)
    result = str(friendList).replace(",", "", ).replace(")", " ").replace("(", "", -1)
    print(result)
    messages = "&$&onlinefriend&$&" + userID + "&$&"
    for user_ID in result.split("  "):
        print(user_ID)
        sqlSelect = sqlSelectName + "'" + user_ID + "';"
        user_name = conneMysql.getOne(sqlSelect)
        user_name = str(user_name).split("',")[0].replace("('","",-1)
        messages += str(user_ID) + "&$&" + user_name + "&$&"
    print(messages)
    senddata(ck, messages)

def logout(ck, recvdata):
    userID = recvdata.split(format)[2]
    sql = "UPDATE user_log SET user_log_ip = '0.0.0.0:00000' WHERE user_ID = '" +  userID + "';"
    print(sql)
    conneMysql = mysqlOperaction("localhost", "root", "westos", "userInfo")
    conneMysql.connect()
    conneMysql.update(sql)
    sqlselect = "SELECT user_log_ip FROM user_log WHERE user_ID = '" + userID + "';"
    print(sqlselect)
    result = str(conneMysql.getOne(sqlselect)).replace("',)","").replace("('","")
    print(result)
    if result == "0.0.0.0:00000":
        print("exit successful !!!")
        senddata(ck, "&$&logout&$&" + userID + "&$&log out successful&$&")
        return True
    return False

def run(ck):
   while True:
       rdata = ck.recv(1024)
       recvdata = rdata.decode("utf-8")
       print(recvdata)
       taskclassification(ck, recvdata)

def start():
    ipStr = "127.0.0.1"
    ipPort = 12131
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ipStr, int(ipPort)))
    server.listen(5)
    print("server start successful...")
    while True:
        ck, ca = server.accept()
        t = threading.Thread(target=run, args=(ck,))
        t.start()

def startServer():
    s = threading.Thread(target=start)
    s.start()


startServer()