# -*- coding: utf-8 -*-

import yaml
import json
from src.preprocesser import Preprocesser
from src.tfidf import TfIdfCalculator
from src.normalizer import Normalizer
from src.analyzer import DocumentAnalyzer


class Config():
    def __init__(self):
        # load configuration
        try:
            with open("config.yaml", "r", encoding='utf-8') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
        except:
            print("config.yaml not found")

        # set configuration variables
        self.load_dir = config["load_dir"]
        self.save_dir = config["save_dir"]
        self.fields = config["fields"]
        self.preprocessing = config["preprocessing"]
        self.word_num = config["word_num"]
        self.word_order = config["word_order"]
        self.analysis_option = config["word_analysis"]


class KeywordExtractor():
    def __init__(self, conf):
        self.conf = conf
        self.texts = []
        self.doc_ids = []
        self.documents = []
        self.tfidf = []
        self.scores = []
        self.calculator = TfIdfCalculator()

    def extract(self):
        self.load_data()
        self.preprocess()
        self.calculate_tfidf()
        self.get_importance_scores()
        self.export_result()

    def load_data(self):
        # load document data
        try:
            with open(self.conf.load_dir, encoding="utf-8") as f:
                for obj in f:
                    data = json.loads(obj)
                    text = ""
                    for field in self.conf.fields:
                        text += data[field]
                    self.texts.append(text)
                    self.doc_ids.append(data["doc_id"])
        except:
            print("Failed to load data")

    def preprocess(self):
        preprocesser = Preprocesser(self.conf.preprocessing)
        # preprocess data
        for text in self.texts:
            self.documents.append(preprocesser.preprocess(text,
                                                          split_sentences=False))

    def calculate_tfidf(self):
        # calculate tfidf
        self.tfidf = self.calculator.get_tfidf(self.documents)
    
    def get_importance_scores(self):
        normalizer = Normalizer(100)
        # get importance scores 
        for dic in self.tfidf:
            if not dic:
                continue
            normalized_tfidf = normalizer.normalize(dic)
            self.scores.append(normalized_tfidf)
    
    def export_result(self):
        # export result
        with open(self.conf.save_dir, "w", encoding="utf-8") as json_file:
            for doc_id, score in zip(self.doc_ids, self.scores):
                line = self.score_to_json(doc_id, score)
                json_file.write(json.dumps(line, ensure_ascii=False) + "\n")
    
    def score_to_json(self, doc_id, score):
        result = {}
        
        result["DOCID"] = doc_id
        score_li = [[key, val] for key, val in score.items()]

        self.sort_score(score_li, self.conf.word_order)

        # 단어 출력 개수: 0 ~ N
        # 0으로 설정할 시 모든 단어 출력
        n = len(score) if self.conf.word_num == 0 else self.conf.word_num

        self.scores_to_string(n, score_li, result)
            
        return result

    def sort_score(self, score_li, word_order):
        # 단어 출력 방법
        # 1: 단어 점수 기준 내림차순, 2: 단어 글자 기준 오름차순
        if self.conf.word_order == 1:
            score_li.sort(key=lambda x:x[1], reverse=True)
        elif self.conf.word_order == 2:
            score_li.sord(key=lambda x:x[0])

    def scores_to_string(self, n, score_li, result):
        score_strs = []
        for i in range(n):
            if i == len(score_li):
                break
            key, val = score_li[i]
            score_str = "^".join([key,str(val)])
            score_strs.append(score_str)
        result["KEYWORD"] = " ".join(score_strs)


if __name__ == "__main__":
    conf = Config()
    extractor = KeywordExtractor(conf)
    extractor.extract()
    analyzer = DocumentAnalyzer(conf.analysis_option, "result")
    analyzer.analyze(extractor)
