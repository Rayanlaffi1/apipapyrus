import json
import logging
import random
from flask import Flask, jsonify, request, redirect, session, url_for, g
from keycloak import KeycloakOpenID
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

import pkgutil
def list_imported_packages():
    imported_packages = set()
    for importer, modname, ispkg in pkgutil.walk_packages():
        try:
            __import__(modname)
            imported_packages.add(modname)
        except Exception as e:
            print(f"Error importing {modname}: {e}")
    return imported_packages

if __name__ == "__main__":
    imported_packages = list_imported_packages()
    print("Modules and packages imported in this script:")
    for package in sorted(imported_packages):
        print(package)

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

keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:9009/",
    client_id="papyrus",
    realm_name="papyrus",
    client_secret_key="OCdDz9y5RtcLrsPry49bmka4iIE0p8vv"
)


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
            return {'message': 'Connexion échouée'}, 401

api.add_namespace(login_namespace)


chatbot_model = api.model('Chatbot', {
    'question': fields.String(required=True, description='Quelle est ton nom?'),
})
chatbot_namespace = Namespace('Chatbot', description='Chatbot endpoints')
@chatbot_namespace.route('/chat')
class ChatbotResource(Resource):
    @chatbot_namespace.expect(chatbot_model)
    def post(self):
        chemin_intents_json = "./json/intents.json"
        question = chatbot_namespace.payload['question']
        model = load_model("./models/papyrusmodel.keras")
        processed_question = preprocess_sentence(question)
        train_X, train_y = getDataModel(chemin_intents_json)
        max_sequence_length = max(len(seq) for seq in train_X)
        input_data = get_response(processed_question,max_sequence_length)
        prediction = model.predict(np.array([input_data]))
        predicted_class_index = np.argmax(prediction)
        with open(chemin_intents_json, 'r', encoding='utf-8') as file:
            intents = json.load(file)
        response = intents['intents'][predicted_class_index]['responses']
        predictions = []
        for index, (intent, score) in enumerate(zip(intents['intents'], prediction[0])):
            rep = random.choice(intents['intents'][index]["responses"])
            predictions.append({'tag': intents['intents'][index]["tag"], 'reponse': rep, 'score': float(score)})
        sorted_predictions = sorted(predictions, key=lambda x: x['score'], reverse=True)
        if sorted_predictions[0]["score"] < 0.55:
            return jsonify({"reponse":{ "reponse": "Je n'ai pas compris.", "score": 0, "prediction":sorted_predictions[0] }})
        else:  
            return jsonify({"reponse":sorted_predictions[0]})     
    
api.add_namespace(chatbot_namespace)

if __name__ == '__main__':
    app.run(debug=True)