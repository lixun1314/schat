import socket

class clientInit(object):

    def __init__(self, serverIp, port):
        self.__serverIp = serverIp
        self.__port = port
        self.__icharFormat = "&$&"
        self.__login = "logIn"
        self.__logup = "logUp"
        self.__userlist = "userlist"
        self.__clienSocket = ""
    def conneServer(self):
        clientResult = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientResult.connect((self.__serverIp,self.__port))
        self.__clienSocket = clientResult
    def Welcome(self):
        print("Welcome to use Ichat")
        print("<<<<<<<<1.login>>>>>>>")
        print("<<<<<<<<2.logup>>>>>>>>>>>>>")
        choice = input("please input your choice: ")
        if choice == 1:
            self.logIn()
        else:
            self.logUp()

    def logIn(self):
        NumID = input("please input Your NumID: ")
        self.__user_ID = NumID
        NumPass = input("please input Your Pass: ")
        messages = ""
        for I in [self.__login,NumID,NumPass]:
            messages = messages + "&$&" + I
            I += str(I)
        messages =   messages + "&$&"
        print(messages)
        self.sendMessage(messages)
        result = str(self.acceptMessage())
        print(result)
        if result.split("&$&")[1] == "successful":
            print("successful log in")
            self.onlineFriend()
            self.logInChoice()
        else:
            print(result.split("&$&")[1])
            self.logIn()
    def logUp(self):
        print("Welcome to use ichat !!!")
        messages = ""
        nickName = input("please input your nick name: ")
        passWord = input("please input your password: ")
        gender = input("please input your gender:(default:secret): ")
        phoneNumber = input("please input your phonenumber: ")
        address = input("please input your address: ")
        print("this is wait a few minutes later")
        for I in [self.__logup,nickName,passWord,gender,phoneNumber,address]:
            messages = messages + "&$&" + I
            I += str(1)
        messages = messages +  "&$&"
        print(messages)
        self.sendMessage(messages)
        result = self.acceptMessage()
        self.__user_ID = result
        print("Your NumID is %s" %(result))
        self.logIn()
    def sendMessage(self,message):
        self.__clienSocket.send(message.encode("utf-8"))
    def acceptMessage(self):
        info = self.__clienSocket.recv(1024).decode("utf-8")
        return info
    def onlineFriend(self):
        result = self.acceptMessage()
        count = 1
        print("---user_list BEGAIN----")
        for I in result.split("&$&")[1:-1]:
            if count % 2 == 0:
                print("user_name: %s" % (I))
            else:
                print("\b\b\buser_ID: %s" % (I))
            count += 1
        print("---user_list END------")
    def searchFriend(self):
        friend_ID = str(input("please input your friend ID: "))
        confirm = "&$&" + "searchfriend" + "&$&" + self.__user_ID + "&$&" + friend_ID + "&$&"
        self.sendMessage(confirm)
        friend_name = self.acceptMessage()
        if friend_name == "No such user":
            print("No such user")

        else:
            print("Your friend name is: %s" % (friend_name))
        if friend_ID == self.__user_ID:
            print("this is you ")

        else:
            confirm = input("Would you like to add or del: ")
            if confirm =="add":
                self.addFriend(friend_ID)
            elif confirm == "del":
                self.delFriend(friend_ID)
            else:
                print("inut error")

    def addFriend(self,friendID):
        confirm = "&$&" + "addfriend" + "&$&" + self.__user_ID + "&$&" + friendID + "&$&"
        self.sendMessage(confirm)
        result = self.acceptMessage()
        if result == "user exist in list":
            print(result)
        self.onlineFriend()

    def delFriend(self,friendID):
        confirm = "&$&" + "delfriend" + "&$&" + self.__user_ID + "&$&" + friendID + "&$&"
        self.sendMessage(confirm)
        result = self.acceptMessage()
        if result == "this user is not your friend":
            print("this user is not your friend")
        elif result == "delete user successful !!":
            print(result)
        self.onlineFriend()

    def connectID(self):
        self.onlineFriend()
        friend_ID = input("please input your friend ID: ")
        confirm = "&$&" + "connectfriend" + "&$&" + self.__user_ID + "&$&" + friend_ID + "&$&"
        self.sendMessage(confirm)
        friendSocket = str(self.acceptMessage())
        print(friendSocket)
    def quit(self):
        confirm = "&$&" + "logout" + "&$&" + self.__user_ID + "&$&"
        self.sendMessage(confirm)
        result = str(self.acceptMessage())
        print(result)