'''
cron 주기 : 10분에 1회
'''

import requests

# 조위관측소 최신 관측데이터(울산)
# https://www.khoa.go.kr/oceangrid/member/mypage/selectOpenApiState.do?isCreate=true
# http://www.khoa.go.kr/oceangrid/khoa/takepart/openapi/openApiObsRecentDataInfo.do
# chmod 755 weather.py 적용(나중에 자동화 할때 필요할거같아서)

open_api_key = '6swLHOrqrrWmQMgPm3h1mg=='  # 공공데이터 인증키
params = '&ObsCode=DT_0020&ResultType=json'  # 파라미터의 값을 params의 변수에 저장
open_url = 'http://www.khoa.go.kr/oceangrid/grid/api/tideObsRecent/search.do?ServiceKey=' + \
    open_api_key + params
# open API URL 생성

r = requests.get(open_url)
weather = r.json()


meta = weather['result']['meta']
data = weather['result']['data']


obs_post_name = meta['obs_post_name'] # 관측소 명 울산

record_time = data['record_time']  # 관측시간 ex)2016-01-01 00:01:00
tide_level = data['tide_level'] # 조위 cm
water_temp = data['water_temp'] # 수온 ℃
Salinity = data['Salinity'] # 염분 psu
air_temp = data['air_temp'] # 기온 ℃
air_press = data['air_press'] # 기압 hPa
wind_dir = data['wind_dir'] # 풍향 deg
wind_speed = data['wind_speed'] # 풍속 m/s
wind_gust = data['wind_gust'] #돌풍 m/s




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

cur.execute("INSERT INTO wheather_current (id, 관측소_명, 관측_시간, 조위, 수온, 염분, 기온, 기압, 풍향, 풍속, 돌풍 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )", (cnt, obs_post_name, record_time, tide_level, water_temp, Salinity, air_temp, air_press, wind_dir, wind_speed,wind_gust))
con.commit()

con.close()