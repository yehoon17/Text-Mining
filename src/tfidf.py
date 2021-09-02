# -*- coding: utf-8 -*-

from collections import Counter
from math import log


class TfIdfCalculator:
    def __init__(self):
        self.tf = []
        self.df = Counter()
        self.idf = []
        self.tfidf = []
        self.words = None

    def get_tfidf(self, documents):
        # size: number of documents
        size = len(documents)

        # get term frequency for each document
        for document in documents:
            self.tf.append(Counter(document))
        
        # get document frequency
        for counter in self.tf:
            self.df.update(set(counter.elements()))

        # get inverse document frequenct
        self.idf = self.get_idf(size)

        # calculate tf-idf
        self.cal_tfidf()
        
        return self.tfidf

    def get_idf(self, size):
        idf = {}
        self.words = set(self.df.elements())
        for word in self.words:
            idf[word] = log(size / (1 + self.df[word]))

        return idf

    def cal_tfidf(self):
        for counter in self.tf:
            tfidf = {}
            for word in set(counter.elements()):
                tfidf[word] = counter[word] * self.idf[word]
            self.tfidf.append(tfidf)

    def get_tf(self, n):
        total_tf = Counter()
        for counter in self.tf:
            total_tf.update(counter)

        return total_tf.most_common(n)
