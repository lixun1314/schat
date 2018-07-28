import socket
import tkinter
import threading
import time
def recvprocess():
    while True:
        recvdata = ck.recv(1024).decode("utf-8")
        for I in recvdata.split("@@@@")[0:-1]:
            print(I)
            recv = I.split("&$&")[1]
            if  recv == "login":
                userID = I.split("&$&")[2]
                result = I.split("&$&")[3]
                text.insert(tkinter.INSERT,"user " + userID + " log " + result + "\n")
            elif recv == "logup":
                text.insert(tkinter.INSERT, "user ID: " + I.split("&$&")[2] + "\n")
            elif recv == "searchfriend":
                friend_name = I.split("&$&")[3]
                if friend_name == "No such user":
                    text.insert(tkinter.INSERT, "No such user" + "\n")
                else:
                    text.insert(tkinter.INSERT, "username: " + friend_name + "\n")
            elif recv == "connectfriend":
                friendsaid(I)
            elif recv == "addfriend":
                text.insert(tkinter.INSERT, I.split("&$&")[4] + "\n")
            elif recv == "delfriend":
                text.insert(tkinter.INSERT, I.split("&$&")[4] + "\n")
            elif recv == "friendlist":
                count = 1
                text.insert(tkinter.INSERT, "->user_list BEGAIN<-\n")
                print(recvdata)
                for J in I.split("&$&")[3:-3]:
                    print(J)
                    if count % 2 == 0:
                        text.insert(tkinter.INSERT, "name: " + J + "\n")
                    else:
                        text.insert(tkinter.INSERT, "ID: " + J + "\n")
                        print("user_ID %s" % (J))
                    count += 1
                text.insert(tkinter.INSERT, "->user_list END<-" + "\n")
            elif recv == "onlinefriend":
                count = 1
                text.insert(tkinter.INSERT, "->online start<-\n")
                print(I)
                for J in I.split("&$&")[3:-3]:
                    print(I)
                    if count % 2 == 0:
                        text.insert(tkinter.INSERT, "name: " + J + "\n")
                    else:
                        text.insert(tkinter.INSERT, "ID: " + J + "\n")
                        print("user_ID %s" % (I))
                    count += 1
                text.insert(tkinter.INSERT, "->online end<-" + "\n")
            elif recv == "logout":
                text.insert(tkinter.INSERT, I.split("&$&")[3])
                ck.close()
                exit(0)
            else:
                text.insert(tkinter.INSERT,"No such Option")
def login():
    global userID
    userID = euser.get()
    messages = common("login", euser.get(), epass.get())
    ck.send(messages.encode("utf-8"))
def logup():
    nickName = ename.get()
    passWord = epasswd.get()
    gender = egender.get()
    phoneNumber = ephone.get()
    address = eaddress.get()
    # print("this is wait a few minutes later")
    messages = common("logup", nickName, passWord, gender, phoneNumber, address)
    print(messages)
    ck.send(messages.encode("utf-8"))

def friendsaid(recvdata):
    friend = recvdata.split("&$&")[2]
    mess = recvdata.split("&$&")[4]
    text.insert(tkinter.INSERT, friend + ": " + mess + "\n")
def connectserver():
    global ck
    ipStr = "119.29.63.48"
    portStr = 12131
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ipStr, int(portStr)))
    ck = client
    print(ck)
    t = threading.Thread(target=recvprocess)
    t.start()

def add():
    confirm =  common("addfriend", userID, eadd.get())
    ck.send(confirm.encode("utf-8"))
    print(confirm)
def dell():
    confirm =  common("delfriend", userID, edel.get())
    ck.send(confirm.encode("utf-8"))
def search():
    confirm =  common("searchfriend", userID, esearch.get())
    print(confirm)
    ck.send(confirm.encode("utf-8"))
def connectfriend():
    confirm =  common("connectfriend", userID, efriend.get(), emessage.get())
    ck.send(confirm.encode("utf-8"))
    text.insert(tkinter.INSERT,"I said: " + emessage.get() + "\n")
def logout():
    confirm =  common("logout", userID)
    ck.send(confirm.encode("utf-8"))
def common(*par):
    confirm = ""
    for I in par:
        confirm = confirm + "&$&" + I
        I += str(1)
    confirm += "&$&"
    return confirm

win = tkinter.Tk()
win.title("schat client")
win.geometry("350x700+900+50")
connectserver()
labeluser = tkinter.Label(win, text="user").grid(row=0, column=0)
euser = tkinter.Variable()
entryuser = tkinter.Entry(win, textvariable=euser).grid(row=0, column=1)

labelpass = tkinter.Label(win, text="pass").grid(row=1, column=0)
epass = tkinter.Variable()
entrypass = tkinter.Entry(win, textvariable=epass).grid(row=1, column=1)

button = tkinter.Button(win, text="log in",
                        command=login).grid(row=2, column=0)


buttonlogout = tkinter.Button(win, text="logout",
                         command=logout).grid(row=2, column=1)


labelname = tkinter.Label(win, text="name").grid(row=3, column=0)
ename = tkinter.Variable()
entyname = tkinter.Entry(win, textvariable=ename).grid(row=3, column=1)

labelpasswd = tkinter.Label(win, text="passwd").grid(row=4, column=0)
epasswd = tkinter.Variable()
entrypasswd = tkinter.Entry(win, textvariable=epasswd).grid(row=4, column=1)

labelgender = tkinter.Label(win, text="Gender").grid(row=5, column=0)
egender = tkinter.Variable()
entrygender = tkinter.Entry(win, textvariable=egender).grid(row=5, column=1)

labelphone = tkinter.Label(win, text="phone").grid(row=6, column=0)
ephone = tkinter.Variable()
entryphone = tkinter.Entry(win, textvariable=ephone).grid(row=6, column=1)


labeladdress = tkinter.Label(win, text="address").grid(row=7, column=0)
eaddress = tkinter.Variable()
entryaddress = tkinter.Entry(win, textvariable=eaddress).grid(row=7, column=1)

buttonlogup = tkinter.Button(win, text="log Up",
                         command=logup).grid(row=8, column=0)

labelsearch = tkinter.Label(win, text="search").grid(row=9, column=0)
esearch = tkinter.Variable()
entysearch = tkinter.Entry(win, textvariable=esearch).grid(row=9, column=1)
buttnsearch = tkinter.Button(win, text="search",
                         command=search).grid(row=9, column=0)

labeladd = tkinter.Label(win, text="add").grid(row=10, column=0)
eadd = tkinter.Variable()
entyadd = tkinter.Entry(win, textvariable=eadd).grid(row=10, column=1)
buttonadd = tkinter.Button(win, text="add",
                         command=add).grid(row=10, column=0)

labeldel = tkinter.Label(win, text="del").grid(row=11, column=0)
edel = tkinter.Variable()
entydel = tkinter.Entry(win, textvariable=edel).grid(row=11, column=1)
buttondel = tkinter.Button(win, text="del",
                         command=dell).grid(row=11, column=0)

text = tkinter.Text(win, width=20, height=15)
text.grid(row=12, column=1)

labelfriend = tkinter.Label(win, text="friend").grid(row=13, column=0)
efriend = tkinter.Variable()
entyfriend = tkinter.Entry(win, textvariable=efriend).grid(row=13, column=1)

labelmessage = tkinter.Label(win, text="send").grid(row=14, column=0)
emessage = tkinter.Variable()
entymessage = tkinter.Entry(win, textvariable=emessage).grid(row=14, column=1)
buttonmessage = tkinter.Button(win, text="send",
                         command=connectfriend).grid(row=14, column=0)

win.mainloop()