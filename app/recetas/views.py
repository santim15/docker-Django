from django.shortcuts import render

# recetas/views.py

from django.shortcuts import  HttpResponse

# Create your views here.

def index(request):
    return HttpResponse('Hello World!')
