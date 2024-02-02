import pandas as pd
from wordcloud import WordCloud
import collections
import matplotlib.pyplot as plt

from matplotlib import font_manager

font_path = "../malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rc("font", family="NanumBarunGothic")  # plot에 폰트를 적용

df = pd.read_csv("../learning_data/cleaned_one_review.csv")

words = df.iloc[1829, 1].split()  # X번째 영화의 1번째 rows
print(words)

worddict = collections.Counter(words)  # 유니크한 단어 들의 출현 빈도를 계산
worddict = dict(worddict)  # 딕션 형태로 만들어줌
print(worddict)

wordcloud_img = WordCloud(
    background_color="white",
    max_words=2000,
    font_path=font_path,
).generate_from_frequencies(worddict)  # 단어 구름 그림을 단어 빈도수를 이용하여 그림

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud_img, interpolation="bilinear")
plt.axis("off")
plt.show()

# bag of word : 단어를 순서 없이 묶어서 묶음
# bow 안의 빈도수를 보여줌
