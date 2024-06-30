#Copyright Bail 2023
#bssenglish:libnetwork 网络模块

APISOURCE = 'https://bailplus.github.io/bssenglish.pages/api/'

import requests,libfile,os,webbrowser,asyncio,edge_tts

async def run_tts(text:str,output:str,voice:str='en-US-JennyNeural'):
    '''调用tts获取音频
text(str):需要转语音的文本
output(str):输出文件路径
voice(str):音色，详见下述文档
--------------
特别鸣谢：edge-tts项目
项目地址：https://github.com/rany2/edge-tts/
(非官方)文档地址：https://www.bingal.com/posts/edge-tts-usage/'''
    await edge_tts.Communicate(text,voice).save(output)
def getaudio(word:str):
    '''获取音频并下载
word(str):单词'''
    path = os.path.join(libfile.getpath('audio'),f'{word}.mp3')
    asyncio.run(run_tts(word,path))
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
