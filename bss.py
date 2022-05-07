#!/usr/bin/python3
#coding:utf-8
#Copyright Bail 2021-2022
#bssenglish 白杉树背单词训练软件 v1.3.1_31
#2021.7.11-2022.4.3

'''
灵感来源:红杉树智能英语(http://www.hssenglish.com)
生词字典:{单词(str):生词对象(__main__.Sc)}
'''

from tkinter import Tk
import sys,os,libgui,libfile,libsc

def init():
    '''初始化'''
    if not libfile.INSTALLED and not os.path.exists('lessons'):
        __import__('init').main()
    if libfile.INSTALLED and not os.path.exists(libfile.getpath('lessons')):
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
def main():
    init()
    loadplugins()
    libsc.readfile()
    root = libgui.root()
    files = libfile.getfile()
    libgui.inroot(root,files)
    root.mainloop()
    libsc.savefile()
    return 0

if __name__ == '__main__':
    sys.exit(main())
