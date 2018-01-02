# -*- coding: utf-8 -*-
import os
import re
import paramiko
import ConfigParser
import datetime
from ftplib import FTP

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/content.conf'
    config.read(path)
    return config.get(section, key)

class Linux(object):

    def __init__(self, hostname, username, password, port):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

    def ssh_connect(self):
        """ 建立远程ssh连接 """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)


    def ssh_cmd(self, CMD):
        """远程执行命令"""
        stdin, stdout, stderr =self.ssh.exec_command(CMD)
        print stderr.read()
        print stdout.read()

    def sftp_connect(self):
        """建立远程sftp连接"""
        t = paramiko.Transport((self.hostname, self.port))
        t.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(t)


    def close(self):
        """关掉连接"""
        try:
            self.ssh.close()
        except:
            pass
        try:
            self.sftp.close()
        except:
            pass


    def upload_dir(self,local_dir, remote_dir):
        """ sftp上传文件夹 """
        for root, dirs, files in os.walk(local_dir):
            for filespath in files:
                local_file = os.path.join(root, filespath)
                a = local_file.replace(local_dir, '').lstrip('\\')
                remote_file = os.path.join(remote_dir, a).replace('\\', '/')
                try:
                    self.sftp.put(local_file, remote_file)
                except Exception, e:
                    # sftp.mkdir(os.path.split(remote_file)[0])
                    CMD = "mkdir -p %s" % os.path.split(remote_dir)[0]
                    self.ssh_cmd(CMD)
                    self.sftp.put(local_file, remote_file)
                print "upload %s to remote %s" % (local_file, remote_file)
            for name in dirs:
                local_path = os.path.join(root, name)
                a = local_path.replace(local_dir, '').lstrip('\\')
                remote_path = os.path.join(remote_dir, a).replace('\\', '/')
                try:
                    CMD = "mkdir -p %s" % remote_path
                    self.ssh_cmd(CMD)
                    print "mkdir path %s" % remote_path
                except Exception, e:
                    print e


class Windows(object):

    def __init__(self, ftp_host, ftp_name, ftp_pass, ftp_port):
        self.hostname = ftp_host
        self.username = ftp_name
        self.password = ftp_pass
        self.port = ftp_port
        self.timeout = 600

    def ftp_connect(self):
        self.ftp = FTP()
        self.ftp.connect(self.hostname, self.port, self.timeout)
        self.ftp.login(self.username,self.password)

    def ftp_close(self):
        self.ftp.close()

    def upload_file(self, localfile, remotefile):
        if not os.path.isfile(localfile):
            return
        file_handler = open(localfile, 'rb')
        self.ftp.storbinary('STOR %s' % remotefile, file_handler)
        file_handler.close()
        print('已传送: %s' % localfile)

    def upload_files(self, localdir='./', remotedir='./'):
        if not os.path.isdir(localdir):
            return
        localnames = os.listdir(localdir)
        try:
            self.ftp.mkd(remotedir)
        except:
            pass
        self.ftp.cwd(remotedir)
        for item in localnames:
            src = os.path.join(localdir, item)
            if os.path.isdir(src):
                try:
                    self.ftp.mkd(item)
                except:
                    print('目录已存在 %s' % item)
                self.upload_files(src, item)
            else:
                self.upload_file(src, item)
        self.ftp.cwd('..')


