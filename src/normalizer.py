# -*- coding: utf-8 -*-

class Normalizer:
    def __init__(self, scale=1):
        self.scale = scale
        
    def normalize(self, dic, digits=0):
        max_val = max(dic.values())
        min_val = min(dic.values())

        normalized_dic = {}
        for key, val in dic.items():
            if max_val == min_val:
                normalized_val = 1
            else:
                normalized_val = (val - min_val) / (max_val - min_val)
            normalized_dic[key] = round(normalized_val * self.scale, digits)

        return normalized_dic