#Copyright Bail 2021-2023
#bssenglish:libgui 图形界面模块

from tkinter import *
from tkinter import messagebox as msgbox,ttk
from _tkinter import TclError
import libsc as sc,libfile,bss,libaudio,threading,libnetwork,libclass

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
        Button(root,text='记忆',command=lambda arg=path:bss.learnctrl(root,libfile.readfile(arg).words,'remember')).grid(row=i,column=1)
        Button(root,text='听写',command=lambda arg=path:bss.learnctrl(root,libfile.readfile(arg).words,'listen')).grid(row=i,column=2)
        Button(root,text='默写',command=lambda arg=path:bss.learnctrl(root,libfile.readfile(arg).words,'write')).grid(row=i,column=3)
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
def remember(root:Tk,wlst:list):
    '''记忆模块界面
root(tkinter.Tk):根窗口
wslt(list):单词列表
返回值:生词列表(list)'''
    def hui4(): #会，进入看对错
        translab.config(text=current_word.trans)
        huibtn.grid_forget()
        buhuibtn.grid_forget()
        duibtn.grid(row=1,column=0)
        buduibtn.grid(row=1,column=1)
    def dui4(): #对，进入下一个单词
        nonlocal index  #防止下一行的判断出现bug
        if index+1 == len(wlst):  #如果是最后一个单词
            msgbox.showinfo('提示','恭喜你学完本课',parent=win)
            win.destroy()
        else:
            #隐藏按钮
            duibtn.grid_forget()
            buduibtn.grid_forget()
            recitebtn.grid_forget()
            
            #初始化变量
            nonlocal current_word   #index上面已经声明
            index += 1
            current_word = wlst[index]

            #播放等
            win.title(f'记忆 {index+1}/{len(wlst)}')
            current_word.play()
            wordlab.config(text=current_word.word)
            pronlab.config(text=current_word.pronounce)
            huibtn.grid(row=0,column=0)
            buhuibtn.grid(row=0,column=1)
    def bu4():  #不会/不对，进入复习
        sclst.append(current_word)
        translab.config(text=current_word.trans)
        huibtn.grid_forget()
        buhuibtn.grid_forget()
        duibtn.grid_forget()
        buduibtn.grid_forget()
        recitebtn.grid(row=2)
        recite(2)
    def recite(ci4:int):   #下一次复习
        '''复习
ci(int):剩余复习次数'''
        if ci4 <= -1: #复习完了   #使用`<=`防止出现bug  #使用`-1`为了满足复习3次
            recitebtn.grid_forget()
            dui4()
        else:   #没复习完
            current_word.play()
            recitebtn.config(text=f'复习（剩余{ci4}次）',command=lambda:recite(ci4-1))
    
    #排除空列表
    if len(wlst) == 0:
        msgbox.showinfo('提示','列表为空，无可学习')
        return []

    #窗口初始化
    win = Toplevel(root)
    win.title('记忆')

    #放置组件
    wordlab = Label(win);wordlab.pack()
    pronlab = Label(win);pronlab.pack()
    translab = Label(win);translab.pack()
    btnsframe = Frame(win);btnsframe.pack()
    huibtn = Button(btnsframe,text='会',command=hui4);huibtn.grid(row=0,column=0)
    buhuibtn = Button(btnsframe,text='不会',command=bu4);buhuibtn.grid(row=0,column=1)
    duibtn = Button(btnsframe,text='对',command=dui4);duibtn.grid(row=1,column=0)
    buduibtn = Button(btnsframe,text='不对',command=bu4);buduibtn.grid(row=1,column=1)
    recitebtn = Button(btnsframe,text='复习');recitebtn.grid(row=2) #command在函数中设置

    #默认隐藏按钮
    huibtn.grid_forget()
    buhuibtn.grid_forget()
    duibtn.grid_forget()
    buduibtn.grid_forget()
    recitebtn.grid_forget()

    #初始化各种变量
    index = 0
    sclst = []
    current_word = None

    #显示第一个单词
    win.title(f'记忆 {index+1}/{len(wlst)}')
    current_word = wlst[index]
    current_word.play()
    wordlab.config(text=current_word.word)
    pronlab.config(text=current_word.pronounce)
    huibtn.grid(row=0,column=0)
    buhuibtn.grid(row=0,column=1)

    #主循环与返回
    win.mainloop()
    return sclst
    #现在问题:所有窗口(包括主窗口)都关闭后才会return
