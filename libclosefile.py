#Copyright Bail 2022
#libclosefile 关闭文件库 v1.0_1
#2022.9.2

ORIGIN_OPEN = open
files = []

def myopen(*args,**kw):
    file = ORIGIN_OPEN(*args,**kw)
    files.append(file)
    return file
def status():
    for i in files:
        print(i,i.closed,sep='\t')
def close_all_files():
    for i in files:
        i.close()

__builtins__['open'] = myopen
