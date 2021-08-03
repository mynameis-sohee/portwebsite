from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
from pymongo import MongoClient

# 선박입출항현황

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 크롬 드라이버 경로 설정, 및 옵션 설정(옵션은 DevToolsActivePort를 찾을 수 없다는 에러 해결을 위해)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")
path = '/home/ubuntu/crawling/chromedriver'
driver = webdriver.Chrome(path, options=chrome_options)

driver.implicitly_wait(3)

driver.get('https://new.portmis.go.kr/portmis/websquare/websquare.jsp?w2xPath=/portmis/w2/main/intro.xml')
driver.implicitly_wait(3)

btn = driver.find_element_by_id('mf_btnSiteMap')
btn.click()

btn = driver.find_element_by_id('mf_tacMain_contents_M0045_body_genMenuLevel1_1_genMenuLevel2_0_genMenuLevel3_1_btnMenuLevel3')
btn.click()
driver.implicitly_wait(10)



selected_tag=driver.find_element_by_css_selector('input#mf_tacMain_contents_M1319_body_udc_prtAgCd_cmmCd')
selected_tag.click()

time.sleep(1.5)
driver.implicitly_wait(10)
selected_tag.send_keys('820')

driver.implicitly_wait(10)
btn = driver.find_element_by_id('mf_tacMain_contents_M1319_body_btnSrch_btnSearch')
btn.click()


el = driver.find_element_by_id('mf_tacMain_contents_M1319_body_udcGridPageView2_sbxRecordCount_input_0')
for option in el.find_elements_by_tag_name('option'):
    if option.text == '50000개씩 보기':
        option.click()
        break


driver.implicitly_wait(10)
btn = driver.find_element_by_id('mf_tacMain_contents_M1319_body_btnSrch_btnSearch')
btn.click()
driver.implicitly_wait(10)



btn = driver.find_element_by_id('mf_tacMain_contents_M1319_body_gridList2_cell_0_0')
btn.click()

save_dict={}
DOWN = '/ue015'
cnt = 0



def tail_value():
        for i in range(0,15):
            save_value = {}
            try:
                for k in range(0,32):
                    value = soup.select_one('#mf_tacMain_contents_M1319_body_gridList2_cell_{}_{} > nobr'.format(i, k)).text
                    save_value.setdefault('key_{}'.format(k), value)
                save_dict['n_{}_{}'.format(datetime.datetime.now().strftime("%Y%m%d"), save_value['key_1'])] = save_value
            except AttributeError:
                break


for _ in range(0,30):
    btn.send_keys(Keys.DOWN)
    save_value = {}
    for k in range(0,32):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        value = soup.select_one('#mf_tacMain_contents_M1319_body_gridList2_cell_{}_{} > nobr'.format(0, k)).text
        save_value.setdefault('key_{}'.format(k), value)

    if 'n_{}_{}'.format(datetime.datetime.now().strftime("%Y%m%d"), save_value['key_1']) in save_dict:
        cnt += 1

    if cnt > 15:
        tail_value()
        break

    save_dict['n_{}_{}'.format(datetime.datetime.now().strftime("%Y%m%d"), save_value['key_1'])] = save_value
print(save_dict)



# DB 삽입

client = MongoClient(
    username='FIREMOTH',
    password='glacksqnfskqkd1!'
)


db = client.portwebsite_db  # portwebsite_db가 우리 데이터베이스 이름
db.선박입출항현황.drop()  # 콜렉션 초기화
collection = db.선박입출항현황  # 콜렉션 정의

post_list = []

for value in save_dict.values():
    post_list.append({
        "항명": value['key_0'],
        "호출부호": value['key_1'],
        "선명": value['key_2'],
        "입항횟수_년도": value['key_3'],
        "압항횟수_횟수": value['key_4'],
        "구분": value['key_5'],
        "외내": value['key_6'],
        "입출": value['key_7'],
        "총톤수": value['key_8'],
        "국제톤수": value['key_9'],
        "징수톤수": value['key_10'],
        "입항일시": value['key_11'],
        "출항일시": value['key_12'],
        "CIO수속일자": value['key_13'],
        "수리일시": value['key_14'],
        "항해구분": value['key_15'],
        "MRN번호": value['key_16'],
        "국적_약어": value['key_17'],
        "국적_kr": value['key_18'],
        "계선장소1": value['key_19'],
        "계선장소2": value['key_20'],
        "계선장소3": value['key_21'],
        "차항지": value['key_22'],
        "전출항지": value['key_23'],
        "선박용도": value['key_24'],
        "승무원(한국인)": value['key_25'],
        "승무원(외국인)": value['key_26'],
        "승객": value['key_27'],
        "예선": value['key_28'],
        "도선": value['key_29'],
        "부선호출부호1": value['key_30'],
        "부선호출부호2": value['key_31'],
    })


post_id = collection.insert_many(post_list)