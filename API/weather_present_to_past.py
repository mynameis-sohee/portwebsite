# 폐기지만 혹시 모르니 남겨둡니다..

from warnings import resetwarnings
import requests
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas
from urllib.parse import urlencode, quote_plus
from pymongo import MongoClient
import pymongo

# 국립해양측위정보원 해양기상 정보서비스
# https://marineweather.nmpnt.go.kr/serviceReq/serviceOpenApiIntro.do
# 기상청_지상(종관,ASOS) 시간자료 조회서비스
# https://www.data.go.kr/data/15057210/openapi.do


# ---최신해양기상자료---

open_api_key = '840A18CA-EC7C-423E-A1B6-FDFB48CD2BA1'  # 인증키
agency = '104'  # 울산항 기관코드(104)
point = '1000520'  # 울산항등부표 지점코드(1000520)

today_date = datetime.today() + relativedelta(days=-1)  # 오늘 날짜 datetime형태
today_is = today_date.strftime("%Y%m%d")  # 오늘 날짜 YYmmdd형태

past_date = today_date + relativedelta(years=-4)  # 4년전 날짜 datetime형태
pastdate_is = past_date.strftime("%Y%m%d")  # 4년전 날짜 YYmmdd형태

recent_weather = 'http://marineweather.nmpnt.go.kr:8001/openWeatherNow.do?serviceKey=' +\
    open_api_key + '&resultType=json&mmaf=' + agency + \
    '&mmsi=' + point  # 가장 최근 측정된 해양기상 자료(국립해양측위정보원)

# ---최신해양기상자료 끝---

# while (past_date < today_date):
#     print(today_date)
#     print(past_date)
#     print(past_date < today_date)


past_weather_pre = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList'
queryParams = '?' + urlencode({quote_plus('ServiceKey'): 'BQbARTGT5QG2jla7rNWHXeDuEUo4H6FSZAY4NX461tepYo6UihfFcWakHW/ZuwuMd/B8HYbGpXYeKuA/4ftHvw==', quote_plus('pageNo'): '40', quote_plus('numOfRows'): '999',
                            quote_plus('dataType'): 'JSON', quote_plus('dataCd'): 'ASOS', quote_plus('dateCd'): 'HR', quote_plus('startDt'): 20170101,
                            quote_plus('startHh'): '01', quote_plus('endDt'): today_is, quote_plus('endHh'): '01', quote_plus('stnIds'): '152'})
# 서비스키 BQbARTGT5QG2jla7rNWHXeDuEUo4H6FSZAY4NX461tepYo6UihfFcWakHW%2FZuwuMd%2FB8HYbGpXYeKuA%2F4ftHvw%3D%3D or BQbARTGT5QG2jla7rNWHXeDuEUo4H6FSZAY4NX461tepYo6UihfFcWakHW/ZuwuMd/B8HYbGpXYeKuA/4ftHvw==
# 위의 둘중 하나를 사용 어느걸 사용해야하는지는 자기네들도 모르니 둘다 시도해보라함

past_weather = past_weather_pre + queryParams  # 기상청 Open API 주소

print(past_weather)

r = requests.get(past_weather)

weather_record = r.json()

try:
    weather_past = weather_record['response']['body']['items']
except KeyError:
    pass

#---DB삽입---

client = MongoClient(
    username='FIREMOTH',
    password='glacksqnfskqkd1!'
)


db = client.portwebsite_db # portwebsite_db가 우리 데이터베이스 이름
collection = db.과거날씨_데이터 #20170101~20210708


for w in weather_past['item']:
    # print("지점 번호(종관기상관측 지점 번호): " + w["stnId"])
    # print("시간(yyyy-mm-dd hh:mm)" + w["tm"])
    # print("지점명(종관기상관측 지점명)" + w["stnNm"])
    # print("적설" + w["dsnw"])
    # print("일조" + w["ss"])
    # print("해면기압" + w["ps"])
    # print("현지기압" + w["pa"])
    # print("습도" + w["hm"])
    # print("풍향" + w["wd"])
    # print("풍속" + w["ws"])
    # print("강수량" + w["rn"])
    # print("기온" + w["ta"])
    weather_dic = {
        "지점 번호(종관기상관측 지점 번호): " : w["stnId"],
        "시간(yyyy-mm-dd hh:mm)" : w["tm"],
        "지점명(종관기상관측 지점명)" : w["stnNm"],
        "적설" : w["dsnw"],
        "일조" : w["ss"],
        "해면기압" : w["ps"],
        "현지기압" : w["pa"],
        "습도" : w["hm"],
        "풍향" : w["wd"],
        "풍속" : w["ws"],
        "강수량" : w["rn"],
        "기온" : w["ta"],
    }
    try:
        post_id = collection.insert_one(weather_dic)
    except pymongo.errors.DuplicateKeyError:
        continue
        # for doc in collection.find():
        #     client.update_one({'_id': doc['_id']}, doc, upsert=True)

    # today_date = today_date + relativedelta(months=-1)  # 오늘 날짜 datetime형태
    # today_is = today_date.strftime("%Y%m%d")  # 오늘 날짜 YYmmdd형태
    
