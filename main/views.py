from django.shortcuts import render
from django.http import HttpResponse # 임시표기HttpResponse용 
from pymongo import MongoClient
from django.http import JsonResponse
from operator import itemgetter
# import json

client = MongoClient(
    username='FIREMOTH',
    password='glacksqnfskqkd1!'
)

#--------------------------------------------------------------------------
# db = client.portwebsite_db
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


# Create your views here.
def index(request):
    return render(request, 'main/main_page.html',{**ShowingPortStatus(),**ShowingWeather()})

def ShowingPortStatus():
    db = client.portwebsite_db
    collection0 = db.실시간_부두상황정보_울산본항
    collection1 = db.실시간_부두상황정보_울산신항
    collection2 = db.실시간_부두상황정보_온산항
    collection3 = db.실시간_부두상황정보_미포항
    test_list = list(collection0.find({},{'_id':False}))
    test_list1 = list(collection1.find({},{'_id':False}))
    test_list2 = list(collection2.find({},{'_id':False}))
    test_list3 = list(collection3.find({},{'_id':False}))
    temp_status=[]
    port_status=[]
    port_name=[]
    temp_status.append(test_list)
    temp_status.append(test_list1)
    temp_status.append(test_list2)
    temp_status.append(test_list3)
    i=0
    for test_list in temp_status:
        for eachport in test_list:
            port_status.append(test_list[i]['상태'])
            port_name.append(test_list[i]['부두명'])
            i=i+1
        i=0
    dictionary = {
        '상태' :port_status,
        '항구이름' :port_name  
    }
    return dictionary

def ShowingWeather():
    db = client.portwebsite_db
    weather_collection = db.현재날씨
    weather_list = sorted(list(weather_collection.find({},{'_id':False})), key=itemgetter('관측_시간'),reverse=True)
    # weather_json = json.dumps(weather_list,ensure_ascii=False)
    context = weather_list[0]

    return context