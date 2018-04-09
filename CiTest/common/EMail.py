# FileName : EMail.py
# Author   : Adil
# DateTime : 2017/12/7 17:37
# SoftWare : PyCharm

import smtplib
import time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from CiTest import readConfig as RC
from CiTest.common.TestLog import MyLog

from  selenium import webdriver


class Email(object):
    '''创建一个邮件类'''

    def __init__(self):
        '''初始化邮件属性'''

        self.Rc = RC.ReadConfig()
        self.server = self.Rc.getMail('Smtp_Server')
        self.sender = self.Rc.getMail('Smtp_Sender')
        self.receiver = []
        self.password = self.Rc.getMail('Password')
        self.LReceiver = self.Rc.getMail('OnLine_Receiver')
        self.PReceiver = self.Rc.getMail('Pre_Receiver')
        # self.PReceiver =
        self.TReceiver = self.Rc.getMail('Test_Receiver')
        self.Msg_Title = self.Rc.getMail('Msg_Title')
        self.Content_Type = self.Rc.getMail('Content_Type')
        self.Content_Disposition = self.Rc.getMail('Content_Disposition')
        self.resultPath = self.Rc.getMail('resultPath')

        # 实例化MyLog
        self.log = MyLog.getLog('SendEmail')
        self.logger = self.log.logger
        # 实例化msg
        self.msg = MIMEMultipart()

    def get_Result(self, reportFile):
        '获取测试结果'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        ##得到测试报告路径
        self.result_url = "file://%s" % reportFile
        self.driver.get(self.result_url)
        time.sleep(3)
        resultPath = self.resultPath

        self.result = self.driver.find_element_by_xpath(resultPath).text
        self.result = self.result.split(':')
        self.driver.quit()
        self.setHeader(self.result[-1])

    def setHeader(self, result):
        '设置邮件主题'
        now = time.strftime("%Y-%m-%d-%H_%M_%S")
        # 设置邮件主题 必须项
        self.msg['subject'] = Header('[执行结果：' + result + ']' + self.Msg_Title + now, 'utf-8')

    def setContent(self, reportFile):
        '设置邮件正文'
        f = open(reportFile, 'rb')
        # 读取测试报告正文
        self.mail_body = f.read()
        f.close()
        self.contentText = MIMEText(self.mail_body, 'html', 'UTF-8')
        self.msg.attach(self.contentText)
        self.setAccessory(self.mail_body)

    def setAccessory(self, mail_body):
        '设置附件'
        self.accessory = MIMEText(mail_body, 'html', 'utf-8')
        self.accessory['Content-Type'] = self.Content_Type
        self.accessory["Content-Disposition"] = self.Content_Disposition
        self.msg.attach(self.accessory)

        # 定义发送邮件函数，只需要传报告的绝对路径即可

    def sendEMail(self, reportFile):
        '发送邮件'
        self.get_Result(reportFile)
        self.setContent(reportFile)
        try:
            self.smtp = smtplib.SMTP(self.server, 25)
            self.smtp.login(self.sender, self.password)
            # self.receiver = ['hebaochen@tenez.cn','mazhuang@tenez.cn','yangyaojun@tenez.cn']
            self.receiver.append(self.PReceiver)
            # self.receiver = ['yangyaojun@tenez.cn','272981562@qq.com']
            print(self.receiver)
            # 定义发件人，如果不写，发件人为空
            self.msg['From'] = self.sender
            # 定义收件人，如果不写，收件人为空
            self.msg['To'] = ",".join(self.receiver)
            self.smtp.sendmail(self.sender, self.receiver, self.msg.as_string())
            self.smtp.quit()
            self.logger.info("The test report has send to developer by email.")
            return True
        except smtplib.SMTPException as e:
            self.logger.error(str(e))
            print(str(e))
            return False