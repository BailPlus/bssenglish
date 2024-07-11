#Copyright Bail 2023
#bssenglish:libstudy 学习模块

import libgui,libsc,libclass

def remember(root:libgui.Tk,lesson:libclass.Lesson):
    '''记忆模块
root(tkinter.Tk):根窗口
wlst(list):包含要学习的单词对象的列表'''
    def hui4(): #会，进入看对错
        translab.config(text=current_word.trans)
        huibtn.grid_forget()
        buhuibtn.grid_forget()
        duibtn.grid(row=1,column=0)
        buduibtn.grid(row=1,column=1)
    def dui4(): #对，标为熟词并进入下一个单词
        nonlocal index
        huilst.append(current_word)
        index += 1
        nextword()
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
            index += 1
            recitebtn.grid_forget()
            nextword()
        else:   #没复习完
            current_word.play()
            recitebtn.config(text=f'复习（剩余{ci4}次）',command=lambda:recite(ci4-1))
    def nextword():
        nonlocal index  #防止下一行的判断出现bug
        if index == len(wlst):  #如果是最后一个单词
            libgui.showinfo('恭喜你学完本课',parent=win)
            close()
        else:
            #隐藏按钮
            duibtn.grid_forget()
            buduibtn.grid_forget()
            recitebtn.grid_forget()
            translab.config(text='')

            #初始化变量
            nonlocal current_word   #index上面已经声明
            current_word = wlst[index]

            #播放等
            win.title(f'记忆 {index+1}/{len(wlst)}')
            current_word.play()
            wordlab.config(text=current_word.word)
            pronlab.config(text=current_word.pronounce)
            huibtn.grid(row=0,column=0)
            buhuibtn.grid(row=0,column=1)
    def close():
        libsc.mark('remember',sclst,huilst)
        lesson.progress[0] = index
        win.destroy()

    #初始化各种变量
    wlst = lesson.words #单词列表
    index = lesson.progress[0]  #当前学习的单词在单词列表中的索引
    sclst = []          #生词列表
    huilst = []         #熟词列表
    current_word:libclass.Word = None   #当前学习的单词

    #初始化界面
    win = libgui.remember(root)
    win.protocol('WM_DELETE_WINDOW',close)
    wordlab,pronlab,translab,huibtn,buhuibtn,duibtn,buduibtn,recitebtn = win.wordlab,win.pronlab,win.translab,win.huibtn,win.buhuibtn,win.duibtn,win.buduibtn,win.recitebtn
    huibtn.config(command=hui4)
    buhuibtn.config(command=bu4)
    duibtn.config(command=dui4)
    buduibtn.config(command=bu4)
    #recitebtn的command在recite函数里指定

    #显示第一个单词
    nextword()
