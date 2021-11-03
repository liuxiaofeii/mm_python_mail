import poplib

# 输入邮件地址, 口令和POP3服务器地址:
from email import header
from email.header import decode_header
from email.parser import Parser

# indent用于缩进显示:
from email.utils import parseaddr
from tkinter import messagebox


def print_info(msg, indent=0,contents={},i=1):
    headers={}

    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                    headers['Subject']=value
                else:
                    if header=='From':
                        addr,addr=parseaddr(value)
                        headers['From']=addr
                    else:
                        if header=='To':
                            name=decode_str(value)
                            headers['To']=name
                    # hdr, addr = parseaddr(value)
                    # name = decode_str(hdr)
                    #value = u'%s <%s>' % (name, addr)


        #print("---------------"+str(name))
        #print("++++++++++++++++++++"+str(addr))


    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            headerss,contents,i=print_info(part, indent + 1,contents,i)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
                contents['content'+str(i)]=content
                i=i+1

        else:
            print('无内容')

    print()
    return headers,contents,i
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

    # 解析邮件,获取附件
def get_att(msg_in):
        attachment_files = []
        try:
            for part in msg_in.walk():
                # 获取附件名称类型
                #file_name = part.get_param("filename")  # 如果是附件，这里就会取出附件的文件名
                file_name=part.get_filename();
                print(part.get_filename())
                # file_name = part.get_filename() #获取file_name的第2中方法
                # contType = part.get_content_type()
                if file_name:
                    h = header.Header(file_name)
                    # 对附件名称进行解码
                    dh = header.decode_header(h)
                    filename = dh[0][0]
                    if dh[0][1]:
                        # 将附件名称可读化
                        filename = decode_str(str(filename, dh[0][1]))
                        # print(filename)
                        # filename = filename.encode("utf-8")
                    # 下载附件
                    data = part.get_payload(decode=True)
                    # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
                    att_file = open('./' + filename, 'wb')
                    att_file.write(data)  # 保存附件
                    att_file.close()
                    attachment_files.append(filename)


        except Exception as error:
             messagebox.showinfo(title='消息',message=error)

        return attachment_files

def get_content(msg):
    content=''
    content_type = msg.get_content_type()
    # print('content_type:',content_type)
    if content_type == 'text/plain': # or content_type == 'text/html'
        content = msg.get_payload(decode=True)
        charset = guess_charset(msg)
        if charset:
            content = content.decode(charset)
    return content