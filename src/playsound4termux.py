#/usr/bin/python3
#Copyright Bail 2024
#playsound4termux 针对termux的playsound模块 v1.0_1
#2024.7.29

import sys,os

def playsound(fn:str):
    '''播放声音
fn(str):声音文件名称'''
    os.system(f'termux-media-player play "{fn}"')
def main():
    fn = sys.argv[1]
    playsound(fn)
    return 0

if __name__ == '__main__':
    sys.exit(main())
