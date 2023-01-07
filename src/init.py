#Copyright Bail 2021-2022
#bssenglish:init 程序初始化
#2021.10.16-2022.12.5

import sys,os,libsc,shelve,libfile

def makedir():
    print('开始创建数据目录')
    for i in libfile.getpath('<all>'):
        try:
            os.makedirs(i)
            print(f'已创建：{i}')
        except FileExistsError:
            print(f'警告：{i}已存在',file=sys.stderr)
##def makedata():
##        dic = shelve.open(libfile.getpath('sc'))
##        dic['rem'] = dic['lis'] = dic['wri'] = []
##        print('生词数据库创建成功')
def makedata():
    print('开始创建生词数据库')
    for i in ('rem.csv','lis.csv','wri.csv'):
        path = os.path.join(libfile.getpath('data'),i)
        if os.path.exists(path): #若存在则不创建，修复了v1.5.5_50之前小概率删库的bug
            print(f'警告：{i}已存在',file=sys.stderr) #用i而不是用path
        else:
            open(path,'w').close()
            print(f'已创建：{i}')   #用i而不是用path
    # 备选方案：open(path,'a').close()
    # 若可行，则可替换以上if语句
def main():
    makedir()
    makedata()
    return 0

if __name__ == '__main__':
    main()
