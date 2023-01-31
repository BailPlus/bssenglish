#Copyright Bail 2023
#bssenglish:liblearn 学习模块

import libgui,libsc,libclass

def remember(root:libgui.Tk,lesson:libclass.Lesson):
    def hui4(): #会，进入看对错
        translab.config(text=current_word.trans)
        huibtn.grid_forget()
        buhuibtn.grid_forget()
        duibtn.grid(row=1,column=0)
        buduibtn.grid(row=1,column=1)
    def dui4(): #对，进入下一个单词
        nonlocal index  #防止下一行的判断出现bug
        if index+1 == len(wlst):  #如果是最后一个单词
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
    def close():
        libsc.marks('remember',sclst)
        win.destroy()

    #初始化各种变量
    wlst = lesson.words
    index = 0
    sclst = []
    current_word = None

    #排除空列表
    if len(wlst) == 0:
        libgui.showinfo('列表为空，无可学习',parent=win)
        return []

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
    win.title(f'记忆 {index+1}/{len(wlst)}')
    current_word = wlst[index]
    current_word.play()
    wordlab.config(text=current_word.word)
    pronlab.config(text=current_word.pronounce)
    huibtn.grid(row=0,column=0)
    buhuibtn.grid(row=0,column=1)
