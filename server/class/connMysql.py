import pymysql
class mysqlOperaction(object):
    def __init__(self, host, user, password, dbname):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__dbname = dbname
    def connect(self):
        self.db = pymysql.connect(self.__host, self.__user, self.__password,
                                  self.__dbname)
        self.cursor = self.db.cursor()
    def close(self):
        self.cursor.close()
        self.db.close()
    def getOne(self, sql):
        res = None
        try:
            self.connect()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
        except:
            print("select error")
        return res
    def getAll(self, sql):
        res = None
        try:
            self.connect()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
        except:
            print("select error")
        return res
    def insert(self, sql):
        return self.__edit(sql)
    def select(self, sql):
        return self.__edit(sql)
    def update(self, sql):
        return self.__edit(sql)
    def delete(self, sql):
        return self.__edit(sql)
    def create(self,sql):
        return self.__edit(sql)
    def __edit(self, sql):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql)
            self.db.commit()
            self.close()
        except:
            print("commit Error")
            self.db.commit()
        return count