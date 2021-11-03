#coding:utf-8
import poplib
import smtplib
import types
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate
from re import *

import consts




def login_mailserver(server=None):
    username=consts.get_value('username')
    password=consts.get_value('password')
    email=consts.get_value('email')

    if server!=None:
        server.close()
    server = poplib.POP3(email)
    # 可以打开或关闭调试信息:
    server.set_debuglevel(1)

    # 身份认证:
    server.user(username)
    server.pass_(password)
    return server

def connectMail(server,username,password):

    # 身份认证:
    server.user(username)
    server.pass_(password)
    return server

def deletemail(mailserver,deleteMailGroup):
    if isinstance(deleteMailGroup,int):
        for mailindex in range(1,deleteMailGroup):
            mailserver.dele(mailindex)
    else:
        for mailindex in deleteMailGroup:
            mailserver.dele(mailindex)
    mailserver.quit()
    login_mailserver(mailserver)
    return True

def decodeMailContent(content,from_person):
    pat=compile('<style>.*<\/style>|<.*?>|'+str(from_person))
    return sub(pat,'',content)


def decodeToContent(content):
    print(content)
    pat=compile('<.*?>')
    return sub(pat,'',content)

#发送邮件
def sendMail(tempToPerson,tempSubject,tempContent):
    username=consts.get_value('username')
    password=consts.get_value('password')
    smtpname=consts.get_value('smtpname')
    ret=True
    try:
            msg=MIMEText(tempContent,'plain','utf-8')
            msg['From']=formataddr([username,username])
            msg['To']=formataddr([tempToPerson,tempToPerson])
            msg['Subject']=tempSubject
            msg['Date'] = formatdate(localtime = True)
            server=smtplib.SMTP(smtpname,25)
            server.login(username,password)
            server.sendmail(username,[tempToPerson,],msg.as_string())
            server.quit()
    except Exception:
            ret=False
    return ret

#发送带有附件的邮件
def send_emailAttach(tempToPerson, tempSubject, tempContent,attachList):
        username=consts.get_value('username')
        password=consts.get_value('password')
        smtpname=consts.get_value('smtpname')
        try:
            msg = MIMEMultipart()
            msg['From']=formataddr([username,username])
            msg['To']=formataddr([tempToPerson,tempToPerson])
            msg['Subject'] = Header(tempSubject, 'utf-8')
            msg['Date'] = formatdate(localtime = True)
            msg.attach(MIMEText(tempContent, 'plain', 'utf-8'))  # 把正文附在邮件上
            for file in attachList:
                with open(file[0], 'rb') as f:
                    print("-------------")
                    print(file[1])
                    print(file[2])
                    mime = MIMEBase(file[1], file[3], filename=file[2]+file[3])  # 创建表示附件的MIMEBase对象，重新命名为test.png
                    mime.add_header('Content-Disposition', 'attachment', filename=file[2]+file[3])
                    mime.set_payload(f.read())  # 读取附件内容
                    encoders.encode_base64(mime)  # 对附件Base64编码
                    msg.attach(mime)  # 把附件附在邮件上
                    server = smtplib.SMTP(smtpname, 25)
                    server.login(username, password)
                    server.sendmail(username, tempToPerson, msg.as_string())
                    print('发送成功！')
                    return True
        except Exception as error:
            print(error)
            return False

