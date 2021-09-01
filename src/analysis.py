# -*- coding: utf-8 -*-

import os
import heapq


def analysis(doc_ids, scores, calculator, save_path=""):
    # 전체 문서에서 단어 개수 구하여 정렬하여 출력하기 (상위 100개)
    file_dir = os.path.join(save_path, "tf.txt")
    with open(file_dir, "w", encoding="utf-8") as f:
        f.write("\n".join("%s %s" % x 
                            for x in calculator.get_tf(100)))

    # 각 문서에 가장 많이 등장한 단어 정렬하기 출력하기(상위 100개)
    file_dir = os.path.join(save_path, "df.txt")
    with open(file_dir, "w", encoding="utf-8") as f:
        f.write("\n".join("%s %s" % x 
                            for x in calculator.df.most_common(100)))

    # 단어 스코어 상위 10개 기준으로 스코어 편차가 가장 많이 나는 문서 구하기
    file_dir = os.path.join(save_path, "diff.txt")
    with open(file_dir, "w", encoding="utf-8") as f:
        temp = sorted(zip(doc_ids, scores),
                      key=lambda x: deviation(x[1]),
                      reverse=True)
        f.write("\n".join("%0.1f %s" % (deviation(score), doc_id)
                           for doc_id, score in temp[:5]))

    # 스코어 100점이 가능 많은 문서대로 나열하기
    file_dir = os.path.join(save_path, "doc.txt")
    with open(file_dir, "w", encoding="utf-8") as f:
        temp = sorted(zip(doc_ids, scores),
                      key=lambda x: list(x[1].values()).count(100),
                      reverse=True)
        f.write("\n".join("%s %s" % (list(score.values()).count(100), doc_id)
                           for doc_id, score in temp))

    # 전체문서에서 단어 길이가 긴 순서대로 정렬하기(상위10개)
    file_dir = os.path.join(save_path, "long.txt")
    with open(file_dir, "w", encoding="utf-8") as f:
        f.write("\n".join(heapq.nlargest(10,
                                         calculator.words,
                                         key=lambda x: len(x))))

    # 전체문서에서 한글자 단어 출력하기
    file_dir = os.path.join(save_path, "one.txt")
    with open(file_dir, "w", encoding="utf-8") as f:
        f.write("\n".join([word 
                           for word in calculator.words 
                           if len(word) == 1]))

def deviation(score):
    temp = heapq.nlargest(10, list(score.values()))
    mean = sum(temp) / len(temp)
    dev = sum([abs(x-mean) for x in temp])

    return dev