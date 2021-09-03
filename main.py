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
        self.preprocess_option = config["preprocess_option"]
        self.word_num = config["word_num"]
        self.word_order = config["word_order"]
        self.analysis_option = config["word_analysis"]


class KeywordExtractor():
    def __init__(self, conf: Config):
        self.conf = conf
        self.calculator = TfIdfCalculator()
        self.doc_ids = []
        self.scores = []

    def extract(self):
        texts, self.doc_ids = self.load_data(self.conf)
        documents = self.preprocess(texts, self.conf.preprocess_option)
        tfidf = self.calculate_tfidf(documents)
        self.scores = self.get_importance_scores(tfidf)
        self.export_result(self.conf.save_dir, self.doc_ids, self.scores)

    def load_data(self, conf: Config):
        doc_ids = []
        texts = []
        # load document data
        try:
            with open(conf.load_dir, encoding="utf-8") as f:
                for obj in f:
                    # load object to data
                    data = json.loads(obj)
                    
                    doc_ids.append(data["doc_id"])

                    text = ""
                    for field in conf.fields:
                        text += data[field]
                    texts.append(text)
        except:
            print("Failed to load data")
        
        return doc_ids, texts

    def preprocess(self, texts: list, preprocess_option: int) -> list:
        documents = []
        preprocesser = Preprocesser(preprocess_option)
        # preprocess data
        for text in texts:
            documents.append(preprocesser.preprocess(text,
                                                     split_sentences=False))

        return documents

    def calculate_tfidf(self, documents: list) -> list:
        # calculate tfidf
        tfidf = self.calculator.get_tfidf(documents)

        return tfidf

    def get_importance_scores(self, tfidf: list) -> list:
        scores = []
        normalizer = Normalizer(100)
        # get importance scores 
        for dic in tfidf:
            if not dic:
                continue
            normalized_tfidf = normalizer.normalize(dic)
            scores.append(normalized_tfidf)

        return scores
    
    def export_result(self, save_dir: str, doc_ids: list, scores: list) -> None:
        # export result
        with open(save_dir, "w", encoding="utf-8") as json_file:
            for doc_id, score in zip(doc_ids, scores):
                line = self.score_to_json(doc_id, score)
                json_file.write(json.dumps(line, ensure_ascii=False) + "\n")
    
    def score_to_json(self, doc_id: str, score: dict) -> dict:
        result = {}
        
        result["DOCID"] = doc_id
        word_score_li = [[key, val] for key, val in score.items()]

        self.sort_score(word_score_li, self.conf.word_order)

        # 단어 출력 개수: 0 ~ N
        # 0으로 설정할 시 모든 단어 출력
        n = len(score) if self.conf.word_num == 0 else self.conf.word_num

        self.scores_to_string(n, word_score_li, result)
            
        return result

    def sort_score(self, word_score_li: list, word_order: int) -> None:
        # 단어 출력 방법
        # 1: 단어 점수 기준 내림차순, 2: 단어 글자 기준 오름차순
        if self.conf.word_order == 1:
            word_score_li.sort(key=lambda x:x[1], reverse=True)
        elif self.conf.word_order == 2:
            word_score_li.sort(key=lambda x:x[0])

    def scores_to_string(self, n: int, word_score_li: list, result: dict) -> None:
        score_strs = []
        for i in range(n):
            if i == len(word_score_li):
                break
            key, val = word_score_li[i]
            score_str = "^".join([key,str(val)])
            score_strs.append(score_str)
        result["KEYWORD"] = " ".join(score_strs)


if __name__ == "__main__":
    conf = Config()
    extractor = KeywordExtractor(conf)
    extractor.extract()
    analyzer = DocumentAnalyzer(conf.analysis_option, "result")
    analyzer.analyze(extractor.calculator,
                     extractor.doc_ids,
                     extractor.scores)
