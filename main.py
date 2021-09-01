# -*- coding: utf-8 -*-

import yaml
import json
import numpy as np
from src.preprocess import preprocess
from src.tfidf import TfIdfVectorizer
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
def get_result(doc_ids, scores):
    result = {}
    
    for doc_id, score in zip(doc_ids, scores):
        result["DOCID"] = doc_id
        score_strs = []
        for key, val in score.items():
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
    vectorizer = TfIdfVectorizer()
    vectorizer.fit(documents)

    # get scores 
    print("calculating scores")
    scores = []
    for document in documents:
        tfidf = vectorizer.transform(document)
        normalized_tfidf = normalize(tfidf)
        scores.append(normalized_tfidf)

    # export result
    print("exporting result...")
    result = get_result(doc_ids, scores)

    with open(save_dir, "w", encoding="utf-8") as json_file:
        json.dump(result, json_file)

    # analysis
    pass


if __name__ == "__main__":
    main()

