#Copyright Bail 2021-2023
#bssenglish:libgui 图形界面模块

from tkinter import *
from tkinter import messagebox as msgbox,ttk
from _tkinter import TclError
import libsc as sc,libfile,bss,libaudio,libnetwork,libclass,libstudy

def root():
    root = Tk()
    root.title('白杉树背单词训练软件')
    root.geometry('800x600')
    try:
        root.iconphoto(False,PhotoImage(file=libfile.getpath('icon')))
    except TclError:
        print('W: 未找到图标')

    lesson_choose_frame = Frame(root)
    lesson_choose_frame.pack(anchor=NW)
    Label(lesson_choose_frame,text='请选择课程').grid()
    Button(lesson_choose_frame,text='添加课程',command=libfile.add_lesson).grid(row=0,column=1)
    Button(lesson_choose_frame,text='获取课程',command=libnetwork.open_browser_to_fetch_lessons).grid(row=0,column=2)

    sccontrol_frame = Frame(root)
    sccontrol_frame.pack(anchor=NW)
    Button(sccontrol_frame,text='生词管理',command=lambda:sc.control(root)).grid(row=0,column=0)
    rem_need_review_label = Label(sccontrol_frame)
    rem_need_review_label.grid(row=0,column=1)
    lis_need_review_label = Label(sccontrol_frame)
    lis_need_review_label.grid(row=0,column=2)
    wri_need_review_label = Label(sccontrol_frame)
    wri_need_review_label.grid(row=0,column=3)
    #将三个Label添加为root的属性，临时解决方案
    root.rem_need_review_label = rem_need_review_label
    root.lis_need_review_label = lis_need_review_label
    root.wri_need_review_label = wri_need_review_label

    lessons_frame = Frame(root)
    lessons_frame.pack(anchor=NW)
    root.lessons_frame = lessons_frame  #把这个frame夹带出去，方便其他函数使用。后期将会把libgui用class重写，届时将不需要这样操作

    Label(root,text='特别鸣谢：红杉树智能英语(http://www.hssenglish.com)提供运行逻辑',fg='#7f7f7f').pack(side=BOTTOM,fill=X)
    return root
def inroot(root:Tk,fnlst:list):
    root = root.lessons_frame
    for i,path in enumerate(fnlst):
        if not libfile.islessonfile(path):  #如果不是课程文件则跳过
            print(f'W: {path} 不是课程文件')
            continue
        lesson_title = libfile.readfile(path).name
        Label(root,text=lesson_title).grid(row=i,column=0)
        Button(root,text='记忆',command=lambda arg=path:libstudy.remember(root,libfile.readfile(arg))).grid(row=i,column=1)
        Button(root,text='听写',command=lambda arg=path:libstudy.listen(root,libfile.readfile(arg))).grid(row=i,column=2)
        Button(root,text='默写',command=lambda arg=path:libstudy.write(root,libfile.readfile(arg))).grid(row=i,column=3)
        Button(root,text='课程信息',command=lambda arg=path:lesson_info(root,libfile.readfile(arg))).grid(row=i,column=4)
        Button(root,text='下载音频',command=lambda arg=path:libaudio.download(root,libfile.readfile(arg).words)).grid(row=i,column=5)
def count_need_review(root:Tk):
    '''统计需要复习的单词数
root(tkinter.Tk):（包含三个Label属性的）根窗口'''
    remlab = root.rem_need_review_label
    lislab = root.lis_need_review_label
    wrilab = root.wri_need_review_label
    rem = sc.remlst
    lis = sc.lislst
    wri = sc.wrilst

    for i in ('rem','lis','wri'):
        if i == 'rem':
            sub = '记忆'
        elif i == 'lis':
            sub = '听写'
        elif i == 'wri':
            sub = '默写'

        need = sc.get_need_review_list(eval(i))
        needn = len(need)
        eval(i+'lab').config(text=f'{sub}需复习个数:{needn}')
