# FileName : runMain.py
# Author   : Adil
# DateTime : 2018/4/9 18:08
# SoftWare : PyCharm


import unittest,os,time
from CiTest.common.MyHTMLTestReportCN import HTMLTestRunner
from CiTest.common.EMail import  Email

from CiTest import readConfig as RC
from CiTest.common.TestLog import MyLog

class ExecutCase(object):
    '''定义执行用例的类'''

    def __init__(self):
        '''初始化参数'''
        readConfig = RC.ReadConfig()
        self.Msg_Title = readConfig.getMail('Msg_Title')
        self.casePath = os.path.join(RC.path, 'test_case')
        self.reportPath = os.path.join(RC.path, 'test_report')
        self.Text_description = readConfig.getMail('Text_description')

        self.on_off = readConfig.getMail('on-off')
        # 实例化MyLog
        self.log = MyLog.getLog('ExecuteCase')
        self.logger = self.log.logger

    def exeCase(self):
        '''执行用例'''
        test_discover = unittest.defaultTestLoader.discover(self.casePath, pattern='*test.py')
        now = time.strftime("%Y-%m-%d-%H_%M_%S")
        if not os.path.exists(self.reportPath):
            os.mkdir(self.reportPath)
        filename = self.reportPath + r'\result-' + now + '.html'
        fp = open(filename, 'wb')
        self.logger.info("开始执行用例！")
        runner = HTMLTestRunner(stream=fp, title=self.Msg_Title, description=self.Text_description)
        runner.run(test_discover)
        fp.close()
        self.logger.info("用例执行完毕！")
        self.logger.info("开始执行发送邮件！")
        self.sendEmail(filename)

    def sendEmail(self,filename):

        if self.on_off == 'on':
            sendMail = Email()
            mail = sendMail.sendEMail(filename)
            if mail:
                print("发送成功！")
                self.logger.info("邮件发送成功！")
            else:
                print("发送失败！")
                self.logger.info("邮件发送失败！")
        else:
            print ('邮件未发送，如需发送邮件，请打开邮件发送开关！')
            self.logger.info("邮件未发送，如需发送邮件，请打开邮件发送开关！")


if __name__=='__main__':
    runCase = ExecutCase()
    runCase.exeCase()



