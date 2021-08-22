from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='main'),
    path('GetHarborData/',views.GetHarborData,name='GetHarborData')    
]
