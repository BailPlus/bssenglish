#Copyright Bail 2021
#bssenglish:init 程序初始化
#2021.10.16

import sys,os,libsc,shelve,libfile

def makedir():
    for i in libfile.getpath('<all>'):
        try:
            os.makedirs(i)
            print(f'已创建：{i}')
        except FileExistsError:
            pass
'''def makedata():
        dic = shelve.open(libfile.getpath('sc'))
        dic['rem'] = dic['lis'] = dic['wri'] = []
        print('生词数据库创建成功')'''
def makedata():
    for i in ('rem.csv','lis.csv','wri.csv'):
        open(os.path.join(libfile.getpath('scdir'),i),'w').close()
def main():
    makedir()
    makedata()
    return 0

if __name__ == '__main__':
    main()
