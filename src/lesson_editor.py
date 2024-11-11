#!/usr/bin/python3
#Copyright Bail 2024
#bssenglish:lesson_editor 课程文件编辑器 v1.0_1
#2024.7.19-2024.7.22

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import libfile,libclass,json,sys,traceback,os

def add(word:libclass.Word=None):
    '''添加单词条目'''
    row = len(word_entry_lst)
    wordent = Entry(words_frame);wordent.grid(row=row,column=0)
    pronent = Entry(words_frame);pronent.grid(row=row,column=1)
    tranent = Entry(words_frame);tranent.grid(row=row,column=2)
    delbtn = Button(words_frame,text='-');delbtn.grid(row=row,column=3)
    c.yview_moveto(1)   # 滚动到底部
    if word:
        wordent.insert(0,word.word)
        pronent.insert(0,word.pronounce)
        tranent.insert(0,word.trans)
    tup = (wordent,pronent,tranent,delbtn)
    delbtn.config(command=lambda:delete(tup))
    word_entry_lst.append(tup)
def delete(tup:tuple):
    '''删除单词条目
tup(tuple):包含单词条目所有控件的元组'''
    for i in tup:
        i.grid_forget()
    word_entry_lst.remove(tup)
def openfile():
    global filename
    if word_entry_lst:  # 编辑器中有内容
        if messagebox.askyesno('警告','此操作将会清空编辑器中的所有内容，是否继续？',parent=root):
            for i in range(len(word_entry_lst)):
                delete(word_entry_lst[0])
            name_entry.delete(0,END)
            fullname_entry.delete(0,END)
            author_entry.delete(0,END)
        else:   # 用户不同意
            return
    if not filename:
        filename = filedialog.askopenfilename(parent=root,title='打开')
        if libfile.islessonfile(filename):
            # 先创建进度文件
            progress_file_name = os.path.join(libfile.path['progress'],libfile.get_file_md5(filename))
            if not os.path.exists(progress_file_name):
                with open(progress_file_name,'w') as file:
                    file.write('0\n0\n0')
            try:
                lesson = libfile.readfile(filename)
            except libclass.WrongFileVersion as e:
                messagebox.showerror('文件错误',f'文件版本错误: {e}')
                filename = None
                return
            except Exception:
                messagebox.showerror('文件错误',f'"{filename}"课程文件已损坏')
                traceback.print_exc()
                filename = None
                return
        else:
            messagebox.showerror('文件错误',f'"{filename}"不是课程文件')
            filename = None
            return
    filename_label.config(text=f'当前文件：{filename}')
    name_entry.insert(0,lesson.name)
    fullname_entry.insert(0,lesson.fullname)
    author_entry.insert(0,lesson.author)
    for i in lesson.words:
        add(i)
def save(issaveas:bool=False):
    '''保存文件
issaveas(bool):是否为另存为模式'''
    global filename
    if (issaveas) or (not filename):
        filename = filedialog.asksaveasfilename(parent=root,title='另存为')
    info = {
        'name':name_entry.get(),
        'fullname':fullname_entry.get(),
        'author':author_entry.get(),
        'file_version':4
    }
    words = []
    for i in word_entry_lst:
        word = '\t'.join((j.get() for j in i[:3]))
        words.append(word)
    with open(filename,'w',encoding='utf-8') as file:
        file.write(libfile.LESSON_FILE_HEADER)  # 文件头
        file.write(json.dumps(info)+'\n')   # 信息头
        file.write('\n'.join(words))

word_entry_lst = [] # 所有单词条目
filename = None

# 配置界面
root = Tk()
root.title('课程文件编辑器')
root.bind_all('<Return>',lambda _:add())
filename_frame = Frame(root);filename_frame.pack()   # 界面第一行
filename_label = Label(filename_frame,text=f'当前文件：{filename}')
filename_label.grid(row=0,column=0)
Button(filename_frame,text='打开',command=openfile).grid(row=0,column=1)
Button(filename_frame,text='保存',command=save).grid(row=0,column=2)
Button(filename_frame,text='另存为',command=lambda:save(True)).grid(row=0,column=3)
lessoninfo_frame = Frame(root);lessoninfo_frame.pack()  # 课程基本信息
Label(lessoninfo_frame,text='简称').grid(row=1,column=0)
name_entry = Entry(lessoninfo_frame)
name_entry.grid(row=1,column=1)
Label(lessoninfo_frame,text='全称').grid(row=2,column=0)
fullname_entry = Entry(lessoninfo_frame)
fullname_entry.grid(row=2,column=1)
Label(lessoninfo_frame,text='作者').grid(row=3,column=0)
author_entry = Entry(lessoninfo_frame)
author_entry.grid(row=3,column=1)
c = Canvas(root)    # 中间主体
c.pack(fill=BOTH,expand=True)
words_frame = Frame(c)
words_frame.pack()
c.create_window(0,0,window=words_frame)
bar = Scrollbar(c,orient=VERTICAL,command=c.yview)
bar.pack(side=RIGHT,fill=Y)
c.config(yscrollcommand=bar.set)
words_frame.bind_all('<Configure>',lambda _:c.config(scrollregion=c.bbox(ALL)))
'''鼠标滚轮适配参考文献:
https://www.codenong.com/17355902'''
c.bind_all('<Button-4>',lambda _:c.yview_scroll(-1,UNITS))  # linux鼠标上键
c.bind_all('<Button-5>',lambda _:c.yview_scroll(1,UNITS))   # linux鼠标下键
c.bind_all('<MouseWheel>',lambda e:c.yview_scroll(1,UNITS) if e.delta<0 else c.yview_scroll(-1,UNITS))  #windows/mac鼠标滚轮
Button(root,text='+',command=add).pack(side=BOTTOM)
# 处理参数
if len(sys.argv) == 2:
    filename = sys.argv[1]
    openfile()
root.mainloop()
