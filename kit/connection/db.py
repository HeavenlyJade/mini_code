# coding: utf-8

import pymysql


class DB:
    pass


class MySQL(DB):

    def __init__(self, host='192.168.220.135', port=3322, user='root', passwd='root', db='mock'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.cursor = None
        self.conn = None

    def connect(self):
        # 打开数据库连接
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    password=self.passwd,
                                    database=self.db)

        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.conn.cursor()

    def exec(self, sql):
        # 使用 execute()  方法执行 SQL 查询
        self.cursor.execute(sql)
        # 使用 fetchone() 方法获取单条数据.
        data = self.cursor.fetchone()
        # print("Data: %s " % data)
        return data[0]

    def close(self):
        # 关闭数据库连接
        self.conn.close()


if __name__ == '__main__':
    db = MySQL(host='192.168.220.135', port=3322, user='root', passwd='root', db='mock')
    db.connect()
    db.exec('select factor1 from pl')
