#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author : Liangdong Zhang
# @date : 2020/6/28 17:37
# @file : readConfig.py
import os
import codecs
import configparser
import re
# prodir=os.path.abspath(".")

prodir=os.path.split(os.path.realpath(__file__))[0]
confPath=os.path.join(prodir,"auto_test.ini").replace("\\","/")

class Config:

    def __init__(self):
        fd = open(confPath)
        data = fd.read()
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(confPath, "w")
            file.write(data)
            file.close()
        fd.close()
        self.cf=configparser.ConfigParser()

        self.cf.read(confPath,encoding='utf-8')

    def get_email(self,name):
        value=self.cf.get("EMAIL",name)
        return value

    def get_localService(self,name):
        value=self.cf.get("LOCAL-SERVICE",name)
        return value

    def get_environment(self,name):
        value=self.cf.get("ENVIRONMENT",name)
        return value

    def get_userConfig(self,name):
        value=self.cf.get("USERCONFIG",name)
        return value

    def get_serverConfig(self,name):
        value=self.cf.get("SERVERCONFIG",name)
        return value

    def get_localDB(self,name):
        value=self.cf.get("LOCAL-DB",name)
        return value

    def set_value(self,section,option,setValue):
        self.cf.set(section,option,setValue)
        self.cf.write(open(confPath,"w+",encoding="utf-8"))

    def set_email(self,option,setValue):
        self.cf.set("EMAIL",option,setValue)
        self.cf.write(open(confPath,"w+",encoding="utf-8"))

    def set_localService(self,option,setValue):
        self.cf.set("LOCAL-SERVICE",option,setValue)
        self.cf.write(open(confPath,"w+",encoding="utf-8"))


    def set_userConfig(self,option,setValue):
        self.cf.set("USERCONFIG",option,setValue)
        self.cf.write(open(confPath,"w+",encoding="utf-8"))

    def set_serverConfig(self,option,setValue):
        self.cf.set("SERVERCONFIG",option,setValue)
        self.cf.write(open(confPath,"w+",encoding="utf-8"))

    def set_localDB(self,option,setValue):
        self.cf.set("LOCAL-DB", option, setValue)
        self.cf.write(open(confPath, "w+", encoding="utf-8"))


