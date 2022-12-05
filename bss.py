#!/usr/bin/python3
#coding:utf-8
#Copyright Bail 2021-2022
#bssenglish 白杉树背单词训练软件 v1.5.6_51
#2021.7.11-2022.12.5

'''
灵感来源:红杉树智能英语(http://www.hssenglish.com)
'''

from tkinter import Tk
import sys,os,libgui,libfile,libsc

def init():
    '''初始化'''
##    if not libfile.INSTALLED and not os.path.exists('lessons'):
##        __import__('init').main()
##    if libfile.INSTALLED and not os.path.exists(libfile.getpath('lessons')):
##        __import__('init').main()
    if not os.path.exists(libfile.getpath('lessons')):
        __import__('init').main()
def learnctrl(root:Tk,wlst:list,sctype:str):
    sclst = eval(f'libgui.{sctype}')(root,wlst)
    for i in sclst:
        libsc.mark(i,eval(f'libsc.{sctype[:3]}lst'))
    libsc.savefile()
def loadplugins():
    '''加载模块'''
    sys.path.append('.',)
    os.chdir(libfile.getpath('plugins'))
    for i in os.listdir('.'):
        pkgname = i.split('.')[0] #去掉后缀名
        __import__(pkgname)
def printe(*args,**kw):
    '''从stderr通道输出内容
与内置函数print用法相同'''
    # 为了后续版本的libcli从stdout输出，故将日志输出到stderr通道
    # 需要其他模块进行适配，将在后续版本完成
    print(file=sys.stderr,*args,**kw)
def main():
    init()
    loadplugins()
    libsc.readfile()
    root = libgui.root()
    libgui.init(root)
##    files = libfile.getfile()
##    libgui.inroot(root,files)
    root.mainloop()
    libsc.savefile()
    return 0

if __name__ == '__main__':
    sys.exit(main())
