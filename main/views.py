from django.shortcuts import render
from django.http import HttpResponse # 임시표기HttpResponse용 
from django.http import JsonResponse
from operator import itemgetter
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
# from main.models import HarborData
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

# print(AnchorageChart())

# connection.close()