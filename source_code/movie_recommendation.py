import pandas as pd

from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle

from konlpy.tag import Okt
from gensim.models import Word2Vec


def getRecommaendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))  # enumerate를 통해 idx 값도 같이
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)  # 정렬
    simScore = simScore[:11]  # 상위 11개(자기 자신 포함)
    movieIdx = [i[0] for i in simScore]
    recmovieList = df_reviews.iloc[movieIdx, 0]  # 해당하는 인덱스의 영화 제목을 리스트로 만듬

    return recmovieList[1:]


df_reviews = pd.read_csv("../learning_data/cleaned_one_review.csv")

Tfidf_matrix = mmread("../models/Tfidf_movie_reviews.mtx").tocsr()

with open("../models/tfidf.pickle", "rb") as file:
    Tfidf = pickle.load(file)

movie_idx = 10

print(df_reviews.iloc[movie_idx, 0])

cosine_sim = linear_kernel(Tfidf_matrix[movie_idx], Tfidf_matrix)
# (타겟, 전체 행렬) cos 값을 계산, 전체 행렬에 대한 타겟의 코사인 값을 계산

# print(cosine_sim[0])
print(len(cosine_sim[0]))

recommendation = getRecommaendation(cosine_sim)

print(recommendation)

# 추천은 정답이 없고, 매출(히트)등으로 평가를 해야함
