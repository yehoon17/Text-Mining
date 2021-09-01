# -*- coding: utf-8 -*-

import yaml
import json
import os
from src.preprocess import preprocess
from src.tfidf import TfIdfCalculator
from src.normalization import normalize

# load configuration
with open("config.yaml", "r", encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# set configuration variables
load_dir = config["load_dir"]
save_dir = config["save_dir"]
fields = config["fields"]
preprocessing = config["preprocessing"]
word_num = config["word_num"]
word_order = config["word_order"]


# get score 
def get_result(doc_id, score):
    result = {}
    
    result["DOCID"] = doc_id
    score_li = [[key, val] for key, val in score.items()]

    # 단어 출력 방법
    # 1: 단어 점수 기준 내림차순, 2: 단어 글자 기준 오름차순
    if word_order == 1:
        score_li.sort(key=lambda x:x[1], reverse=True)
    elif word_order == 2:
        score_li.sord(key=lambda x:x[0])

    # 단어 출력 개수: 0 ~ N
    # 0으로 설정할 시 모든 단어 출력
    n = len(score) if word_num == 0 else word_num

    score_strs = []
    for i in range(n):
        if i == len(score_li):
            break
        key, val = score_li[i]
        score_str = "^".join([key,str(val)])
        score_strs.append(score_str)
    result["KEYWORD"] = " ".join(score_strs)
        
    return result

def main():
    # load document data
    print("loading data...")
    texts = []
    doc_ids = []
    with open(load_dir, encoding="utf-8") as f:
        for obj in f:
            data = json.loads(obj)
            text = ""
            for field in fields:
                text += data[field]
            texts.append(text)
            doc_ids.append(data["doc_id"])

    print("data loaded")
    print("doc_id:", doc_ids[0])
    print(texts[0])

    # preprocess data
    print("preprocessing data...")
    documents = []
    for text in texts:
        documents.append(preprocess(text,
                                    preprocessing,
                                    split_sentences=False))

    # calculate idf
    print("calculating idf...")
    calculator = TfIdfCalculator()
    tfidf = calculator.get_tfidf(documents)

    # get scores 
    print("calculating scores...")
    scores = []
    for dic in tfidf:
        normalized_tfidf = normalize(dic, 100)
        scores.append(normalized_tfidf)

    # export result
    print("exporting result...")

    with open(save_dir, "w", encoding="utf-8") as json_file:
        for doc_id, score in zip(doc_ids, scores):
            result = get_result(doc_id, score)
            json_file.write(json.dumps(result, ensure_ascii=False) + "\n")
    print("complete\n")

    # analysis
    print("start analysis")
    save_path = "result"
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
        pass

    # 스코어 100점이 가능 많은 문서대로 나열하기
    file_dir = os.path.join(save_path, "doc.txt")
    with open(file_dir, "w", encoding="utf-8") as f:
        pass

    # 전체문서에서 단어 길이가 긴 순서대로 정렬하기(상위10개)
    file_dir = os.path.join(save_path, "long.txt")
    with open(file_dir, "w", encoding="utf-8") as f:
        pass

    # 전체문서에서 한글자 단어 출력하기
    file_dir = os.path.join(save_path, "one.txt")
    with open(file_dir, "w", encoding="utf-8") as f:
        pass


if __name__ == "__main__":
    main()

