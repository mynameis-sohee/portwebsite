from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ship_position'),
    path('search/', views.test, name='single_Vessel_position'),
]