from django.shortcuts import render
from django.http import HttpResponse # 임시표기HttpResponse용
from django.http import JsonResponse
import pickle

# Create your views here.
def index(request):
    return render(request, 'wharf/wharf_page.html')

def container_predict(request):
    # load the model from disk
    loaded_model = pickle.load(open('컨테이너수송량예측.sav', 'rb'))

    search_key1 = request.GET['search_key1']
    search_key2 = request.GET['search_key2']
    search_key3 = request.GET['search_key3']
    search_key4 = request.GET['search_key4']
    search_key5 = request.GET['search_key5']

    if search_key3 == "국적선":
        search_key3 = 0
    elif search_key3 == "외국선":
        search_key3 = 1

    if search_key5 == "공컨테이너":
         search_key5 = 0
    elif search_key5 == "적컨테이너":
        search_key5 = 1

    result = loaded_model.predict([[search_key1, search_key2, search_key3, search_key4, search_key5]]).round(2)[0]

    print(result)
    print(search_key3)

    return JsonResponse({'result': result})
