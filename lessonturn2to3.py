#Copyright Bail 2022
#bssenglish:lessonturn:2to3 课程文件转换v2到v3 v1.0.0.1_2
#2022.6.21

import sys,os

if len(sys.argv) == 1:
    fn = input('要转换的文件 >')
else:
    fn = sys.argv[1]
slst = []
with open(fn) as file:
    s = file.read().replace(' ','\t')
    s = s.replace('_',' ')
os.rename(fn,f'{fn}.bak')
with open(fn,'w') as file:
    file.write('file_version=3\n'+s)

