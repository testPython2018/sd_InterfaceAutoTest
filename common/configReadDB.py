#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author : Liangdong Zhang
# @date : 2020/6/28 17:37
# @file : configReadDB.py


import pymysql
import config.readConfig as rc
import common.log as logger

localConfig = rc.Config()
import common.userDFunction as userDFuction

userDFuction = userDFuction.userDFunction()
log = logger.logger()


class mySqlDB:


    def __init__(self):
        self.db = None
        self.cursor = None

    @classmethod
    def connet_gernalDB(cls, hosts, username, pwd, dbname):

        try:
            connect = pymysql.connect(host=hosts, user=username, passwd=pwd, database=dbname, port=3306, charset='utf8',
                                      connect_timeout=30, cursorclass=pymysql.cursors.DictCursor)
            logger.logger().info(">>>>>>>>>>>>>>>>>DataBase Connect Scucessfully!<<<<<<<<<<<<<<<<<<<<<<<")
            return connect
        except ConnectionError as ex:
            logger.logger().error(">>>>>>>>>>>>>>>>>DataBase Connect Failed! Please Check Reason:%s" % ex)

    @classmethod
    def closedb(cls, connect):

        cur = connect.cursor()
        connect.close()
        cur.close()

    @classmethod
    def getSignalData(cls, connect, sql, param=None):

        with connect.cursor() as cur:
            if param == None:
                cur.execute(sql)
            else:
                cur.execute(sql, param)
        connect.commit()
        return cur.fetchall()

    @classmethod
    def getOneData(cls, connect, sql, param=None):

        with connect.cursor() as cur:
            if param == None:
                cur.execute(sql)
            else:
                cur.execute(sql, param)
        connect.commit()
        return cur.fetchone()

    @classmethod
    def getMuliData(cls, connect, sql, param=None):

        with connect.cursor() as cur:
            if param == None:
                cur.execute(sql)
            else:
                cur.execute(sql, param)
        connect.commit()
        return cur.fetchall()


    @classmethod
    def insertSQLData(cls, connect, tableName, fieldDict):
        fieldName = []
        fieldKey = []
        for fk in fieldDict:
            fieldName.append(fk)
            fieldKey.append(str(fieldDict[fk]))

        fieldName = ','.join(fieldName)
        fieldKey = ','.join(fieldKey)

        insert_sql = "insert into {} ({}) values ({})".format(tableName, fieldName, fieldKey)

        try:
            with connect.cursor() as cur:

                cur.execute(insert_sql)
            connect.commit()


        except Exception as ex:
            connect.rollback()
            log.error(">>>>>>>>>>>>>>>>>SQL Insert Failed! Please Check your insert sql value! Check:%s" % ex)
            connect.close()

    @classmethod
    def updateSQLData(cls, connect, tableName, fieldDict, condition):

        fileKv = []

        for fk in fieldDict:
            fileKv.append("{} = {}".format(fk, str(fieldDict[fk])))

        fileKv = ', '.join(fileKv)
 
        update_sql = "update {} set {} where {}".format(tableName, fileKv, condition)
        # print(update_sql)
        try:
            with connect.cursor() as cur:

                cur.execute(update_sql)
            connect.commit()

        except Exception as ex:
            connect.rollback()
            log.error(">>>>>>>>>>>>>>>>>SQL Update Failed! Please Check your insert sql value! Check:%s" % ex)
            connect.close()
