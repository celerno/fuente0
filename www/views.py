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
__client = MongoClient("mongodb://45.33.32.87:27017")
def refresh(request):
    src = 'https://lopezobrador.org.mx/secciones/version-estenografica/'
    respuestas = []
    _db = __client["eventos"]
    _eventos = _db["eventos_raw"]
    page = 2

    if 'text' in cache:
        text = cache['text']
        print('using cache')
    else:
        req = requests.get(src)
        text = req.text
        while req.status_code != 404:
            print(str(datetime.now()) +  ' - GET ' + src + 'page/' + str(page))
            req = requests.get(src + 'page/' + str(page))
            page+=1
            text+=req.text
        cache['text']=text

    __regex = r'(?:<p\s*(?:style=\"[^\"]+\")?>\s*(?:<strong>)?VE-\d+(?:[-.]\d+)?(?:</strong>)?\s*</p>|>VE-\d+(?:[-.]\d+)?\s*)'
    veCodes = defaultdict()
    for veCode in re.findall(__regex, text, re.RegexFlag.M):
        veCode = veCode.replace('</','<').replace('<p>','').replace('<strong>','').replace('>','')
        veCode = veCode[veCode.rindex('VE'):]
        veCodes[veCode] = '<p><strong>' + veCode +'</strong></p>'
    
    
    veText = re.split(__regex, text)
    
    response = str(len(veCodes.keys()))  + ' versiones estenográficas en ' + str(page - 1) + ' páginas<br><table>'
    for i, ve in enumerate(veCodes.keys()):
        veCodes[ve] += veText[i+1]
        response += '<tr><td>' + str(i+1) + '</td><td>' + ve + '</td><td><textarea rows ="5" cols = "100">' + veCodes[ve] + '</textarea></td></tr>'
        if _eventos.find({"veId":ve}).count() == 0:
            _eventos.insert_one({"veId": ve, "text": veCodes[ve]})

    response+='</table>'
        


    '''
    response ='<table><tr><td>code</td><td>preguntas</td><td>actores</td><td>nombres</td></tr>'
    for i, ve in enumerate(veText):
        entrevistados = {}
        preguntas = {}
        ve = veCodes[i] if len(veCodes) < i is not None else 'NULO'
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
    '''
    return HttpResponse(response)