# FileName : Log.py
# Author   : Adil
# DateTime : 2017/12/7 18:22
# SoftWare : PyCharm

import logging

from datetime import datetime

import threading

from CiTest import readConfig as RC
import os

class TestLog(object):
    '''定义Log类'''
    def __init__(self,name):
        '重构__init__方法，传入logger的参数，name，这样打印的日志就是传入参数的的名字'

        self.path = RC.path
        self.logPath = os.path.join(self.path,'Log')
        # 判断是否存在log文件，如果不存在，自动创建
        if not os.path.exists(self.logPath):
            os.mkdir(self.logPath)

        self.logFile = os.path.join(self.logPath,str(datetime.now().strftime('%Y%m%d')))

        if not os.path.exists(self.logFile):
            os.mkdir(self.logFile)
        # defined logger  获取 logger 实例
        self.logger = logging.getLogger(name)
        # defined log level 设置级别，如下级别依次递增，设置高级别的，会过滤不显示低级别的日志。
        # 2016-10-08 21:59:19,493 INFO    : this is information
        # 2016-10-08 21:59:19,493 WARNING : this is warning message
        # 2016-10-08 21:59:19,493 ERROR   : this is error message
        # 2016-10-08 21:59:19,493 CRITICAL: this is fatal message, it is same as logger.critical
        # 2016-10-08 21:59:19,493 CRITICAL: this is critical message

        self.logger.setLevel(logging.INFO)

        self.logFileName = 'TestLog-' + str(datetime.now().strftime('%H%M%S')) +'.log'


        # class logging.FileHandler(filename, mode='a', encoding=None, delay=False)  构造方法，后面加上 encoding='utf-8'是为了处理
        # 日志文件中，中文乱发的问题，不加就会出现中文乱码。
        self.handler = logging.FileHandler(os.path.join(self.logFile,self.logFileName),encoding='utf-8')

        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.handler.setFormatter(self.formatter)

        self.logger.addHandler(self.handler)


class MyLog:
    log = None
    mutex = threading.Lock()

    @staticmethod
    def getLog(name):

        if MyLog.log is None:
            # 获取线程
            MyLog.mutex.acquire()
            MyLog.log = TestLog(name)
            MyLog.mutex.release()
        return MyLog.log



# if __name__ == '__main__':
#
#     myLog = MyLog()
#     Log=myLog.getLog("TestApi")
#     Log.logger.info("The test report has send to developer by email.")
#

