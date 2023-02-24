#Copyright Bail 2021-2023
#bssenglish:libsc 生词模块

from tkinter import *
from tkinter import messagebox as msgbox,ttk
import time,libclass,os,libfile,libgui,libstudy

remlst = [];lislst = [];wrilst = []

def imp(lst:list):
    '''从外部csv导入生词'''
    newlst = libfile.readfromcsv()
    lst += newlst
    msgbox.showinfo('提示','导入成功，请重启程序。')
def exp(lst:list):
    '''导出生词到外部csv'''
    libfile.saveascsv(lst)
def readfile():
    '''读取生词文件'''
    global remlst,lislst,wrilst
    for i in ('rem','lis','wri'):
        lst = eval(f'{i}lst')
        fn = os.path.join(libfile.getpath('sc'),f'{i}.csv')
        lst0 = libfile.readfromcsv(fn)
        lst += [libclass.Sc(*i) for i in lst0]
def treesort(tree:ttk.Treeview,col:str,reverse:bool):
    print(tree.get_children(''))
    l = [tree.set((k,col),k) for k in tree.get_children('')]
    l.sort(reverse)
    for i,(val,k) in enumerate(l):
        tree.move(k,'',i)
        print(k)
    tree.heading(col,command=lambda:treesort(tree,col,True))
def gui_main(root:Tk):
    '''主窗口
root(Tk):bss根窗口'''
    scmain = Toplevel(root)
    scmain.title('生词管理')

    #记忆模块生词
    screm = LabelFrame(scmain,text='记忆模块');screm.pack()
    rembtns = Frame(screm);rembtns.pack()
    Button(rembtns,text='立即复习',command=lambda:review(scmain,'remember')).grid()
##    Button(rembtns,text='导入',command=lambda:imp(remlst)).grid(row=0,column=1)
##    Button(rembtns,text='导出',command=lambda:exp(remlst)).grid(row=0,column=2)
    remtree = ttk.Treeview(screm,columns=('音标','词义','学习次数','错误次数','记忆强度','复习时间'));remtree.pack()

    remtree.heading('音标',text='音标',command=lambda:treesort(remtree,'音标',False))
    remtree.heading('词义',text='词义',command=lambda:treesort(remtree,'词义',False))
    remtree.heading('学习次数',text='学习次数',command=lambda:treesort(remtree,'学习次数',False))
    remtree.heading('错误次数',text='错误次数',command=lambda:treesort(remtree,'错误次数',False))
    remtree.heading('记忆强度',text='记忆强度',command=lambda:treesort(remtree,'记忆强度',False))
    remtree.heading('复习时间',text='复习时间',command=lambda:treesort(remtree,'复习时间',False))

    #听写模块生词
    sclis = LabelFrame(scmain,text='听写模块');sclis.pack()
    lisbtns = Frame(sclis);lisbtns.pack()
    Button(lisbtns,text='立即复习',command=lambda:review(scmain,'listen')).grid()
##    Button(lisbtns,text='导入',command=lambda:imp(lislst)).grid(row=0,column=1)
##    Button(lisbtns,text='导出',command=lambda:exp(lislst)).grid(row=0,column=2)
    listree = ttk.Treeview(sclis,columns=('音标','词义','学习次数','错误次数','记忆强度','复习时间'));listree.pack()

    listree.heading('音标',text='音标',command=lambda:treesort(listree,'音标',False))
    listree.heading('词义',text='词义',command=lambda:treesort(listree,'词义',False))
    listree.heading('学习次数',text='学习次数',command=lambda:treesort(listree,'学习次数',False))
    listree.heading('错误次数',text='错误次数',command=lambda:treesort(listree,'错误次数',False))
    listree.heading('记忆强度',text='记忆强度',command=lambda:treesort(listree,'记忆强度',False))
    listree.heading('复习时间',text='复习时间',command=lambda:treesort(listree,'复习时间',False))

    #默写模块生词
    scwri = LabelFrame(scmain,text='默写模块');scwri.pack()
    wribtns = Frame(scwri);wribtns.pack()
    Button(wribtns,text='立即复习',command=lambda:review(scmain,'write')).grid()
