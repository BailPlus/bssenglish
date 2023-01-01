#Copyright Bail 2021-2023
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
class Sc(Word):
    '''生词类 继承于:单词类'''
##    learn = wrong = 1	#学习1次，错误1次
    def __init__(self,word:str,pro:str,trans:str,learn:int,wrong:int,review:int):
        '''word(str):单词
pro(str):音标
trans(str):词义
review(int※不可为float):复习时间戳'''
        self.word = word
        self.pronounce = pro
        self.trans = trans
        self.learn = int(learn)
        self.wrong = int(wrong)
        self.review = int(review)
    def strenth(self):
        '''用于计算记忆强度
word(Sc):生词对象
返回值:记忆强度(float:.2f)'''
        return round((self.learn - self.wrong)/self.learn,2)
    def items(self):
        return [self.word,self.pronounce,self.trans,
                self.learn,self.wrong,self.review]
