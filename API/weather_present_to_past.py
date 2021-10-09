### DB 연동 완료 
'''
cron 주기 : 1일 5회, 3시간에 1번. 변동 사항 생길 때마다 insert.
'''

# 폐기지만 혹시 모르니 남겨둡니다..

from warnings import resetwarnings
import requests
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas
from urllib.parse import urlencode, quote_plus

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
                            quote_plus('dataType'): 'JSON', quote_plus('dataCd'): 'ASOS', quote_plus('dateCd'): 'HR', quote_plus('startDt'): today_is,
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

#---DB삽입--

import psycopg2

con = psycopg2.connect(
    host = "portwebsite.cictpybqx5bj.ap-northeast-2.rds.amazonaws.com",
    database = "portwebsite_db",
    user = "FIREMOTH",
    password = "glacksqnfskqkd1!",
    port = 5432
)

cur = con.cursor()
cur.execute("SELECT id, 시간 FROM wheather_present_to_past ORDER BY id DESC LIMIT 1")
row = cur.fetchall()

if row:
    print(row)
    cnt = row[0][0]+1
else:
    cnt = 1


last_id = row[0][1].split()[0].replace("-","")

if last_id != today_is:
    for w in weather_past['item']:
        cur.execute("INSERT INTO wheather_present_to_past (지점번호, 시간, 지점명, 적설, 일조, 해면기압, 현지기압, 습도, 풍향, 풍속, 강수량, 기온, id ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )", (w["stnId"], w["tm"], w["stnNm"], w["dsnw"], w["ss"], w["ps"], w["pa"], w["hm"], w["wd"], w["ws"], w["rn"], w["ta"], cnt ))
        cnt += 1
        con.commit()
        print('done')

con.close()