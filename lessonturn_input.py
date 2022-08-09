#Copyright Bail 2022
#bssenglish:lessonturn:input 课程文件转换从输入 v1.0.0.4_5
#2022.8.1

import sys,os

if len(sys.argv) == 1:
    fn = input('要转换的文件 >')
else:
    fn = sys.argv[1]
slst = []
with open(fn) as file:
    for i in file.readlines():
        lst = i.split('\t')
        lst.insert(1,'(暂无音标)')
        s = '\t'.join(lst)
        slst.append(s)
os.rename(fn,f'{fn}.bak')
with open(fn,'w') as file:
    file.write('file_version=3\n')
    for i in slst:
        file.write(f'{i}')
