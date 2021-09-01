# -*- coding: utf-8 -*-

from collections import Counter
from math import log


class TfIdfCalculator:
    def __init__(self):
        self.tf = []
        self.df = Counter()
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
        idf = {}
        self.words = set(self.df.elements())
        for word in self.words:
            idf[word] = log(size / (1 + self.df[word]))

        # calculate tf-idf
        for counter in self.tf:
            temp = {}
            for word in set(counter.elements()):
                temp[word] = counter[word] * idf[word]
            self.tfidf.append(temp)
        
        return self.tfidf

    def get_tf(self, n):
        total_tf = Counter()
        for counter in self.tf:
            total_tf.update(counter)

        return total_tf.most_common(n)
