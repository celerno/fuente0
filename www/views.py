from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from pymongo import MongoClient
from pyquery import PyQuery
from collections import defaultdict

import os
import requests
import json
import re

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

def refresh(request):
    entrevistados = {}
    preguntas = {}
    respuestas = []
    req = requests.get('https://lopezobrador.org.mx/secciones/version-estenografica/')
    response = ''
    pq = PyQuery(req.text)
    for elem in pq('p'):
        if elem is not None and elem.text is not None:
            print(elem)
            matchS = re.match(r'strong', elem.text, re.RegexFlag.IGNORECASE) 
            if matchS:            
                if "PREGUNTA" not in elem.text:
                    matchE = re.match(r'strong.(.+)./strong.(.*)', elem.text, re.RegexFlag.I | re.RegexFlag.M)
                    entrevistado = matchE.group(1)
                    respuestas.insert(matchE.group(2))
                    if entrevistado is not None and not entrevistado in entrevistados:
                        entrevistados[entrevistado] = 1
                    elif entrevistado is not None: 
                        entrevistados[entrevistado] += 1
                else:
                    pregunta = elem.text.replace('<strong>PREGUNTA:</strong>','')
                    if not pregunta in preguntas:
                        preguntas[pregunta] = 1
                    else: 
                        preguntas[pregunta] += 1
    
    response = '<strong>ENTREVISTADOS</strong>'
    for entrevistado in entrevistados.keys():
        response += entrevistado + ': ' +  str(entrevistados[entrevistado]) + ' apariciones.' + '<br />'
    response += ' <strong> PREGUNTAS </strong>'
    for pregunta in preguntas.keys():
        response += pregunta.replace(':', '') + '<br />'

    return HttpResponse(response)