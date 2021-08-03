from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return redirect('/main/') # /main/으로 리다이렉트