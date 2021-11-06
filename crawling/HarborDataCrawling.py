from django.shortcuts import render
from django.http import HttpResponse # 임시표기HttpResponse용 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from operator import itemgetter
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import psycopg2
import json
import requests

try:
    connection = psycopg2.connect("dbname='portwebsite_db' user='FIREMOTH' host='portwebsite.cictpybqx5bj.ap-northeast-2.rds.amazonaws.com' port='5432' password='glacksqnfskqkd1!'")
    connection.autocommit = True
except:
    print("Not Connected!")
cursor = connection.cursor()
cursor.execute("SELECT * FROM harborcode")
data = cursor.fetchall()
def GetHarborDataFunc():
    for harbor in data:
        GetHarborData(harbor[1],harbor[2],harbor[0])
def GetHarborData(maincode,subcode,harborname):
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
    sleep(1)  # 페이지가 로딩되는 동안 5초 간 기다립니다.
    a = driver.find_element_by_id(
        "mf_tacMain_contents_M4735_body_genMenuLevel1_1_genMenuLevel2_4_genMenuLevel3_3_btnMenuLevel3")
    a.click()


    harborcode_box = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M5784_body_udc_prtAgCd_cmmCd"]')
    harborcode_box.send_keys('820')  # 울산항코드

    input_box = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M5784_body_calSrchFrDt_img"]')
    input_box.click()

    date_button = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M5784_body_calSrchFrDt_calendar_cell_3_1"]/button')
    date_button.click()

    fac_code = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M5784_body_srchFcltyCd"]')
    fac_code.send_keys(maincode)
    fac_code_add = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M5784_body_srchFcltySubCd"]')
    fac_code_add.send_keys(subcode)

    search_button = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M5784_body_udcSearch_btnSearch"]')
    search_button.click()
    sleep(1)
    temp_date = driver.find_element_by_xpath(
        '//*[@id="mf_tacMain_contents_M5784_body_grdNlgVsslInOutList_cell_0_0"]/nobr').text
    temp_shipname = driver.find_element_by_xpath(
        '//*[@id="mf_tacMain_contents_M5784_body_grdNlgVsslInOutList_cell_0_2"]/nobr').text
    temp_worktype = driver.find_element_by_xpath(
        '//*[@id="mf_tacMain_contents_M5784_body_grdNlgVsslInOutList_cell_0_8"]/nobr').text
    sql = "INSERT INTO main_harbordata (date,shipname,worktype,선석,부두이름) VALUES (%s,%s,%s,%s,%s)"
    val = (temp_date,temp_shipname,temp_worktype,subcode,harborname)
    cursor.execute(sql,val)
    driver.quit()
GetHarborDataFunc()
