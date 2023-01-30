#Copyright Bail 2021-2023
#bssenglish:libfile 文件处理模块

from tkinter import filedialog  #将在后期替换为libgui.filedialog，为了代码整洁
from typing import Generator    #用于描述类型
import os,libclass,csv,shutil,libgui,bss,json

OSNAME = bss.OSNAME
LESSON_FILE_HEADER = 'bssenglish lesson file\n' #课程文件头

home = os.path.expanduser('~')
path = {
    'cache':{
        'nt':os.path.join(home,'appdata','local','bss'),
        'posix':os.path.join(home,'.cache','bss'),
        'deepin':os.path.join(home,'.cache','bss'),
        'termux':os.path.join(home,'.cache','bss')
    },
    'data':{
        'nt':os.path.join(home,'appdata','roaming','bss'),
        'posix':os.path.join(home,'.config','bss'),
        'deepin':os.path.join(home,'.config','bss'),
        'termux':os.path.join(home,'.config','bss')
    },
    'icon':{    #不添加到<all>
        'nt':os.path.join(os.getcwd(),'bss.png'),
        'posix':'/usr/share/pixmaps/bss.png',
        'deepin':os.path.join(os.getcwd(),'bss.png'),   #不用绝对路径的原因是开发要用这个配置
        'termux':'/data/data/com.termux/files/usr/share/pixmaps/bss.png'
    }
}
path1 = {
    'lessons':os.path.join(path['data'][OSNAME],'lessons'),
    'sc':os.path.join(path['data'][OSNAME],'sc'),
    'audio':os.path.join(path['cache'][OSNAME],'audio'),
    'plugins':os.path.join(path['data'][OSNAME],'plugins'),
    'notice':os.path.join(path['data'][OSNAME],'notice'),
    'progress':os.path.join(path['data'][OSNAME],'progress'),
}
path = {**path,**path1}

def getfile()->Generator:
    '''获取所有课程文件
返回值:生成器，包含所有课程文件'''
    lst = os.listdir(getpath('lessons'))	#检测文件
    for i in lst:
        yield os.path.join(getpath('lessons'),i)	#返回文件名
def islessonfile(fn:str)->bool:
    '''判断是否为课程文件（通过比对文件头）
fn(str):文件名
返回值：为课程文件性(bool)'''
    with open(fn) as file:
        if file.readline() == LESSON_FILE_HEADER:
            return True
        else:
            return False
def readfile(fn:str)->libclass.Lesson:
    '''读取课程文件
fn(str):文件名
返回值:课程对象(libclass.Lesson)'''
    #读取课程信息
    with open(fn) as file:
        file.readline()
        lesson_info = json.loads(file.readline())
    #读取课程内容
    lst = readfromcsv(fn,2) #我也不知道该起啥名
    words = tuple(libclass.Word(*i) for i in lst)
    lesson = libclass.Lesson(**lesson_info,words=words)   #使用`words=words`是为了避免参数传乱出现bug
    return lesson
def readfromcsv(fn:str=None,jump_lines:int=1)->list:
    '''从csv读取内容
fn(str):文件名。若不指定则呼出文件选择窗口手动选择
jump_lines(int):跳过行数。若不指定则跳过第一行
返回值:二维列表，第一维为每一行，第二维为这一行的每一列(list)'''
    if not fn:
        fn = filedialog.askopenfilename(filetypes=[('CSV表格','.csv')])
    lst = []
    with open(fn,newline='',encoding='utf-8') as file:
        reader = csv.reader(file,delimiter='\t')
        for index,items in enumerate(reader):
            if index in range(jump_lines):  #跳过指定行
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
    if name == '<all>':
        return (getpath('audio'),getpath('lessons'),getpath('sc'),getpath('plugins'),getpath('notice'),getpath('progress')) #待优化:用for循环写
    elif name in ('cache','data','icon'):
        return path[name][OSNAME]
    else:
        return path[name]
def add_lesson():
    '''添加课程文件'''
    fn = filedialog.askopenfilename()
    if islessonfile(fn): 
        path = getpath('lessons')
        shutil.copy(fn,path)
        libgui.msgbox.showinfo('添加成功','课程添加成功，请重启程序。')
    else:
        libgui.showerror('你选择的不是课程文件，请重新选择')
