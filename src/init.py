#Copyright Bail 2021-2023
#bssenglish:init 程序初始化
#2021.10.16-2023.1.17

import sys,os,libsc,libfile

def create(type:str,path:str):
    '''创建
type(str):（备选：dir,file）创建的类型
path(str):文件名'''
    if os.path.exists(path):    #如果已存在（防止重复创建。1. 创建文件夹会报错；2. 创建文件会清除数据,v1.5.5_50之前小概率删库的bug由此引起）
        print(f'已存在：{path}')
    else:                       #如果不存在
        if type == 'dir':           #如果创建目录
            os.makedirs(path)
        elif type == 'file':        #如果创建文件
            open(path,'a').close()
        else:
            raise ValueError('不存在的创建类型')
        print(f'已创建：{path}')
def makedir():
    print('开始创建数据目录')
    for i in libfile.getpath('<all>'):
        create('dir',i)
##def makedata():
##        dic = shelve.open(libfile.getpath('sc'))
##        dic['rem'] = dic['lis'] = dic['wri'] = []
##        print('生词数据库创建成功')
def makedata():
    print('开始创建生词数据库')
    for i in ('rem.csv','lis.csv','wri.csv'):
        path = os.path.join(libfile.getpath('sc'),i)
        create('file',path)
def makenotice():
    print('开始创建公告处理文件')
    path = os.path.join(libfile.getpath('notice'),'newest.md5')
    create('file',path)
def makeprogress():
    for i in os.listdir(libfile.path['lessons']):
        fn = os.path.join(libfile.path['lessons'],i)
        md5 = libfile.get_file_md5(fn)
        path = os.path.join(libfile.path['progress'],md5)
        if not os.path.exists(path):
            with open(path,'w') as file:
                file.write(os.linesep.join(('0','0','0')))
def main():
    print('开始初始化')
    makedir()
    makedata()
    makenotice()
    makeprogress()
    print('初始化完毕')
    return 0

if __name__ == '__main__':
    main()
