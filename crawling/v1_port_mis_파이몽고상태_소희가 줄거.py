
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime

# 사용시설현황

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

driver.get('https://new.portmis.go.kr/portmis/websquare/websquare.jsp?w2xPath=/portmis/w2/main/intro.xml')
driver.implicitly_wait(3)

btn = driver.find_element_by_id('mf_btnSiteMap')
btn.click()

driver.implicitly_wait(10)

btn = driver.find_element_by_id(
    'mf_tacMain_contents_M0045_body_genMenuLevel1_1_genMenuLevel2_1_genMenuLevel3_1_btnMenuLevel3')
btn.click()

driver.implicitly_wait(10)

selected_tag = driver.find_element_by_css_selector(
    'input#mf_tacMain_contents_M1554_body_srchPrtAgCd')
selected_tag.click()

time.sleep(1.5)
driver.implicitly_wait(10)
selected_tag.send_keys('820')

driver.implicitly_wait(10)
btn = driver.find_element_by_id(
    'mf_tacMain_contents_M1554_body_udcSearchList_btnSearch')
btn.click()

driver.implicitly_wait(10)

el = driver.find_element_by_id(
    'mf_tacMain_contents_M1554_body_udcGridPageView_sbxRecordCount_input_0')
for option in el.find_elements_by_tag_name('option'):
    if option.text == '50000개씩 보기':
        option.click()
        break

driver.implicitly_wait(10)
btn = driver.find_element_by_id(
    'mf_tacMain_contents_M1554_body_udcSearchList_btnSearch')
btn.click()

driver.implicitly_wait(10)


btn = driver.find_element_by_id(
    'mf_tacMain_contents_M1554_body_grpSrchList_cell_0_0')
btn.click()

save_dict = {}
DOWN = '/ue015'
cnt = 0


def tail_value():
    for i in range(0, 9):
        save_value = {}
        try:
            for k in range(0, 22):
                value = soup.select_one(
                    '#mf_tacMain_contents_M1554_body_grpSrchList_cell_{}_{} > nobr'.format(i, k)).text
                save_value.setdefault('key_{}'.format(k), value)
            save_dict['n_{}_{}'.format(datetime.datetime.now().strftime(
                "%Y%m%d"), save_value['key_0'])] = save_value
        except AttributeError:
            break


for _ in range(0, 10000):
    btn.send_keys(Keys.DOWN)
    save_value = {}
    for k in range(0, 22):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        value = soup.select_one(
            '#mf_tacMain_contents_M1554_body_grpSrchList_cell_{}_{} > nobr'.format(0, k)).text
        save_value.setdefault('key_{}'.format(k), value)

    if 'n_{}_{}'.format(datetime.datetime.now().strftime("%Y%m%d"), save_value['key_0']) in save_dict:
        cnt += 1
    if cnt > 15:
        tail_value()
        break

    save_dict['n_{}_{}'.format(datetime.datetime.now().strftime(
        "%Y%m%d"), save_value['key_0'])] = save_value
print(save_dict)
print(type(save_dict))


# DB 삽입

client = MongoClient(
    username='FIREMOTH',
    password='glacksqnfskqkd1!'
)


db = client.portwebsite_db  # portwebsite_db가 우리 데이터베이스 이름


db.시설사용현황.drop()  # 콜랙선 초기화

collection = db.시설사용현황  # 콜렉션 정의

post_list = []

for value in save_dict.values():
    post_list.append({
        "순번": value['key_0'],
        "호출부호": value['key_1'],
        "입항횟수_년도": value['key_2'],
        "입항횟수_횟수": value['key_3'],
        "시설사용횟수": value['key_4'],
        "신고톤수": value['key_5'],
        "선박명": value['key_6'],
        "선사": value['key_7'],
        "대리점": value['key_8'],
        "신청시설1": value['key_9'],
        "신청시설2": value['key_10'],
        "신청시설3": value['key_11'],
        "신청일시(FROM)": value['key_12'],
        "신청일시(TO)": value['key_13'],
        "지정시설1": value['key_14'],
        "지정시설2": value['key_15'],
        "지정시설3": value['key_16'],
        "지정일시(FROM)": value['key_17'],
        "지정일시(TO)": value['key_18'],
        "사용목적명": value['key_19'],
        "예보일시": value['key_20'],
        "허가유무": value['key_21'],
    })


post_id = collection.insert_many(post_list)