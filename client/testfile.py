


def dell():
    confirm = ""
    for I in ["delfriend", userID, edel.get()]:
        confirm = confirm + "&$&" + I
        I += str(1)
    confirm += "&$&"

def common(*par):
    confirm = ""
    for I in par:
        confirm += I
        I += str(1)
    print(confirm)
    print(type(confirm))
common('1','2','3','4','4')