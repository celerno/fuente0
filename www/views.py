from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import requests
import json

# Create your views here.
def index(request):
    return HttpResponse('Hola, gueguegue')

def estado(request):
    req = requests.get('https://api.github.com/repos/celerno/fuente0/commits')
    jData = json.loads(req.content)
    print(jData[0]['sha'])
    req = requests.get('https://api.github.com/repos/celerno/fuente0/commits/' + jData[0]['sha'])
    jData = json.loads(req.content)
    print(jData)
    message = jData['commit']
    return HttpResponse('última actualización: ' + message['message'] + ' / ' + message['committer']['date'])

