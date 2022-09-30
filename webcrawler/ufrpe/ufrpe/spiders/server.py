# exemplo de servidor simples usando flask
from pymongo import MongoClient

def get_database():  
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://gabrielHCS:teste@cluster0.sqgb8.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['feira_online']

from dateutil import parser
import os
from flask import Flask, request
from flask_cors import CORS
import urllib.parse
import json
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
SAMS = 'https://www.samsclub.com.br/'
AMAZON = 'https://www.amazon.com.br/s?k='
# rota na url
@app.route("/")
def welcome():
    return f"sucesso !!"


@app.route("/search", methods=['GET'])
def search():
    args = request.args
    global termo_pesquisa
    global BOMPRECO
    global SAMS
    global AMAZON
    termo_pesquisa = args.get('pesquisa', default="", type=str) # pega os termos da pesquisa
    
    consulta_BOMPRECO = BOMPRECO + montar_url(termo_pesquisa, 'BOMPRECO') # ponto que monta a url com a consulta
    consulta_AMAZON = AMAZON + montar_url(termo_pesquisa, 'AMAZON')
    consulta_SAMS = SAMS + montar_url(termo_pesquisa, 'SAMS')
    consultas = [   {'name':'Bompreço',
                    'url':consulta_BOMPRECO},
                    {'name':'Amazon',
                    'url':consulta_AMAZON},
                    {'name':'Sams',
                    'url':consulta_SAMS}
                    ]
    chamar_crawler(consultas)
    termo_pesquisa = ''
    json = carregar_json()
    result = [{
        'name': 'Amazon',
        'products': json[0]
    },{
        'name': 'Bompreço',
        'products': json[1]
    },{
        'name': 'Sams',
        'products': json[2]
    }
    ]
    return result



    
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
    
    if mercado == 'AMAZON':
        url =  urllib.parse.quote(termo_pesquisa, safe='') 
    elif mercado == 'BOMPRECO':
        url = urllib.parse.quote(termo_pesquisa, safe='')
    elif mercado == 'SAMS':
        url = urllib.parse.quote(termo_pesquisa + "?_q=" + termo_pesquisa+"&map=ft", safe='')
    return url


def chamar_crawler(consultas):

    for consulta in consultas:
        os.system('scrapy crawl ufrpe_crawler -a start_urls="{url}" -O {name}.json'.format(name=consulta['name'], url=consulta['url']))
        
    
def carregar_json():
    data = []
    with open("Amazon.json", 'r') as j:
        data.append(json.loads(j.read())) 
    j.close()
    with open("Bompreço.json", 'r') as j:
        data.append(json.loads(j.read())) 
    j.close()
    with open("Sams.json", 'r') as j:
        data.append(json.loads(j.read())) 
    j.close()
    return data

if __name__ == "__main__":
    app.run()
