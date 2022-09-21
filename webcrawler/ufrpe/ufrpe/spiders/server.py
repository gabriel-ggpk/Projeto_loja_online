# exemplo de servidor simples usando flask

import re
from dateutil import parser
import os
from flask import Flask, request
from flask_cors import CORS
import urllib.parse
import json
from database import get_database
dbname = get_database()
from donttrust import Schema
collection_name = dbname["feira_online"]
# instancia o objeto flask
app = Flask(__name__)
CORS(app)
email_schema = Schema("email").email().required()
password_schema = Schema("password").string().min(8).required()

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



    
@app.route("/login", methods=['POST'])
def login():
    args = request.get_json()
    email = args["email"]
    password = args["password"]
    try:
        email_schema.validate(email)
    except:
        return "Email inválido", 400   
    try:   
        password_schema.validate(password)
    except:
        return "Senha inválida", 400   

    user = collection_name.find({"email": email})
    try:   
        if user[0]["password"] == password:
            return "Login realizado com sucesso", 200
        else:  
            return "Senha incorreta", 400
    except:
        return "Usuário não encontrado", 400

@app.route("/signup", methods=['POST'])
def signup():  
    args = request.get_json()  
    email = args["email"]  
    password = args["password"]
    if not email_schema.validate(email):
        return "Email inválido", 400   
    if not password_schema.validate(password):
        return "Senha inválida", 400   
    item_details = collection_name.find({"email": email})
    for item in item_details:  
        if item["email"] == email: 
            return "Email already exists",409
    collection_name.insert_one({"email": email, "password": password})
    return f"sucesso !!", 201  
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
def get_database():
    

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://localhost:27017/"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['user_shopping_list']

# verifica se eh da propria instacia para iniciar
if __name__ == "__main__":
    app.run()
