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
Reference :
"""

import re
from simhash import Simhash, SimhashIndex
import time, os
from data_operation.function import standardize_text_similarity
from  data_operation.excel_operate import OperateExcel
import pickle

def get_features(s):
    width = 4
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


def get_similarity_list(judged_sentence: str):
    pass
    datas = get_datas()
    if bool(datas):  #非空
        index = get_indexs()
        s1 = Simhash(get_features(judged_sentence))

        # index.add(excel_name, s1)
        return index.get_near_dups(s1)
    else:
        return []


def get_datas():
    pass
    try:
        with open(r'.\data\objs.txt', 'rb') as f1:
            data_dict = pickle.load(f1)
            return data_dict
    except EOFError:
        return []


def get_indexs():
    with open(r'.\data\index.txt', 'rb') as f2:
        indexs = pickle.load(f2)
        return indexs


def update_datas(content, excel_name):

    obj_list = get_datas()  # 获取当前词典
    print(obj_list, '$$$$$$$$$$$')
    print('14903)-原始需求导出 - 副本.xlsx' in obj_list, '$$$$$$$$$$$')

    if i in obj_list:
        # 注意excel_name 可能存在名称一样， 内容不一样
        if excel_name in i:
            excel_name += '(重名)'

    a = {}
    a[excel_name] = content
    obj_a = [(str(k), Simhash(get_features(v))) for k, v in a.items()]
    obj_list.append(obj_a[0])
    f3 = open(r'.\data\objs.txt', 'wb')  # 覆盖写入
    pickle.dump(obj_list, f3)
    f3.close()
    print(f'添加：{excel_name}!!!!')

    update_indexs(obj_list)


def update_indexs(obj_list, k0=10):  # 更新datas同时更新索引
    pass
    print(obj_list, '!!!!!!!!!')
    objs = obj_list
    print(objs, type(objs), len(objs), '~~~~~~~~~')
    index = SimhashIndex(objs, k=k0)  # k是容忍度；k越大，检索出的相似文本就越多
    with open(r'.\data\index.txt', 'wb') as f4:
        pickle.dump(index, f4)


if __name__ == "__main__":
    filePath = r'D:\dufy\语料\different'
    filePath = r'D:\dufy\语料\test3'
    filePath = r'C:\Users\Administrator\Documents\Tencent Files\3007490756\FileRecv\100'

    file_names = os.listdir(filePath)

    time0 = time.time()
    similarity_dict = {}

    for i, name0 in enumerate(file_names):
        print(f'========进度：{i/len(file_names)}====用时：{time.time()-time0}s=========')
        print(name0, ': ')
        excel_i_path = filePath + '\\' + name0
        content_i = standardize_text_similarity(OperateExcel(excel_i_path).excel_content_all())

        if not content_i:
            print('空文本')
            continue

        similarity_lists_for_contentI = get_similarity_list(content_i)
        print(similarity_lists_for_contentI,'------------')
        if similarity_lists_for_contentI:  # 有相似
            print(f'相似文本：{similarity_lists_for_contentI}')
            similarity_dict[name0] = similarity_lists_for_contentI

        else:
            update_datas(content_i, name0)

    print('相似组数：', len(similarity_dict), similarity_dict)

