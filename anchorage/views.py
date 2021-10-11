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
    search_key2 = request.GET['search_key2']
    search_key3 = request.GET['search_key3']
    search_key4 = request.GET['search_key4']
    search_key5 = request.GET['search_key5']

    loaded_model = pickle.load(open('정박지대기율예측.sav', 'rb'))
    result = loaded_model.predict([[30.028, 3, 1, 10.2, 359.0, 81.0, 2.7, 1.2, 1, 1, 5.0, 7]]).round(2)[0] * 100
    print(result) #퍼센트값이라 *100해줫으면 좋겟음

    #result = loaded_model.predict([[search_key1, search_key2, search_key3, search_key4, search_key5]]).round(2)[0]

    #print(result)
    #print(search_key3)

    return JsonResponse({'result': round(result)})
