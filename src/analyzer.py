# -*- coding: utf-8 -*-

import os
from heapq import nlargest


class DocumentAnalyzer:
    def __init__(self, analysis_option: dict, save_path: str):
        self.analysis_option = analysis_option
        self.save_path = save_path

    def analyze(self, calculator, doc_ids, scores):
        if self.analysis_option["tf_top_100"]:
            self.tf_top_100(calculator)

        if self.analysis_option["df_top_100"]:
            self.df_top_100(calculator)

        if self.analysis_option["tfidf_deviation_doc"]:
            self.tfidf_deviation_doc(doc_ids, scores)

        if self.analysis_option["sort_by_score_100"]:
            self.sort_by_score_100(doc_ids, scores)

        if self.analysis_option["longest_word_top_10"]:
            self.longest_word_top_10(calculator)

        if self.analysis_option["length_one_words"]:
            self.length_one_words(calculator)

    def tf_top_100(self, calculator):
        # 전체 문서에서 단어 개수 구하여 정렬하여 출력하기 (상위 100개)
        file_dir = os.path.join(self.save_path, "tf.txt")

        with open(file_dir, "w", encoding="utf-8") as f:
            f.write("\n".join("%s %s" % x 
                                for x in calculator.get_tf(100)))

    def df_top_100(self, calculator):
        # 각 문서에 가장 많이 등장한 단어 정렬하기 출력하기(상위 100개)
        file_dir = os.path.join(self.save_path, "df.txt")

        with open(file_dir, "w", encoding="utf-8") as f:
            f.write("\n".join("%s %s" % x 
                                for x in calculator.df.most_common(100)))

    def tfidf_deviation_doc(self, doc_ids, scores):
        # 문서별 단어 스코어 상위 10개 기준으로 가장 높은 스코어 편차 구하기
        file_dir = os.path.join(self.save_path, "diff.txt")

        with open(file_dir, "w", encoding="utf-8") as f:
            for doc_id, score in zip(doc_ids, scores):
                top_10 = nlargest(10, score.items(), key=lambda x:x[1])
                max_word = top_10[0][0]
                max_score = top_10[0][1]
                min_word = top_10[-1][0]
                min_score = top_10[-1][1]
                deviation = max_score - min_score
                f.write(f"{deviation} {max_word}:{max_score} {min_word}:{min_score} {doc_id}\n")        

    def sort_by_score_100(self, doc_ids, scores):
        # 스코어 100점이 가능 많은 문서대로 나열하기
        file_dir = os.path.join(self.save_path, "doc.txt")

        with open(file_dir, "w", encoding="utf-8") as f:
            sorted_doc = sorted(zip(doc_ids, scores),
                                key=lambda x: list(x[1].values()).count(100),
                                reverse=True)
            f.write("\n".join("%s %s" % (list(score.values()).count(100), doc_id)
                            for doc_id, score in sorted_doc))

    def longest_word_top_10(self, calculator):
        # 전체문서에서 단어 길이가 긴 순서대로 정렬하기(상위10개)
        file_dir = os.path.join(self.save_path, "long.txt")

        with open(file_dir, "w", encoding="utf-8") as f:
            f.write("\n".join(nlargest(10,
                              calculator.words,
                              key=lambda x: len(x))))

    def length_one_words(self, calculator):
        # 전체문서에서 한글자 단어 출력하기
        file_dir = os.path.join(self.save_path, "one.txt")

        with open(file_dir, "w", encoding="utf-8") as f:
            f.write("\n".join([word 
                            for word in calculator.words 
                            if len(word) == 1]))
