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

from fonctions.model import getDataModel

nltk.download("punkt")
nltk.download("wordnet")

train_X, train_y = getDataModel()

input_shape = (len(train_X[0]),)
output_shape = len(train_y[0])
epochs = 200

model = Sequential() # squelette de base
model.add(Dense(128, input_shape=input_shape, activation="relu")) # ajoute une couche au modèle de réseau de neurones 128 neurones 
model.add(Dropout(0.5)) # aide pour pas qu'elle surapprend
model.add(Dense(64, activation="relu")) # nouvelle couche de réseau de neurones
model.add(Dropout(0.3)) # aide pour pas qu'elle surapprend
model.add(Dense(output_shape, activation = "softmax")) # couche finale 
adam = tf.keras.optimizers.Adam(learning_rate=0.01) # minimiser les pertes et améliorer les performances du modèle

model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=["accuracy"])
model.fit(x=train_X, y=train_y, epochs=200, verbose=1)
model.save("./models/papyrusmodel.keras")