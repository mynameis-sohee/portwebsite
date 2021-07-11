"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
1. Add an import: from my_app import views
2. Add a URL to urlpatterns: path('', views.home, name='home')
Class-based views
1. Add an import: from other_app.views import Home
2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf
1. Import the include() function: from django.urls import include, path
2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""
from safety.views import index
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from . import views

urlpatterns = [
path('admin/', admin.site.urls),
path('', views.index),# /main/으로 리다이렉트
path('main/',include('main.urls')), #메인 페이지
path('anchorage/',include('anchorage.urls')), #정박지 현황
path('ship_position/',include('ship_position.urls')), #실시간 선박 위치추적
path('wharf/',include('wharf.urls')), # 부두 현황
path('safety/', include('safety.urls')), # 안전/재난 정보
]
