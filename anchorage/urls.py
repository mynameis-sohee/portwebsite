from safety import views
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='anchorage'),
    path('anchorage_predict/', views.anchorage_predict, name='anchorage_predict'),
]