def listen(root:Tk,wlst:list)->list:
    '''听写窗口
root(tkinter.Tk):根窗口
wlst(list):单词列表
返回值:生词列表(list)'''
    def enter():
        nonlocal current_word,status,index,sclst

        if status == None:  #未判
            entry.config(state=DISABLED)
            wordlab.config(text=current_word.word)
            myinput = entry.get()
            if myinput == current_word.word:
                judgelab['text'] = '(v)'
                status = True
            else:
                judgelab['text'] = '(x)'
                sclst.append(current_word)
                status = False
        elif status == True:    #已判，正确
            if index+1 == len(wlst):    #如果是最后一个单词
                msgbox.showinfo('提示','恭喜你学完本课',parent=win)
                win.destroy()
            else:
                #初始化变量
                index += 1
                current_word = wlst[index]

                #显示下一个单词
                win.title(f'听写 {index+1}/{len(wlst)}')
                judgelab.config(text='')
                entry.config(state=NORMAL)
                entry.delete(0,END)
                current_word.play()
                pronlab.config(text=current_word.pronounce)
                wordlab.config(text='')
                status = None
        elif status == False:   #已判，错误
            judgelab.config(text='')
            entry.config(state=NORMAL)
            entry.delete(0,END)
            current_word.play()
            status = None

    #排除空列表
    if len(wlst) == 0:
        msgbox.showinfo('提示','列表为空，无可学习')
        return []

    #窗口初始化
    win = Toplevel(root)
    win.title('听写')

    #放置组件
    pronlab = Label(win);pronlab.grid(row=0)
    entry = Entry(win);entry.grid(row=1,column=0)
    judgelab = Label(win);judgelab.grid(row=1,column=1)
    wordlab = Label(win);wordlab.grid(row=2)

    #输入框绑定信号
    entry.bind('<Return>',lambda event:enter())
    entry.bind('<Control_L>',lambda event:current_word.play())

    #初始化各种变量
    index = 0
    status = None   #备选：None,True,False
                    #None:未判；True:已判，正确；False:已判，错误
    sclst = []
    current_word = None

    #显示第一个单词
    win.title(f'听写 {index+1}/{len(wlst)}')
    current_word = wlst[index]
    current_word.play()
    pronlab.config(text=current_word.pronounce)

    #主循环与返回
    win.mainloop()
    return sclst
    #现在问题:所有窗口(包括主窗口)都关闭后才会return
def write(root:Tk,wlst:list)->list:
    '''默写窗口
root(tkinter.Tk):根窗口
wlst(list):单词列表
返回值:生词列表(list)'''
    def enter():
        nonlocal current_word,status,index,sclst

        if status == None:  #未判
            entry.config(state=DISABLED)
            wordlab.config(text=current_word.word)
            myinput = entry.get()
            if myinput == current_word.word:
                judgelab['text'] = '(v)'
                status = True
            else:
                judgelab['text'] = '(x)'
                sclst.append(current_word)
                status = False
        elif status == True:    #已判，正确
            if index+1 == len(wlst):    #如果是最后一个单词
                msgbox.showinfo('提示','恭喜你学完本课',parent=win)
                win.destroy()
            else:
                #初始化变量
                index += 1
                current_word = wlst[index]

                #显示下一个单词
                win.title(f'默写 {index+1}/{len(wlst)}')
                judgelab.config(text='')
                entry.config(state=NORMAL)
                entry.delete(0,END)
                translab.config(text=current_word.trans)
                wordlab.config(text='')
                status = None
        elif status == False:   #已判，错误
            judgelab.config(text='')
            entry.config(state=NORMAL)
            entry.delete(0,END)
            status = None

    #排除空列表
    if len(wlst) == 0:
        msgbox.showinfo('提示','列表为空，无可学习')
        return []

    #窗口初始化
    win = Toplevel(root)
    win.title('默写')

    #放置组件
    translab = Label(win);translab.grid(row=0)
    entry = Entry(win);entry.grid(row=1,column=0)
    judgelab = Label(win);judgelab.grid(row=1,column=1)
    wordlab = Label(win);wordlab.grid(row=2)

    #输入框绑定信号
    entry.bind('<Return>',lambda event:enter())
    entry.bind('<Control_L>',lambda event:current_word.play())

    #初始化各种变量
    index = 0
    status = None   #备选：None,True,False
                    #None:未判；True:已判，正确；False:已判，错误
    sclst = []
    current_word = None

    #显示第一个单词
    win.title(f'默写 {index+1}/{len(wlst)}')
    current_word = wlst[index]
    translab.config(text=current_word.trans)

    #主循环与返回
    win.mainloop()
    return sclst
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
