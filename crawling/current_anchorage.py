from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.select import Select
import psycopg2

# ---DB 세팅---
try:
    connection = psycopg2.connect("dbname='portwebsite_db' user='FIREMOTH' host='portwebsite.cictpybqx5bj.ap-northeast-2.rds.amazonaws.com' port='5432' password='glacksqnfskqkd1!'")
    connection.autocommit = True
except:
    print("Not Connected!")

cursor = connection.cursor()
# --------

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


url = "https://new.portmis.go.kr/portmis/websquare/websquare.jsp?w2xPath=/portmis/w2/main/index.xml&page=/portmis/w2/cm/sys/UI-PM-MT-001-021.xml&menuId=0045&menuCd=M4735&menuNm=%BB%E7%C0%CC%C6%AE%B8%CA"


driver.get(url)  # 드라이버에 해당 url의 웹페이지를 띄웁니다.
driver.implicitly_wait(10)  # 페이지가 로딩되는 동안 5초 간 기다립니다.
a = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M4735_body_genMenuLevel1_1_genMenuLevel2_4_genMenuLevel3_1_btnMenuLevel3"]')
a.click()
sleep(1)
harborcode_box = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M0225_body_prtAgCd"]')
harborcode_box.send_keys('820') #울산항코드

sleep(1)
req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup으로 파싱해줍니다.

type_button = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M0225_body_schFcltyType_input_2"]')
type_button.click()

search_button = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M0225_body_udcSearch_btnSearch"]')
search_button.click()
sleep(1)

select = Select(driver.find_element_by_id("mf_tacMain_contents_M0225_body_udcGridPageView_sbxRecordCount_input_0"))
select.select_by_visible_text('10개씩 보기')
sleep(1)

save_dict={}
cnt = 1
cursor.execute("TRUNCATE TABLE current_anchorage;")
for num in range(15):
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup로 파싱
    temp_dict={}
    superBreak = False
    for i in range(0, 10):
        for j in range(0, 19):
            try:
                if soup.select_one(f"#mf_tacMain_contents_M0225_body_grdVsslStuList_cell_{i}_{j} > nobr").text != '':
                    temp_dict[j] = soup.select_one(f"#mf_tacMain_contents_M0225_body_grdVsslStuList_cell_{i}_{j} > nobr").text
                else:
                    temp_dict[j] = None
            except AttributeError:
                break
        if cnt == int(temp_dict[0]): #한번에 들어가도록 수정
            cursor.execute("INSERT INTO current_anchorage (순번,호출부호,입항년도,입항횟수,선명,국적,imo번호,총톤수,총길이,선박종류,선박구분,선종분류,계선장소,입항일시_관제,입항최초신고시간,입항최초허가일시,선사_대리점,신고구분,부두구분) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (temp_dict[0],temp_dict[1],temp_dict[2],temp_dict[3],temp_dict[4],temp_dict[5],temp_dict[6],temp_dict[7],temp_dict[8],temp_dict[9],temp_dict[10],temp_dict[11],temp_dict[12],temp_dict[13],temp_dict[14],temp_dict[15],temp_dict[16],temp_dict[17],temp_dict[18]))
            save_dict[cnt-1] = temp_dict
            print(temp_dict)
        else:
            superBreak = True
            break
        cnt += 1
    if superBreak:
        break
    btn = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M0225_body_udcGridPageList_pglGridView_next_btn"]/a')
    btn.click()
    sleep(1)

print(save_dict)