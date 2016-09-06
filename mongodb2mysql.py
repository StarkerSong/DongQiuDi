# -*- coding: utf-8 -*-
import pymongo
import MySQLdb

class Mongodb2MySQL:
    ############     mysql 操作


    def mongoCollection(self):
        # db和collection都是延时创建的，在添加Document时才真正创建
        client = pymongo.MongoClient("localhost", 27017) #创建连接
        db = client.dqd_db #切换数据库 或者 db = client['dqd_db']
        collection=db.dqd_collection #获取collection,相当于数据库中的table

        count=collection.count()
        return collection

    def mysqlConnect(self):
        connection = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="song0202",
            db="dqd_database",
            port=3306,
            charset="utf8")
        return connection

