#coding:utf8
#coding=utf-8
''''' 
    ftp自动下载、自动上传脚本，可以递归目录操作 
'''  
  
from ftplib import FTP  
import os,time
import socket
from config import *
  
class MYFTP:  
    def __init__(self, hostaddr, username, password, remotedir, port=21):  
        self.hostaddr = hostaddr  
        self.username = username  
        self.password = password  
        self.remotedir  = remotedir  
        self.port     = port  
        self.ftp      = FTP()  
        self.file_list = []  
        # self.ftp.set_debuglevel(2)  
    def __del__(self):  
        self.ftp.close()  
        # self.ftp.set_debuglevel(0)
    def printxx(self,context):
        try:
            debug_print(context)
        except:
            debug_print(u'正常')

    def login(self):  
        ftp = self.ftp  
        try:   
            timeout = 300  
            socket.setdefaulttimeout(timeout)  
            ftp.set_pasv(True)  
            print u'开始连接到 %s' %(self.hostaddr)  
            ftp.connect(self.hostaddr, self.port)  
            print u'成功连接到 %s' %(self.hostaddr)  
            print u'开始登录到 %s' %(self.hostaddr)  
            ftp.login(self.username, self.password)  
            print u'成功登录到 %s' %(self.hostaddr)  
            debug_print(ftp.getwelcome())  
        except Exception:  
            print u'连接或登录失败'  
        try:  
            ftp.cwd(self.remotedir)  
        except(Exception):  
            print u'切换目录失败'  
  
    def is_same_size(self, localfile, remotefile):  
        try:  
            remotefile_size = self.ftp.size(remotefile)  
        except:  
            remotefile_size = -1  
        try:  
            localfile_size = os.path.getsize(localfile)  
        except:  
            localfile_size = -1  
        debug_print('localfile_size:%d  remotefile_size:%d' %(localfile_size, remotefile_size),)  
        if remotefile_size == localfile_size:  
            return 1  
        else:  
            return 0  

    def upload_file(self, localfile, remotefile):  
        if not os.path.isfile(localfile):  
            return  
        if self.is_same_size(localfile, remotefile):
            try:
                debug_print(u'跳过[相等]: %s' %localfile)
            except:
                debug_print(u'文件相同')
            return  
        file_handler = open(localfile, 'rb')  
        self.ftp.storbinary('STOR %s' %remotefile, file_handler)  
        file_handler.close()
        try:
            debug_print(u'已传送: %s' %localfile)
        except:
            debug_print(u'文件传送完毕')
    def upload_files(self, localdir='./', remotedir = './'):  
        if not os.path.isdir(localdir):  
            return  
        localnames = os.listdir(localdir)  
        self.ftp.cwd(remotedir)  
        for item in localnames:  
            src = os.path.join(localdir, item)  
            if os.path.isdir(src):  
                try:  
                    self.ftp.mkd(item)  
                except:  
                    debug_print(u'目录已存在 %s' %item)  
                self.upload_files(src, item)  
            else:  
                self.upload_file(src, item)  
        self.ftp.cwd('..')  
  
    def get_file_list(self, line):  
        ret_arr = []  
        file_arr = self.get_filename(line)  
        if file_arr[1] not in ['.', '..']:  
            self.file_list.append(file_arr)  
              
    def get_filename(self, line):  
        pos = line.rfind(':')  
        while(line[pos] != ' '):  
            pos += 1  
        while(line[pos] == ' '):  
            pos += 1  
        file_arr = [line[0], line[pos:]]  
        return file_arr  
def debug_print(s):  
    print s  
  
if __name__ == '__main__':  
    timenow  = time.localtime()  
    datenow  = time.strftime('%Y-%m-%d', timenow)  

    hostaddr = WanFTPIP # ftp地址
    username = FTPuser # 用户名
    password = FTPpasswd # 密码
    port  =  FTPPORT   # 端口号
    rootdir_local  = WanLocalDIR # 本地目录
    rootdir_remote = FTPDIR          # 远程目录
      
    f = MYFTP(hostaddr, username, password, rootdir_remote, port)  
    f.login()  
    f.upload_files(rootdir_local, rootdir_remote)
      
    timenow  = time.localtime()  
    datenow  = time.strftime('%Y-%m-%d', timenow)  
    logstr = u"%s 成功执行了备份\n" %datenow  
    debug_print(logstr) 