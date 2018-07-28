# schat
this is a mall communaction software
This small project is used to implement communication between multiple users. Using the common Client/server architecture, the functions supported by the client include user login, user registration, finding users, adding friends, deleting friends and sending and receiving messages, and in the client. Provides simple graphical support;
The functions supported by the server include connecting the redis database to check the user account password, connecting mysq to record the user's registration information, and providing interaction with the client by opening a separate thread for each user.
## installation:
1. Find the project's address git@github.com:lixun1314/schat.git and execute git clone git@github.com:lixun1314/schat.git;
2. Install the required dependencies: pip install -r Requirements.txt;
3. It is recommended to open this project via pycharm;
4. should provide redis, and configure the password;
## run;
1.server: cd server/execute ./schatserver;
2.client: cd client/ Execute ./schatclient;
## adversive
#### In order to facilitate the verification to provide server-side hosting on Tencent Cloud, you only need to use the client for verification. You just need to run client/schatclient.py, it will connect the server on Tecent cloud;
#### In client, You should log up first,server will return the userID for you, and next use this ID and passwd to log in. after log in, You will get the friendlist,You can choose add,del,search afriend,These operations depend on the UserID you entered.if you have friend in online list, You can chat with him;
#### This simple software does not use SSL to verify the legitimacy of the user, nor does it use an encryption algorithm to encrypt the communication session;
