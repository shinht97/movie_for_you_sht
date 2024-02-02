from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from selenium.webdriver.common.keys import Keys

import pandas as pd
import time
import datetime


options = ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

options.add_argument(f"user-agent={user_agent}")
options.add_argument("lang=ko_KR")
# options.add_argument("headless")  # 실제 웹 페이지 띄우지 않음
# options.add_argument("window-size=1920X1080")  # 웹 창 크기 지정

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

start_url = "https://m.kinolights.com/discover/explore"
driver.get(start_url)  # start_url 접속
time.sleep(1)  # 1초 대기

button_movie_tv_xpath = '//*[@id="contents"]/section/div[3]/div/div/div[3]/button'  # 영화/tv 버튼의 xpath
button_movie_tv = driver.find_element(By.XPATH, button_movie_tv_xpath)  # 버튼을 찾음
driver.execute_script("arguments[0].click();", button_movie_tv)  # 버튼 클릭(javascript 실행)
time.sleep(1)  # 1초 대기

button_movie_xpath = '//*[@id="contents"]/section/div[4]/div[2]/div[1]/div[3]/div[2]/div[2]/div/button[1]'  # 영화 버튼의 xpath
button_movie = driver.find_element(By.XPATH, button_movie_xpath)
driver.execute_script("arguments[0].click();", button_movie)
time.sleep(0.5)

button_ok_xpath = '//*[@id="contents"]/section/div[4]/div[2]/div[2]/button'  # 필터링 확인 버튼의 xpath
button_ok = driver.find_element(By.XPATH, button_ok_xpath)
driver.execute_script("arguments[0].click();", button_ok)
time.sleep(0.5)

for _ in range(27):
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")  # 스크롤 내리는 동작
    time.sleep(3)

list_review_url = []
movie_titles = []

for i in range(1, 1001):
    movie_link_xpath = f'//*[@id="contents"]/div/div/div[3]/div[2]/div[{i}]/a'
    base = driver.find_element(By.XPATH, movie_link_xpath).get_attribute("href")  # 영화의 정보가 있는 영화 링크
    # get_attribute : 속성 값을 가져옴
    list_review_url.append(f"{base}/reviews")  # 영화의 리뷰가 있는 링크로 만들어서 추가

    # title_xpath = f'//*[@id="contents"]/div/div/div[3]/div[2]/div[{i}]/div/div[1]'
    # title = driver.find_element(By.XPATH, title_xpath).text  # 영화 제목
    title = driver.find_element(By.XPATH, movie_link_xpath).get_attribute("title")
    # text : 해당 하는 요소에 있는 텍스트
    movie_titles.append(title)

print(list_review_url[:5])
print(len(list_review_url))

print(movie_titles[:5])
print(len(movie_titles))

reviews = []

for idx, url in enumerate(list_review_url):
    driver.get(url)  # 리스트 안에 있는 주소에 접근
    time.sleep(2)  # 2초 대기

    for _ in range(6):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")  # 스크롤 내리는 동작
        time.sleep(3)

    review = ''

    for j in range(1, 51):
        review_title_xpath = '//*[@id="contents"]/div[2]/div[2]/div[{}]/div/div[3]/a[1]/div'.format(j)
        review_more_xpath = '//*[@id="contents"]/div[2]/div[2]/div[{}]/div/div[3]/div/button'.format(j)  # 더보기

        try:
            review_more = driver.find_element(By.XPATH, review_more_xpath)  # 더보기가 있는 리뷰의 경우
            driver.execute_script("arguments[0].click();", review_more)  # 더보기를 눌러 들어가서
            time.sleep(1)
            review_xpath = '//*[@id="contents"]/div[2]/div[1]/div/section[2]/div/div'
            review = review + " " + driver.find_element(By.XPATH, review_xpath).text  # 리뷰 전문을 가져옴
            driver.back()  # 더보기로 들어왔기 때문에 이전 창으로 돌아감
            time.sleep(1)

            for _ in range(6):
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")  # 스크롤 내리는 동작
                time.sleep(3)

        except NoSuchElementException as noelement:  # 더보기 가 없는 경우 실행 되는 예외 처리
            print("더보기 error")

            try:
                review = review + " " + driver.find_element(By.XPATH, review_title_xpath).text
            except:
                print("title error")

        except StaleElementReferenceException as e:  # 페이지 로딩이 아직 안되었을 때
            print("stale error")

        except:
            print("Error")

    print(review)

    reviews.append(review)

print(reviews[:5])

print(len(reviews))

df = pd.DataFrame({"titles": movie_titles[150:201], "reviews": reviews})
today = datetime.datetime.now().strftime("%Y%m%d")
df.to_csv(f"../crawling_data/reviews_all.csv", index=False)
