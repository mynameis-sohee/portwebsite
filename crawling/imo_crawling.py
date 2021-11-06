from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep


def get_IMO(search_key):

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
    #--------------------------------------------------------------------------------------------------------

    url = "https://new.portmis.go.kr/portmis/websquare/popup.jsp?w2xPath=/portmis/w2/sample/popup/pop/UC_PM_CM_002_07_02.xml&menuCd=M0182&popupID=mf_tacMain_contents_M0182_body_popupSearchVsslInnb&idx=idx10_16361987602659424.307303020947&w2xHome=/portmis/w2/main/&w2xDocumentRoot="

    driver.get(url)

    search_key = search_key.lower()


    # search_box = driver.find_element_by_css_selector("input#mf_ipt1")
    search_box = driver.find_element_by_xpath('//*[@id="mf_ipt1"]')
    search_box.send_keys(search_key)

    driver.implicitly_wait(1)

    search_btn = driver.find_element_by_css_selector("div#mf_udcSearch_btnSearch")

    search_btn.click()

    # driver.implicitly_wait(10)
    sleep(0.5)

    req = driver.page_source

    soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup로 파싱

    ship_name = None
    IMO_num =None

    for i in range(0, 9):
        try:
            ship_name_temp = soup.select_one(f"#mf_grdCallList_cell_{i}_0 > nobr").text
            IMO_num_temp = soup.select_one(f"#mf_grdCallList_cell_{i}_3 > nobr").text
            if search_key == ship_name_temp.lower():
                ship_name = ship_name_temp
                IMO_num = IMO_num_temp

        except AttributeError:
            break

    print(ship_name)
    
    driver.quit()
    if ship_name is not None:
        return IMO_num
    else:
        return False


# # search_key = input()
# search_key = "Global STAR"
# print(get_IMO(search_key))