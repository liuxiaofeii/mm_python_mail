"""
创建一个经典的GUI应用程序，通过面向对象方法
"""
import os
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Notebook, Separator

from filetype import filetype

from mail_service import *

from decodeMailContentDao import decodeMailContentDao
from consts import *
from file_service import get_filetype
from decodeMailContent import get_att
from mm.dataDao import getAddressListByUsername, dao1, addAddress, deleteAddress

"""创建gui"""
class Application(Frame):
    #初始化
    def __init__(self,master=None,server=None):# 把root传进去
        super().__init__(master)
        self.master=master
        self.pack()
        self.allmails={}
        self.attachList=[]
        self.mailserver=server
        self.to_persons=[]
        self.acceptMailsList=None
        self.createWidget(master)



    #创建主窗口
    def createWidget(self,master=None):
        """创建组件"""
        mainwin=Notebook(master)
        mainwin.place(width=600,height=500,relx=0,rely=0)

        #创建2个标签frame
        #homeFrame 首页
        homeFrame=Frame(mainwin,bg='white')
        homeFrame.place(width=600,height=500,relx=0,rely=0.1)
        mainwin.add(homeFrame,text='首页',)

        #收信发信窗体
        win2=Notebook(homeFrame)
        win2.place(width=600,height=500,relx=0,rely=0)

        #acceptFrame 收信窗体
        acceptFrame=Frame(win2,bg='#f6f5ec')
        acceptFrame.place(width=600,height=500,relx=0,rely=0.1)

        #收信列表窗口
        acceptOptionFrame=Frame(acceptFrame,bg='white',bd='3',relief=GROOVE)
        acceptOptionFrame.place(width=250,height=500,relx=0,rely=0)
        #收取邮件
        acceptButton=Button(acceptOptionFrame,bg="white",text="收取邮件",command=lambda :self.inrec(acceptOptionContentFrame,acceptOptionFrame))
        acceptButton.place(relx=0,rely=0.01)
        #删除邮件
        deleteButton=Button(acceptOptionFrame,bg="white",text="删除邮件",command=self.deletem)
        deleteButton.place(relx=0.3,rely=0.01)
        #清空邮箱
        cleanButton=Button(acceptOptionFrame,bg="white",text="清空收件箱",command=self.cleanm)
        cleanButton.place(relx=0.6,rely=0.01)
        #邮件列表窗口
        acceptOptionContentFrame=Frame(acceptOptionFrame,bg='white',bd='1',relief=GROOVE)
        acceptOptionContentFrame.place(width=250,height=410,relx=0,rely=0.08)
        #邮件内容窗口
        self.acceptContentFrame=Frame(acceptFrame,bg='white',bd='3',relief=GROOVE)
        self.acceptContentFrame.place(width=350,height=500,relx=0.42,rely=0)
        self.createMailContentDao()

        #sendFrame 发信窗体
        sendFrame=Frame(win2,bg='#f6f5ec')
        sendFrame.place(width=600,height=500,relx=0,rely=0.1)

        self.createSendWin(sendFrame)

        win2.add(acceptFrame,text='收信',)
        win2.add(sendFrame,text='发信')
        #------------------------------------------------------------
        #addressFrame 通讯录
        addressFrame=Frame(mainwin,bg='#f6f5ec')
        addressFrame.place(width=600,height=500,relx=0,rely=0.1)
        mainwin.add(addressFrame,text='通讯录')
        self.createAddressDao(addressFrame)
    #收取邮件
    def inrec(self,acceptOptionContentFrame,acceptOptionFrame):
        self.mailserver=login_mailserver(self.mailserver)
        self.allmails=decodeMailContentDao(self.mailserver)
        self.allmailslen=len(self.allmails)
        self.deleteMailGroup=list()
        self.createRec(acceptOptionContentFrame,acceptOptionFrame)
    #创建邮件列表
    def createRec(self,acceptOptionContentFrame,acceptOptionFrame):
        #print(self.allmails)
        acceptOptionContentFrame.destroy()
        acceptOptionContentFrame=Frame(acceptOptionFrame,bg='white',bd='1',relief=GROOVE)
        acceptOptionContentFrame.place(width=250,height=410,relx=0,rely=0.08)
        i=0.05
        i2=0.05
        Label(acceptOptionContentFrame,text='主题',bg='#f6f5ec').place(relx=0.24,rely=0.01,height=15,width=50)
        self.vars=[None]*(self.allmailslen+1)
        self.mailindex=1
        sb=Scrollbar(acceptOptionContentFrame)
        sb.place(relx=0.01,rely=0.06,height=360)

        self.acceptMailsList=Listbox(acceptOptionContentFrame,bg='#f6f5ec',yscrollcommand=sb.set)
        self.acceptMailsList.bind('<<ListboxSelect>>', self.createMailContent)
        self.acceptMailsList.insert(END,'------------邮件列表------------')
        for index in range(1,len(self.allmails)):
            mail=self.allmails[index]
            self.mailindex=index
            self.vars[self.mailindex]=IntVar()
            self.acceptMailsList.insert(END,str(mail['headers']['Subject']))
            i2=i2+0.067
            i=i+0.08
        sb.config(command=self.acceptMailsList.yview())
        self.acceptMailsList.place(relx=0.07,rely=0.06,width=200,height=360)

    def selectwhat(self,var1):
        messagebox.showinfo(title='',message=var1)

    #读取邮件内容并写入到窗体
    """
    mindex：读取邮件的索引号
    """
    def createMailContentDao(self):
        self.l1=Label(self.acceptContentFrame,bg='#f6f5ec',bd='2',text="")
        self.l1.place(relx=0,rely=0,width=200)
        self.l2=Label(self.acceptContentFrame,bg='#f6f5ec',bd='2',text="")
        self.l2.place(relx=0,rely=0.08,width=200)
        self.t1=Text(self.acceptContentFrame,bg='white')
        print()
        self.t1.place(height=250,relx=0,rely=0.16)

        #邮件内容
        self.l3=Label(self.acceptContentFrame,bg='#f6f5ec',bd='2',text="")
        self.l3.place(relx=0,rely=0.7,width=200)
        self.l4=Label(self.acceptContentFrame,bg='#f6f5ec',bd='2',text="")
        self.l4.place(relx=0,rely=0.76,width=200)

    #读取邮件内容窗体
    def createMailContent(self,event=None,mindex=None):
        """
        这里切换到发信页面会报错，因为访问了这个方法2次造成数组越界，没有找到哪里访问了2次
        :param event:
        :return:
        """
        if event==None and mindex==None:
            From_persond='发件人：'
            To_person='收件人：'
            SubjectMail='主题：'
            contents=''
            dates=''
            haveAttach=False
        else:
                mindex=event.widget.curselection()[0]
                headers=self.allmails[mindex]['headers']
                contents=self.allmails[mindex]['contents']
                dates=self.allmails[mindex]['dates']
                haveAttach=self.allmails[mindex]['haveAttach']
                if len(headers)==0:
                    From_persond='发件人：'
                    To_person='收件人：'
                    SubjectMail='主题：'
                else:
                    From_person=headers['From']
                    From_persond='发件人：'+str(headers['From'])+''
                    To_person=decodeToContent(headers['To'])[1:-2]
                    To_person='收件人：'+str(To_person)
                    SubjectMail='主题：'+headers['Subject']
                if len(contents)==0:contents=''
                else:
                    content=contents['content1']
                    contents=decodeMailContent(str(content),From_person)
                if len(dates)==0:
                    dates=''
        try:
            self.l1.config(text=From_persond)
            self.l2.config(text=SubjectMail)
            self.t1.delete(1.0,'end')
            self.t1.insert(2.0,contents)
            self.t1.insert(INSERT,'\n')
            self.l3.config(text=To_person)
            self.l4.config(text=dates)
            if haveAttach:
                Button(self.acceptContentFrame,text='附件下载',bg='#f6f5ec',command=lambda :self.dowAttach(mindex))\
                        .place(relx=0.8,rely=0.68)
        except Exception as error:
            messagebox.showinfo(title='',message=error)

    #下载附件
    def dowAttach(self,index):
        attachment_files=get_att(self.allmails[index]['msg'])
        if len(attachment_files)>0:
            messagebox.showinfo(title='',message='下载成功')
        else:
            messagebox.showinfo(title='',message='下载失败')
    #删除邮件
    def deletem(self):
        mindex=int(self.acceptMailsList.curselection()[0])
        self.acceptMailsList.delete(mindex)
        #messagebox.showinfo(title='',message=mindex)
        self.deleteMailGroup.append(mindex)
        deletemail(self.mailserver,self.deleteMailGroup)
        self.createMailContent()


    #选择邮件
    def selectmail(self,var1):
        #print(self.vars[var1].get())
        if self.vars[var1].get()==1:
            self.deleteMailGroup.append(var1)
    #打开邮件
    def openmail(self,mail):
        mailtop=Toplevel()
        mailtop.title("邮件内容")
        mailtop.geometry("300x300+700+300")
        text=Text(mailtop)
        text.place(relx=0,rely=0)
        text.insert('end',mail['contents'])

    #创建发信窗体内容
    def createSendWin(self,sendFrame):
        to_personLabel=Label(sendFrame,text='收件人')
        to_personLabel.place(relx=0.01,rely=0.01,width=50)
        self.tempToPerson=StringVar()



        to_personEntry=Entry(sendFrame,width=50,textvariable=self.tempToPerson)
        to_personEntry.place(relx=0.1,rely=0.01)
        self.select_to_person=Button(sendFrame,text='+',bg='#f6f5ec',cursor='hand1',command=lambda :self.chooseFromPerson())
        self.select_to_person.place(relx=0.7,rely=0.01,height=20)

        subjectLabel=Label(sendFrame,text='主题')
        subjectLabel.place(relx=0.01,rely=0.08,width=50)
        self.tempSubject=StringVar()
        subjectEntry=Entry(sendFrame,width=50,textvariable=self.tempSubject)
        subjectEntry.place(relx=0.1,rely=0.08)

        contentLabel=Label(sendFrame,text='正文')
        contentLabel.place(relx=0.01,rely=0.15,width=50)
        self.contentText=Text(sendFrame,width=200,height=10)
        self.contentText.place(relx=0.1,rely=0.15)
        self.select_file=Button(sendFrame,text='+',bg='#f6f5ec',cursor='hand1',command=lambda :self.chooseFileDao())
        self.select_file.place(relx=0.1,rely=0.44,height=20)

        b1=Button(sendFrame,text='发送',command=lambda:self.sendMailDao())
        b1.place(relx=0.1,rely=0.74,width=60)

    #选择收件人窗口
    def chooseFromPerson(self):
        chooseToWin=Toplevel(bg='white')
        chooseToWin.geometry("200x250+800+250")
        sb=Scrollbar(chooseToWin)
        sb.place(relx=0.1,y=0,height=190)
        var1=StringVar()
        cf=Listbox(chooseToWin,listvariable=var1,bg='#f6f5ec',yscrollcommand=sb.set)
        cf.bind()
        chooseToWin.title('选择发件人')
        to_persons=consts.get_value('to_persons')
        print(to_persons)
        if len(to_persons)==0 or to_persons==None:
            messagebox.showinfo(title='消息',message="通讯录还没有人，请先添加")
            return chooseToWin.destroy()
        for to_person in to_persons:
            cf.insert('end',to_person)
        b1=Button(chooseToWin,text='确定',command=lambda:self.getTempFromPerson(cf.get(cf.curselection()),chooseToWin))
        b1.place(relx=0.38,rely=0.74)
        sb.config(command=cf.yview())
        cf.place(relx=0.17,rely=0)

        

    #获得收件人
    def getTempFromPerson(self,var1,chooseToWin):
        self.tempToPerson.set(var1)
        return chooseToWin.destroy()

    #发送邮件
    def sendMailDao(self):
        contentText=self.contentText.get('1.0','end')
        tempToPerson=self.tempToPerson.get()
        tempSubject=self.tempSubject.get()
        if tempToPerson==None or tempSubject==None or contentText==None or tempToPerson=='' or tempSubject=='' or contentText=='':
            return messagebox.showinfo(title='提醒',message='请填好全部的信息再发送')
        if len(self.attachList)>0:
            ret=send_emailAttach(tempToPerson, tempSubject, contentText,self.attachList)
        else:
            ret=sendMail(str(tempToPerson),str(tempSubject),str(contentText))
        if ret:
            to_personlists=consts.get_value('to_persons')
            to_personlists.append(tempToPerson)
            consts.set_value('to_persons',to_personlists)
            print(consts.get_value('to_persons'))
            messagebox.showinfo(title='消息',message="发送成功")
        else:
            messagebox.showinfo(title='消息',message="发送失败")

    def chooseFileDao(self):
        contentText=self.contentText.get('1.0','end')
        tempToPerson=self.tempToPerson.get()
        tempSubject=self.tempSubject.get()
        filePath=askopenfilename(title="请选择文件")
        ftype=filetype.guess(filePath).extension
        if len(filePath)!=0:
            filename=os.path.basename(filePath)
            fileprefix=os.path.splitext(filename)[0]
            filesuffix=os.path.splitext(filename)[1]
            #print(filename)
            #print(filesuffix)
            file=[filePath,ftype,fileprefix,filesuffix]
            self.attachList.append(file)

        #print(self.attachList)

    #创建通讯录窗口
    def createAddressDao(self,addressFrame):
        sb=Scrollbar(addressFrame)
        sb.place(relx=0,y=0,height=475)

        self.addresslist=Listbox(addressFrame,bg='#f6f5ec',yscrollcommand=sb.set)
        to_persons=consts.get_value('to_persons')
        if to_persons==None or len(to_persons)==0:
            self.addresslist.insert(0,"通讯录还没有人，请先添加")
        else:
            self.createAddressWin(to_persons)
        refreshAddress=Button(addressFrame,text='刷新',command=lambda:self.doRefreshAddress(to_persons))
        refreshAddress.place(relx=0.53,rely=0.0,width=283)
        addAddress=Button(addressFrame,text='添加',command=lambda:self.doAddAddress())
        addAddress.place(relx=0.53,rely=0.1,width=283)
        deleteAddress=Button(addressFrame,text='删除',command=lambda:self.doDeleteAddress(self.addresslist.curselection()))
        deleteAddress.place(relx=0.53,rely=0.2,width=283)
        sb.config(command=self.addresslist.yview())
        self.addresslist.place(relx=0.029,rely=0,height=500,width=300)
    def createAddressWin(self,to_persons):
        self.addresslist.delete(0,END)
        for to_person in to_persons:
            self.addresslist.insert('end',to_person)
    #刷新通讯录
    def doRefreshAddress(self,to_persons):
        if to_persons==None or len(to_persons)==0:
            return messagebox.showinfo(title='消息',message="通讯录还没有人，请先添加")
        db=dao1('mmMail')
        addressLists=getAddressListByUsername(db,consts.get_value('username'))
        db.close()
        consts.set_value('to_persons',addressLists)

        self.addresslist.delete(0,END)
        to_persons=consts.get_value('to_persons')
        i=0
        for to_oneperson in to_persons:
            print(to_oneperson)
            self.addresslist.insert(i,to_oneperson)
            i=i+1

    #添加联系人
    def doAddAddress(self):
        addAddressWin=Toplevel()
        addAddressWin.title('添加联系人')
        addAddressWin.geometry('300x100+650+350')
        Label(addAddressWin,text='邮箱地址',bg='grey').place(relx=0.1,rely=0)
        var1=StringVar()
        Entry(addAddressWin,textvariable=var1,bg='#f6f5ec').place(relx=0.3,rely=0)
        Button(addAddressWin,text='确定添加',bg='grey',command=lambda :self.addOneAddress(var1.get(),addAddressWin)).place(relx=0.37,rely=0.25)

    #删除联系人
    def doDeleteAddress(self,var1):
        #var1是个元组
        #messagebox.showinfo(title='',message=var1)
        if var1==None or len(var1)==0:
            return messagebox.showinfo(title='消息',message="请选择联系人后再点击删除")
        self.addresslist.delete(var1)
        friendname=consts.get_value('to_persons')[int(var1[0])]
        del consts.get_value('to_persons')[int(var1[0])]
        try:
            db=dao1('mmMail')
            print(friendname)
            deleteAddress(db,consts.get_value('username'),friendname)
            db.close()
            return messagebox.showinfo(title='消息',message='删除成功')
        except Exception as error:
            return messagebox.showinfo(title='消息',message=error)
