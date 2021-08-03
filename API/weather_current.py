import requests
from pymongo import MongoClient

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

print(weather)

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

client = MongoClient(
    username='FIREMOTH',
    password='glacksqnfskqkd1!'
)


db = client.portwebsite_db # portwebsite_db가 우리 데이터베이스 이름
collection = db.현재날씨# 콜렉션 정의


post = {
    "관측소_명" : obs_post_name,
    "관측_시간" : record_time,
    "조위" : tide_level,
    "수온" : water_temp,
    "염분" : Salinity,
    "기온" : air_temp,
    "기압" : air_press,
    "풍향" : wind_dir,
    "풍속" : wind_speed,
    "돌풍" : wind_gust
}

post_id = collection.insert_one(post)