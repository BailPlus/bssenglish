#Copyright Bail 2021
#bssenglish:sc 生词模块

from tkinter import *
from tkinter import messagebox as msgbox,ttk
import shelve,time,libwordclass,libgui,liblist,os,libfile

FN = libfile.getpath('sc')
remlst = [];lislst = [];wrilst = []

class Sc(libwordclass.Word):
    '''生词类 继承于:单词类'''
##    learn = wrong = 1	#学习1次，错误1次
    def __init__(self,word:str,pro:str,trans:str,learn:int,wrong:int,review:int):
        '''word(str):单词
pro(str):音标
trans(str):词义
review(int※不可为float):复习时间戳'''
        self.word = word
        self.pronounce = pro
        self.trans = trans
        self.learn = int(learn)
        self.wrong = int(wrong)
        self.review = int(review)
    def strenth(self):
        '''用于计算记忆强度
word(Sc):生词对象
返回值:记忆强度(float:.2f)'''
        return round((self.learn - self.wrong)/self.learn,2)
    def items(self):
        return [self.word,self.pronounce,self.trans,
                self.learn,self.wrong,self.review]

def imp(lst:list):
    '''从外部csv导入生词'''
    newlst = libfile.readfromcsv()
    lst += newlst
    msgbox.showinfo('提示','导入成功，请重启程序。')
def exp(lst:list):
    '''导出生词到外部csv'''
    libfile.saveascsv(lst)
"""def readfile():
    '''读取生词文件'''
    global remlst,lislst,wrilst
    dic = shelve.open(FN)
    remlst = dic['rem']
    lislst = dic['lis']
    wrilst = dic['wri']
    dic.close()"""
def readfile():
    '''读取生词文件'''
    global remlst,lislst,wrilst
    for i in ('rem','lis','wri'):
        lst = eval(f'{i}lst')
        fn = os.path.join(libfile.getpath('scdir'),f'{i}.csv')
        lst += libfile.readfromcsv(fn)
def treesort(tree:ttk.Treeview,col:str,reverse:bool):
    print(tree.get_children(''))
    l = [tree.set((k,col),k) for k in tree.get_children('')]
    l.sort(reverse)
    for i,(val,k) in enumerate(l):
        tree.move(k,'',i)
        print(k)
    tree.heading(col,command=lambda:treesort(remtree,col,True))
def gui_main(root:Tk):
    '''主窗口
root(Tk):bss根窗口'''
    scmain = Toplevel(root)
    scmain.title('生词管理')

    #记忆模块生词
    screm = LabelFrame(scmain,text='记忆模块');screm.pack()
    rembtns = Frame(screm);rembtns.pack()
    Button(rembtns,text='立即复习',command=lambda:review(scmain,'remember')).grid()
    Button(rembtns,text='导入',command=lambda:imp(remlst)).grid(row=0,column=1)
    Button(rembtns,text='导出',command=lambda:exp(remlst)).grid(row=0,column=2)
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
    Button(lisbtns,text='导入',command=lambda:imp(lislst)).grid(row=0,column=1)
    Button(lisbtns,text='导出',command=lambda:exp(lislst)).grid(row=0,column=2)
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
    Button(wribtns,text='导入',command=lambda:imp(wrilst)).grid(row=0,column=1)
    Button(wribtns,text='导出',command=lambda:exp(wrilst)).grid(row=0,column=2)
    writree = ttk.Treeview(scwri,columns=('音标','词义','学习次数','错误次数','记忆强度','复习时间'));writree.pack()

    writree.heading('音标',text='音标',command=lambda:treesort(writree,'音标',False))
    writree.heading('词义',text='词义',command=lambda:treesort(writree,'音标',False))
    writree.heading('学习次数',text='学习次数',command=lambda:treesort(writree,'音标',False))
    writree.heading('错误次数',text='错误次数',command=lambda:treesort(writree,'音标',False))
    writree.heading('记忆强度',text='记忆强度',command=lambda:treesort(writree,'音标',False))
    writree.heading('复习时间',text='复习时间',command=lambda:treesort(writree,'音标',False))

    return (scmain,remtree,listree,writree)
def reviewtime(obj:Sc):
    '''计算到该单词复习时刻的时间
obj(Sc):生词对象'''
    if obj.review <= time.time():
        return '0'
    sec = obj.review-time.time()
    timeobj = time.localtime(sec)
    timelst = time.strftime('%m,%d,%H,%M,%S',timeobj).split(',')
    timelst[0] = str(int(timelst[0])-1);timelst[1] = str(int(timelst[1])-1) #to solve problem `Jan 1'
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
def deltatime(word:Sc):
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
        raise ValueError('值超出范围')
def mark(word:libwordclass.Word,lst:list):
    '''将单词标记为生词
word(libwordclass.Word):要标记的单词对象
lst:要存入的列表'''
    for i in lst:
        if word == i:
            i.learn += 1
            i.wrong += 1
            return
    sc = Sc(word.word,word.pronounce,word.trans,1,1,int(time.time()))
    lst.append(sc)
def review(scmain:Tk,sctype:str):
    '''生词复习及处理
scmain(tkinter.Tk):生词管理窗口
sclst(list):要复习的单词列表
lst(list):该类型的生词列表
sctype(str:remember/listen/write):生词类型名称，用于调用libgui的函数'''
    #获取对应列表
    if sctype == 'remember':
        lst = remlst
    elif sctype == 'listen':
        lst = lislst
    else:
        lst = wrilst
    #分出需要复习的词
    sclst = []
    for i in lst:
        if i.review <= time.time():
            sclst.append(i)
    #复习生词
    relst = eval(f'libgui.{sctype}')(scmain,sclst)
    #处理生词
    olst = liblist.other(relst,sclst)
    for i in olst:
        i.learn += 1
        i.review = int(time.time()+deltatime(i))
    for i in relst:
        i.learn += 1
        i.wrong += 1
        i.review = int(time.time()+deltatime(i))
    #删除熟记生词
    for i in sclst:
        if i.strenth() > 0.95:
            lst.remove(i)
"""def savefile():
    '''将生词列表保存到文件'''
    dic = shelve.open(FN)
    dic['rem'] = remlst
    dic['lis'] = lislst
    dic['wri'] = wrilst
    dic.close()"""
def savefile():
    '''将生词列表保存到文件'''
    for i in ('rem','lis','wri'):
        lst = eval(f'{i}lst')
        fn = os.path.join(libfile.getpath('scdir'),f'{i}.csv')
        libfile.saveascsv(lst,fn)
def control(root):
    '''生词模块主控
root(tkinter.Tk):主窗口'''
    scmain,*trees = gui_main(root)
    intree(*trees)
