import json
import string
import random 
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer 
import tensorflow as tf 
from tensorflow.keras import Sequential 
from tensorflow.keras.layers import Dense, Dropout
import json
import numpy as np
import random
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pymongo
import os
from dotenv import load_dotenv
nltk.download("punkt")
nltk.download("wordnet")

def getDataModel():
    load_dotenv()
    client_string = os.getenv("MONGODB_URL")
    db_string = os.getenv("DB_NAME")
    client = pymongo.MongoClient(client_string)
    db = client[db_string]
    collectionintents = db["intents"] 
    intents = collectionintents.find({})

    lemmatizer = WordNetLemmatizer()
    words = []
    classes = []
    doc_X = []
    doc_y = []
    for intent in intents:
        for pattern in intent["patterns"]:
            tokens = nltk.word_tokenize(pattern)
            words.extend(tokens)
            doc_X.append(pattern)
            doc_y.append(intent["tag"])
        if intent["tag"] not in classes:
            classes.append(intent["tag"])
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]
    words = sorted(set(words))
    classes = sorted(set(classes))
    training = []
    out_empty = [0] * len(classes)
    for idx, doc in enumerate(doc_X):
        bow = []
        text = lemmatizer.lemmatize(doc.lower())
        for word in words:
            bow.append(1) if word in text else bow.append(0)
        output_row = list(out_empty)
        output_row[classes.index(doc_y[idx])] = 1
        training.append([bow, output_row])
    random.shuffle(training)
    print(training)
    training = np.array(training, dtype=object)
    train_X = np.array(list(training[:, 0]))
    train_y = np.array(list(training[:, 1]))
    return train_X,train_y

def preprocess_sentence(sentence):
    lemmatizer = WordNetLemmatizer()
    tokens = nltk.word_tokenize(sentence.lower())  # Tokenisation et mise en minuscules
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens

def get_response(processed_sentence, max_sequence_length):
    # Tokenizer pour convertir les mots en indices
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(processed_sentence)
    word_index = tokenizer.word_index

    # Convertir les mots en indices
    sequence = tokenizer.texts_to_sequences([processed_sentence])[0]

    # Padding pour obtenir une séquence de longueur fixe
    padded_sequence = pad_sequences([sequence], maxlen=max_sequence_length)[0]
    return padded_sequence

