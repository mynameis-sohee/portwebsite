from django.shortcuts import render
from typing import Protocol
import requests
import json
from django.http import HttpResponse

# Create your views here.

def index(request):       
    return render(request, 'ship_position/ship_position_page.html')

def single_Vessel_position(request):
    if request.method == 'GET':
        api_key ='1f86e6bc78c4a862fc418932b8649f7d44469e32'
        timespan = '20'
        Protocol_type = 'jsono'
        mmsi = request.GET['search_key']

        pre_single_vessel = 'https://services.marinetraffic.com/api/exportvessel/v:5/'
        queryParams = {'service_key': api_key, 'timespan': timespan, 'Protocol_type' : Protocol_type, 'mmsi' : mmsi}

        api_url = pre_single_vessel + queryParams['service_key'] + '/timespan:' + queryParams['timespan'] + '/protocol:' + queryParams['Protocol_type'] + '/mmsi:' + queryParams['mmsi']

        print(api_url)

        r = requests.get(api_url)
        r = r.json()
        

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
        
        return render(request, 'ship_position/ship_position_page.html',context)

    else:
        return HttpResponse("GET이아님")

def test(request):

    context = {
            'mmsi' : "370937000",
            'latitude' : "35.509144",
            'longitude' : "129.389110",
            'speed' : "127",
            'heading' : "33",
            'course' : "36",
            'status' : "0",
            'timestamp' : "2021-07-11T10:44:20",
            'dsrc' : "TER"
        }
    testJson = json.dumps(context)
    print(testJson)
    return render(request, 'ship_position/ship_position_page.html',{'testJson':testJson})