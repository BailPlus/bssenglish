#Copyright Bail 2021-2022
#bssenglish:libfile 文件处理模块

from tkinter import filedialog
import os,libwordclass,csv,libsc,shutil,libgui,bss

##INSTALLED = True
SC = 'sc'
AUDIO = 'audio'
LESSONS = 'lessons'
PLUGINS = 'plugins'
OSNAME = bss.OSNAME

home = os.path.expanduser('~')
path = {
        'nt':{
              'audio':os.path.join(home,'appdata','local','bss','audio'),
              'lessons':os.path.join(home,'appdata','roaming','bss','lessons'),
              'plugins':os.path.join(home,'appdata','roaming','bss','plugins'),
              'cache':os.path.join(home,'appdata','local','bss'),
              'data':os.path.join(home,'appdata','roaming','bss')
             },
        'posix':{
                 'audio':os.path.join(home,'.cache','bss','audio'),
                 'lessons':os.path.join(home,'.config','bss','lessons'),
                 'plugins':os.path.join(home,'.config','bss','plugins'),
                 'cache':os.path.join(home,'.cache','bss'),
                 'data':os.path.join(home,'.config','bss')
                },
        'termux':{
                  'audio':os.path.join(home,'.cache','bss','audio'),
                  'lessons':os.path.join(home,'.config','bss','lessons'),
                  'plugins':os.path.join(home,'.config','bss','plugins'),
                  'cache':os.path.join(home,'.cache','bss'),
                  'data':os.path.join(home,'.config','bss')
                 },
        'deepin':{
                  'audio':os.path.join(home,'.cache','bss','audio'),
                  'lessons':os.path.join(home,'.config','bss','lessons'),
                  'plugins':os.path.join(home,'.config','bss','plugins'),
                  'cache':os.path.join(home,'.cache','bss'),
                  'data':os.path.join(home,'.config','bss')
                 }
        }

def getfile():	#获取目录中所有文件
    lst = os.listdir(getpath('lessons'))	#检测文件
    for i in lst:
        yield os.path.join(getpath('lessons'),i)	#返回文件名
'''
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
'''
def readfile(fn:str)->list:	#读取文件并转化为单词字典
    lst = readfromcsv(fn)  ###############
    lst2 = [libwordclass.Word(*i) for i in lst]
    return lst2
'''
def readfromcsv(fn=None)->list:
    if not fn:
        fn = filedialog.askopenfilename(filetypes=[('CSV表格','.csv')])
    lst = []
    with open(fn,newline='',encoding='utf-8') as file:
        reader = csv.reader(file,delimiter='\t')
        for index,items in enumerate(reader):
            if index == 0:  #跳过第一行
                continue
            lst.append(libsc.Sc(*items))
    return lst
'''
def readfromcsv(fn=None)->list:    
    if not fn:
        fn = filedialog.askopenfilename(filetypes=[('CSV表格','.csv')])
    lst = []
    with open(fn,newline='',encoding='utf-8') as file:
        reader = csv.reader(file,delimiter='\t')
        for index,items in enumerate(reader):
            if index == 0:  #跳过第一行
                continue
            lst.append(items)
    return lst
def saveascsv(lst:list,fn=None):
    if not fn:
        fn = filedialog.asksaveasfilename(filetypes=[('CSV表格','.csv')])
    with open(fn,'w',newline='',encoding='utf-8') as file:
        writer = csv.writer(file,delimiter='\t')
        writer.writerow(['单词','音标','词义','学习次数','错误次数','复习时间'])
        for i in lst:
            writer.writerow(i.items())
def getpath(name:str):  #此函数现已弃用，在版本兼容时起过渡作用。新版本应直接访问path字典。
    return path[OSNAME][name]
####    if INSTALLED:
####        if name == 'sc':
####            return os.path.join(eval(os.name+'data'),SC)
##        if name == 'scdir':
##            return eval(os.name+'data')
##        elif name == 'audio':
##            return os.path.join(eval(os.name+'cache'),AUDIO)
##        elif name == 'lessons':
##            return os.path.join(eval(os.name+'data'),LESSONS)
##        elif name == 'plugins':
##            return os.path.join(eval(os.name+'data'),PLUGINS)
##        elif name == '<all>':
##            return (getpath('audio'),getpath('lessons'),getpath('scdir'),getpath('plugins'))
##    else:
####        if name == 'sc':
####            return SC
##        if name == 'scdir':
##            return '.'
##        elif name == 'audio':
##            return AUDIO
##        elif name == 'lessons':
##            return LESSONS
##        elif name == 'plugins':
##            return PLUGINS
##        elif name == '<all>':
##            return (getpath('audio'),getpath('lessons'),getpath('scdir'),getpath('plugins'))
def add_lesson():
    '''添加课程文件'''
    fn = filedialog.askopenfilename()
    path = getpath('lessons')
    print(path)
    shutil.copy(fn,path)
    libgui.msgbox.showinfo('添加成功','课程添加成功，请重启程序。')
