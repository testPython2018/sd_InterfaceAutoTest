#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author : Liangdong Zhang
# @date : 2020/6/29 9:31
# @file : interface.py

import common.myException as me
import common.log as lg
import requests
import json
import common.configReadDB as cc
import config.readConfig as rc
from contextlib import closing

crb=cc.mySqlDB()
log=lg.logger()
read=rc.Config()

class HttpCase(object):
    global host, username, password, port, database
    host = read.get_localDB('host')
    username = read.get_localDB('username')
    password = read.get_localDB('password')
    port = read.get_localDB('port')
    database = read.get_localDB('database')
    def __init__(self):
        pass

    # @classmethod
    # def get_data_generator(cls,data):
    #
    #     try:
    #         if isinstance(data,list):
    #             for i in range(len(data)):
    #                 yield data[i]
    #         else:
    #             return data
    #     except:
    #         return None

    @classmethod
    def get_body_data(cls):
        try:
            with closing(crb.connet_gernalDB(host,username,password,database)) as conn:
                sql="SELECT * FROM `robottest`.`api_http_autotest`"
                get_data=crb.getSignalData(conn,sql)
                try:
                    if isinstance(get_data, list):
                        for i in range(len(get_data)):
                            yield get_data[i]
                    else:
                        return get_data
                except:
                    return None

                # print(get_data)
        except Exception as ex:
            print(ex)
            log.error("Exception {}".format(ex))

    @classmethod
    def http_request(cls,method,url,header=None,data=None,timeout=80):
        """
        header = {"Content-Type": "application/json"}
        :param method:请求类型,必填
        :param url:请求URL,必填
        :param header:请求头
        :param files:请求文件
        :param params:请求参数
        :param data:请求数据
        :param timeout:超时时间
        :return:返回请求结果
        """
        if header is not None and header!="":
            header = json.loads(header)


        try:
            if method=='get' or method=='GET':

                result = requests.get(url=url, headers=header, data=data, timeout=timeout)
                return result
            elif method=='post' or method=='POST':
                if "Content-Type" in header.keys() or "json" in header['Content-Type']:
                    if isinstance(data,bytes):
                        data=data.decode("latin1")
                    elif not isinstance(data,str):
                        if isinstance(data,dict):data=json.dumps(data)
                        data=str(data.encode("utf-8").decode('latin1'))
                    else:
                        data = data.encode("utf-8").decode("latin1")
                    try:
                        json.loads(data,encoding='utf-8')
                    except ValueError:
                        log.error("Try to change the data,but failed! Please check！")
                        data=json.dumps(data)

                result = requests.post(url=url, headers=header, data=data, timeout=timeout)
                return result
            else:
                raise me.getNoDataError("NO DATA")
        except me.getNoDataError as ex:
            log.error("getNoDataError {}".format(ex))
            print(ex)
        except Exception as ex:
            log.error("Exception {}".format(ex))
            print(ex)






# if __name__ == '__main__':
#     method='post'
#     # url='http://{test_env}/api/content/aritclecontent?id=1472'.format(test_env='101.37.148.125:8081')
#     header = {"Content-Type": "application/json"}
#     # files = None
#     # params = {"id": "1472"}
#     # data = None
#     # #
#     # t=HttpCase.http_request(method,url,header)
#     # print(t.text)
#
#     url="http://{test_env}/api/video/videolist".format(test_env='101.37.148.125:8081')
#     data={"page": 1, "title": "", "limit": 100, "sourceTerminalId": "", "videoUse": 2}
#     t=HttpCase.http_request(method,url,header,None,None,data)
#     print(t.text)
#
#

# if __name__ == '__main__':
#     data=HttpCase.get_body_data()
#     print(type(HttpCase.get_data_generator(data)))
#     for i in HttpCase.get_data_generator(data):
#         print(i)
