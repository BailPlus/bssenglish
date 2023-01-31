#Copyright Bail 2023
#bssenglish:libnetwork 网络模块

APISOURCE = 'https://bailplus.github.io/bssenglish.pages/api/'

import requests,libfile,os,webbrowser

'''https://tts.baidu.com/text2audio?cuid=baike&lan=en&ctp=1&pdt=301&vol="+vol+"&rate=32&spd="+spd+"&per="+per+"&tex="+a
spd 语速 default:5
per 语调 1-6 default:4
vol 音量 5
a 文本内容'''
'https://fanyi.sogou.com/reventondc/synthesis?text=hello&speed=1&lang=en&from=translateweb&speaker=1'
'https://dlweb.sogoucdn.com/phonetic/{word}DELIMITER_us_1.mp3'

"""def getaudio(word:str,lan:str='en',spd:int=5,per:int=1,vol:int=5)->str:
    '''获取音频并下载（百度tts引擎，已失效）
word(str):单词
lan(str):语种（zh,en,jp,...）
spd(int):语速
per(int:1-6):语调
vol(int):音量
返回值:音频文件路径(str)'''
    PATH = os.path.join(libfile.getpath('audio'),f'{word}.mp3')
    url = 'https://tts.baidu.com/text2audio'
    params = {'cuid':'baike',
              'lan':lan,
              'ctp':1,
              'pdt':301,
              'vol':vol,
              'rate':32,
              'spd':spd,
              'per':per,
              'text':word,
              'ie':'utf-8'}
    #访问
    response = requests.get(url,params=params,timeout=5)
    #存储
    with open(PATH,'wb') as file:
       file.write(response.content)"""
def getaudio1(word:str,lan:str='en',spd:int=1)->str:
    '''获取音频并下载（搜狗tts引擎）
word(str):单词
lan(str):语种（zh,en,jp,...）
spd(int):语速
per(int:1-6):语调
vol(int):音量
返回值:音频文件路径(str)'''
    PATH = os.path.join(libfile.getpath('audio'),f'{word}.mp3')
    url = 'https://fanyi.sogou.com/reventondc/synthesis'
    params = {'lang':lan,
              'speed':spd,
              'text':word,
              'ie':'utf-8'}
    #访问
    response = requests.get(url,params=params,timeout=5)
    #存储
    with open(PATH,'wb') as file:
       file.write(response.content)
def getaudio2(word:str):
    '''获取音频并下载（搜狗美式发音）
word(str):单词
返回值:音频文件路径(str)'''
    PATH = os.path.join(libfile.getpath('audio'),f'{word}.mp3')
    url = f'https://dlweb.sogoucdn.com/phonetic/{word}DELIMITER_us_1.mp3'
    #访问
    response = requests.get(url,timeout=5)
    #查错
    if b'<html>' in response.content:
        getaudio1(word)
        return
    #存储
    with open(PATH,'wb') as file:
       file.write(response.content)
def open_browser_to_fetch_lessons(url='https://bailplus.github.io/bssenglish.pages/lessons'):
    '''使用浏览器打开“获取课程”界面
url(str):要打开的网址'''
    webbrowser.open(url)
def get_text_api(url:str,timeout:int=3)->str:
    '''获取文字类型api（若超时，请自行处理）
url(str):api地址
timeout(int):超时秒数
返回值：api结果(str)'''
    res = requests.get(url,timeout=timeout).text
    return res
