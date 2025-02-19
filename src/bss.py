#!/usr/bin/python3
#coding:utf-8
#Copyright Bail 2021-2025
#bssenglish 白杉树背单词训练软件 v2.2.5_79
#2021.7.11-2025.2.18

'''
灵感来源:红杉树智能英语(http://www.hssenglish.com)
'''

import sys,os
#按系统类型配置导入模块的目录
OSNAME = None   #备选:None,deepin,termux
OSNAME = OSNAME if OSNAME else os.name
if OSNAME in ('nt','deepin'):
    import_path = '.'
elif OSNAME in ('posix',):
    import_path = '/usr/lib/bssenglish'
elif OSNAME in ('termux',):
    import_path = '/data/data/com.termux/files/usr/lib/bssenglish'
else:
    raise EnvironmentError('系统不支持')
sys.path.append(import_path)
import libgui,libfile,libsc,init,libnotice

def loadplugins():
    '''加载模块'''
    sys.path.append(libfile.getpath('plugins'))
    os.chdir(libfile.getpath('plugins'))
    for i in os.listdir('.'):
        pkgname = os.path.splitext(i)[0] #去掉后缀名
        __import__(pkgname)
        print(f'I: 已加载模块: {pkgname}')
def printe(*args,**kw):
    '''从stderr通道输出内容
与内置函数print用法相同'''
    # 为了后续版本的libcli从stdout输出，故将日志输出到stderr通道
    # 需要其他模块进行适配，将在后续版本完成
    print(file=sys.stderr,*args,**kw)
def main():
    init.main()
    loadplugins()
    libsc.readfile()
    root = libgui.root()
    libnotice.process(root)
    lessonlst = libfile.getlessons()
    libgui.init(root,lessonlst)
##    files = libfile.getfile()
##    libgui.inroot(root,files)
    root.mainloop()
    libsc.savefile()
    libfile.saveprogress(lessonlst)
    return 0

if __name__ == '__main__':
    sys.exit(main())
