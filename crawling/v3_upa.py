from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
from pymongo import MongoClient

# 실시간 부두상황정보

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 크롬 드라이버 경로 설정, 및 옵션 설정(옵션은 DevToolsActivePort를 찾을 수 없다는 에러 해결을 위해)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")
path = '/home/ubuntu/portwebsite/crawling/chromedriver'
driver = webdriver.Chrome(path, options=chrome_options)
# -------------------------------------------------------------------------------------------------

driver.implicitly_wait(3)

driver.get('https://www.upa.or.kr/safe/pub/main/index.do')
driver.implicitly_wait(3)



table = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/ul/li[1]/ol')
ul = table.find_elements_by_tag_name("li")

save_dict_1={}
for i in ul:
    save_dict_1['n_{}_{}'.format(datetime.datetime.now().strftime("%Y%m%d"), i.text[:6])] = i.text




btn = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/ul/li[2]/button')
btn.click()

table = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/ul/li[2]/ol')
ul = table.find_elements_by_tag_name("li")

save_dict_2={}
for i in ul:
    save_dict_2['n_{}_{}'.format(datetime.datetime.now().strftime("%Y%m%d"), i.text[:6])] = i.text





btn = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/ul/li[3]/button')
btn.click()

table = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/ul/li[3]/ol')
ul = table.find_elements_by_tag_name("li")

save_dict_3={}
for i in ul:
    save_dict_3['n_{}_{}'.format(datetime.datetime.now().strftime("%Y%m%d"), i.text[:6])] = i.text





btn = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/ul/li[4]/button')
btn.click()

table = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/ul/li[4]/ol')
ul = table.find_elements_by_tag_name("li")

save_dict_4={}
for i in ul:
    save_dict_4['n_{}_{}'.format(datetime.datetime.now().strftime("%Y%m%d"), i.text[:6])] = i.text


print(save_dict_1)
print(save_dict_2)
print(save_dict_3)
print(save_dict_4)

# DB 삽입

client = MongoClient(
    username='FIREMOTH',
    password='glacksqnfskqkd1!'
)

db = client.portwebsite_db  # portwebsite_db가 우리 데이터베이스 이름

db.실시간_부두상황정보_울산본항.drop()  # 콜렉션 초기화
collection = db.실시간_부두상황정보_울산본항  # 콜렉션 정의

post_list = []

for value in save_dict_1.values():
    val_list = value.split("\n")
    post_list.append({
        "부두명" : val_list[0],
        "조회시간" : val_list[1],
        "상태": val_list[2]
    })

post_id = collection.insert_many(post_list)

#---울산본항 끝---

db.실시간_부두상황정보_온산항.drop() # 콜렉션 초기화
collection = db.실시간_부두상황정보_온산항  # 콜렉션 정의

post_list = []

for value in save_dict_2.values():
    val_list = value.split("\n")
    post_list.append({
        "부두명" : val_list[0],
        "조회시간" : val_list[1],
        "상태": val_list[2]
    })

post_id = collection.insert_many(post_list)

#---온산항 끝---

db.실시간_부두상황정보_울산신항.drop() # 콜렉션 초기화
collection = db.실시간_부두상황정보_울산신항  # 콜렉션 정의

post_list = []

for value in save_dict_3.values():
    val_list = value.split("\n")
    post_list.append({
        "부두명" : val_list[0],
        "조회시간" : val_list[1],
        "상태": val_list[2]
    })

post_id = collection.insert_many(post_list)

# ---울산신항 끝---

db.실시간_부두상황정보_미포항.drop() # 콜렉션 초기화
collection = db.실시간_부두상황정보_미포항  # 콜렉션 정의

post_list = []

for value in save_dict_4.values():
    val_list = value.split("\n")
    post_list.append({
        "부두명" : val_list[0],
        "조회시간" : val_list[1],
        "상태": val_list[2]
    })

post_id = collection.insert_many(post_list)