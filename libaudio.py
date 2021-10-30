#Copyright Bail 2021
#bssenglish:libaudio 音频模块
#2021.8.25

'''https://tts.baidu.com/text2audio?cuid=baike&lan=en&ctp=1&pdt=301&vol="+vol+"&rate=32&spd="+spd+"&per="+per+"&tex="+a
spd 语速 default:5
per 语调 1-6 default:4
vol 音量 5
a 文本内容'''

import requests,os,libgui,tqdm,playsound,libwordclass,libfile

def getaudio(word:str,lan:str='en',spd:int=5,per:int=1,vol:int=5)->str:
    '''获取音频并下载
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
       file.write(response.content)
def download(root:libgui.Tk,wlst:list):
    files = os.listdir(libfile.getpath('audio'))
    barlst = tqdm.tqdm(wlst)
    update = libgui.download(root,len(wlst))
    try:
        for index,i in enumerate(barlst):
            if f'{i}.mp3' not in files:
                barlst.set_description(f'下载中:{i}')
                getaudio(i.word)
            update(index)
    except:
        libgui.msgbox.showerror('错误','无法下载，请检查网络连接',parent=root)
        raise
def play(word:libwordclass.Word):
    w = word.word
    path = os.path.join(libfile.getpath('audio'),f'{w}.mp3')
    if os.path.exists(path):
        playsound.playsound(path)

