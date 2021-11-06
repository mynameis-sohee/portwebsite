import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import psycopg2

#https://openweathermap.org/forecast5

url = "http://api.openweathermap.org/data/2.5/forecast?q=Ulsan&appid=my_key"

res = requests.get(url)
dataList = res.json()['list']

# print(dataList[0])

tempListDic = []

for d in dataList:
    tempListDic.append({d["dt_txt"] : d["main"]["temp"]})

tempData = None
tempList = []


for d in tempListDic:
    key, value = list(d.items())[0]
    if tempData != key[:10]:
        print(key[:10])
        tempList.append(round(value - 273.15))
        tempData = key[:10]

# ---DB 세팅---
try:
    connection = psycopg2.connect("dbname='portwebsite_db' user='FIREMOTH' host='portwebsite.cictpybqx5bj.ap-northeast-2.rds.amazonaws.com' port='5432' password='glacksqnfskqkd1!'")
    connection.autocommit = True
except:
    print("Not Connected!")

cursor = connection.cursor()
# --------
cursor.execute("TRUNCATE TABLE forecast;")
for i in range(len(tempList)):
    cursor.execute("INSERT INTO forecast (temp) VALUES (%s);", (tempList[i],))
    print(i, tempList[i])

cursor.execute("SELECT (temp) FROM forecast")

for rec in cursor.fetchall():
    print(rec[0])
