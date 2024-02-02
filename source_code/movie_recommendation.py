import pandas as pd

from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle

from konlpy.tag import Okt
from gensim.models import Word2Vec


def getRecommendation(cosine_sim):
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

# 문장 유사도를 이용한 영화 추천
# movie_idx = 320
#
# print(df_reviews.iloc[movie_idx, 0])
#
# cosine_sim = linear_kernel(Tfidf_matrix[movie_idx], Tfidf_matrix)
# # (타겟, 전체 행렬) cos 값을 계산, 전체 행렬에 대한 타겟의 코사인 값을 계산
#
# # print(cosine_sim[0])
# print(len(cosine_sim[0]))
#
# recommendation = getRecommendation(cosine_sim)
#
# print(recommendation)

# 추천은 정답이 없고, 매출(클릭수)등으로 평가를 해야함


# 키워드 유사도를 이용한 영화 추천
embedding_model = Word2Vec.load("../models/word2vec_movie_reviews.model")

keyword = "스파이더맨"

sim_word = embedding_model.wv.most_similar(keyword, topn=10)  # 주어진 단어와 유사한 단어 10개 추출

words = [keyword]

for word, _ in sim_word:  # sim_word => (유사 단어, 유사도)의 리스트이기 때문에 유사 단어만 이용
    words.append(word)

sentence = []

count = 10

for word in words:  # 10개의 상위 유사 키워드에 대해
    sentence = sentence + [word] * count  # 단어를 복사하여 리스트에 넣음
    count -= 1

sentence = " ".join(sentence)  # " "를 추가 하여 하나의 문장으로 만듬 

print(sentence)

sentence_vec = Tfidf.transform([sentence])  # 키워드로 이루어진 문장을 tfidf 계산

cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)  # 키워드 문장의 코사인 유사도를 계산

recommendation = getRecommendation(cosine_sim)  # 키워드로만 이루어진 문장 때문에 유사 키워드가 가장 많은 댓글이 있는 영화를 찾게 됨

print(recommendation)
