#Copyright Bail 2021-2022
#bssenglish:libgui 图形库

from tkinter import *
from tkinter import messagebox as msgbox
from tkinter import ttk
import libsc as sc,libfile,bss,libaudio,threading

def root():
    root = Tk()
    root.title('白杉树背单词训练软件')
    root.geometry('800x600')

##    msgbox.showinfo('公告','''此版本优化了课程文件格式，更新为第3版，
##原有课程文件需要通过lessonturn2to3.py进行转换。
##此公告将在下个版本移除。''')

    lesson_choose_frame = Frame(root)
    lesson_choose_frame.grid()
    Label(lesson_choose_frame,text='请选择课程').grid()
    Button(lesson_choose_frame,text='添加课程',command=libfile.add_lesson).grid(row=0,column=1)

    sccontrol_frame = Frame(root)
    sccontrol_frame.grid()
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
    lessons_frame.grid()
    root.lessons_frame = lessons_frame

    return root
def inroot(root:Tk,fnlst:list):
    root = root.lessons_frame
    for i,s in enumerate(fnlst):
        if 'bak' in s:
            continue
        Label(root,text=s).grid(row=i+2,column=0)
        Button(root,text='记忆',command=lambda arg=s:bss.learnctrl(root,libfile.readfile(arg),'remember')).grid(row=i+2,column=1)
        Button(root,text='听写',command=lambda arg=s:bss.learnctrl(root,libfile.readfile(arg),'listen')).grid(row=i+2,column=2)
        Button(root,text='默写',command=lambda arg=s:bss.learnctrl(root,libfile.readfile(arg),'write')).grid(row=i+2,column=3)
        Button(root,text='单词本',command=lambda arg=s:wordbook(root,libfile.readfile(arg))).grid(row=i+2,column=4)
        Button(root,text='下载音频',command=lambda arg=s:libaudio.download(root,libfile.readfile(arg))).grid(row=i+2,column=5)
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
def wordbook(root:Tk,lst:list):
    '''单词本
root(tkinter.Tk):根窗口
lst(list:[libwordclass.Word,...]):单词列表'''
    book = Toplevel(root)
    book.title('单词本')

    tree = ttk.Treeview(book,columns=('音标','词义'));tree.pack()
    for i in lst:
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
def init(root:Tk):
    '''初始化界面
root(tkinter.Tk):根窗口'''
    inroot(root,libfile.getfile())
    count_need_review(root)
    print('界面初始化完毕')
