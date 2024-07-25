#Copyright Bail 2021-2023
#bssenglish:libfile 文件处理模块

from tkinter import filedialog  #将在后期替换为libgui.filedialog，为了代码整洁
import os,libclass,csv,shutil,libgui,bss,json,hashlib,traceback

OSNAME = bss.OSNAME
LESSON_FILE_HEADER = 'bssenglish lesson file\n' #课程文件头
FILE_VERSION = 4    #当前课程文件版本

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

def getlessons()->list:
    '''获取所有课程
返回值:包含所有课程对象的列表(list)'''
    lst = os.listdir(getpath('lessons'))	#检测文件
    lessonlst = []
    for i in lst:
        fn = os.path.join(getpath('lessons'),i)
        if islessonfile(fn):
            try:
                lesson = readfile(fn)
            except libclass.WrongFileVersion as e:
                print(f'E: 文件版本错误: {e}')
            except Exception:
                print(f'E: "{fn}"课程文件已损坏')
                traceback.print_exc()
            else:
                lessonlst.append(lesson)
        else:
            print(f'W: "{fn}"不是课程文件')
    return lessonlst
def islessonfile(fn:str)->bool:
    '''判断是否为课程文件（通过比对文件头）
fn(str):文件名
返回值：为课程文件性(bool)'''
    with open(fn,encoding='utf-8') as file:
        if file.readline() == LESSON_FILE_HEADER:
            return True
        else:
            return False
def readfile(fn:str)->libclass.Lesson:
    '''读取课程文件
fn(str):文件名
返回值:课程对象(libclass.Lesson)'''
    #读取课程信息
    with open(fn,encoding='utf-8') as file:
        file.readline()
        lesson_info = json.loads(file.readline())
    #比对文件版本
    current_file_version = lesson_info['file_version']
    if current_file_version != FILE_VERSION:
        raise libclass.WrongFileVersion(f'{fn}: {current_file_version}，预期为{FILE_VERSION}')
    #读取课程内容
    words = tuple(libclass.Word(*i) for i in readfromcsv(fn,2))
    md5 = get_file_md5(fn)
    progress_file_name = os.path.join(path['progress'],md5)
    with open(progress_file_name,encoding='utf-8') as progress_file:
        progress = list(map(int,progress_file.readlines()))
    lesson = libclass.Lesson(**lesson_info,words=words,md5=md5,progress=progress)   #使用`words=words`是为了避免参数传乱出现bug
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
def get_file_md5(file_name:str)->str:
    '''计算文件的md5
file_name(str):文件路径
返回值:文件的md5(str)

鸣谢：墨痕诉清风 (https://blog.csdn.net/u012206617/article/details/108083431)'''
    m = hashlib.md5()   #创建md5对象
    with open(file_name,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  #更新md5对象
    return m.hexdigest()    #返回md5对象
def saveprogress(lessonlst:list):
    '''保存课程进度
lessonlst(list[libclass.Lesson]):课程对象列表'''
    for i in lessonlst:
        progress_file_name = os.path.join(path['progress'],i.md5)
        with open(progress_file_name,'w',encoding='utf-8') as progress_file:
            progress_file.write('\n'.join(map(str,i.progress)))
