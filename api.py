import json
import logging
import random
from flask import Flask, jsonify, request, redirect, session, url_for, g
# from keycloak import KeycloakOpenID
from keycloak.keycloak_openid import KeycloakOpenID
import requests
from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, fields,Namespace,reqparse
from keras.models import load_model
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import numpy as np
import tensorflow as tf 
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, Dropout
from fonctions.model import preprocess_sentence, get_response, getDataModel
from fonctions.initkeycloak import get_access_token, get_client_id,get_client_secret
import pymongo
import os
from dotenv import load_dotenv
import subprocess
subprocess.run(["python", "loadmodel.py"])

load_dotenv()
client_string = os.getenv("MONGODB_URL")
db_string = os.getenv("DB_NAME")
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
REALM_NAME = os.getenv("KEYCLOAK_REALM_NAME")
ADMIN_USERNAME = os.getenv("KEYCLOAK_USER")
ADMIN_PASSWORD = os.getenv("KEYCLOAK_PASSWORD")
KEYCLOAK_CLIENT_NAME = os.getenv("KEYCLOAK_CLIENT_NAME")
FLASK_PORT = os.getenv("FLASK_PORT")

access_token = get_access_token(ADMIN_USERNAME, ADMIN_PASSWORD, "admin-cli", "")
client_id = get_client_id()
client_secret = get_client_secret()
os.environ['KEYCLOAK_CLIENT_SECRET'] = client_secret
os.environ['KEYCLOAK_CLIENT_ID'] = client_id
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
print(KEYCLOAK_CLIENT_ID)

client = pymongo.MongoClient(client_string)
db = client[db_string]
collectionintents = db["intents"] 
intents = collectionintents.find({})

app = Flask(__name__)

CORS(app, origins="*")

authorizations = {
    'bearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    app, 
    version='1.0', 
    title='Swagger API PAPYRUS', 
    description='API PAPYRUS',
    authorizations=authorizations
)

logging.basicConfig(level=logging.DEBUG)

app.config.update({
    'SECRET_KEY': 'XlBGtHzPOefRKjiEB9yTcQS0WBHllAcx',
    'TESTING': True,
    'DEBUG': True
})
os.system('cls')

keycloak_auth="http://keycloak:8080/auth/"
keycloak_openid = KeycloakOpenID(
    server_url=keycloak_auth,
    client_id=KEYCLOAK_CLIENT_NAME,
    realm_name=REALM_NAME,
    client_secret_key=KEYCLOAK_CLIENT_SECRET
)
try:
    openid_configuration = keycloak_openid.well_known()
    print("Keycloak connection setup is successful.")
except Exception as e:
    print("Error occurred during Keycloak connection setup:", e)


login_model = api.model('Authentification', {
    'username': fields.String(required=True, description='exemple:rayangbe69@gmail.com'),
    'password': fields.String(required=True, description='exemple:test')
})
login_namespace = Namespace('Authentification', description='Authentification via Keycloak')
@login_namespace.route('/connexion')
class LoginResource(Resource):
    @login_namespace.expect(login_model)
    def post(self):
        username = login_namespace.payload['username']
        password = login_namespace.payload['password']

        token = keycloak_openid.token(username, password)  
        if token:
            return {'message': 'Connexion réussie', 'token': token}
        else:
            return {'message': 'Connexion échouée', 'token': token}, 401

api.add_namespace(login_namespace)


chatbot_model = api.model('Chatbot', {
    'question': fields.String(required=True, description='Quelle est ton nom?'),
})
chatbot_namespace = Namespace('Chatbot', description='Chatbot endpoints')
@chatbot_namespace.route('/chat')
class ChatbotResource(Resource):
    @chatbot_namespace.expect(chatbot_model)
    def post(self):
        question = chatbot_namespace.payload['question']
        model = load_model("./models/papyrusmodel.keras")
        processed_question = preprocess_sentence(question)
        train_X, train_y = getDataModel()
        max_sequence_length = max(len(seq) for seq in train_X)
        input_data = get_response(processed_question,max_sequence_length)
        prediction = model.predict(np.array([input_data]))
        predicted_class_index = np.argmax(prediction)
        confidence_scores = prediction[0].tolist()
        confidence_score = np.max(prediction)
        
        index_to_tag = {}
        for index, intent in enumerate(intents):
            index_to_tag[index] = intent['tag']
        predicted_tag = index_to_tag.get(predicted_class_index, "Unknown")
        intent = collectionintents.find_one({"tag": predicted_tag})
        responses = intent.get('responses', [])
        
        response_scores = [(response, score) for response, score in zip(responses, confidence_scores)]
        response_scores.sort(key=lambda x: x[1], reverse=True)
        top_5_responses = response_scores[:5]
        response_table = [{"reponse": response, "score": score} for response, score in top_5_responses]
        return jsonify({"reponses": response_table})     
    
api.add_namespace(chatbot_namespace)

if __name__ == '__main__':
    app.run(debug=True, port=FLASK_PORT)
    # exec(open("loadmodel.py").read())
    # app.run(debug=True)
