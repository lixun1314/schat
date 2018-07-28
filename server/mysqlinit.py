from connMysql import mysqlOperaction
from connectRedis import connectRedis

def initmysql(host, user, passwd, dbname):
    operationhandle = mysqlOperaction(host, user, passwd, dbname)
    operationhandle.connect()
    createuser_log = "CREATE TABLE user_log (user_ID int(11) NOT NULL, user_name varchar(64) NOT NULL DEFAULT 'newschatuser', user_passwd varchar(128) NOT NULL, user_log_ip varchar(128) DEFAULT NULL, is_delete enum('0','1') DEFAULT '0', PRIMARY KEY (user_ID),CONSTRAINT fk_user_ID FOREIGN KEY (user_ID) REFERENCES user_detail (user_ID),CONSTRAINT fk_user_ID1 FOREIGN KEY (user_ID) REFERENCES user_detail (user_ID)) ENGINE=InnoDB DEFAULT CHARSET='latin1';"
    createuser_detail = "CREATE TABLE user_detail (user_ID int(11) NOT NULL,user_gender enum('girl','boy','secret') DEFAULT 'secret',user_phone varchar(11) DEFAULT NULL,user_address varchar(50) DEFAULT NULL,is_delete enum('0','1') DEFAULT '0',PRIMARY KEY (user_ID)) ENGINE=InnoDB DEFAULT CHARSET='latin1';"
    operationhandle.create(createuser_detail)
    operationhandle.create(createuser_log)
initmysql("localhost", "root", "westos", "user_test")

