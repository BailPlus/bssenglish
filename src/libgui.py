#Copyright Bail 2021-2023
#bssenglish:libgui 图形界面模块

from tkinter import *
from tkinter import messagebox as msgbox
from tkinter import ttk
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

##    msgbox.showinfo('公告','''此版本优化了课程文件格式，更新为第3版，
##原有课程文件需要通过lessonturn2to3.py进行转换。
##此公告将在下个版本移除。''')

    lesson_choose_frame = Frame(root)
    lesson_choose_frame.pack(anchor=NW)
    Label(lesson_choose_frame,text='请选择课程').grid()
    Button(lesson_choose_frame,text='添加课程',command=libfile.add_lesson).grid(row=0,column=1)
    Button(lesson_choose_frame,text='获取课程（网站尚未完善，敬请期待）',command=libnetwork.open_browser_to_fetch_lessons,state=DISABLED).grid(row=0,column=2)

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
            print(f'警告：{path}不是课程文件')
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
    def winexit():
        if msgbox.askyesno('警告','现在退出，学习进度将不会保存。\n是否仍要退出？',parent=rem):
            rem.destroy()
    
    rem = Toplevel(root)
    rem.title('记忆')
    rem.protocol("WM_DELETE_WINDOW",winexit)

    wordl = Label(rem);wordl.pack()
    pronl = Label(rem);pronl.pack()
    tranl = Label(rem);tranl.pack()

    sclst = []
    for i in wlst:
        wordl['text'] = i.word
        pronl['text'] = i.pronounce
        libaudio.play(i)
        res = msgbox.askyesno('','会？',parent=rem)
        tranl['text'] = i.trans
        if res:
            if msgbox.askyesno('','正确？',parent=rem):
                pass
            else:
                for j in range(2,-1,-1):
                    libaudio.play(i)
                    msgbox.showinfo('复习',f'还剩{j}次',parent=rem)
                sclst.append(i)
        else:
            for j in range(2,-1,-1):
                libaudio.play(i)
                msgbox.showinfo('复习',f'还剩{j}次',parent=rem)
            sclst.append(i)
        tranl['text'] = ''

    msgbox.showinfo('提示','恭喜你学完本课',parent=rem)
    rem.destroy()
    return sclst
def listen(root:Tk,wlst:list)->list:
    '''听写窗口
root(tkinter.Tk):根窗口
wlst(list):单词列表
返回值:生词列表(list)'''
    def gui(word):
        def judge():
            if entry['state'] == NORMAL:
                entry['state'] = DISABLED
                wordl.grid(row=2)
                myinput = entry.get()
                if myinput == word.word:
                    judgel['text'] = '(v)'
                else:
                    judgel['text'] = '(x)'
                    sclst.append(word)
            else:
                if judgel['text'] == '(v)':
                    lis.destroy()
                else:
                    entry['state'] = NORMAL
                    entry.delete(0,END)
                    threading.Thread(target=lambda:libaudio.play(word)).start()

        lis = Toplevel(lisroot)
        lis.title('听写')

        Label(lis,text=word.pronounce).grid(row=0)
        entry = Entry(lis);entry.grid(row=1,column=0)
        judgel = Label(lis);judgel.grid(row=1,column=1)
        wordl = Label(lis,text=word.word)
        entry.bind('<Return>',lambda event:judge())
        entry.bind('<Button-1>',lambda event:threading.Thread(target=lambda:libaudio.play(word)).start())   #绑定鼠标点击时播放音频
        entry.bind('<Control_L>',lambda event:threading.Thread(target=lambda:libaudio.play(word)).start())  #绑定按下左Ctrl时播放音频

    lisroot = Toplevel(root)
    lisroot.title('听写模块总窗口')
    Label(lisroot,text='该窗口为听写模块总窗口，请确保完成学习后关闭').pack()

    sclst = []
    for i in wlst:
        gui(i)
    lisroot.mainloop()
    return sclst
    #现在问题:所有窗口(包括主窗口)都关闭后才会return
def write(root:Tk,wlst:list)->list:
    '''默写窗口
root(tkinter.Tk):根窗口
wlst(list):单词列表
返回值:生词列表(list)'''
    def gui(word):
        def judge():
            if entry['state'] == NORMAL:
                entry['state'] = DISABLED
                wordl.grid(row=2)
                myinput = entry.get()
                if myinput == word.word:
                    judgel['text'] = '(v)'
                else:
                    judgel['text'] = '(x)'
                    sclst.append(word)
            else:
                if judgel['text'] == '(v)':
                    wri.destroy()
                else:
                    entry['state'] = NORMAL
                    entry.delete(0,END)

        wri = Toplevel(wriroot)
        wri.title('默写')

        Label(wri,text=word.trans).grid(row=0)
        entry = Entry(wri);entry.grid(row=1,column=0)
        judgel = Label(wri);judgel.grid(row=1,column=1)
        wordl = Label(wri,text=word.word)
        entry.bind('<Return>',lambda event:judge())

    wriroot = Toplevel(root)
    wriroot.title('默写模块总窗口')
    Label(wriroot,text='该窗口为默写模块总窗口，请确保完成学习后关闭').pack()

    sclst = []
    for i in wlst:
        gui(i)
    wriroot.mainloop()
    return sclst
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
