#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author : Liangdong Zhang
# @date : 2020/6/29 15:31
# @file : api_http_autotest.py
import common.configReadDB as cc
import os
import unittest
import HTMLTestRunner
from config.sendEmail import MyEmail
import common.log as lg
import config.readConfig as rc
import common.userDFunction as udf
import common.myException as me
import time


readConfig=rc.Config()
userDFuction=udf.userDFunction()
crb=cc.mySqlDB()
read=rc.Config()
log=lg.logger()


class ApiHttp(object):
    global host, username, password, port, database
    host = read.get_localDB('host')
    username = read.get_localDB('username')
    password = read.get_localDB('password')
    port = read.get_localDB('port')
    database = read.get_localDB('database')

    def __init__(self):
        self.on_off = readConfig.get_email("on_off")
        self.email = MyEmail.get_email()
        self.url="http://{}:{}".format(read.get_environment("testUrl"),read.get_environment("testport"))

    def run(self):
        now = time.strftime("%Y%m%d_%H%M", time.localtime())
        resReport=os.path.join(os.getcwd(),"result","test_report_{time}.html".format(time=now))
        discover = unittest.defaultTestLoader.discover(os.getcwd(), pattern='getCaseRes.py', top_level_dir=None)
        fp = open(resReport, 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='接口自动化测试报告', description='Test Description')
        runResult=runner.run(discover)
        # print(runResult)
        try:
            if self.on_off == 'off':
                self.email.send_email(resReport)
                log.info(">>>>>>>>>>>>>>>>>send email successful")

            elif self.on_off == 'on':
                log.warning(">>>>>>>>>>>>>>>>>Doesn't send report email to developer.")
            else:
                log.error(">>>>>>>>>>>>>>>>>Wrong Config,Please Check!")
                raise me.getWrongCfgError()
            # userDFuction.send_dingding("接口自动化测试已完成,请查收邮件，谢谢！,本次测试用例执行{}条，通过{}条，失败{}条，通过率{}%，请关注失败测试用例".format(
            #     runResult.testsRun,runResult.success_count,runResult.failure_count,round(float(runResult.success_count)/float(runResult.testsRun)*100,2)
            # ))
            log.info(">>>>>>>>>>>>>>>>>send DingDing successful")

        except me.getWrongCfgError as ex:
            print(ex)
            print(ex.msg)
        except FileNotFoundError as ex:
            log.error(">>>>>>>>>>>>>>Can not find File!!!! Please Check! {}".format(ex))


if __name__ == '__main__':
    ApiHttp().run()

    # def excute_case(self):
    #     getsql_data=HttpCase.get_body_data()
    #
    #     with closing(crb.connet_gernalDB(host, username, password, database)) as conn:
    #         for data in HttpCase.get_data_generator(getsql_data):
    #             getRes=HttpCase.http_request(data['requestMethod'],"http://"+self.url+data['URI'],data['headers'],data['data'])
    #             getDict=json.loads(getRes.text)
    #
    #             # print(data)
    #             # datac=json.loads(data['expectedResult'])
    #             if getDict['code']==json.loads(data['expectedResult'])['code'] and getDict['msg']==json.loads(data['expectedResult'])['msg']:
    #                 if getRes.status_code==int(data['expectedStatus']):
    #                     sql_data={
    #                         'actualStatus':"'{}'".format(getRes.status_code),
    #                         'actualResult':"'{}'".format(getRes.text),
    #                         'result':"'{}'".format("PASS")
    #                     }
    #                     crb.updateSQLData(conn,"api_http_autotest",sql_data,"ID={id}".format(id=data['ID']))
    #                     log.info(">>>>>>>>case {} execute successfully!".format(data['case_name']))
    #                 else:
    #                     sql_data={
    #                         'actualStatus':"'{}'".format(getRes.status_code),
    #                         # 'actualResult':"'{}'".format(getRes.text),
    #                         'result':"'{}'".format("FAILED")
    #                     }
    #                     crb.updateSQLData(conn,"api_http_autotest",sql_data,"ID={id}".format(id=data['ID']))
    #             else:
    #                 sql_data = {
    #                     'actualStatus': "'{}'".format(getRes.status_code),
    #                     'actualResult': "'{}'".format(getRes.text),
    #                     'result': "'{}'".format("FAILED")
    #                 }
    #                 crb.updateSQLData(conn, "api_http_autotest", sql_data,
    #                                   "ID={id}".format(id=data['ID']))
    #
    #     get_data=HttpCase.get_body_data()
    #
    #     for data in HttpCase.get_data_generator(get_data):
    #
    #         data=json.dumps(data)
    #
    #         fp = open(os.path.join(os.getcwd(),"report1.html"), 'wb')
    #         runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='测试报告', description='Test Description')
    #         runner.run(data)