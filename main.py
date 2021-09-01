# -*- coding: utf-8 -*-

import yaml
import json
from src.preprocess import preprocess
from src.tfidf import TfIdfCalculator
from src.normalization import normalize
from src.analysis import analysis

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
    analysis(calculator, save_path)


if __name__ == "__main__":
    main()

