import poplib
from email.parser import Parser

from decodeMailContent import print_info, get_att


def decodedict(dict1):
    temp=dict()
    for key in dict1:
        value=dict1[key]
        temp[key]=value

    return temp
def decodeBoolean(boolean1):
    temp=False;
    temp=boolean1;
    return temp;
def decodeMailContentDao(server):
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    #print(mails)
    # 获取最新一封邮件, 注意索引号从1开始:
    indexs = len(mails)
    if indexs==0:
        return []

    allmails=list(range(indexs+1))
    for index in range(1,indexs+1):
        haveAttach=False
        resp, lines, octets = server.retr(index)
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        print("---------------------------日期")
        print(msg)
        dates=str(msg.get('Date',))
        headers,contents,num=print_info(msg)
        i=0
        for p in msg.walk():
            i=i+1
        if i>1:
            haveAttach=True;
        """
        为什么这么麻烦不直接把headers,contents封装成字典呢？
        因为print_info返回的是地址，所以牵一发动全身，所以重新创建个对象装
        """
        headers=decodedict(headers)
        contents=decodedict(contents)
        haveAttach=decodeBoolean(haveAttach)
        key=['headers','contents','dates','haveAttach','msg']

        value=[headers,contents,dates,haveAttach,msg]

        allmails[index]=dict(zip(key,value))
        #print("---------第%d次循环----------------"%index)




    return allmails