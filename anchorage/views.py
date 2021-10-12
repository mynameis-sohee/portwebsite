from django.shortcuts import render
from typing import Protocol
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from django.http import HttpResponse # 임시표기HttpResponse용 
from django.http import JsonResponse
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
import pickle
from datetime import datetime

try:
    connection = psycopg2.connect("dbname='portwebsite_db' user='FIREMOTH' host='portwebsite.cictpybqx5bj.ap-northeast-2.rds.amazonaws.com' port='5432' password='glacksqnfskqkd1!'")
    connection.autocommit = True
except:
    print("Not Connected!")

# Create your views here.
def index(request):
    return render(request, 'anchorage/anchorage_page.html',{**AnchorageChart()})


def AnchorageChart():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM current_anchorage")
    data = cursor.fetchall()
    E1 = []
    E2 = []
    E3 = []
    etc = []
    for d in data:
        if d[12] == "정박지-E1":
            E1.append(d)
        elif d[12] == "정박지-E2":
            E2.append(d)
        elif d[12] == "정박지-E3":
            E3.append(d)
        else:
            etc.append(d)
    print(E2)
    context = {
        "E1": E1,
        "E2": E2,
        "E3": E3,
        "E1_quantity" : len(E1),
        "E2_quantity" : len(E2),
        "E3_quantity" : len(E3),
        "etc_quantity": len(etc),
    }
    print(context)
    return context

def anchorage_predict(request):

    loaded_model = pickle.load(open('정박지대기율예측.sav', 'rb'))

    search_key1 = request.GET['search_key1']
    # search_key2 = request.GET['search_key2']
    usage_input = request.GET['search_key3']
    servicenum = int(request.GET['search_key4'])
    waitingnum = int(request.GET['search_key5'])

    #선박용도
    usage_list = [(0, 0),
    (1, '석유제품 운반선'),
    (2, '케미칼 운반선'),
    (3, '기타 유조선'),
    (4, 'LPG 운반선'),
    (5, '일반화물선'),
    (6, '풀컨테이너선'),
    (7, '견인용예선'),
    (8, '원유운반선'),
    (9, '자동차운반선'),
    (10, '산물선(벌크선)'),
    (11, '기타 예선'),
    (12, '급유선'),
    (13, '기타선'),
    (14, '케미칼가스 운반선'),
    (15, '시멘트운반선'),
    (16, '모래운반선'),
    (17, '코일전용선'),
    (18, '폐기물 운반선'),
    (19, '압항 예선'),
    (20, '철강재 운반선'),
    (21, 'LNG 운반선'),
    (22, '신조선'),
    (23, '이.접안용 예선'),
    (24, '핫코일운반선'),
    (25, '크루즈선'),
    (26, '준설선'),
    (27, '세미(혼재)컨테이너선'),
    (28, '예부선'),
    (29, '관공선'),
    (30, '여객선'),
    (31, '유람선'),
    (32, '용달선(통선)'),
    (33, '광석운반선'),
    (34, '석탄운반선'),
    (35, '원목운반선'),
    (36, '기타 부선'),
    (37, '급수선')]

    for i in usage_list:
        if i[1] == usage_input:
            usage_input = i[0]



    print(servicenum)
    print(waitingnum)

    loaded_model = pickle.load(open('정박지대기율예측.sav', 'rb'))
    #신고톤수 차항지 선박용도 풍속 풍향 습도 최대파고 평균파고, servicenum(서비스 횟수), waitingnum(정박대기 횟수), month_y(이번달), waitingberth(대기 원하는 정박지)
    month_y = datetime.today().month
    result = loaded_model.predict([[int(search_key1), 3, usage_input, 10.2, 359.0, 81.0, 2.7, 1.2, servicenum, waitingnum, month_y, 7]]).round(2)[0] * 100
    print(result) #퍼센트값이라 *100해줫으면 좋겟음

    #result = loaded_model.predict([[search_key1, search_key2, search_key3, search_key4, search_key5]]).round(2)[0]

    #print(result)
    #print(search_key3)

    return JsonResponse({'result': round(result)})
