# -*- coding: utf-8 -*-


def normalize(dic, scale=1, digits=0):
    max_val = max(dic.values())
    min_val = min(dic.values())

    normalized_dic = []
    for key, val in dic.items():
        normalized_val = (val - min_val) / (max_val - min_val)
        normalized_dic.append(round(normalized_val * scale, digits))

    return normalized_dic