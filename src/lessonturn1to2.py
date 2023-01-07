#Copyright Bail 2021-2022
#bssenglish:lessonturn:1to2 课程文件转换v1到v2 v1.0.2_3
#2021.8.12-2022.8.1

import sys,os

if len(sys.argv) == 1:
    fn = input('要转换的文件 >')
else:
    fn = sys.argv[1]
slst = []
with open(fn) as file:
    for i in file.readlines():
        lst = i.split()
        lst.insert(1,'(暂无音标)')
        s = ' '.join(lst)
        slst.append(s)
os.rename(fn,f'{fn}.1bak')
with open(fn,'w') as file:
    for i in slst:
        file.write(f'{i}\n')
