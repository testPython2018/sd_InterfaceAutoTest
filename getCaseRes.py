#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author : Liangdong Zhang
# @date : 2020/7/2 9:23
# @file : getCaseRes.py
import unittest
from common.interface import HttpCase
import paramunittest
# from parameterized import parameterized
from common.userDFunction import userDFunction
import config.readConfig as rc
import common.log as lg

read=rc.Config()
log=lg.logger()
get_sheet=userDFunction.get_xls("api_http_autotest.xlsx","api_http_autotest")

@paramunittest.parametrized(*get_sheet)
class getCaseRes(unittest.TestCase):

    def setParameters(self,ID,case_name,case_description,requestMethod,URI,headers,data,expectedStatus,expectedResult):
        getsqldata=HttpCase.get_body_data()
        self.case_name=str(case_name)
        self.case_description=str(case_description)
        self.requestMethod=str(requestMethod)
        self.url="http://{}:{}{}".format(read.get_environment("testUrl"),read.get_environment("testport"),URI)
        self.headers =headers if headers is not None and headers != '' else None
        self.data=data if data is not None and data!='' else None
        self.expectedStatus=int(expectedStatus)
        self.expectedResult=str(expectedResult)
        self.return_json=None
        self.ID=ID

    def setUp(self):
        log.info(self.case_name + "——测试开始前准备")
        print(self.case_name + "——测试开始前准备")

    def description(self):
        pass

    def test_getCaseRes(self):

        log.info(">>>>>>>>>>>>>>测试执行")
        print("请求方式:{},请求url:{}".format(self.requestMethod,self.url))
        getRes = HttpCase.http_request(self.requestMethod,self.url,self.headers,self.data)
        self.return_json=getRes
        # self.code=getRes.status_code
        self.checkRes()


    def tearDown(self):

        log.info("测试结束，输出log完结\n\n")
        print("测试结束，输出log完结\n\n")

    def checkRes(self):
        userDFunction.show_return_msg(self.return_json)
        self.assertEqual(self.expectedStatus, self.return_json.status_code)
        log.info(self.case_name+"预期响应：" + str(self.expectedStatus) + "实际响应：" + str(self.return_json.status_code))
        print(self.case_name+"预期响应：" + str(self.expectedStatus) + "实际响应：" + str(self.return_json.status_code))
        self.assertIn(self.expectedResult, self.return_json.text)
        print("预期值" + str(self.expectedResult) + "在返回响应中，返回字段过多暂不打印！")

