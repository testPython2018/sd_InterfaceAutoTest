#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author : Liangdong Zhang
# @date : 2020/6/28 17:37
# @file : myException.py


class MyException(Exception):
    def __init__(self,*args):
        super().__init__(self)
        self.args=args

class getNoDataError(MyException):
    def __init__(self,args,msg='输入类型存在异常！'):
        self.args=args
        self.msg=msg


class getNoSQLError(MyException):
    def __init__(self):
        self.args=('>>>>>>>>>>>>>>>>>>>>>数据库查询不到相关数据！请查看对应的SQL语句是否正确或者sql能否查询到数据',)
        self.msg='数据库查询不到相关数据！'

class getNoFileError(MyException):
    def __init__(self):
        self.args=('>>>>>>>>>>>>>>>>>>>>>查询不到文件信息！请查看对应的输入的cmd指令或者文件夹下是否存在数据',)
        self.msg='查询不到文件信息！'

class getWrongCfgError(MyException):
    def __init__(self):
        self.args=('>>>>>>>>>>>>>>>>>>>>>配置项异常，请查看config/auto_test.ini中对应配置项是否正确',)
        self.msg='查询不到配置项异信息！'

