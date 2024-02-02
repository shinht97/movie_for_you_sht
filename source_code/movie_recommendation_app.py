import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle

from PyQt5.QtCore import QStringListModel

form_window = uic.loadUiType("../ui/movie_recommendation.ui")[0]


class Main(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Tfidf_matrix = mmread("../models/Tfidf_movie_reviews.mtx").tocsr()  # matrix 불어오기

        with open("../models/tfidf.pickle", "rb") as file:
            self.Tfidf = pickle.load(file)  # tfidf 계산 값 불러오기

        self.embedding_model = Word2Vec.load("../models/word2vec_movie_reviews.model")  # word2vec 불러오기

        self.df_reviews = pd.read_csv("../learning_data/cleaned_one_review.csv")

        self.titles = list(self.df_reviews["titles"])
        self.titles.sort()

        self.cb_movie_list.addItem("")
        
        for title in self.titles:
            self.cb_movie_list.addItem(title)  # 콤보 박스에 아이템 추가

        self.cb_movie_list.currentIndexChanged.connect(self.cb_movie_list_changed_slot)  # 콤보박스의 아이템이 변경되면 실행

        self.btn_recommendation.clicked.connect(self.btn_recommendation_click_slot)  # 키워드를 통한 버튼 클릭시 실행
        
        model = QStringListModel()
        model.setStringList(self.titles)  # 자동완성에 대한 리스트를 줌
        completer = QCompleter(model)
        completer.setModel(model)
        self.le_keyword.setCompleter(completer)  # 자동완성 기능을 추가

    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))  # enumerate를 통해 idx 값도 같이
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)  # 정렬
        simScore = simScore[:11]  # 상위 11개(자기 자신 포함)
        movieIdx = [i[0] for i in simScore]
        recmovieList = self.df_reviews.iloc[movieIdx, 0]  # 해당하는 인덱스의 영화 제목을 리스트로 만듬

        return recmovieList[1:]

    def recommendation_by_movie_title(self, title):
        movie_idx = self.df_reviews[self.df_reviews["titles"] == title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        recommendation = "\n".join(list(recommendation))

        return recommendation

    def cb_movie_list_changed_slot(self):
        self.le_keyword.setText("")
        title = self.cb_movie_list.currentText()
        # print(title)
        recommendation = self.recommendation_by_movie_title(title)
        self.lbl_recommendation.setText(recommendation)

    def recommendation_by_keyword(self, keyword):
        try:
            sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)  # 주어진 단어와 유사한 단어 10개 추출
        except:
            recommendation = "모르는 키워드 입니다."
            return recommendation

        words = [keyword]

        for word, _ in sim_word:  # sim_word => (유사 단어, 유사도)의 리스트이기 때문에 유사 단어만 이용
            words.append(word)

        sentence = []

        count = 10

        for word in words:  # 10개의 상위 유사 키워드에 대해
            sentence = sentence + [word] * count  # 단어를 복사하여 리스트에 넣음
            count -= 1

        sentence = " ".join(sentence)  # " "를 추가 하여 하나의 문장으로 만듬

        sentence_vec = self.Tfidf.transform([sentence])  # 키워드로 이루어진 문장을 tfidf 계산

        cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)  # 키워드 문장의 코사인 유사도를 계산

        recommendation = self.getRecommendation(cosine_sim)  # 키워드로만 이루어진 문장 때문에 유사 키워드가 가장 많은 댓글이 있는 영화를 찾게 됨

        recommendation = "\n".join(list(recommendation))

        return recommendation

    def btn_recommendation_click_slot(self):
        keyword = self.le_keyword.text()
        # print(keyword)
        if keyword != "":
            if keyword in self.titles:
                recommendation = self.recommendation_by_movie_title(keyword)
            else:
                recommendation = self.recommendation_by_keyword(keyword)
    
            self.lbl_recommendation.setText(recommendation)
        else:
            self.lbl_recommendation.setText("키워드나 영화 제목을 입력해주세요")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Main()
    mainWindow.show()
    sys.exit(app.exec_())
