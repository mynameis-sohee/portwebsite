from django.shortcuts import render
from django.http import HttpResponse # 임시표기HttpResponse용 
from django.http import JsonResponse
from operator import itemgetter
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from main.models import HarborData
import psycopg2
import json
import requests

try:
    connection = psycopg2.connect("dbname='portwebsite_db' user='FIREMOTH' host='portwebsite.cictpybqx5bj.ap-northeast-2.rds.amazonaws.com' port='5432' password='glacksqnfskqkd1!'")
    connection.autocommit = True
except:
    print("Not Connected!")

# Create your views here.
def index(request):

    return render(request, 'main/main_page.html',{**ShowingPortStatus(),**ShowingWeather(),**AnchorageChart()})
    # return render(request, 'main/main_page.html',{**ShowingPortStatus()})

def ShowingPortStatus():
    port_status = []
    port_name = []

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM upa_v3")
    for rec in cursor.fetchall():
        port_name.append(rec[0])
        port_status.append(rec[2]) 

    print(port_status)
    print(port_name)

    dictionary = {
        '상태' :port_status,
        '항구이름' :port_name  
    }

    cursor.close()

    return dictionary

# ShowingPortStatus()

def ShowingWeather():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM wheather_current")
    data = cursor.fetchone()
    print(data)
    cursor.close()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM today_weather_main")
    weather = cursor.fetchone()
    print(weather)
    context = {
        "관측소명": data[0],
        "관측시간": data[1],
        "조위": data[2],
        "수온": data[3],
        "염분": data[4],
        "기온": data[5],
        "기압": data[6],
        "풍향": data[7],
        "풍속": data[8],
        "돌풍": data[9],
        "날씨": weather[0],
    }

    cursor.close()
    return context

# print(ShowingWeather())

def AnchorageChart():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM current_anchorage")
    data = cursor.fetchall()
    E1 = []
    E2 = []
    E3 = []
    etc = []
    print(data)
    for d in data:
        if d[12] == "정박지-E1":
            E1.append(d)
        elif d[12] == "정박지-E2":
            E2.append(d)
        elif d[12] == "정박지-E3":
            E3.append(d)
        else:
            etc.append(d)
        context = {
        "E1_quantity": len(E1),
        "E2_quantity": len(E2),
        "E3_quantity": len(E3),
        "etc_quantity": len(etc),
    }
    return context
def GetHarborData(request):
    if request.method == 'GET':
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
        req = driver.page_source
        # driver.quit()  # 정보를 가져왔으므로 드라이버는 꺼줍니다.

        # soup = BeautifulSoup(data.text, 'html.parser')
        soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup으로 파싱해줍니다.

        date_array = soup.select_one("table.w2calender_content_table > tbody > tr >td")

        harborcode_box = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M5784_body_udc_prtAgCd_cmmCd"]')
        harborcode_box.send_keys('820')  # 울산항코드

        input_box = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M5784_body_calSrchFrDt_img"]')
        input_box.click()

        date_button = driver.find_element_by_xpath(
            '//*[@id="mf_tacMain_contents_M5784_body_calSrchFrDt_calendar_cell_2_3"]')
        date_button.click()

        fac_code = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M5784_body_srchFcltyCd"]')
        fac_code.send_keys('MB1')
        fac_code_add = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M5784_body_srchFcltySubCd"]')
        fac_code_add.send_keys('01')

        search_button = driver.find_element_by_xpath('//*[@id="mf_tacMain_contents_M5784_body_udcSearch_btnSearch"]')
        search_button.click()
        sleep(1)
        temp_date = driver.find_element_by_xpath(
            '//*[@id="mf_tacMain_contents_M5784_body_grdNlgVsslInOutList_cell_0_0"]/nobr').text
        temp_shipname = driver.find_element_by_xpath(
            '//*[@id="mf_tacMain_contents_M5784_body_grdNlgVsslInOutList_cell_0_2"]/nobr').text
        temp_worktype = driver.find_element_by_xpath(
            '//*[@id="mf_tacMain_contents_M5784_body_grdNlgVsslInOutList_cell_0_8"]/nobr').text
        HarborData.objects.create(date=temp_date, shipname=temp_shipname, worktype=temp_worktype)
        

        r = HarborData.objects.values()
        print(r[0]['date'])
      
        context1 = {
        "date": 'date',
        "shipname":'shipname',  
        "worktype":'worktype',
        }
        return JsonResponse(context1)
    else:
        return HttpResponse("GET이아님")
# print(AnchorageChart())

# connection.close()