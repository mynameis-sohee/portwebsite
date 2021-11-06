from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='main'),
    path('GetHarborData/',views.GetHarborData,name='GetHarborData'),
    path('search/', views.single_Vessel_position1, name='vesselpositiontest'),
]
