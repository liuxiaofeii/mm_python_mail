def _init():#初始化
    global global_dict
    global_dict = {}
    print("执行了_init")


def set_value(key,value):
    """ 定义一个全局变量 """
    global_dict[key] = value


def get_value(key,defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return global_dict[key]
    except KeyError:
        return defValue











# email=''
# smtpname=''
# username=''
# password=''
# user_M=''
# From_persons=['amy@mm.server.com','user@mm.server.com','hh@mm.server.com','aa@mm.server.com','bb@mm.server.com'
#               ,'amy@mm.server.com','user@mm.server.com','hh@mm.server.com','aa@mm.server.com','bb@mm.server.com'
#     ,'amy@mm.server.com','user@mm.server.com','hh@mm.server.com','aa@mm.server.com','bb@mm.server.com'
#     ,'amy@mm.server.com','user@mm.server.com','hh@mm.server.com','aa@mm.server.com','bb@mm.server.com']