from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("<a href='./text_analysis'>Go to chat</a>")
