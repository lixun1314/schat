str = "&$&1&$&"

for I in str.split("&$&")[1:-1]:
    print(I)
    print(type(I))
