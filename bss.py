#!/usr/bin/python3
#coding:utf-8
#Copyright Bail 2021
#bssenglish 白杉树背单词训练软件 v1.0_1
#2021.7.11-2021.10.30

'''
灵感来源:红杉树智能英语(http://www.hssenglish.com)
生词字典:{单词(str):生词对象(__main__.Sc)}
'''

from tkinter import Tk
import sys,os,libgui,libfile,libsc,init

def learnctrl(root:Tk,wlst:list,sctype:str):
    sclst = eval(f'libgui.{sctype}')(root,wlst)
    for i in sclst:
        sc.mark(i,eval(f'sc.{sctype[:3]}lst'))
def main():
    if not libfile.INSTALLED and not os.path.exists('audio'):
        init.main()
    libsc.readfile()
    root = libgui.root()
    files = libfile.getfile()
    libgui.inroot(root,files)
    root.mainloop()
    libsc.savefile()
    return 0

if __name__ == '__main__':
    sys.exit(main())
