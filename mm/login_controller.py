import poplib
from tkinter import messagebox

import consts


"""
判断是pop3还是imap
"""

def server_type_value(select_type,recusername,recpassword,pop_servername,smtp_servername):
    consts.set_value('username',recusername)
    consts.set_value('password',recpassword)
    consts.set_value('email',pop_servername)
    consts.set_value('smtpname',smtp_servername)

    print("--------aa--------")
    print(consts.get_value('email'))

    if select_type=='POP3':
        res=loginPOP3(recusername,recpassword,pop_servername,smtp_servername)

    if select_type=='IMAP':
        res=False

    return res


"""用pop3方式登录"""
def loginPOP3(username,password,pop_servername,smtp_servername):
    try:
        pop=poplib.POP3(pop_servername)
        pop.user(username)
        res=pop.pass_(password)
        if str(res) in 'b\'+OK Mailbox locked and ready\'':
            return pop
        else:
            return False
    except Exception as error:
        return False

