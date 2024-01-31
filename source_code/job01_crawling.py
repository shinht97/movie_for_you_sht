from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import pandas as pd
import re
import time
import datetime


options = ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

options.add_argument(f"user-agent={user_agent}")
options.add_argument("lang=ko_KR")
# options.add_argument("headless")  # 실제 웹 페이지를 띄우지 않음
# options.add_argument("window-size=1920X1080")  # 웹 창 크기 지정

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

start_url = "https://m.kinolights.com/discover/explore"

driver.get(start_url)  # start_url에 접속

time.sleep(1)  # 1초 대기

button_movie_tv_xpath = '//*[@id="contents"]/section/div[3]/div/div/div[3]/button'  # 영화/tv 버튼의 xpath

button_movie_tv = driver.find_element(By.XPATH, button_movie_tv_xpath)  # 버튼을 찾음

driver.execute_script("arguments[0].click();", button_movie_tv)  # 버튼 클릭(javascript 실행)

time.sleep(1)  # 1초 대기

button_movie_xpath = '//*[@id="contents"]/section/div[4]/div[2]/div[1]/div[3]/div[2]/div[2]/div/button[1]'

button_movie = driver.find_element(By.XPATH, button_movie_xpath)

driver.execute_script("arguments[0].click();", button_movie)

time.sleep(0.5)

button_ok_xpath = '//*[@id="contents"]/section/div[4]/div[2]/div[2]/button'

button_ok = driver.find_element(By.XPATH, button_ok_xpath)

driver.execute_script("arguments[0].click();", button_ok)

time.sleep(0.5)

for _ in range(12):
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")  # 스크롤을 내리는 동작
    time.sleep(5)

list_review_url = []
movie_titles = []

for i in range(1, 501):
    base = driver.find_element(By.XPATH, f'//*[@id="contents"]/div/div/div[3]/div[2]/div[{i}]/a').get_attribute("href")
    list_review_url.append(f"{base}/reviews")
    title = driver.find_element(By.XPATH, f'//*[@id="contents"]/div/div/div[3]/div[2]/div[{i}]/div/div[1]').text
    movie_titles.append(title)

print(list_review_url[:5])
print(len(list_review_url))

print(movie_titles[:5])
print(len(movie_titles))

reviews = []

for url in list_review_url:
    driver.get(url)  # 리스트 안에 있는 주소에 접근
    time.sleep(2)  # 2초 대기

    review = ''

    for j in range(1, 11):
        try:
            review_title_xpath = '//*[@id="contents"]/div[2]/div[2]/div[{}]/div/div[3]/a[1]/div'.format(j)
            review_more_xpath = '//*[@id="contents"]/div[2]/div[2]/div[{}]/div/div[3]/div/button'.format(j)
            try:
                review_more = driver.find_element(By.XPATH, review_more_xpath)
                driver.execute_script("arguments[0].click();", review_more)
                time.sleep(0.5)
                review_xpath = '//*[@id="contents"]/div[2]/div[1]/div/section[2]/div/div'
                review = review + " " + driver.find_element(By.XPATH, review_xpath).text
                driver.back()
                time.sleep(0.5)

            except Exception as exc:
                review = review + " " + driver.find_element(By.XPATH, review_title_xpath).text

        except Exception as exc:
            print(url, j)

    print(review)

    reviews.append(review)

print(reviews[:5])

print(len(reviews))