def remember(root:Tk):
    '''记忆模块界面
root(tkinter.Tk):根窗口
返回值：带有组件属性的记忆窗口(tkinter.Toplevel)'''
    #窗口初始化
    win = Toplevel(root)
    win.title('记忆')

    #放置组件
    win.wordlab = Label(win);win.wordlab.pack()
    win.pronlab = Label(win);win.pronlab.pack()
    win.translab = Label(win);win.translab.pack()
    win.btnsframe = Frame(win);win.btnsframe.pack()
    win.huibtn = Button(win.btnsframe,text='会');win.huibtn.grid(row=0,column=0)
    win.buhuibtn = Button(win.btnsframe,text='不会');win.buhuibtn.grid(row=0,column=1)
    win.duibtn = Button(win.btnsframe,text='对',);win.duibtn.grid(row=1,column=0)
    win.buduibtn = Button(win.btnsframe,text='不对');win.buduibtn.grid(row=1,column=1)
    win.recitebtn = Button(win.btnsframe,text='复习');win.recitebtn.grid(row=2) #command在函数中设置

    #默认隐藏按钮
    win.huibtn.grid_forget()
    win.buhuibtn.grid_forget()
    win.duibtn.grid_forget()
    win.buduibtn.grid_forget()
    win.recitebtn.grid_forget()

    return win
def listen(root:Tk)->list:
    '''听写模块界面
root(tkinter.Tk):根窗口
返回值:带有组件属性的听写窗口(tkinter.Toplevel)'''
    #窗口初始化
    win = Toplevel(root)
    win.title('听写')

    #放置组件
    win.pronlab = Label(win);win.pronlab.grid(row=0)
    win.entry = Entry(win);win.entry.grid(row=1,column=0)
    win.judgelab = Label(win);win.judgelab.grid(row=1,column=1)
    win.wordlab = Label(win);win.wordlab.grid(row=2)

    return win
    #现在问题:所有窗口(包括主窗口)都关闭后才会return
def write(root:Tk)->list:
    '''默写模块界面
root(tkinter.Tk):根窗口
返回值:带有组件属性的默写窗口(tkinter.Toplevel)'''
    #窗口初始化
    win = Toplevel(root)
    win.title('默写')

    #放置组件
    win.translab = Label(win);win.translab.grid(row=0)
    win.entry = Entry(win);win.entry.grid(row=1,column=0)
    win.judgelab = Label(win);win.judgelab.grid(row=1,column=1)
    win.wordlab = Label(win);win.wordlab.grid(row=2)

    return win
    #现在问题:所有窗口(包括主窗口)都关闭后才会return
def lesson_info(root:Tk,lesson:libclass.Lesson):
    '''课程信息（原为“单词本”）
root(tkinter.Tk):根窗口
lesson(libclass.Lesson):课程'''
    book = Toplevel(root)
    book.title('课程信息')

    #基本信息
    Label(book,text=f'课程名称：{lesson.name}').pack(anchor=NW)
    Label(book,text=f'课程全称：{lesson.fullname}').pack(anchor=NW)
    Label(book,text=f'作者：{lesson.author}').pack(anchor=NW)

    #单词表
    tree = ttk.Treeview(book,columns=('音标','词义'));tree.pack()
    for i in lesson.words:
        tree.insert('','end',text=i.word,values=(i.pronounce,i.trans))
def download(root:Tk,wordnum:int):
    def update(value:int):
        per = round(value/wordnum,2)*100
        bar['value'] = per
        label['text'] = f'{per}%'
        down.update()
        if per == 100:
            msgbox.showinfo('提示','下载完成',parent=down)
            down.destroy()

    down = Toplevel(root)
    down.title('下载中...')

    bar = ttk.Progressbar(down);bar.pack()
    label = Label(down,text='0%');label.pack()
    return update
def show_notice(root:Tk,notice:str):
    msgbox.showinfo('公告',notice,parent=root)
def showinfo(msg:str,parent=None):
    '''显示提示信息
msg(str):提示信息的内容
parent(tkinter的窗口对象，包含Tk和Toplevel等):提示信息附属的窗口'''
    msgbox.showinfo('提示',msg,parent=parent)
def showerror(msg:str,parent=None):
    '''显示错误信息
msg(str):错误信息的内容
parent(tkinter的窗口对象，包含Tk和Toplevel等):错误信息附属的窗口'''
    msgbox.showerror('错误',msg,parent=parent)
def init(root:Tk):
    '''初始化界面
root(tkinter.Tk):根窗口'''
    inroot(root,libfile.getfile())
    count_need_review(root)
    print('界面初始化完毕')
