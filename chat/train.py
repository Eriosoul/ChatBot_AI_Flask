import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords  # Añadir esto

# Descargar recursos necesarios
nltk.download('punkt')  # Asegúrate de que nltk tenga los recursos necesarios
nltk.download('stopwords')  # Descargar las stopwords en español

# Inicializar el lematizador
lemmatizer = WordNetLemmatizer()

# Cargar los intents con codificación UTF-8
with open('intents.json', encoding='utf-8') as file:
    intents = json.load(file)

# Crear listas para almacenar las palabras, clases y documentos
words = []
classes = []
documents = []

# Ignorar algunos signos de puntuación
ignoreLetters = ['?', '!', '¿', '¡', '.', ',', ';', ':']

# Cargar las stopwords en español
spanish_stopwords = stopwords.words('spanish')

# Procesar cada intención en el archivo intents2.json
for intent in intents['intents']:
    for pattern in intent['patterns']:
        wordList = nltk.word_tokenize(pattern)  # Tokenizar las palabras en cada patrón
        words.extend(wordList)
        documents.append((wordList, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Normalizar las palabras, eliminar las stopwords y los signos de puntuación
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignoreLetters and word not in spanish_stopwords]

# Asegurarnos de que `words` tenga palabras únicas y ordenadas
words = sorted(set(words))
classes = sorted(set(classes))

# Guardar las palabras y clases en archivos pickle
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Preparar los datos para el entrenamiento
training = []
outputEmpty = [0] * len(classes)

for document in documents:
    bag = []
    wordPatterns = document[0]
    wordPatterns = [lemmatizer.lemmatize(word.lower()) for word in wordPatterns if word not in spanish_stopwords]  # Eliminar stopwords
    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)
    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1  # Etiquetar la clase correspondiente
    training.append(bag + outputRow)

# Mezclar los datos
random.shuffle(training)
training = np.array(training)

# Dividir los datos en entradas (X) y salidas (Y)
trainX = training[:, :len(words)]
trainY = training[:, len(words):]

# Crear el modelo de la red neuronal
model = tf.keras.Sequential()

# Añadir las capas al modelo
model.add(tf.keras.layers.Dense(128, input_shape=(len(trainX[0]),), activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(len(trainY[0]), activation='softmax'))

# Usar el optimizador SGD con tasa de aprendizaje y momentum
sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)

# Compilar el modelo
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Entrenar el modelo
hist = model.fit(np.array(trainX), np.array(trainY), epochs=200, batch_size=5, verbose=1)

# Guardar el modelo entrenado
model.save('chatbot_simple_libro_model.h5')

print("EXECUTE... El modelo ha sido guardado.")
