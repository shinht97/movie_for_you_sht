# TFIDF : Text Frequency In Document Frequency
# Text Frequency : 하나의 문장 안의 빈도수
# Document Frequency : 문서 전체의 빈도수
# 비슷한 빈도수를 가지면 유사 하다 판단, 전체 문서에서 많이 나오는 단어인 경우는 가중치를 깎음
# TF * 1/IDF 계산

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle


df_reviews = pd.read_csv("../learning_data/cleaned_one_review.csv")
print(df_reviews.info())

Tfidf = TfidfVectorizer(sublinear_tf=True)  # 리뷰의 모든 단어들의 TFIDF 값을 계산
Tfidf_matrix = Tfidf.fit_transform(df_reviews["reviews"])
print(Tfidf_matrix.shape)  # (657, 16825)

# 리뷰 안의 모든 단어들의 유사도를 계산 -> cos 유사도
# TF IDF 값을 이용 하여 vectorize => 비슷한 방향 이면 비슷한 문장 으로 생각 할수 있음
# 방향 => cos 값으로 계산
# cos 유사도
# ~1 : 유사
# 0 : 관계 없음
# -1~ : 반대

with open("../models/tfidf.pickle", "wb") as file:
    pickle.dump(Tfidf, file)  # Tfidf vectorizer을 파일로 저장

mmwrite("../models/Tfidf_movie_reviews.mtx", Tfidf_matrix)  # Tfidf 행렬 저장

