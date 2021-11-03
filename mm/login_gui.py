"""
创建一个经典的GUI应用程序，通过面向对象方法
"""
from tkinter import Frame, StringVar, Label, Entry, Button, messagebox
from tkinter.ttk import Combobox

import consts
from mm.InMainWin import InMainWin
from mm.dataDao import getAddressListByUsername, dao1
from mm.login_controller import server_type_value

"""创建gui"""
class Application(Frame):
    def __init__(self,master=None):# 把root传进去
        super().__init__(master)
        self.master=master
        self.server_type=StringVar()
        self.recusername=StringVar()
        self.recpassword=StringVar()
        self.pop_name=StringVar()
        self.smtp_name=StringVar()
        self.grid()
        self.createWidget(master)


    def createWidget(self,master=None):
        """创建组件"""
        servername=Label(master,text="接受服务器类型:")
        servername.grid(row=0,column=0)
        types=['POP3','IMAP']
        server_list=Combobox(master,textvariable=self.server_type)
        server_list.grid(row=0,column=1)
        server_list['values']=types

        recusernameLabel=Label(master,text="邮箱地址:")
        recusernameLabel.grid(row=1,column=0)
        recusernameEntry=Entry(master,show=None,textvariable=self.recusername)
        recusernameEntry.grid(row=1,column=1,padx=10)

        recpasswordLabel=Label(master,text="邮箱密码:")
        recpasswordLabel.grid(row=2,column=0)
        recpasswordEntry=Entry(master,show='*',textvariable=self.recpassword)
        recpasswordEntry.grid(row=2,column=1,padx=10)

        pop_server=Label(master,text="pop服务器:")
        pop_server.grid(row=3,column=0)
        pop_server_value=Entry(master,show=None,textvariable=self.pop_name)
        pop_server_value.grid(row=3,column=1,padx=10)

        smtp_server=Label(master,text="smtp服务器:")
        smtp_server.grid(row=4,column=0)
        smtp_server_value=Entry(master,show=None,textvariable=self.smtp_name)
        smtp_server_value.grid(row=4,column=1,padx=10)

        login_button=Button(master,text="登录",command=self.inlogin)
        login_button.grid(row=5,column=1,padx=50)

    def inlogin(self,master=None):
        res=server_type_value(self.server_type.get(),self.recusername.get(),self.recpassword.get(),self.pop_name.get(),self.smtp_name.get())
        
        if res:
            messagebox.showinfo(title='',message='登录成功')
            db=dao1('mmMail')
            addressLists=getAddressListByUsername(db,consts.get_value('username'))
            db.close()
            if len(addressLists)!=0:
                consts.set_value('to_persons',addressLists)
            else:
                addressLists=[]
                consts.set_value('to_persons',addressLists)
            self.master.destroy()
            InMainWin(res)

        else:
            messagebox.showinfo(title='',message='登录失败，请重新登录')

   
        



