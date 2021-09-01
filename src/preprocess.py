# -*- coding: utf-8 -*-

import re


class NotValidPreprocessError(Exception):
    def __init__(self):
        super().__init__("NotValidPreprocessError")


# preprocess text
def preprocess(text, preprocessing, split_sentences=True):
    if split_sentences:
        # Split text to sentences by [!], [?], [.]
        sentences = re.split("[!?.]", text.strip())

        # Preprocess by option
        # 1: Remove special char, 2: Remove all except Kor
        if preprocessing == 1:
            sentences = [re.sub("[^A-Za-z0-9ㄱ-ㅎ가-힣\s]+", "", sentence) 
            for sentence in sentences]
        elif preprocessing == 2:
            sentences = [re.sub("[^ㄱ-ㅎ가-힣\s]+", "", sentence)
            for sentence in sentences]
        else:
            raise NotValidPreprocessError

        # Split sentences by space
        preprocessed_text = []
        for sentence in sentences:
            preprocessed_text.append(re.split("\s", sentence.strip()))

    else:
        # Preprocess by option
        # 1: Remove special char, 2: Remove all except Kor
        if preprocessing == 1:
            text = re.sub("[^A-Za-z0-9ㄱ-ㅎ가-힣\s]+", "", text)
        elif preprocessing == 2:
            text = re.sub("[^ㄱ-ㅎ가-힣\s]+", "", text)
        else:
            raise NotValidPreprocessError

        # Split sentences by space
        preprocessed_text = text.strip().split()

    return preprocessed_text