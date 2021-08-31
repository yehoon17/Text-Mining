# -*- coding: utf-8 -*-

import yaml
import json
import re

with open("config.yaml", "r", encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

load_dir = config["load_dir"]
preprocessing = config["preprocessing"]
word_num = config["word_num"]
word_order = config["word_order"]

def preprocess_text(text):
    # Split text to sentences by [!], [?], [.]
    sentences = re.split("[!?.]",text.strip())

    # Preprocess by option
    # 1: Remove special char, 2: Remove all except Kor
    if preprocessing == 1:
        sentences = [re.sub("[^A-Za-z0-9ㄱ-ㅎ가-힣\s]+","",sentence) for sentence in sentences]
    elif preprocessing == 2:
        sentences = [re.sub("[^ㄱ-ㅎ가-힣\s]+","",sentence) for sentence in sentences]

    # Split sentences by space
    preprocessed_text = []
    for sentence in sentences:
        preprocessed_text.append(re.split("\s",sentence.strip()))

    return preprocessed_text

def main():
    data = []

    with open(load_dir) as f:
        for obj in f:
            data.append(json.loads(obj))

    


if __name__ == "__main__":
    main()

