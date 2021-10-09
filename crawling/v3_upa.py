'''
cron 주기 : 10분에 1회
'''

# 필요한 라이브러리 import
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime



import psycopg2

con = psycopg2.connect(
    host = "portwebsite.cictpybqx5bj.ap-northeast-2.rds.amazonaws.com",
    database = "portwebsite_db",
    user = "FIREMOTH",
    password = "glacksqnfskqkd1!",
    port = 5432
)

cur = con.cursor()

# 테이블 전체 삭제 후 재생성
cur.execute("DROP TABLE UPA_V3")

cur.execute("CREATE TABLE UPA_V3 (분류 TEXT, 부두명 TEXT, 시간 TEXT, 상태 TEXT);")
con.commit()


# 크롬 드라이버 통한 접속

# 크롬 드라이버 경로 설정, 및 옵션 설정(옵션은 DevToolsActivePort를 찾을 수 없다는 에러 해결을 위해)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")
path = '/home/ubuntu/portwebsite/crawling/chromedriver'
driver = webdriver.Chrome(path, options=chrome_options)
driver.implicitly_wait(3)

# 웹사이트 접속
driver.get('https://www.upa.or.kr/safe/pub/main/index.do')
driver.implicitly_wait(3)



# 울산본항 데이터 수집
table = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/ul/li[1]/ol')
ul = table.find_elements_by_tag_name("li")

save_dict_1={}
for i in ul:
    save_dict_1['n_{}_{}'.format(datetime.datetime.now().strftime("%Y%m%d"), i.text[:6])] = i.text
    name = i.text.split(sep='\n')[0]
    times = i.text.split(sep='\n')[1]
    status = i.text.split(sep='\n')[2]
    cur.execute("INSERT INTO UPA_V3 (분류, 부두명, 시간, 상태) VALUES (%s, %s, %s, %s)", ('울산본항', name, times, status))
    con.commit()



# 온산항 데이터 수집
btn = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/ul/li[2]/button')
btn.click()

table = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/ul/li[2]/ol')
ul = table.find_elements_by_tag_name("li")

save_dict_2={}
for i in ul:
    name = i.text.split(sep='\n')[0]
    times = i.text.split(sep='\n')[1]
    status = i.text.split(sep='\n')[2]
    cur.execute("INSERT INTO UPA_V3 (분류, 부두명, 시간, 상태) VALUES (%s, %s, %s, %s)", ('온산항', name, times, status))
    con.commit()




# 울산신항 데이터 수집
btn = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/ul/li[3]/button')
btn.click()

table = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/ul/li[3]/ol')
ul = table.find_elements_by_tag_name("li")

save_dict_3={}
for i in ul:
    name = i.text.split(sep='\n')[0]
    times = i.text.split(sep='\n')[1]
    status = i.text.split(sep='\n')[2]
    cur.execute("INSERT INTO UPA_V3 (분류, 부두명, 시간, 상태) VALUES (%s, %s, %s, %s)", ('울산신항', name, times, status))
    con.commit()




# 미포항 데이터 수집
btn = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/ul/li[4]/button')
btn.click()

table = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/ul/li[4]/ol')
ul = table.find_elements_by_tag_name("li")

save_dict_4={}
for i in ul:
    name = i.text.split(sep='\n')[0]
    times = i.text.split(sep='\n')[1]
    status = i.text.split(sep='\n')[2]
    cur.execute("INSERT INTO UPA_V3 (분류, 부두명, 시간, 상태) VALUES (%s, %s, %s, %s)", ('미포항', name, times, status))
    con.commit()


# 출력 - {'key값':'선석 당 데이터 (3개의 columns이 한 개의 데이터로 집계)}
# print(save_dict_1)
# print(save_dict_2)
# print(save_dict_3)
# print(save_dict_4)


con.close()