#添加联系人
    def addOneAddress(self,var1,addAddressWin):
        if var1==None or var1=='':
            return messagebox.showinfo(title='消息',message="请正确输入邮箱地址")
        consts.get_value('to_persons').append(var1)
        self.addresslist.insert(END,var1)
        try:
            db=dao1('mmMail')
            addAddress(db,consts.get_value('username'),var1)
            db.close()
        except Exception as error:
            messagebox.showinfo(title='消息',message=error)
            return addAddressWin.destroy()
        messagebox.showinfo(title='消息',message='添加成功')
        return addAddressWin.destroy()
    #清空收件箱
    def cleanm(self):
        if self.acceptMailsList==None:
            return
        
        if deletemail(self.mailserver,int(self.allmailslen)):
            self.acceptMailsList.delete(0,END)
            return messagebox.showinfo(title='消息',message='清空成功')
        else:
            return messagebox.showinfo(title='消息',message='清空失败')

# #测试代码
# if __name__=="__main__":
#     consts._init()
#     global main_root
#     main_root=Tk()
#     main_root.title(consts.get_value('username'))
#     main_root.geometry("600x500+530+200")
#     #测试代码
#     consts.set_value('username','amy@mm.server.com')#
#     consts.set_value('password','amy')#
#     consts.set_value('email','mm.server.com')#
#     consts.set_value('smtpname','mm.server.com')#
#     db=dao1('mmMail')
#     addressLists=getAddressListByUsername(db,consts.get_value('username'))
#     if len(addressLists)!=0:
#         consts.set_value('to_persons',addressLists)
#     else:
#         addressLists=[]
#         consts.set_value('to_persons',addressLists)
#     Application(main_root,login_mailserver())
#
#     main_root.mainloop()


