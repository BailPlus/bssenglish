#Copyright Bail 2023
#bssenglish:libnotice 公告模块

# ===========================
# |     I  S  S  U  E       |
# | 已知问题：              |
# | 如果出现多条未读公告，  |
# | 则只能显示最近的一条。  |
# ===========================

##URLPREFIX = 'https://bailplus.github.io/bssenglish.pages/api/notice/'

import libnetwork,libfile,libgui,os,sys,traceback

urlprefix = libnetwork.APISOURCE+'notice/'

# 编程误区警示：
# 如果模块间有循环依赖关系，则不能在全局相互调用。
# 否则会因为模块未完整定义而引发AttributeError。
# 如下例：
##filename = os.path.join(libfile.getpath('notice'),'newest.md5')
# 修复方法：先定义一个空白的全局变量，再在函数中赋值。
filename = ''   #在isread函数中赋值
# 定义空白变量可以使代码逻辑更加清晰

def fetch_md5()->str:
    '''获取远程公告md5
返回值：远程公告md5(str)'''
    url = urlprefix+'newest.md5'
    remote_md5 = libnetwork.get_text_api(url)
    return remote_md5
def isread(remote_md5:str)->bool:
    '''判断公告是否已读
remote_md5(str):获取到的远程md5
返回值：已读性(bool)'''
    global filename
    filename = os.path.join(libfile.getpath('notice'),'newest.md5') #对全局变量赋值
    local_md5 = open(filename).read()
    if remote_md5 == local_md5: #如果公告已读
        return True
    else:                       #未读
        return False
def fetch_notice()->str:
    '''获取最新公告
返回值：公告(str)'''
    url = urlprefix+'newest'
    notice = libnetwork.get_text_api(url)
    return notice
def fetch_history()->str:
    '''获取历史公告
返回值：历史公告(str)'''
    url = urlprefix+'history'
    history_notice = libnetwork.get_text_api(url)
    return history_notice
def save_remote_md5(value:str): #这个功能尚未开放
    '''保存远程md5，以将公告标记为已读
value(str):获取到的远程md5'''
    with open(filename,'w') as file:
        file.write(value)
def process(root:libgui.Tk):
    '''公告处理
root(Tk):主窗口'''
    print('开始获取公告')

    try:
        remote_md5 = fetch_md5()
    except libnetwork.requests.exceptions.ReadTimeout: #若超时
        print('W: 获取公告md5超时',file=sys.stderr)
        libgui.showerror('获取公告超时')  #后期改为showwarn，需在libgui适配
        return  #跳过获取
    except libnetwork.requests.exceptions.ConnectionError:  #若无法连接
        print('W: 无法连接到服务器')
        libgui.showerror('无法连接到服务器，\n获取公告失败') #后期改为showwarn，需在libgui适配
        return

    if not isread(remote_md5):  #如果有未读公告
        print('发现新公告')
        try:
            notice = fetch_notice()
        except libnetwork.requests.exceptions.ReadTimeout: #若超时
            print('E: 获取公告超时',file=sys.stderr)
            libgui.showerror('获取公告超时（有新公告）')
            return  #跳过获取
        libgui.show_notice(root,notice)
        save_remote_md5(remote_md5)
    print('公告获取完毕')
