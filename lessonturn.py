#Copyright Bail 2021
#bssenglish:lessonturn 课程文件转换 v1.0_1
#2021.8.12

import os

fn = input('要转换的文件 >')
slst = []
with open(fn) as file:
    for i in file.readlines():
        lst = i.split()
        lst.insert(1,'(暂无音标)')
        s = ' '.join(lst)
        slst.append(s)
os.rename(fn,f'{fn}.bak')
with open(fn,'w') as file:
    for i in slst:
        file.write(f'{i}\n')

