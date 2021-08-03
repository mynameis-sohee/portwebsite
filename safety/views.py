from django.shortcuts import render
from django.http import HttpResponse # 임시표기HttpResponse용 

# Create your views here.
def index(request):
    return render(request, 'safety/safety_page.html')
