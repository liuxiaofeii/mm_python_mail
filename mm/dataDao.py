"""
连接mysql数据库
"""
import pymysql#调用模块
def dao1(database=None):
    if database==None:
        return False
    db = pymysql.connect(host='172.17.187.201',port=3306,user = 'mm',password='Mysql@123',database=database,charset='utf8')#打开数据库连接
    return db

def close(db):
    db.close()

#查看
def getAddressListByUsername(db,username):
    cursor=db.cursor()
    n=cursor.execute("select * from hm_friends where accountaddress='"+username+"'")
    results=cursor.fetchall()
    addressLists=[]
    #print(n)
    for result in results:
        addressLists.append(result[1])
    # print(addressLists)
    return addressLists
#添加
def addAddress(db,username,friendname):
    cursor=db.cursor()
    n=cursor.execute("insert into hm_friends values ('%s','%s')"%(username,friendname))
    db.commit()
    #print(n)

#删除
def deleteAddress(db,username,friendname):
    cursor=db.cursor()
    n=cursor.execute("delete from hm_friends where accountaddress='%s' and friend='%s'"%(username,friendname))
    db.commit()


if __name__=='__main__':
    db=dao1('mmMail')
    addAddress(db,'amy@mm.server.com','11@mm.server.com')
    deleteAddress(db,'amy@mm.server.com','11@mm.server.com')
    getAddressListByUsername(db,"amy@mm.server.com")