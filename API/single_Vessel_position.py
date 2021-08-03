from typing import Protocol
import requests





api_key ='1f86e6bc78c4a862fc418932b8649f7d44469e32'
timespan = '20'
Protocol_type = 'jsono'
mmsi = input()

pre_single_vessel = 'https://services.marinetraffic.com/api/exportvessel/v:5/'
queryParams = {'service_key': api_key, 'timespan': timespan, 'Protocol_type' : Protocol_type, 'mmsi' : mmsi}

api_url = pre_single_vessel + queryParams['service_key'] + '/timespan:' + queryParams['timespan'] + '/protocol:' + queryParams['Protocol_type'] + '/mmsi:' + queryParams['mmsi']

print(api_url)

r = requests.get(api_url)
r = r.json()
print(r)

res_mmsi = r[0]['MMSI']
res_latitude = r[0]['LAT']
res_longitude = r[0]['LON']
res_speed = r[0]['SPEED']
res_heading = r[0]['HEADING']
res_course = r[0]['COURSE']
res_status = r[0]['STATUS']
res_timestamp = r[0]['TIMESTAMP']
res_dsrc = r[0]['DSRC']


print('mmsi:' + res_mmsi)
print('latutude:' + res_latitude)
print('speed:' + res_longitude)
print('speed:' + res_speed)
print('heading:' + res_heading)
print('course:' + res_course)
print('status:' + res_status)
print('timestamp:' + res_timestamp)
print('dsrc:' + res_dsrc)