# Text-Mining
Text mining project with Wisenut week 1

## 프로젝트 개요
tf-idf 점수로 요구사항에 맞게 문서를 분석  
(자세한 사항은 Toy Project1(DM팀).pdf에 기재되어 있음)

## 실행 방법
1. config.yaml 에서 설정 작성
2. main.py 실행  
 -> result 폴더에 결과가 파일로 출력됨

## 코드 설명
#### main.py
config.yaml 에서 설정을 읽고, tf-idf 점수를 계산하여 문서를 분석한 결과를 result 폴더에 결과를 파일로 출력

#### src/preprocesser.py
문서의 내용을 설정에 맞게 전처리

#### src/tfidf.py
전처리된 텍스트 데이터의 tf-idf 점수를 계산

#### src/normalizer.py
단어의 가장 큰 점수가 `scale`이 되도록 정규화

#### src/analyzer.py
Toy Project1(DM팀).pdf에서 주어진 6개 항목으로 문서 분석
