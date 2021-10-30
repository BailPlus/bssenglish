def other(lst:list,ulst:list):
    '''对一个列表取补集
lst(list):要取补集的列表
ulst(list):列表全集
返回值:此列表的补集(list)'''
    olst = []
    for i in ulst:
        if i not in lst:
            olst.append(i)
    return olst
