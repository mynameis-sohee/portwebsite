from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='wharf'),
    path('container_predict/', views.container_predict, name='container_predict'),
]