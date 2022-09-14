# exemplo de servidor simples usando flask

import os
from flask import Flask, request
import urllib.parse
import json

# instancia o objeto flask
app = Flask(__name__)

termo_pesquisa = ""
url = ""
BOMPRECO = 'https://www.bompreco.com.br/'
PAO_AC = 'https://www.paodeacucar.com/'
EXTRA = 'https://www.extra.com.br/'

# rota na url
@app.route("/")
def welcome():
    return f"sucesso !!"


@app.route("/search", methods=['GET'])
def search():
    args = request.args
    global termo_pesquisa
    global BOMPRECO
    global PAO_AC
    termo_pesquisa = args.get('pesquisa', default="", type=str) # pega os termos da pesquisa
    
    consulta = BOMPRECO + montar_url(termo_pesquisa, 'BOMPRECO') # ponto que monta a url com a consulta
    #consulta = EXTRA + montar_url(termo_pesquisa, 'EXTRA')
  
    chamar_crawler(consulta)
    termo_pesquisa = ''
    json = carregar_json()
    return json


def montar_url(termo_pesquisa, mercado):
    
    if mercado == 'EXTRA':
        url =  urllib.parse.quote(termo_pesquisa, safe='') + '/b'
    elif mercado == 'BOMPRECO':
        url = urllib.parse.quote(termo_pesquisa, safe='')
    return url


def chamar_crawler(consulta):
    print(f'"{consulta}"')
    os.system('scrapy crawl ufrpe_crawler -a start_urls="{}" -O crawler_teste.json'.format(consulta))
    
def carregar_json():
    f = open('crawler_teste.json',"r")
    data = json.loads(f.read())
    f.close()
    return data

# verifica se eh da propria instacia para iniciar
if __name__ == "__main__":
    app.run()
