#Copyright Bail 2021-2023
#bssenglish:libaudio 音频模块
#2021.8.25


import os,libgui,playsound,libclass,libfile,libnetwork,threading

def download(root:libgui.Tk,lesson:libclass.Lesson):
    wlst = lesson.words
    files = os.listdir(libfile.getpath('audio'))
    update = libgui.download(root,len(wlst))
    try:
        for index,i in enumerate(wlst):
            if f'{i}.mp3' not in files:
                if ' ' in i.word:    #词组（搜狗tts引擎）
                    libnetwork.getaudio1(i.word)
                else:   #单词（搜狗美式发音）
                    libnetwork.getaudio2(i.word)
            update(index)
        update(index+1)
    except:
        libgui.msgbox.showerror('错误','无法下载，请检查网络连接',parent=root)
        raise
def play(word:libclass.Word):
    w = word.word
    path = os.path.join(libfile.getpath('audio'),f'{w}.mp3')
    if os.path.exists(path):
        threading.Thread(target=lambda:playsound.playsound(path)).start()