##    Button(wribtns,text='导入',command=lambda:imp(wrilst)).grid(row=0,column=1)
##    Button(wribtns,text='导出',command=lambda:exp(wrilst)).grid(row=0,column=2)
    writree = ttk.Treeview(scwri,columns=('音标','词义','学习次数','错误次数','记忆强度','复习时间'));writree.pack()

    writree.heading('音标',text='音标',command=lambda:treesort(writree,'音标',False))
    writree.heading('词义',text='词义',command=lambda:treesort(writree,'音标',False))
    writree.heading('学习次数',text='学习次数',command=lambda:treesort(writree,'音标',False))
    writree.heading('错误次数',text='错误次数',command=lambda:treesort(writree,'音标',False))
    writree.heading('记忆强度',text='记忆强度',command=lambda:treesort(writree,'音标',False))
    writree.heading('复习时间',text='复习时间',command=lambda:treesort(writree,'音标',False))

    return (scmain,remtree,listree,writree)
def reviewtime(obj:libclass.Sc):
    '''计算到该单词复习时刻的时间
obj(libclass.Sc):生词对象'''
    if obj.review <= time.time():
        return '0'
    sec = obj.review-time.time()
    timeobj = time.localtime(sec)
    timelst = time.strftime('%m,%d,%H,%M,%S',timeobj).split(',')

    #to solve problem `Jan 1'
    timelst[0] = str(int(timelst[0])-1)
    timelst[1] = str(int(timelst[1])-1)

    #解决“8时”时差（※其他系统可能会-8h或报错）
    timelst[2] = str(int(timelst[2])-8)

    times = '{}月{}天{}时{}分{}秒'.format(*timelst)
    return times
def intree(remtree:ttk.Treeview,listree:ttk.Treeview,writree:ttk.Treeview):
##    rem,lis,wri = remlst,lislst,wrilst
    for i in remlst:
        remtree.insert('','end',
                       text=i.word,	#单词
                       values=(i.pronounce,i.trans,	#发音，词义
                               i.learn,i.wrong,	#学习次数，错误次数
                               i.strenth(),	#记忆强度
                               reviewtime(i)))	#复习时间
    for i in lislst:
        listree.insert('','end',
                       text=i.word,	#单词
                       values=(i.pronounce,i.trans,	#发音，词义
                               i.learn,i.wrong,	#学习次数，错误次数
                               i.strenth(),	#记忆强度
                               reviewtime(i)))	#复习时间
    for i in wrilst:
        writree.insert('','end',
                       text=i.word,	#单词
                       values=(i.pronounce,i.trans,	#发音，词义
                               i.learn,i.wrong,	#学习次数，错误次数
                               i.strenth(),	#记忆强度
                               reviewtime(i)))	#复习时间
"""def deltatime(word:Sc):
    '''计算复习延后秒数
word(Sc):生词对象
返回值:距下次复习秒数(int)'''
    strenth = word.strenth()*100
    x = int(('%.2f' % strenth)[-1])
    if x == 0:
        x = 10
    if strenth == 0:
        return 0
    elif 0 < strenth <= 10:
        return 100*x
    elif 10 < strenth <= 20:
        return 200*x+1000
    elif 20 < strenth <= 30:
        return 300*x+3000
    elif 30 < strenth <= 40:
        return 2*(400*x+6000)
    elif 40 < strenth <= 50:
        return 2*(500*x+10000)
    elif 50 < strenth <= 60:
        return 2*(600*x+15000)
    elif 60 < strenth <= 70:
        return 4*(700*x+21000)
    elif 70 < strenth <= 80:
        return 4*(800*x+30000)
    elif 80 < strenth <= 90:
        return 8*(900*x+60000)
    elif 90 < strenth <= 100:
        return 8*(100*x+100000)
    else:
        raise ValueError('值超出范围')"""