def listen(root:libgui.Tk,lesson:libclass.Lesson):
    '''听写模块
root(tkinter.Tk):根窗口
wlst(list):包含要学习的单词对象的列表'''
    def enter():
        nonlocal current_word,status,index,sclst

        if status == None:  #未判：判，并加入生词熟词列表
            entry.config(state=libgui.DISABLED)
            wordlab.config(text=current_word.word)
            myinput = entry.get()
            if myinput == current_word.word:
                judgelab['text'] = '(v)'
                huilst.append(current_word)
                status = True
            else:
                judgelab['text'] = '(x)'
                sclst.append(current_word)
                status = False
        elif status == True:    #已判，正确：下一个
            index += 1
            nextword()
        elif status == False:   #已判，错误：进入抄写
            judgelab.config(text='')
            entry.config(state=libgui.NORMAL)
            entry.delete(0,libgui.END)
            current_word.play()
            status = 'copy'
        elif status == 'copy':  #抄写：判※不加生词熟词列表
            entry.config(state=libgui.DISABLED)
            wordlab.config(text=current_word.word)
            myinput = entry.get()
            if myinput == current_word.word:
                judgelab['text'] = '(v)'
                status = True
            else:
                judgelab['text'] = '(x)'
                status = False
        else:
            raise ValueError(f'错误的状态: {status}')
    def nextword():
        if index == len(wlst):    #如果是最后一个单词
            libgui.showinfo('恭喜你学完本课',parent=win)
            close()
        else:
            #初始化变量
            nonlocal current_word,status
            current_word = wlst[index]
            status = None

            #显示下一个单词
            win.title(f'听写 {index+1}/{len(wlst)}')
            judgelab.config(text='')
            entry.config(state=libgui.NORMAL)
            entry.delete(0,libgui.END)
            current_word.play()
            pronlab.config(text=current_word.pronounce)
            wordlab.config(text='')
    def close():
        libsc.mark('listen',sclst,huilst)
        lesson.progress[1] = index
        win.destroy()

    #初始化各种变量
    wlst = lesson.words #单词列表
    index = lesson.progress[1]  #当前学习的单词在单词列表中的索引
    status = None   #备选：None,True,False,'copy'
                    #None:未判；True:已判，正确；False:已判，错误；'copy':抄写
    sclst = []      #生词列表
    huilst = []     #熟词列表
    current_word:libclass.Word = None   #当前学习的单词

    #初始化界面
    win = libgui.listen(root)
    win.protocol('WM_DELETE_WINDOW',close)
    pronlab,entry,judgelab,wordlab = win.pronlab,win.entry,win.judgelab,win.wordlab
    entry.bind('<Return>',lambda event:enter())
    entry.bind('<Control_L>',lambda event:current_word.play())

    #显示第一个单词
    nextword()
def write(root:libgui.Tk,lesson:libclass.Lesson):
    '''默写模块
root(tkinter.Tk):根窗口
wlst(list):包含要学习的单词对象的列表'''
    def enter():
        nonlocal current_word,status,index,sclst

        if status == None:  #未判：判，并加入生词熟词列表
            entry.config(state=libgui.DISABLED)
            wordlab.config(text=current_word.word)
            myinput = entry.get()
            if myinput == current_word.word:
                judgelab['text'] = '(v)'
                huilst.append(current_word)
                status = True
            else:
                judgelab['text'] = '(x)'
                sclst.append(current_word)
                status = False
        elif status == True:    #已判，正确：，下一个
            index += 1
            nextword()
        elif status == False:   #已判，错误：进入抄写
            judgelab.config(text='')
            entry.config(state=libgui.NORMAL)
            entry.delete(0,libgui.END)
            status = 'copy'
        elif status == 'copy':  #抄写：判※不加生词熟词列表
            entry.config(state=libgui.DISABLED)
            wordlab.config(text=current_word.word)
            myinput = entry.get()
            if myinput == current_word.word:
                judgelab['text'] = '(v)'
                status = True
            else:
                judgelab['text'] = '(x)'
                status = False
        else:
            raise ValueError(f'错误的状态: {status}')
    def nextword():
        if index == len(wlst):    #如果是最后一个单词
            libgui.showinfo('恭喜你学完本课',parent=win)
            close()
        else:
            #初始化变量
            nonlocal current_word,status
            current_word = wlst[index]
            status = None

            #显示下一个单词
            win.title(f'默写 {index+1}/{len(wlst)}')
            judgelab.config(text='')
            entry.config(state=libgui.NORMAL)
            entry.delete(0,libgui.END)
            translab.config(text=current_word.trans)
            wordlab.config(text='')
    def close():
        libsc.mark('write',sclst,huilst)
        lesson.progress[2] = index
        win.destroy()

    #初始化各种变量
    wlst = lesson.words #单词列表
    index = lesson.progress[2]  #当前学习的单词在单词列表中的索引
    status = None   #备选：None,True,False,'copy'
                    #None:未判；True:已判，正确；False:已判，错误；'copy':抄写
    sclst = []      #生词列表
    huilst = []     #熟词列表
    current_word:libclass.Word = None   #当前学习的单词

    #初始化界面
    win = libgui.write(root)
    win.protocol('WM_DELETE_WINDOW',close)
    translab,entry,judgelab,wordlab = win.translab,win.entry,win.judgelab,win.wordlab
    entry.bind('<Return>',lambda event:enter())

    #显示第一个单词
    nextword()
