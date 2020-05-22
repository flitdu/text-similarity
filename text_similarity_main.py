# -*- coding: utf-8 -*-
"""
@Time : 2020/4/14 16:22
@Author : Dufy
@Email : 813540660@qq.com
@File : text_similarity.py
@Software: PyCharm
Description :
1)文本相似度查询
2)超参数：width 与 k
Reference :  width 5 比 4,6 好
"""

import re
from simhash import Simhash, SimhashIndex
import time, os
from data_operation.function import standardize_text_similarity
from data_operation.excel_operate import OperateExcel
import pickle


def getFeatures(s):
    width = 5
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


def getSimilarityList(judged_sentence: str):
    pass
    try:
        obj_list = getObjs()
        index = SimhashIndex(obj_list, k=12)  # k是容忍度；k越大，检索出的相似文本就越多
        s1 = Simhash(getFeatures(judged_sentence))
        return index.get_near_dups(s1)
    except EOFError:
        return []


def getObjs():
    try:
        with open(r'.\data\objs.txt', 'rb') as f1:
            objs_list = pickle.load(f1)
            return objs_list
    except EOFError:
        return []


def updateObjs(content, excel_name):
    objs_list = getObjs()  # 获取当前词典

    if i in objs_list:  # 注意excel_name 可能存在名称一样， 内容不一样
        if excel_name in i:
            excel_name += '(重名)'

    to_add_data = {}  # 待更新数据
    to_add_data[excel_name] = content
    obj_i = [(str(k), Simhash(getFeatures(v))) for k, v in to_add_data.items()]
    objs_list.append(obj_i[0])

    f3 = open(r'.\data\objs.txt', 'wb')  # 覆盖写入
    pickle.dump(objs_list, f3)
    f3.close()
    print(f'添加：{excel_name}!!!!')


if __name__ == "__main__":
    # 先清空objs.txt 内容，参数调整使用
    f_train = open(r'.\data\objs.txt', 'w')
    f_train.truncate()
    f_train.close() # 注：在正式环境下不能采用

    filePath = r'D:\dufy\语料\different'
    filePath = r'D:\dufy\语料\test3'
    # filePath = r'C:\Users\Administrator\Documents\Tencent Files\3007490756\FileRecv\100'

    file_names = os.listdir(filePath)

    time0 = time.time()
    similarity_dict = {}

    for i, name0 in enumerate(file_names):
        print(f'========进度：{i/len(file_names)}====用时：{time.time()-time0}s=========')
        print(name0, ': ')
        excel_i_path = filePath + '\\' + name0
        if '~$' in excel_i_path:
            continue
        content_i = standardize_text_similarity(OperateExcel(excel_i_path).excel_content_all())

        if not content_i:
            print('空文本')
            continue

        similarity_lists_for_contentI = getSimilarityList(content_i)

        if similarity_lists_for_contentI:  # 有相似
            print(f'相似文本：{similarity_lists_for_contentI}')
            similarity_dict[name0] = similarity_lists_for_contentI
        else:
            updateObjs(content_i, name0)

    print('相似组数：', len(similarity_dict), similarity_dict)