def deltatime(word:libclass.Sc)->int:
    '''计算复习延后秒数
word(libclass.Sc):生词对象
返回值:距下次复习秒数(int)'''
    strenth = word.strenth()*100
    x = int(('%.d' % strenth)[-1])
    
    #增加可读性
    day = 24*3600
    hour = 3600
    minute = 60

    #分段函数
    if 0 <= strenth < 10:
        return x
    elif 10 <= strenth < 20:
        return 10*x+10
    elif 20 <= strenth < 30:
        return 60*x+60+40
    elif 30 <= strenth < 40:
        return 3600*x+11*minute+40
    elif 40 <= strenth < 50:
        return day*x+10*hour+11*minute+40
    elif 50 <= strenth < 60:
        return 7*day*x+10*day+10*hour+11*minute+40
    elif 60 <= strenth < 70:
        return 10*day*x+80*day+10*hour+11*minute+40
    elif 70 <= strenth < 80:
        return 15*day*x+180*day+10*hour+11*minute+40
    elif 80 <= strenth < 90:
        return 20*day*x+330*day+10*hour+11*minute+40
    elif 90 <= strenth <= 100:
        return 28*day*x+530*day+10*hour+11*minute+40
    else:
        raise ValueError('值超出范围')
def mark(study_type:str,sclst:list,huilst:list):
    '''处理生词与熟词
study_type(str):课程类型 备选：remember,listen,write
sclst(list):生词列表
huilst(list):熟词列表'''
    #根据类型获取数据列表
    if study_type == 'remember':
        data = remlst
    elif study_type == 'listen':
        data = lislst
    elif study_type == 'write':
        data = wrilst
    else:
        raise ValueError(f'非法的学习类型: {study_type}')

    #处理生词
    for i in sclst:
        for j in data:
            if i == j:   #如果生词已存在
                j.learn += 1
                j.wrong += 1
                j.review = int(time.time()+deltatime(j))
                break
            else:
                sc = libclass.Sc(i.word,i.pronounce,i.trans,1,1,int(time.time()))
                data.append(sc)

    #处理熟词
    for i in huilst:
        for j in data:
            if i == j:  #如果存在对应生词
                j.learn += 1
                j.review = int(time.time()+deltatime(j))

    #删除熟记生词
    for i in data:
        if i.strenth() > 0.95:
            data.remove(i)
def get_need_review_list(lst:list):
    '''分出需要复习的词
lst(list):生词列表
返回值:需要复习的生词列表(list)'''
    need_review = []
    for i in lst:
        if i.review <= time.time():
            need_review.append(i)
    return need_review
def review(scmain:Tk,sctype:str):
    '''生词复习及处理
scmain(tkinter.Toplevel):生词管理窗口
sclst(list):要复习的单词列表
lst(list):该类型的生词列表
sctype(str:remember/listen/write):生词类型名称，用于调用libgui的函数'''
    #获取对应列表
    if sctype == 'remember':
        data = remlst
        func = libstudy.remember
    elif sctype == 'listen':
        data = lislst
        func = libstudy.listen
    elif sctype == 'write':
        data = wrilst
        func = libstudy.write
    else:
        raise ValueError(f'非法的学习类型: {sctype}')

    #分出需要复习的词
    sclst = get_need_review_list(data)

    #复习生词
    func(scmain,sclst)
def savefile():
    '''将生词列表保存到文件'''
    for i in ('rem','lis','wri'):
        lst = eval(f'{i}lst')
        fn = os.path.join(libfile.getpath('sc'),f'{i}.csv')
        libfile.saveascsv(lst,fn)
def control(root):
    '''生词模块主控
root(tkinter.Tk):主窗口'''
    scmain,*trees = gui_main(root)
    intree(*trees)
