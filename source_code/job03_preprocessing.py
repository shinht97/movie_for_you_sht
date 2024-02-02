import pandas as pd
import glob
from konlpy.tag import Okt
import re


# 영화 선택 -> 리뷰 -> 유사한 리뷰 -> 영화 추천
# 1) 비슷한 워딩을 찾기 -> 형태소 분리 필요 -> 스탑 워드를 명확 하게 구별 해야함(명사 동사 부사만 남김)
# Okt를 이용해 품사 태깅도 같이(okt.pos)
# 2) 

file_path = "../learning_data/reviews_kinolights.csv"

df = pd.read_csv(file_path)

# print(df.info())

df_stopwords = pd.read_csv("../learning_data/stopwords.csv")

stopwords = list(df_stopwords["stopword"])  # 리스트로 변경
stopwords += ["영화", "감독", "연출", "배우",
              "연기", "작품", "장면", "관객",
              "모르다", "스토리"]  # stopword 추가

cleaned_sentences = []

okt = Okt()

for idx, review in enumerate(df["reviews"]):
    review = re.sub("[^가-힣]", ' ', review)  # 한글만 남기고 그 외에는 공백으로 처리

    tokened_review = okt.pos(review, stem=True)  # 형용사, 동사, 명사는 학습에 도움, 부사, 조사, 감탄사는 학습에 방해됨

    print(tokened_review)  # okt.pos가 [('복수', 'Noun'), ('가', 'Josa'), ('없다', 'Adjective') ...과 같은 형태로 만들어줌

    df_token = pd.DataFrame(tokened_review, columns=["word", "class"])  # 튜플 들의 리스트를 이용 하여 DataFrame을 만듬

    df_token = df_token[df_token["class"].isin(["Noun", "Adjective", "Verb"])]
    # (df_token["class"] == "Noun") | (df_token["class"] == "Adjective") | (df_token["class"] == "Verb")

    words = []

    for word in df_token["word"]:
        if len(word) > 1:
            if word not in stopwords:
                words.append(word)

    cleaned_sentence = " ".join(words)

    cleaned_sentences.append(cleaned_sentence)

df["reviews"] = cleaned_sentences

print(df.info())

df.to_csv("../learning_data/cleaned_reviews.csv", index=False)

df = pd.read_csv("../learning_data/cleaned_reviews.csv")

df.dropna(inplace=True)  # " "만 있는 요소를 제거 하기 위해 다시 한번 불러와 dropna 실행

print(df.info())

df.to_csv("../learning_data/cleaned_reviews.csv", index=False)
