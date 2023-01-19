#Copyright Bail 2023
#bssenglish:lessonturn:3to4 课程文件转换v3到v4 v1.0_1
#2023.1.19

import sys,os,libfile

if len(sys.argv) == 1:
    fn = input('要转换的文件 >')
else:
    fn = sys.argv[1]
os.rename(fn,f'{fn}.2bak')
with open(f'{fn}.blf','w') as file:
    file.write(libfile.LESSON_FILE_HEADER)
    file.write('{"name":"%s","fullname":"None","author":"None","file_version":4}\n' % fn)
    with open(f'{fn}.2bak') as origin_file:
        origin_file.readline()
        file.writelines(origin_file.readlines())
