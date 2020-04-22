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
from data_operation.excel_operate import OperateExcel
import pickle


def get_features(s):
    width = 4
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


def get_similarity_list(judged_sentence: str):
    pass
    try:
        obj_list = get_objs()  # 获取当前词典
        index = SimhashIndex(obj_list, k=10)  # k是容忍度；k越大，检索出的相似文本就越多
        s1 = Simhash(get_features(judged_sentence))
        return index.get_near_dups(s1)
    except EOFError:
        return []


def get_objs():
    try:
        with open(r'.\data\objs.txt', 'rb') as f1:
            objs_list = pickle.load(f1)
            return objs_list
    except EOFError:
        return []


def update_objs(content, excel_name):
    objs_list = get_objs()  # 获取当前词典

    if i in objs_list:  # 注意excel_name 可能存在名称一样， 内容不一样
        if excel_name in i:
            excel_name += '(重名)'

    to_add_data = {}  # 待更新数据
    to_add_data[excel_name] = content
    obj_i = [(str(k), Simhash(get_features(v))) for k, v in to_add_data.items()]
    objs_list.append(obj_i[0])

    f3 = open(r'.\data\objs.txt', 'wb')  # 覆盖写入
    pickle.dump(objs_list, f3)
    f3.close()
    print(f'添加：{excel_name}!!!!')


if __name__ == "__main__":
    filePath = r'D:\dufy\语料\different'
    # filePath = r'D:\dufy\语料\test3'
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

        similarity_lists_for_contentI = get_similarity_list(content_i)

        if similarity_lists_for_contentI:  # 有相似
            print(f'相似文本：{similarity_lists_for_contentI}')
            similarity_dict[name0] = similarity_lists_for_contentI
        else:
            update_objs(content_i, name0)

    print('相似组数：', len(similarity_dict), similarity_dict)

