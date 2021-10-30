#Copyright Bail 2021
#bssenglish:libfile 文件处理模块

from tkinter import filedialog
import os,libwordclass,csv,libsc

INSTALLED = True
SC = 'sc'
AUDIO = 'audio'
LESSONS = '.bsslessons'
ntdata = ntcache = os.path.join(os.path.expanduser('~'),'appdata','local','bss')
posixdata = os.path.join(os.path.expanduser('~'),'.config','bss')
posixcache = os.path.join(os.path.expanduser('~'),'.cache','bss')

def getfile():	#获取目录中所有文件
    lst = os.listdir(getpath('lessons'))	#检测文件
    for i in lst:
        yield os.path.join(getpath('lessons'),i)	#返回文件名
def readfile(fn:str)->list:	#读取文件并转化为单词字典
    lst = []
    try:
        file = open(fn,encoding='utf-8')	#普通打开
        for i in file.readlines():	#读取每个词语记录
            objlst = i.split()
            objlst[0] = objlst[0].replace('_',' ')
            lst.append(libwordclass.Word(*objlst))
            print(f'已读入:{i}')
    except ValueError:
        msgbox.showerror('','文件格式错误')
        raise
    finally:
        file.close()
        print(f'共读入{len(lst)}个单词')
    return lst
def readfromcsv()->list:
    fn = filedialog.askopenfilename(filetypes=[('CSV表格','.csv')])
    lst = []
    with open(fn,newline='') as file:
        reader = csv.reader(file,delimiter='\t')
        for index,items in enumerate(reader):
            if index == 0:  #跳过第一行
                continue
            lst.append(libsc.Sc(*items))
    return lst
def saveascsv(lst:list):
    fn = filedialog.asksaveasfilename(filetypes=[('CSV表格','.csv')])
    with open(fn,'w',newline='') as file:
        writer = csv.writer(file,delimiter='\t')
        writer.writerow(['单词','音标','词义','学习次数','错误次数','复习时间'])
        for i in lst:
            writer.writerow(i.items())
def getpath(name:str):
    if INSTALLED:
        if name == 'sc':
            return os.path.join(eval(os.name+'data'),SC)
        elif name == 'scdir':
            return eval(os.name+'data')
        elif name == 'audio':
            return os.path.join(eval(os.name+'cache'),AUDIO)
        elif name == 'lessons':
            return os.path.join(os.path.expanduser('~'),LESSONS)
        elif name == '<all>':
            return (getpath('audio'),getpath('lessons'),getpath('scdir'))
    else:
        if name == 'sc':
            return SC
        elif name == 'scdir':
            return '.'
        elif name == 'audio':
            return AUDIO
        elif name == 'lessons':
            return LESSONS
        elif name == '<all>':
            return (getpath('audio'),getpath('lessons'),getpath('scdir'))
