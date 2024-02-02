# vectorize : 단어의 축에 대해 단어 끼리의 유사 정도를 이용 하여 의미 공간에 배치
# 비슷한 위치에 있다 => 단어 끼리의 의미 영향이 비슷함, 비슷한 연상이 되는 단어, 사전적 유의어 X


import pandas as pd

from konlpy.tag import Okt
from gensim.models import Word2Vec  # 단어를 의미 공간에 좌표화

import pickle


df_review = pd.read_csv("../learning_data/cleaned_one_review.csv")

df_review.info()

reviews = list(df_review["reviews"])
print(reviews[0])

tokens = []

for sentence in reviews:
    token = sentence.split()
    tokens.append(token)

print(tokens[0])

embedding_model = Word2Vec(tokens, vector_size=100, window=4,
                           min_count=20, workers=4, epochs=100, sg=1)  # 영화 리뷰를 통해 단어들의 관계를 학습함

embedding_model.save("../models/word2vec_movie_reviews.model")

print(list(embedding_model.wv.index_to_key))  # 의미 공간을 만드는 데 사용한 모든 단어
print(len(embedding_model.wv.index_to_key))  # 최소 출현 값을 주었기 때문에 의미 학습을 한 단어는 줄어들 수 밖에 없음



