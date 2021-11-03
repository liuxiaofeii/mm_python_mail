from tkinter import Tk
import consts
from mm.login_gui import Application
"""
以后不要一股脑就用*号，会出问题的，还是得需要什么导入什么
记住是import consts，用from xx import * 会报错
"""
if __name__=="__main__":
    consts._init()
    login_root=Tk()
    login_root.title("请登录")
    login_root.geometry("300x250+600+270")
    Application(login_root)
    login_root.mainloop()

