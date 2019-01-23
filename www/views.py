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

cache = defaultdict()

def refresh(request):
   
    respuestas = []
    text = ''
    if 'text' in cache:
        text = cache['text']
        print('using cache')
    else:
        req = requests.get('https://lopezobrador.org.mx/secciones/version-estenografica/')
        text = req.text
        cache['text'] = text

    veCodes = re.findall(r'VE-\d+-?\d*', text, re.RegexFlag.M)
    veText = re.split(r'<p>\s*<?s?t?r?o?n?g?>?VE-\d+-?\d*', text)
    response ='<table><tr><td>code</td><td>preguntas</td><td>actores</td><td>nombres</td></tr>'
    for i, ve in enumerate(veText):
        entrevistados = {}
        preguntas = {}
        ve = veCodes[i+1]
        response+='<tr><td>'+ve +'</td><td>'
        text = veText[i]
        pq = PyQuery(text)
        for elem in pq('p > strong'):
            if elem is not None and elem.text is not None:
                if "PREGUNTA" in elem.text:
                    pregunta = 'pregunta'
                    if not pregunta in preguntas:
                        preguntas[pregunta] = 1
                    else: 
                        preguntas[pregunta] += 1            
                elif 'fica' not in elem.text and len(re.findall(r'[a-z]{3}', elem.text)) == 0:
                    entrevistado = elem.text
                    if not entrevistado in entrevistados:
                        entrevistados[entrevistado] = 1
                    else: 
                        entrevistados[entrevistado] += 1
        response += str(len(preguntas))+'</td><td>' + str(len(entrevistados)) + '</td></td><td>' + str(entrevistados.keys()).replace('dict_keys([','').replace('\\n',' ').replace('\'','').replace('])','')+'</td></tr>'
    response+='</table>'
    return HttpResponse(response)