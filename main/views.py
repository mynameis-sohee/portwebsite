from django.shortcuts import render
from typing import Protocol
from django.http import HttpResponse # 임시표기HttpResponse용 
from django.http import JsonResponse
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from crawling import imo_crawling
from django.views.decorators.csrf import csrf_exempt
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

    return render(request, 'main/main_page.html',{**ShowingPortStatus(),**ShowingWeather(),**AnchorageChart(),**ShowingTemp()})
    # return render(request, 'main/main_page.html',{**ShowingPortStatus()})

def ShowingTemp():
    cursor = connection.cursor()
    cursor.execute("SELECT (temp) FROM forecast")
    context = {}
    base = "날씨"
    cnt = 1
    for rec in cursor.fetchall():
        key = base + (str(cnt))
        cnt = cnt + 1
        context[key] = rec[0]

    cursor.close()
    return context


def ShowingPortStatus():
    port_status = []
    port_name = []

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM upa_v3")
    for rec in cursor.fetchall():
        port_name.append(rec[1])
        port_status.append(rec[3]) 

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
    cursor.execute("SELECT * FROM wheather_current ORDER BY 관측_시간 DESC LIMIT 1")
    data = cursor.fetchone()
    print(data)
    cursor.close()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM today_weather_main")
    weather = cursor.fetchone()
    print(weather)
    context = {
        "관측소명": data[1],
        "관측시간": data[2],
        "조위": data[3],
        "수온": data[4],
        "염분": data[5],
        "기온": data[6],
        "기압": data[7],
        "풍향": data[8],
        "풍속": data[9],
        "돌풍": data[10],
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
    date=[]
    shipname=[]
    worktype=[]
    latitude=0
    longitude=0

    abc=request.GET.get('HarborName')
    cursor = connection.cursor()
    sql = "SELECT * FROM main_harbordata"
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        if(row[5]==abc):
            date.append(row[1])
            shipname.append(row[2])
            worktype.append(row[3])
    sql = "SELECT * FROM ulsan_main_port"
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        if(row[1]==abc):
            latitude = row[9]
            longitude = row[10]
    if request.method == 'GET':               
        context1 = {
        "date": date,
        "shipname":shipname,  
        "worktype":worktype,
        "latitude":latitude,
        "longitude":longitude
        }
        return JsonResponse(context1)
    else:
        return HttpResponse("GET이아님")
# print(AnchorageChart())

# connection.close()

def single_Vessel_position1(request):
    if request.method == 'GET':
        api_key ='1f86e6bc78c4a862fc418932b8649f7d44469e32'
        timespan = '20'
        Protocol_type = 'jsono'
        search_key = request.GET['search_key']
        IMO = imo_crawling.get_IMO(search_key)

        if IMO == False:
            return {'result' : 'fail'}

        pre_single_vessel = 'https://services.marinetraffic.com/api/exportvessel/v:5/'
        queryParams = {'service_key': api_key, 'timespan': timespan, 'Protocol_type' : Protocol_type, 'IMO' : IMO}

        api_url = pre_single_vessel + queryParams['service_key'] + '/timespan:' + queryParams['timespan'] + '/protocol:' + queryParams['Protocol_type'] + '/imo:' + queryParams['IMO']

        print(api_url)

        r = requests.get(api_url)
        r = r.json()
        #정보가 없는 예외처리
        if not r:
            return JsonResponse({'result' : 'fail_data'})

        
        
        

        res_mmsi = r[0]['MMSI']
        res_latitude = r[0]['LAT']
        res_longitude = r[0]['LON']
        res_speed = r[0]['SPEED']
        res_heading = r[0]['HEADING']
        res_course = r[0]['COURSE']
        res_status = r[0]['STATUS']
        res_timestamp = r[0]['TIMESTAMP']
        res_dsrc = r[0]['DSRC']

        context = {
            'result' : 'success',
            'mmsi' : res_mmsi,
            'latitude' : res_latitude,
            'longitude' : res_longitude,
            'speed' : res_speed,
            'heading' : res_heading,
            'course' : res_course,
            'status' : res_status,
            'timestamp' : res_timestamp,
            'dsrc' : res_dsrc
        }
        print(context)
        print('mmsi:' + res_mmsi)
        print('latutude:' + res_latitude)
        print('longitude:' + res_longitude)
        print('speed:' + res_speed)
        print('heading:' + res_heading)
        print('course:' + res_course)
        print('status:' + res_status)
        print('timestamp:' + res_timestamp)
        print('dsrc:' + res_dsrc)
        
        return JsonResponse(context)

    else:
        return HttpResponse("GET이아님")

def vesselpositiontest(request):
    if request.method == 'GET':
        context = {
            'result' : 'success',
            'mmsi' : 374945000,
            'latitude' : 35.45292,
            'longitude' : 129.4361,
            'speed' : 'a',
            'heading' : 'a',
            'course' : 'a',
            'status' : 'a',
            'timestamp' : 'a',
            'dsrc' : 'a'
        }
        return JsonResponse(context)

    else:
        return HttpResponse("GET이아님")