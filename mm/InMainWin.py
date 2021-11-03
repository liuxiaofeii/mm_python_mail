from tkinter import Tk

import consts
from mm.main_gui import Application


def InMainWin(server):
    global main_root
    main_root=Tk()
    main_root.title(consts.get_value('username'))
    main_root.geometry("600x500+530+200")
    Application(main_root,server)
    main_root.mainloop()
    