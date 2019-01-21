from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# Create your views here.
def index(request):
    return HttpResponse('Hola, gueguegue')

def estado(request):
    return HttpResponse('todo fine: ' + str(datetime.now()))