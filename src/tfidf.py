# -*- coding: utf-8 -*-

import numpy as np
from math import log


class TfIdfVectorizer:
    def __init__(self):
        self.words = []
        self.tf = {}
        self.idf = {}

    def fit(self, documents):        
        # size: number of documents
        size = len(documents)

        # words: list of all word in documents
        self.words = list(set([word for document in documents for word in document]))

        for word in self.words:
            self.idf[word] = inverse_document_frequency(documents, word, size)

    def transform(self, document):
        words = list(set(document))
        # term frequency
        tf = {word : document.count(word) for word in words}

        tfidf = {word : tf[word] * self.idf[word] for word in words}

        return tfidf


# get idf of a word
def inverse_document_frequency(documents, word, size):
    cnt = 0
    for document in documents:
        cnt += document.count(word)
    
    return log(size / (1 + cnt))
