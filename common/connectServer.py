#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author : Liangdong Zhang
# @date : 2020/6/28 17:37
# @file : connectServer.py
# import paramiko
# import config.readConfig as readConfig
# import common.log as log
# import os
# import stat
# import traceback
#
#
# rc=readConfig.Config()
# class connectServer:
#
#
#     def __init__(self):
#         self.log=log.logger()
#
#     def connect_ssh(self,ip,user,passwd,command):
#         ssh=paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
#         ssh.connect(hostname=ip,port=22,username=user,password=passwd)
#         cmd="echo %s'' | sudo -S '%s" %(passwd,command)
#         stdin,stdout,stderr=ssh.exec_command(command=cmd,timeout=300,bufsize=100)
#         res,err=stdout.read(),stderr.readlines()
#         if len(err) >0 and err[0] =="[sudo] password for install":
#             self.log.error("connect_ssh ERROR ——>>"+err[0])
#
#         ssh.close()
#         return res
#
#     def connect_sshNoRes(self,ip,user,passwd,command):
#         ssh=paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
#         ssh.connect(hostname=ip,port=22,username=user,password=passwd)
#
#         cmd="echo %s | sudo -S %s" %(passwd,command)
#         ssh.exec_command(command=cmd,timeout=300,bufsize=100)
#
#         ssh.close()
#
#     def sftp_put(self,ip,user,passwd,localfile,remoteFile):
#
#         try:
#             scp=paramiko.Transport(ip,22)
#             scp.connect(username=user,password=passwd)
#             sftp=paramiko.SFTPClient.from_transport(scp)
#             sftp.put(localfile,remoteFile)
#             scp.close()
#         except Exception as e:
#             self.log.error("sftp_put ERROR ——>>%s" %e)
#
#     def sftp_get(self,ip,user,passwd,localfile,remoteFile):
#         try:
#             scp=paramiko.Transport(ip,22)
#             scp.connect(username=user,password=passwd)
#             sftp=paramiko.SFTPClient.from_transport(scp)
#             sftp.get(localfile,remoteFile)
#             scp.close()
#         except Exception as e:
#             self.log.error("sftp_get ERROR ——>>%s" %e)
#
#     def _get_all_files_in_remoteDir(self,sftp,remoteDir):
#         all_files=list()
#         if remoteDir[-1] == "/":
#             remoteDir = remoteDir[0:-1]
#         files=sftp.listdir_attr(remoteDir)
#
#         for file in files:
#             filename=remoteDir+'/'+file.filename
#
#             if stat.S_ISDIR(file.st_mode):
#                 all_files.extend(self._get_all_files_in_remoteDir(sftp,filename))
#             else:
#                 all_files.append(filename)
#         return all_files
#
#     def getFilesByDir(self,ip,user,passwd,remoteDir,localDir):
#         try:
#             scp=paramiko.Transport(ip,22)
#             scp.connect(username=user,password=passwd)
#             sftp=paramiko.SFTPClient.from_transport(scp)
#             allFiles=self._get_all_files_in_remoteDir(sftp,remoteDir)
#             for file in allFiles:
#                 local_filename=file.replace(remoteDir,localDir)
#                 local_path=os.path.dirname(local_filename)
#                 if not os.path.exists(local_path):
#                     os.makedirs(local_path)
#
#                 sftp.get(file,local_filename)
#
#
#         except:
#             self.log.error(traceback.format_exc())
#
#
#     def _get_all_files_in_localDir(self,localdir):
#         all_files = list()
#
#         for root, dirs, files in os.walk(localdir, topdown=True):
#             for file in files:
#                 filename = os.path.join(root, file)
#                 all_files.append(filename)
#         return all_files