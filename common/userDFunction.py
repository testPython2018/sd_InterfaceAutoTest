#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author : Liangdong Zhang
# @date : 2020/6/28 17:37
# @file : userDFunction.py
import requests
import json
import xlwt
import time
from urllib import parse
import hmac
import base64
import hashlib
from xlrd import open_workbook
import os


# readConfig=rc.Config()

class userDFunction:

    def __init__(self):
        # self.receivers=readConfig.get_email("receivers")
        # self.url=readConfig.get_email("DindDingur1")
        # self.secret=readConfig.get_email("secret")
        self.receivers="18626859903"
        self.url="https://oapi.dingtalk.com/robot/send?access_token=c7513bafe53b87bcbdcc2e6cb0530dd3e96b0daa889643abbcb8697aa12223fb"
        self.secret="SECea18e69297f33f33211260bce25c41d678a589083d9048054d7298f56fa1ce65"



    def get_sign(self):
        timestamp = round(time.time() * 1000)
        secret_enc = self.secret.encode(encoding='utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode(encoding='utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = parse.quote(base64.b64encode(hmac_code))

        return timestamp, sign

    @classmethod
    def get_xls(cls,xls_name, sheet_name):
        cls = []
        # ~ 打开excel表对应的入参值
        # xlsPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "testFile", xls_name)
        xlsPath = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "testFile", xls_name)
        file = open_workbook(xlsPath)
        sheet = file.sheet_by_name(sheet_name)
        nrows = sheet.nrows
        for i in range(nrows):
            if sheet.row_values(i)[0] != u'ID':
                cls.append(sheet.row_values(i))
        return cls

    @classmethod
    def show_return_msg(cls,response):
        """
        show msg detail
        :param response:
        :return:
        """
        url = response.url
        msg = response.text
        # print("\n请求地址：" + url)
        # 可以显示中文
        print("\n请求返回值：" + '\n' + json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))

    def send_dingding(self,content):

        new_url=self.url+"&timestamp={}&sign={}".format(self.get_sign()[0],self.get_sign()[1])
        data= \
            {
            "msgtype": "text",
            "text":  {
                "content": content
            },
            "at":{
                # "atMobiles":[self.receivers],
                "isAtAll":True
            }
        }
        header = {"Content-Type": "application/json"}

        t=requests.post(new_url,headers=header,data=json.dumps(data))
        # print(t.text)





# if __name__ == '__main__':
#     userDFunction().send_dingding("这是一个测试，请忽略！")