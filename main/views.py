from django.shortcuts import render
from django.http import HttpResponse # 임시표기HttpResponse용 
from pymongo import MongoClient
from django.http import JsonResponse
from operator import itemgetter
import psycopg2
# import json

#--------------------------------------------------------------------------
# db = client.portwebsite_dbz
# collection = db.실시간_부두상황정보_울산신항
# results = collection.find({'상태':'정상'},{'_id':False})
# # dictionary = {str(i):test_list[i]for i in range(len(test_list))}
# context = {'budu': results}
# print(context)
# # for result in results:
# #     print(result)
#----------------------------------------------------------------------------

# db = client.portwebsite_db
# collection = db.실시간_부두상황정보_울산신항
# test_list = list(collection.find({'상태':'정상'},{'_id':False}))
# dictionary = {str(i):test_list[i]for i in range(len(test_list))}
# print(dictionary)

try:
    connection = psycopg2.connect("dbname='portwebsite_db' user='FIREMOTH' host='portwebsite.cictpybqx5bj.ap-northeast-2.rds.amazonaws.com' port='5432' password='glacksqnfskqkd1!'")
    connection.autocommit = True
except:
    print("Not Connected!")

# Create your views here.
def index(request):
    return render(request, 'main/main_page.html',{**ShowingPortStatus(),**ShowingWeather()})
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

ShowingPortStatus()

def ShowingWeather():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM wheather_current")
    data = cursor.fetchone()
    cursor.execute("SELECT * FROM today_weather_main")
    weather = cursor.fetchone()

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
    # weather_list = sorted(list(weather_collection.find({},{'_id':False})), key=itemgetter('관측_시간'),reverse=True)
    # # weather_json = json.dumps(weather_list,ensure_ascii=False)
    # context = weather_list[0]
    return context

print(ShowingWeather())

# connection.close()