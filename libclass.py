#Copyright Bail 2021
#bssenglish:libwordclass 单词类模块

class Word:
    def __init__(self,word:str,pronounce:str,trans:str):
        self.word = word
        self.pronounce = pronounce
        self.trans = trans
    def __str__(self)->str:
        return self.word
    def __eq__(self,b):
        if self.word == b.word:
            return True
        else:
            return False

